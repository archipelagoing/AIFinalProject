import sqlite3
from compass import db
from compass.importer import import_statement

# 1. Setup in-memory database
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.executescript(db.SCHEMA)

# 2. Import a fake transaction
csv_data = b"""date,description,amount,account,transaction_id
2026-01-01,Starbucks,-10.00,Checking,TX_001
2026-01-02,Amazon,-50.00,Checking,TX_002
"""

print("--- First Import ---")
result1 = import_statement(conn, csv_data, "statement.csv", source_namespace="test")
print(f"Imported rows: {result1.imported_rows}")
print(f"Duplicate detected: {result1.duplicate}")

# 3. Try to import the exact same data again
print("\n--- Second Import (Duplicate) ---")
result2 = import_statement(conn, csv_data, "statement.csv", source_namespace="test")
print(f"Imported rows: {result2.imported_rows}")
print(f"Duplicate detected: {result2.duplicate}")

# 4. Verify no double-counting
rows = db.list_transactions(conn)
print(f"\nTotal rows in database: {len(rows)}")
assert len(rows) == 2, "Double counting occurred! Database has duplicate rows."
assert result2.duplicate is True, "Duplicate was not flagged!"

print("\n--- TICKET 2 ACCEPTANCE PASSED: No double count ---")