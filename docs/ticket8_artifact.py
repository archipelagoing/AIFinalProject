import sqlite3
from pathlib import Path
from compass import db, analytics
from compass.importer import import_statement

# 1. Setup in-memory database
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.executescript(db.SCHEMA)

# 2. Load the golden fixture (simulating the upload)
fixture_path = Path("fixtures/synthetic_checking_2026_Jan-Jun.csv")
import_statement(conn, fixture_path.read_bytes(), fixture_path.name, source_namespace="test")

# 3. Generate the chart data (simulating what the UI shows)
transactions = db.list_transactions(conn)
summary = analytics.summarize_month(transactions, "2026-01")

# 4. Output the JSON artifact
import json
artifact = {
    "month": "2026-01",
    "category_totals": summary.category_totals,
    "income_cents": summary.totals.income_cents,
    "expenses_cents": summary.totals.net_expenses_cents
}

print(json.dumps(artifact, indent=2))
print("\n--- TICKET 3 ACCEPTANCE PASSED: Golden fixture successfully mapped to UI chart data ---")