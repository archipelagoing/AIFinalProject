"""Run from the repository root with: streamlit run app.py."""

import os
from contextlib import closing
from pathlib import Path
import sqlite3
import sys
import hashlib

if sys.version_info < (3, 11):
    raise RuntimeError("Compass requires Python 3.11 or later.")

import streamlit as st

from compass import analytics, classification, db, importer
from compass.contracts import Transaction, TransactionType, format_money
from compass.mapping import ColumnMapping

ROOT = Path(__file__).resolve().parent


def show_import_report(result: importer.ImportResult) -> None:
    if result.review_required:
        st.warning("Possible overlap needs source review. No rows were imported. Confirm distinct activity only after verifying that these are separate transactions.")
    elif result.issues:
        st.error("Statement rejected. No transactions from this import were saved.")
    elif result.duplicate:
        st.info("This identical statement is already imported, even under a renamed file. Existing records were kept.")
    else:
        st.success(f"Imported {result.imported_rows} transactions atomically.")
    for warning in result.warnings:
        st.warning(warning)
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
        "Account": db.account_label(row, imports[row.import_id]),
        "Normalized amount": format_money(row.amount_cents),
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
    st.warning(f"Activity dates: {dates[0]} through {dates[-1]}. Full statement coverage is unverified; this month may be incomplete. Import any missing statements before relying on this snapshot.")
    st.caption("Verified means classified, not reconciled to a bank balance. Surplus is not available cash.")
    unknown = [row for row in summary.excluded_rows if row.effective_type == TransactionType.UNKNOWN]
    if unknown:
        st.warning(f"{len(unknown)} unresolved transaction(s): {format_money(sum(abs(row.amount_cents) for row in unknown))} absolute value excluded from verified totals.")
    transfers = [row for row in summary.excluded_rows if row.effective_type == TransactionType.TRANSFER]
    if transfers:
        evidence = analytics.reconcile_transfers(transfers)
        st.info(f"{len(transfers)} transfer transaction(s) excluded from income and expenses. Transfer net: {format_money(totals.transfer_net_cents)}. Unique cross-account pairs supported by imported rows: {len(evidence.pairs)}.")
        if evidence.unmatched:
            st.warning(f"{len(evidence.unmatched)} transfer row(s) have missing or ambiguous matching evidence. They remain excluded; zero net does not establish reconciliation.")
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
    st.subheader("Net spending by category")
    st.dataframe([{"Category": category, "Net spending": format_money(amount)} for category, amount in summary.category_totals.items()], hide_index=True)
    show_review(connection, summary)
    with st.expander("Inspect original row and classification rule"):
        by_id = {row.id: row for row in summary.rows}
        selected_id = st.selectbox("Source transaction", list(by_id), format_func=lambda identity: f"{by_id[identity].posted_date} · {by_id[identity].description} · {by_id[identity].source_transaction_id or by_id[identity].source_row_number}", key=f"source_row_{month}")
        selected = by_id[selected_id]
        st.caption("Original field names and signs are preserved below. Table amounts use normalized positive inflows and negative outflows.")
        st.json(selected.original_row)
        st.write("Predicted classification: " + selected.predicted_type.value + " / " + selected.predicted_category)
        st.write("Rule: " + classification.classify(selected.description, selected.amount_cents).explanation)
        st.caption(f"Stable local record ID: {selected.id}; account identity: {selected.account_id}.")


def show_review(connection: sqlite3.Connection, summary: analytics.MonthSummary) -> None:
    with st.expander("Review and correct classifications"):
        st.caption("Only type/category overrides are editable. Original source values and rule predictions remain unchanged. Review is not bank-balance reconciliation.")
        st.write(f"Rows with saved overrides: {sum(row.has_correction for row in summary.rows)} / {len(summary.rows)}")
        only_unknown = st.checkbox("Only unresolved transactions", key="review_only_unknown")
        rows = [row for row in summary.rows if not only_unknown or row.effective_type == TransactionType.UNKNOWN]
        if not rows:
            st.info("No unresolved transactions in this month." if only_unknown else "No transactions to review.")
            return
        by_id = {row.id: row for row in rows}
        key = f"review_row_{summary.month}"
        if st.session_state.get(key) not in by_id:
            st.session_state[key] = next(iter(by_id))
        identity = st.selectbox("Transaction to review", list(by_id), format_func=lambda value: f"{by_id[value].posted_date} · {by_id[value].description} · {by_id[value].source_transaction_id or by_id[value].source_row_number}", key=key)
        row = by_id[identity]
        revision_key = f"review_revision_{identity}"
        revision = st.session_state.get(revision_key, 0)
        st.write(f"Normalized amount: {format_money(row.amount_cents)}; predicted {row.predicted_type.value} / {row.predicted_category}.")
        with st.form(f"review_form_{identity}_{revision}"):
            kind = st.selectbox("Effective transaction type", classification.TRANSACTION_TYPES, index=classification.TRANSACTION_TYPES.index(row.effective_type.value), key=f"edit_type_{identity}_{revision}")
            category = st.text_input("Effective category", value=row.effective_category, max_chars=80, key=f"edit_category_{identity}_{revision}")
            save = st.form_submit_button("Save classification")
            restore = st.form_submit_button("Restore rule classification")
        if save or restore:
            try:
                if restore:
                    db.restore_classification(connection, identity)
                else:
                    db.correct_classification(connection, identity, kind, category)
            except ValueError as error:
                st.error(str(error))
            except sqlite3.Error:
                st.error("The classification could not be saved. Check local storage; prior values were preserved.")
            else:
                st.session_state[revision_key] = revision + 1
                st.session_state["review_notice"] = "Classification saved; all snapshots and category totals recalculated. Original source data is unchanged."
                st.rerun()


