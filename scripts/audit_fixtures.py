"""Independent fixture-only audit. Never imported by the app or financial tools.

This checks statement amounts against reference classifications and expected totals.
It does not evaluate production keyword classification (a later-phase requirement).
"""

import argparse
from collections import defaultdict
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
STATEMENTS = ("synthetic_checking_2026_Jan-Jun.csv", "synthetic_savings_2026_Jan-Jun.csv")
METRICS = ("income", "expenses_net_of_refunds", "surplus_before_transfers_and_unknown", "transfer_net_across_accounts", "unknown_net_excluded")
KINDS = {"income", "expense", "refund", "transfer", "unknown"}


def _cents(value: str | Decimal) -> int:
    text = str(value)
    if not re.fullmatch(r"[+-]?\d+(?:\.\d{1,2})?", text, flags=re.ASCII):
        raise ValueError("Expected a signed decimal with at most two fractional digits.")
    amount = Decimal(text)
    if not amount.is_finite():
        raise ValueError("Amount must be finite.")
    return int(amount * 100)


def _read_csv(path: Path, required: set[str]) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source, strict=True)
        if reader.fieldnames is None or len(set(reader.fieldnames)) != len(reader.fieldnames) or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path.name}: missing or repeated headers.")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{path.name}: no records.")
    return rows


def audit_fixtures(directory: Path) -> dict:
    errors, discrepancies = [], []
    totals = defaultdict(lambda: {metric: 0 for metric in METRICS})
    seen_ids, accounts = set(), set()
    try:
        labels = _read_csv(directory / "synthetic_ground_truth.csv", {"transaction_id", "expected_type", "expected_category"})
        truth = {}
        for label in labels:
            identity = label["transaction_id"]
            if not identity or identity in truth:
                raise ValueError(f"Duplicate/empty reference transaction ID: {identity!r}")
            if label["expected_type"] not in KINDS or not label["expected_category"]:
                raise ValueError(f"Invalid reference classification: {identity}")
            truth[identity] = label
        for filename in STATEMENTS:
            rows = _read_csv(directory / filename, {"date", "description", "amount", "account", "transaction_id"})
            for ordinal, row in enumerate(rows, start=2):
                try:
                    if None in row or any(value is None for value in row.values()):
                        raise ValueError("Malformed source row.")
                    identity = row["transaction_id"]
                    if not identity or identity in seen_ids:
                        raise ValueError("Duplicate/empty reference statement transaction ID.")
                    seen_ids.add(identity)
                    if identity not in truth:
                        raise ValueError(f"Missing classification oracle for {identity}.")
                    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["date"], flags=re.ASCII):
                        raise ValueError("Date must use YYYY-MM-DD.")
                    date.fromisoformat(row["date"])
                    if not row["account"].strip() or not row["description"].strip():
                        raise ValueError("Account/description is empty.")
                    accounts.add(row["account"])
                    amount = _cents(row["amount"])
                    kind = truth[identity]["expected_type"]
                    if (kind in {"income", "refund"} and amount <= 0) or (kind == "expense" and amount >= 0):
                        raise ValueError(f"Amount sign conflicts with reference type {kind}.")
                    total = totals[row["date"][:7]]
                    if kind == "income":
                        total["income"] += amount
                    elif kind in {"expense", "refund"}:
                        total["expenses_net_of_refunds"] -= amount
                    elif kind == "transfer":
                        total["transfer_net_across_accounts"] += amount
                    else:
                        total["unknown_net_excluded"] += amount
                except (ValueError, InvalidOperation) as error:
                    errors.append(f"{filename}, row {ordinal}: {error}")
        unused = set(truth) - seen_ids
        if unused:
            errors.append("Reference classifications without source rows: " + ", ".join(sorted(unused)))
        with (directory / "expected_monthly_totals.json").open(encoding="utf-8") as source:
            expected = json.load(source, parse_float=Decimal, parse_int=Decimal)
        for month in sorted(set(expected) | set(totals)):
            if month not in totals or month not in expected:
                errors.append(f"{month}: month missing from statements or expected totals.")
                continue
            totals[month]["surplus_before_transfers_and_unknown"] = totals[month]["income"] - totals[month]["expenses_net_of_refunds"]
            for metric in METRICS:
                actual = totals[month][metric]
                wanted = _cents(expected[month][metric])
                if actual != wanted:
                    discrepancies.append({"month": month, "metric": metric, "expected_cents": wanted, "actual_cents": actual})
    except (OSError, ValueError, csv.Error, KeyError, TypeError, InvalidOperation) as error:
        errors.append(str(error))
    return {"ok": not errors and not discrepancies, "transaction_count": len(seen_ids), "accounts": sorted(accounts), "totals_cents": dict(sorted(totals.items())), "errors": errors, "discrepancies": discrepancies}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=ROOT / "fixtures")
    parser.add_argument("--json", action="store_true", help="Emit an exact-cent machine-readable report.")
    args = parser.parse_args()
    report = audit_fixtures(args.fixtures)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Fictional fixture audit: {'PASS' if report['ok'] else 'FAIL'}")
        print(f"{report['transaction_count']} transactions; accounts: {', '.join(report['accounts'])}")
        for month, totals in report["totals_cents"].items():
            print(f"{month}: income={totals['income']} expenses={totals['expenses_net_of_refunds']} surplus={totals['surplus_before_transfers_and_unknown']} cents")
        for error in report["errors"]:
            print("ERROR: " + error)
        for discrepancy in report["discrepancies"]:
            print("MISMATCH: " + json.dumps(discrepancy))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
