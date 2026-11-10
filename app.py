"""Run from the repository root with: streamlit run app.py."""

import os
from contextlib import closing
from pathlib import Path
import sqlite3
import sys

if sys.version_info < (3, 11):
    raise RuntimeError("Compass requires Python 3.11 or later.")

import streamlit as st

from compass import analytics, classification, db, importer
from compass.contracts import Transaction, TransactionType, format_money

ROOT = Path(__file__).resolve().parent


def show_import_report(result: importer.ImportResult) -> None:
    if result.issues:
        st.error("Statement rejected. No transactions from this import were saved.")
    elif result.duplicate:
        st.info("This identical statement is already imported, even under a renamed file. Existing records were kept.")
    else:
        st.success(f"Imported {result.imported_rows} transactions atomically.")
    columns = st.columns(3)
    columns[0].metric("Accepted rows", result.imported_rows)
    columns[1].metric("Rejected rows", result.rejected_rows)
    columns[2].metric("Already imported", result.total_rows if result.duplicate else 0)
    st.caption(f"Rows read: {result.total_rows}. Valid CSV rows: {result.valid_rows}. Invalid CSV rows: {result.invalid_rows}. An invalid statement rejects all its rows, including otherwise valid ones.")
    if result.issues:
        st.dataframe([
            {"Row": str(issue.row_number) if issue.row_number is not None else "File",
             "CSV line": str(issue.line_number) if issue.line_number is not None else "—",
             "Reason": issue.reason}
            for issue in result.issues
        ], hide_index=True)


def evidence_rows(rows: tuple[Transaction, ...] | list[Transaction], imports: dict[str, dict]) -> list[dict]:
    return [{
        "Date": row.posted_date,
        "Description": row.description,
        "Account": row.original_row.get("account", row.account_id),
        "Source amount": format_money(row.amount_cents),
        "Type": row.effective_type.value,
        "Category": row.effective_category,
        "Corrected": row.has_correction,
        "Source ID": row.source_transaction_id or "(not supplied)",
        "Source row": row.source_row_number,
        "File": imports[row.import_id]["filename"],
        "Import SHA-256": imports[row.import_id]["sha256"],
    } for row in rows]


def show_snapshot(connection: sqlite3.Connection) -> None:
    transactions = db.list_transactions(connection)
    if not transactions:
        st.info("No transactions imported yet. Load the fictional checking statement or import a supported CSV to see a snapshot.")
        return
    imports = {record["id"]: record for record in db.list_imports(connection)}
    months = sorted({row.posted_date[:7] for row in transactions})
    if st.session_state.get("summary_month") not in months:
        st.session_state["summary_month"] = "2026-05" if "2026-05" in months else months[-1]
    st.subheader("Monthly snapshot")
    month = st.selectbox("Statement month", months, key="summary_month")
    summary = analytics.summarize_month(transactions, month)
    totals = summary.totals
    columns = st.columns(3)
    columns[0].metric("Verified income", format_money(totals.income_cents))
    columns[1].metric("Net expenses", format_money(totals.net_expenses_cents))
    columns[2].metric("Verified surplus", format_money(totals.surplus_cents))
    dates = sorted(row.posted_date for row in summary.rows)
    st.caption(f"Activity dates: {dates[0]} through {dates[-1]}. Full statement coverage is unverified; this month may be incomplete. Verified means classified, not reconciled to a bank balance. Surplus is not available cash.")
    unknown = [row for row in summary.excluded_rows if row.effective_type == TransactionType.UNKNOWN]
    if unknown:
        st.warning(f"{len(unknown)} unresolved transaction(s): {format_money(sum(abs(row.amount_cents) for row in unknown))} absolute value excluded from verified totals.")
    transfers = [row for row in summary.excluded_rows if row.effective_type == TransactionType.TRANSFER]
    if transfers:
        st.info(f"{len(transfers)} transfer transaction(s) excluded from income and expenses. Matching entries across accounts have not been reconciled in this phase.")
    with st.expander("Income calculation and source rows"):
        st.write(f"Sum of {len(summary.income_rows)} classified income transaction(s) = {format_money(totals.income_cents)}.")
        st.dataframe(evidence_rows(summary.income_rows, imports), hide_index=True)
    with st.expander("Net expense calculation and source rows"):
        expenses = sum(-row.amount_cents for row in summary.expense_rows if row.effective_type == TransactionType.EXPENSE)
        refunds = sum(row.amount_cents for row in summary.expense_rows if row.effective_type == TransactionType.REFUND)
        st.write(f"{format_money(expenses)} expenses − {format_money(refunds)} refunds = {format_money(totals.net_expenses_cents)} net expenses.")
        st.dataframe(evidence_rows(summary.expense_rows, imports), hide_index=True)
    with st.expander("Surplus calculation and source rows"):
        st.write(f"{format_money(totals.income_cents)} income − {format_money(totals.net_expenses_cents)} net expenses = {format_money(totals.surplus_cents)} surplus.")
        st.dataframe(evidence_rows(summary.surplus_rows, imports), hide_index=True)
    if summary.excluded_rows:
        with st.expander("Excluded transfers and unresolved source rows"):
            st.dataframe(evidence_rows(summary.excluded_rows, imports), hide_index=True)
    st.subheader("Selected month's transactions")
    st.dataframe(evidence_rows(summary.rows, imports), hide_index=True)
    with st.expander("Inspect original row and classification rule"):
        by_id = {row.id: row for row in summary.rows}
        selected_id = st.selectbox("Source transaction", list(by_id), format_func=lambda identity: f"{by_id[identity].posted_date} · {by_id[identity].description} · {by_id[identity].source_transaction_id or by_id[identity].source_row_number}", key=f"source_row_{month}")
        selected = by_id[selected_id]
        st.json(selected.original_row)
        st.write("Predicted classification: " + selected.predicted_type.value + " / " + selected.predicted_category)
        st.write("Rule: " + classification.classify(selected.description, selected.amount_cents).explanation)
        st.caption(f"Stable local record ID: {selected.id}; account identity: {selected.account_id}.")


