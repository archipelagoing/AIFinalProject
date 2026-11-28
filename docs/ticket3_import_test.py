import sqlite3
from compass.importer import import_statement
from compass import db

# Create an in-memory database using the team's schema
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.executescript(db.SCHEMA)

# Create a deliberately broken CSV (missing description and bad amount)
bad_csv_data = b"""date,description,amount,account,transaction_id
2026-01-01,Bad Row,-12.50,Checking,TX_001
2026-01-02,,,Checking,TX_002
"""

# Try to import it
result = import_statement(conn, bad_csv_data, "bad_statement.csv", source_namespace="test")

# Print the artifact
print("--- TICKET 3 ARTIFACT ---")
print(f"Valid rows: {result.valid_rows}")
print(f"Invalid rows: {result.invalid_rows}")
print(f"Rejected: {result.rejected_rows}")
print("Issues identified:")
for issue in result.issues:
    print(f" - Row {issue.row_number}: {issue.reason}")