def mapping_controls(upload) -> tuple[ColumnMapping | None, bool, str]:
    custom = st.checkbox("Map a different CSV layout", key="use_column_mapping")
    if not custom:
        return None, True, "canonical"
    if upload is None:
        st.info("Choose a CSV before configuring its columns.")
        return None, False, "no-file"
    try:
        headers = importer.read_headers(upload.getvalue())
    except ValueError as error:
        st.warning(str(error))
        return None, False, "invalid-file"
    token = hashlib.sha256(upload.getvalue()).hexdigest()
    with st.expander("Explicit column mapping", expanded=True):
        date_column = st.selectbox("Date column", headers, key=f"map_date_{token}")
        description_column = st.selectbox("Description column", headers, index=min(1, len(headers) - 1), key=f"map_description_{token}")
        account_column = st.selectbox("Account column", [None, *headers], format_func=lambda value: value or "Use one fixed account name", key=f"map_account_{token}")
        fixed_account = st.text_input("Fixed account name", key=f"map_fixed_{token}") if account_column is None else None
        source_column = st.selectbox("Transaction ID column", [None, *headers], format_func=lambda value: value or "No source transaction IDs", key=f"map_id_{token}")
        formats = {"%Y-%m-%d": "YYYY-MM-DD", "%m/%d/%Y": "MM/DD/YYYY", "%d/%m/%Y": "DD/MM/YYYY"}
        date_format = st.selectbox("Date format", list(formats), format_func=formats.get, key=f"map_format_{token}")
        modes = {"": "Choose an amount convention", "inflow_positive": "Signed amount: positive = inflow", "outflow_positive": "Signed amount: positive = outflow", "debit_credit": "Separate debit and credit columns (nonnegative)"}
        mode = st.selectbox("Amount convention", list(modes), format_func=modes.get, key=f"map_mode_{token}")
        if not mode:
            st.info("Explicitly choose debit/credit direction. Compass does not infer it.")
            return None, False, token
        amount = debit = credit = None
        if mode == "debit_credit":
            debit = st.selectbox("Debit column (money leaving)", headers, key=f"map_debit_{token}")
            credit = st.selectbox("Credit column (money entering)", headers, key=f"map_credit_{token}")
        else:
            amount = st.selectbox("Signed amount column", headers, key=f"map_amount_{token}")
        mapping = ColumnMapping(date_column=date_column, description_column=description_column,
                                account_column=account_column, fixed_account=fixed_account,
                                transaction_id_column=source_column, date_format=date_format,
                                amount_mode=mode, amount_column=amount, debit_column=debit, credit_column=credit)
        try:
            mapping.validate(headers)
        except ValueError as error:
            st.warning(str(error))
            return None, False, token
        signature = hashlib.sha256(mapping.to_json().encode()).hexdigest()
        confirmed = st.checkbox("I confirm this column mapping, date order, and amount direction", key=f"map_confirm_{token}_{signature}")
        return mapping, confirmed, token + signature


def main() -> None:
    st.set_page_config(page_title="Compass — local financial snapshot", page_icon="🧭")
    st.title("Compass Alpha 0.1")
    st.caption("Private, local-first financial assistant · Phase 2 import and review")
    st.warning("All bundled demo statements are fictional. This experimental app is not financial advice.")
    st.caption("CSV files are processed locally and stored in SQLite. No cloud model or API key is required. Use fictional data while evaluating this experimental app.")
    database_path = Path(os.environ.get("COMPASS_DB_PATH", str(ROOT / ".local" / "compass.db")))
    try:
        with closing(db.connect(database_path)) as connection:
            st.subheader("Import a statement")
            if st.button("Load fictional checking statement", key="load_checking"):
                data = (ROOT / "fixtures" / importer.DEMO_STATEMENTS[0]).read_bytes()
                st.session_state["last_import_result"] = importer.import_statement(connection, data, importer.DEMO_STATEMENTS[0], source_namespace="fictional-demo")
            if st.button("Load fictional savings statement", key="load_savings"):
                data = (ROOT / "fixtures" / importer.DEMO_STATEMENTS[1]).read_bytes()
                st.session_state["last_import_result"] = importer.import_statement(connection, data, importer.DEMO_STATEMENTS[1], source_namespace="fictional-demo")
            # File selection must rerun immediately to enable the submit button.
            # Putting this uploader inside the form would keep it disabled.
            upload = st.file_uploader("Statement CSV (UTF-8; up to 5 MB)", type=["csv"])
            mapping, ready, context = mapping_controls(upload)
            file_token = hashlib.sha256(upload.getvalue()).hexdigest() if upload is not None else "empty"
            with st.form("statement_upload"):
                namespace = st.text_input("Bank/source identity", value="my-bank", help="Use the same identity for statements from the same bank, and different identities for different banks with similarly named accounts.")
                st.caption("Required columns: " + ",".join(importer.REQUIRED_COLUMNS) + ". Dates: YYYY-MM-DD. Positive amounts are inflows; negative amounts are outflows.")
                confirm_distinct = st.checkbox("Keep flagged look-alike rows as distinct activity (only after source verification)", key=f"confirm_distinct_{file_token}_{context}")
                submitted = st.form_submit_button("Import CSV", disabled=upload is None or not ready)
            if submitted and upload is not None:
                st.session_state["last_import_result"] = importer.import_statement(connection, upload.getvalue(), upload.name, source_namespace=namespace, mapping=mapping, confirm_distinct=confirm_distinct)
            if "last_import_result" in st.session_state:
                show_import_report(st.session_state["last_import_result"])
            if "review_notice" in st.session_state:
                st.success(st.session_state.pop("review_notice"))
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
    st.caption("Ask Compass and What If? remain later Python phases. Evaluation files never supply the app's financial answers.")


if __name__ == "__main__":
    main()
