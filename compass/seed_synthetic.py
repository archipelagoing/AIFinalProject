# compass/seed_synthetic.py
#
# Ticket CMP-1112-D2-01: fill a database with fake (synthetic) test data,
# using the repo's own schema from compass/db.py.
#
# HOW TO RUN IT
#   python -m compass.seed_synthetic
#       -> writes to .local/compass_synthetic.db (a separate file, so fake data
#          never mixes with your own imported data)
#   python -m compass.seed_synthetic --db some/other.db
#
# WHAT YOU'LL SEE
#   1st run:  inserted 1 import(s), 1 coverage row(s), 4 alias(es), 7 transaction(s)
#   2nd run:  inserted 0 import(s), 0 coverage row(s), 0 alias(es), 0 transaction(s)
#             already seeded; nothing new to insert
#
# SAFETY
#   * Safe to run many times: rows already present are skipped.
#   * It refuses to write into a database that already holds OTHER imports
#     (e.g. your real bank data), unless you add --allow-other-data.
#
# WHY "ON CONFLICT ... DO NOTHING" AND NOT "INSERT OR IGNORE"
#   Both skip duplicates. But INSERT OR IGNORE also quietly skips rows that
#   break the table's rules, so a typo like predicted_type = 'purchse' would
#   just vanish. ON CONFLICT ... DO NOTHING skips ONLY duplicates; any other
#   problem still stops with an error.

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path

from compass.db import connect

DEFAULT_DB_PATH = Path(".local/compass_synthetic.db")

# Found relative to this file, so it works from any folder:
#   compass/seed_synthetic.py -> repo root -> tests/python/fixtures/synthetic_oct.json
DEFAULT_FIXTURE = (Path(__file__).resolve().parents[1]
                   / "tests" / "python" / "fixtures" / "synthetic_oct.json")


def cents_to_plain(cents: int) -> str:
    """Integer cents -> plain amount text like a bank CSV, with integer math only.

        -575   -> '-5.75'
        200000 -> '2000.00'
        5      -> '0.05'
    """
    sign = "-" if cents < 0 else ""
    dollars, rem = divmod(abs(cents), 100)
    return f"{sign}{dollars}.{rem:02d}"


def import_sha256(import_id: str, fixture: dict) -> str:
    """A 64-character fingerprint for one import, like the hash of a real CSV file.

    The repo's `imports` table requires one (sha256 TEXT UNIQUE, exactly 64 chars).
    Built from that import's rows, so the same fixture always gives the same value.
    """
    rows = [t for t in fixture["transactions"] if t["import_id"] == import_id]
    text = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def original_row_json(t: dict, account_name: str) -> str:
    """Rebuild the CSV row this transaction 'came from', as JSON text.

    The repo keeps every original row (original_row_json) so numbers can be
    traced back to the bank file. Keys match the repo's CSV header:
        date, description, amount, account, transaction_id
    Example for T1:
        {"account": "Synthetic Checking", "amount": "-5.75", "date": "2026-10-03",
         "description": "STARBUCKS #1234", "transaction_id": "SYN-0001"}
    """
    return json.dumps({
        "date": t["posted_date"],
        "description": t["description"],
        "amount": cents_to_plain(t["amount_cents"]),
        "account": account_name,
        "transaction_id": t["source_transaction_id"],
    }, sort_keys=True)