def main() -> None:
    st.set_page_config(page_title="Compass — local financial snapshot", page_icon="🧭")
    st.title("Compass Alpha 0.1")
    st.caption("Private, local-first financial assistant · Phase 1 import and snapshot")
    st.warning("All bundled demo statements are fictional. This experimental app is not financial advice.")
    st.caption("CSV files are processed locally and stored in SQLite. No cloud model or API key is required. Use fictional data while evaluating this experimental app.")
    database_path = Path(os.environ.get("COMPASS_DB_PATH", str(ROOT / ".local" / "compass.db")))
    try:
        with closing(db.connect(database_path)) as connection:
            st.subheader("Import a statement")
            if st.button("Load fictional checking statement", key="load_checking"):
                data = (ROOT / "fixtures" / importer.DEMO_STATEMENTS[0]).read_bytes()
                st.session_state["last_import_result"] = importer.import_statement(connection, data, importer.DEMO_STATEMENTS[0], source_namespace="fictional-demo")
            # File selection must rerun immediately to enable the submit button.
            # Putting this uploader inside the form would keep it disabled.
            upload = st.file_uploader("Statement CSV (UTF-8; up to 5 MB)", type=["csv"])
            with st.form("statement_upload"):
                namespace = st.text_input("Bank/source identity", value="my-bank", help="Use the same identity for statements from the same bank, and different identities for different banks with similarly named accounts.")
                st.caption("Required columns: " + ",".join(importer.REQUIRED_COLUMNS) + ". Dates: YYYY-MM-DD. Positive amounts are inflows; negative amounts are outflows.")
                submitted = st.form_submit_button("Import CSV", disabled=upload is None)
            if submitted and upload is not None:
                st.session_state["last_import_result"] = importer.import_statement(connection, upload.getvalue(), upload.name, source_namespace=namespace)
            if "last_import_result" in st.session_state:
                show_import_report(st.session_state["last_import_result"])
            show_snapshot(connection)
    except (OSError, ValueError, sqlite3.Error):
        st.error("Compass could not open or process the local statement workspace. Check database permissions and the fictional fixture files. No financial answer can be shown for a failed operation.")
        return
    with st.expander("Fictional demo fixture inventory"):
        try:
            st.table([importer.inspect_demo_statement(ROOT / "fixtures" / name) for name in importer.DEMO_STATEMENTS])
        except (OSError, ValueError):
            st.warning("A bundled fictional fixture could not be inspected; check the fixture audit.")
    with st.expander("Locked data contracts"):
        st.write("Positive signed amounts are inflows; negative amounts are outflows. Money is stored as integer cents and dates as ISO YYYY-MM-DD.")
        st.write("Transaction types: " + ", ".join(classification.TRANSACTION_TYPES) + ". Categories are separate from types; transfers and unknowns are excluded from verified totals.")
        st.write("Original amount, date, description, account, source IDs, row data, and import metadata are preserved. Classification changes are stored separately.")
    st.caption("Review/edit UI, savings-transfer reconciliation, Ask Compass, and What If? are later Python phases. Evaluation files never supply the app's financial answers.")


if __name__ == "__main__":
    main()
