"""Run from the repository root with: streamlit run app.py."""

import os
from pathlib import Path
import sqlite3
import sys

if sys.version_info < (3, 11):
    raise RuntimeError("Compass requires Python 3.11 or later.")

import streamlit as st

from compass import analytics, classification, db, importer, questions, scenarios

ROOT = Path(__file__).resolve().parent


def main() -> None:
    st.set_page_config(page_title="Compass — local alpha foundation", page_icon="🧭")
    st.title("Compass Alpha 0.1")
    st.caption("Private, local-first financial assistant · Phase 0 foundation")
    st.warning("All bundled demo statements are fictional. This experimental app is not financial advice.")
    st.info("Phase 0 establishes the app, contracts, database schema, and fixture validation. CSV ingestion, financial summaries, questions, and What If? UI are later phases.")
    database_path = Path(os.environ.get("COMPASS_DB_PATH", str(ROOT / ".local" / "compass.db")))
    try:
        connection = db.connect(database_path)
        connection.close()
        inventory = [importer.inspect_demo_statement(ROOT / "fixtures" / name) for name in importer.DEMO_STATEMENTS]
    except (OSError, ValueError, sqlite3.Error):
        st.error("Setup validation failed. Check the local database location and bundled fictional CSV files; run the fixture audit from the README for details.")
        return
    st.success("Local SQLite schema and fictional statement files are ready.")
    st.subheader("Fictional demo statements")
    st.table(inventory)
    st.caption("These files are inspected for setup only; no transactions have been imported.")
    with st.expander("Locked data contracts"):
        st.write("Positive signed amounts are inflows; negative amounts are outflows. Money is stored as integer cents and dates as ISO YYYY-MM-DD.")
        st.write("Transaction types: " + ", ".join(classification.TRANSACTION_TYPES) + ". Categories are separate from types; transfers and unknowns are excluded from verified totals.")
        st.write("Original amount, date, description, account, source IDs, row data, and import metadata are preserved. Classification changes are stored separately.")
    st.caption("No cloud key or local language model is required. Test oracles are used only by tests and the separate audit tool.")


if __name__ == "__main__":
    main()