def load_fixture(path: str | Path = DEFAULT_FIXTURE) -> dict:
    """Read the fixture and check the numbers are whole numbers.

        "amount_cents": -575   -> OK
        "amount_cents": -5.75  -> ValueError (someone typed dollars, not cents)
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for t in data["transactions"]:
        # True/False count as ints in Python, so check the exact type.
        for field in ("amount_cents", "source_row_number"):
            if type(t[field]) is not int:
                raise ValueError(f"{t['id']}: {field} must be an integer, got {t[field]!r}")
    return data


def seed(con: sqlite3.Connection, fixture: dict, allow_other_data: bool = False) -> dict[str, int]:
    """Add the fixture's rows. Returns how many NEW rows went into each table.

        first time: {"imports": 1, "import_coverage": 1, "merchant_aliases": 4, "transactions": 7}
        again:      {"imports": 0, "import_coverage": 0, "merchant_aliases": 0, "transactions": 0}

    The tables already exist: the repo's connect() creates them.
    """
    # Safety check: don't mix fake rows into a database with real imports.
    ours = {i["id"] for i in fixture["imports"]}
    others = {r[0] for r in con.execute("SELECT id FROM imports")} - ours
    if others and not allow_other_data:
        raise RuntimeError(
            f"database already holds {len(others)} other import(s); refusing to add synthetic data. "
            "Use a separate --db file, or pass --allow-other-data if you really mean it.")

    inserted = {"imports": 0, "import_coverage": 0, "merchant_aliases": 0, "transactions": 0}
    account_name = fixture.get("account_name", "Synthetic Account")

    # One transaction: if ANY row fails, NOTHING from this run is saved.
    with con:
        # Order matters: imports first, because coverage and transactions point at them.
        for i in fixture["imports"]:
            cur = con.execute(
                "INSERT INTO imports(id, filename, sha256, created_at) VALUES(?,?,?,?) "
                "ON CONFLICT DO NOTHING",
                (i["id"], i["filename"], import_sha256(i["id"], fixture), i["created_at"]))
            inserted["imports"] += cur.rowcount          # 1 = added, 0 = skipped

            cur = con.execute(
                "INSERT INTO import_coverage(import_id, covered_start, covered_end) VALUES(?,?,?) "
                "ON CONFLICT(import_id) DO NOTHING",
                (i["id"], i["covered_start"], i["covered_end"]))
            inserted["import_coverage"] += cur.rowcount

        for m in fixture.get("merchant_aliases", []):
            cur = con.execute(
                "INSERT INTO merchant_aliases(pattern, merchant) VALUES(?,?) "
                "ON CONFLICT(pattern) DO NOTHING",
                (m["pattern"], m["merchant"]))
            inserted["merchant_aliases"] += cur.rowcount

        for t in fixture["transactions"]:
            # (import_id, source_row_number) is UNIQUE in the repo's schema:
            # "row 3 of this file" can only be stored once. That's our duplicate check.
            # The ? marks are filled in safely by SQLite - never paste values into SQL text.
            cur = con.execute(
                "INSERT INTO transactions(id, account_id, source_transaction_id, import_id, "
                "source_row_number, posted_date, description, amount_cents, original_row_json, "
                "predicted_type, predicted_category, created_at) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?,?) "
                "ON CONFLICT(import_id, source_row_number) DO NOTHING",
                (t["id"], t["account_id"], t["source_transaction_id"], t["import_id"],
                 t["source_row_number"], t["posted_date"], t["description"], t["amount_cents"],
                 original_row_json(t, account_name), t["predicted_type"], t["predicted_category"],
                 next(i["created_at"] for i in fixture["imports"] if i["id"] == t["import_id"])))
            inserted["transactions"] += cur.rowcount

    return inserted


def main(argv: list[str] | None = None) -> None:
    """What runs when you type: python -m compass.seed_synthetic"""
    parser = argparse.ArgumentParser(description="Seed a Compass database with synthetic data.")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH),
                        help="database file (default: .local/compass_synthetic.db)")
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE), help="fixture JSON file")
    parser.add_argument("--allow-other-data", action="store_true",
                        help="allow seeding into a database that already has other imports")
    args = parser.parse_args(argv)

    con = connect(args.db)          # the repo's connect(): creates all tables if missing
    try:
        counts = seed(con, load_fixture(args.fixture), args.allow_other_data)
    finally:
        con.close()                 # always close, even if something failed

    print(f"inserted {counts['imports']} import(s), {counts['import_coverage']} coverage row(s), "
          f"{counts['merchant_aliases']} alias(es), {counts['transactions']} transaction(s)")
    if sum(counts.values()) == 0:
        print("already seeded; nothing new to insert")


if __name__ == "__main__":
    main()
