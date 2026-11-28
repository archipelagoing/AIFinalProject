import sqlite3
from compass import db, analytics
from compass.importer import import_statement

# 1. Setup in-memory database
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.executescript(db.SCHEMA)

# 2. Import a fake transaction
csv_data = b"""date,description,amount,account,transaction_id
2026-01-01,Unknown Shop,-50.00,Checking,TX_001
"""
import_statement(conn, csv_data, "test.csv", source_namespace="test")

# 3. Check initial state (it should be 'Uncategorized' or 'unknown')
rows_before = db.list_transactions(conn)
print(f"Before correction - Category: {rows_before[0].effective_category}")

# 4. Perform the correction (What the UI does when you click 'Save')
tx_id = rows_before[0].id
db.correct_classification(conn, tx_id, "expense", "Coffee")

# 5. Check the result
rows_after = db.list_transactions(conn)
print(f"After correction  - Category: {rows_after[0].effective_category}")
print(f"Has correction flag: {rows_after[0].has_correction}")

# 6. Check if aggregates updated
summary = analytics.summarize_month(rows_after, "2026-01")
coffee_total = summary.category_totals.get("Coffee", 0)
print(f"Coffee aggregate total: {coffee_total} cents")

assert rows_after[0].effective_category == "Coffee", "Correction failed to save"
assert coffee_total == 5000, "Aggregates did not update"
print("--- TICKET 1 ACCEPTANCE PASSED ---")