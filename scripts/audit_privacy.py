"""Offline release inspection. Findings expose locations, never matched secret text."""

import argparse
import ast
import csv
import importlib.metadata
import json
from pathlib import Path
import re
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]
FICTIONAL_CSV_NAMES = (
    "synthetic_checking_2026_Jan-Jun.csv", "synthetic_savings_2026_Jan-Jun.csv",
    "synthetic_ground_truth.csv",
)
SECRET_PATTERNS = (
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    r"\bgh[pousr]_[A-Za-z0-9]{30,}\b",
    r"\bgithub_pat_[A-Za-z0-9_]{30,}\b",
    r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b",
    r"\bAIza[A-Za-z0-9_-]{30,}\b",
)


def secret_lines(text: str) -> list[int]:
    return [number for number, line in enumerate(text.splitlines(), 1)
            if any(re.search(pattern, line) for pattern in SECRET_PATTERNS)]


def is_planning_matrix(path: Path, plan: Path) -> bool:
    """Allow the declared ticket matrix, not arbitrary financial CSV uploads."""
    fields = ["requirement_id", "requirement_description", "ticket_id", "mapping_status",
              "verification_status", "automated_test_id", "evidence_url"]
    try:
        tickets = set(re.findall(r"^- \[[ xX]\] \*\*(CMP-\d{4}-D[1-4]-\d{2})\b", plan.read_text(), re.M))
        with path.open(encoding="utf-8-sig", newline="") as source:
            reader = csv.DictReader(source, strict=True)
            if reader.fieldnames != fields:
                return False
            rows = list(reader)
        return bool(rows) and len(tickets) == 96 and all(
            None not in row and all(value is not None for value in row.values())
            and re.fullmatch(r"REQ-(?:0[1-9]|1[0-2])", row["requirement_id"])
            and row["ticket_id"] in tickets
            and row["requirement_description"].strip()
            and row["mapping_status"].strip() and row["verification_status"].strip()
            for row in rows)
    except (OSError, UnicodeError, csv.Error):
        return False


def audit(root: Path = ROOT) -> dict:
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True).stdout.decode().split("\0")
    findings = []
    scanned = 0
    csv_count = planning_csv_count = 0
    canonical = {name: (root / "fixtures" / name).read_bytes() for name in FICTIONAL_CSV_NAMES}
    for name in filter(None, tracked):
        path = root / name
        if not path.is_file():  # Unrelated local deletions are not part of this release.
            continue
        if path.suffix == ".csv":
            if name == "COMPASS_COVERAGE_MATRIX.csv":
                planning_csv_count += 1
                if not is_planning_matrix(path, root / "COMPASS_ENGINEERING_PLAN.md"):
                    findings.append({"path": name, "reason": "Planning CSV has invalid schema or unknown ticket references"})
            elif name in {f"{folder}/{filename}" for folder in ("fixtures", "docs/demo") for filename in canonical} and path.read_bytes() == canonical.get(path.name):
                csv_count += 1
            else:
                findings.append({"path": name, "reason": "CSV is not a matching approved fictional fixture"})
        if (path.suffix in {".db", ".sqlite", ".sqlite3"} or path.name.startswith(".env")
                or name.startswith(("private-uploads/", ".local/", ".venv/"))
                or name == ".streamlit/secrets.toml"):
            findings.append({"path": name, "reason": "Private/generated artifact is tracked"})
        try:
            text = path.read_text()
        except (UnicodeError, OSError):
            continue
        scanned += 1
        for number in secret_lines(text):
            findings.append({"path": name, "line": number, "reason": "Possible secret; value redacted"})
    config = tomllib.loads((root / ".streamlit/config.toml").read_text())
    expected = [("browser", "gatherUsageStats", False), ("server", "address", "127.0.0.1"),
                ("server", "enableCORS", True), ("server", "enableXsrfProtection", True),
                ("client", "showErrorDetails", "none")]
    for section, key, value in expected:
        if config.get(section, {}).get(key) != value:
            findings.append({"path": ".streamlit/config.toml", "reason": f"Check {section}.{key}"})
    for path in [root / "app.py", *(root / "compass").glob("*.py")]:
        for node in ast.walk(ast.parse(path.read_text())):
            names = ([alias.name for alias in node.names] if isinstance(node, ast.Import)
                     else [node.module or ""] if isinstance(node, ast.ImportFrom) else [])
            if path.name != "ollama.py" and any(name.split(".")[0] in {"socket", "requests", "http", "urllib", "httpx", "boto3", "openai"} for name in names):
                findings.append({"path": str(path.relative_to(root)), "line": node.lineno, "reason": "Review new network-capable production import"})
    return {"ok": not findings, "tracked_text_files_scanned": scanned,
            "approved_fictional_csv_copies": csv_count, "planning_csv_files": planning_csv_count, "findings": findings,
            "scope": "Current tracked files and production network imports; heuristic inspection, not a history scan or security certification.",
            "dependencies": dict(sorted((dist.metadata["Name"], dist.version) for dist in importlib.metadata.distributions()))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Offline privacy inspection: {'PASS' if report['ok'] else 'FAIL'}; {report['tracked_text_files_scanned']} tracked text files; {report['approved_fictional_csv_copies']} fictional CSV copies.")
        for finding in report["findings"]:
            print(json.dumps(finding))
    raise SystemExit(0 if report["ok"] else 1)
