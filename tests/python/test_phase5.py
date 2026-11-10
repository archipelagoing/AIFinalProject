"""Release deletion, rollback, privacy guards, and a clean complete demo story."""

import hashlib
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import tomllib

import pytest

from compass import db, importer

ROOT = Path(__file__).resolve().parents[2]


def load(conn):
    for filename in importer.DEMO_STATEMENTS:
        assert importer.import_statement(conn, (ROOT / "fixtures" / filename).read_bytes(), filename).ok


def counts(conn):
    return tuple(conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                 for table in ("transactions", "import_settings", "imports"))


def test_clear_data_persists_after_real_process_restart_and_keeps_fixtures(tmp_path):
    fixture_hashes = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in (ROOT / "fixtures").iterdir() if path.is_file()}
    path = tmp_path / "delete.db"
    conn = db.connect(path)
    load(conn)
    row = db.list_transactions(conn)[0]
    db.correct_classification(conn, row.id, "unknown", "Private review")
    assert counts(conn) == (164, 2, 2)
    db.clear_all_data(conn)
    assert counts(conn) == (0, 0, 0) and not conn.in_transaction
    assert conn.execute("PRAGMA secure_delete").fetchone()[0] == 1
    conn.close()
    result = subprocess.run([sys.executable, "-c", "from compass import db; import sys; c=db.connect(sys.argv[1]); assert not db.list_transactions(c); assert not db.list_imports(c); c.close()", str(path)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert all(hashlib.sha256(path.read_bytes()).hexdigest() == digest for path, digest in fixture_hashes.items())
    conn = db.connect(path)
    load(conn)
    assert counts(conn) == (164, 2, 2)
    conn.close()


def test_clear_data_rolls_back_all_tables_on_failure_and_does_not_commit_callers_work():
    conn = db.connect(":memory:")
    load(conn)
    before = db.list_transactions(conn)
    conn.execute("CREATE TRIGGER fail_clear BEFORE DELETE ON imports BEGIN SELECT RAISE(ABORT, 'test'); END")
    with pytest.raises(sqlite3.IntegrityError):
        db.clear_all_data(conn)
    assert counts(conn) == (164, 2, 2) and db.list_transactions(conn) == before
    conn.execute("DROP TRIGGER fail_clear")
    conn.execute("BEGIN")
    with pytest.raises(ValueError, match="Finish"):
        db.clear_all_data(conn)
    assert conn.in_transaction
    conn.rollback()
    db.clear_all_data(conn)
    assert counts(conn) == (0, 0, 0)
    db.clear_all_data(conn)  # Empty deletion is safe and repeatable.
    conn.close()


def test_local_security_config_and_generated_artifact_ignores():
    config = tomllib.loads((ROOT / ".streamlit/config.toml").read_text())
    assert config["browser"]["gatherUsageStats"] is False
    assert config["server"]["address"] == "127.0.0.1"
    assert config["server"]["enableXsrfProtection"] is True
    assert config["server"]["enableCORS"] is True
    assert config["client"]["showErrorDetails"] == "none"
    assert ":http" not in config["theme"]["font"]
    private_paths = [".venv/example", "example.db", "example.db-wal", "example.db-shm", "example.sqlite3",
                     ".env", ".env.production", "private-uploads/bank.csv", "__pycache__/x.pyc", ".pytest_cache/x", ".local/compass.db", ".streamlit/secrets.toml"]
    result = subprocess.run(["git", "check-ignore", "--stdin"], cwd=ROOT, input="\n".join(private_paths) + "\n", text=True, capture_output=True, check=True)
    assert set(result.stdout.splitlines()) == set(private_paths)
    assert subprocess.run(["git", "check-ignore", "fixtures/synthetic_checking_2026_Jan-Jun.csv"], cwd=ROOT, capture_output=True).returncode == 1


def test_offline_secret_inspection_reports_lines_without_values():
    from scripts.audit_privacy import secret_lines

    assert secret_lines("documentation only\n" + "ghp_" + "a" * 36 + "\n") == [2]
    assert secret_lines("sk-" + "a" * 40) == [1]
    assert secret_lines("Set API_KEY locally; do not commit keys") == []


def test_ticket_matrix_is_validated_separately_from_financial_csv(tmp_path):
    from scripts.audit_privacy import is_planning_matrix

    plan = ROOT / "COMPASS_ENGINEERING_PLAN.md"
    matrix = ROOT / "COMPASS_COVERAGE_MATRIX.csv"
    assert is_planning_matrix(matrix, plan)
    invalid = tmp_path / matrix.name
    invalid.write_text("date,description,amount,account,transaction_id\n2026-05-01,Private,-1,Checking,a\n")
    assert not is_planning_matrix(invalid, plan)
    invalid.write_text(matrix.read_text().replace("CMP-1112-D1-03", "CMP-9999-D1-01", 1))
    assert not is_planning_matrix(invalid, plan)


def test_clean_ui_release_story_and_confirmed_delete(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    path = tmp_path / "release.db"
    monkeypatch.setenv("COMPASS_DB_PATH", str(path))
    # Fail any unexpected backend network connection during the complete story.
    attempts = []
    def forbidden_connect(*args, **kwargs):
        attempts.append(True)
        raise AssertionError("Unexpected backend network connection")
    monkeypatch.setattr(socket.socket, "connect", forbidden_connect)
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    assert app.button(key="clear_all_data").disabled
    app.button(key="load_checking").click().run(timeout=30)
    app.button(key="load_savings").click().run(timeout=30)
    assert not app.exception and not app.error
    metric = lambda label: next(item.value for item in app.metric if item.label == label)
    assert metric("Verified surplus") == "$747.06"
    app.text_input(key="ask_input").input("surplus in May 2026")
    next(item for item in app.button if item.label == "Ask Compass").click().run(timeout=30)
    assert metric("Ask Compass result") == "$747.06"
    conn = db.connect(path)
    row = next(row for row in db.list_transactions(conn) if row.posted_date.startswith("2026-05") and row.effective_category == "Groceries")
    conn.close()
    app.selectbox(key="review_row_2026-05").select(row.id).run(timeout=30)
    app.text_input(key=f"edit_category_{row.id}_0").input("Food at home")
    next(item for item in app.button if item.label == "Save classification").click().run(timeout=30)
    assert metric("Ask Compass result") == "$747.06"
    app.selectbox(key="scenario_mode").select("replace").run(timeout=30)
    assert metric("Projected monthly surplus") == "$522.06"
    app.selectbox(key="scenario_mode").select("additional").run(timeout=30)
    assert metric("Projected monthly surplus") == "−$752.94"
    fresh = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    assert not fresh.exception and not fresh.error
    conn = db.connect(path)
    assert db.get_transaction(conn, row.id).effective_category == "Food at home"
    assert counts(conn) == (164, 2, 2)
    conn.close()
    app.checkbox(key="delete_confirm").check().run(timeout=30)
    assert app.button(key="clear_all_data").disabled
    app.text_input(key="delete_phrase").input("DELETE").run(timeout=30)
    assert not app.button(key="clear_all_data").disabled
    app.button(key="clear_all_data").click().run(timeout=30)
    assert not app.exception and not app.error
    assert any("All imported local records were cleared" in item.value for item in app.success)
    assert any("No transactions imported yet" in item.value for item in app.info)
    assert "asked_question" not in app.session_state
    assert not any(item.label in {"Ask Compass result", "Projected monthly surplus"} for item in app.metric)
    assert app.button(key="clear_all_data").disabled
    assert app.session_state["upload_epoch"] == 1
    reopened = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    assert any("No transactions imported yet" in item.value for item in reopened.info)
    reopened.button(key="load_checking").click().run(timeout=30)
    assert not reopened.exception and not reopened.error
    assert not attempts


def test_failed_deletion_reports_error_and_preserves_rows(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    path = tmp_path / "failure.db"
    monkeypatch.setenv("COMPASS_DB_PATH", str(path))
    conn = db.connect(path)
    load(conn)
    conn.close()
    def fail(conn):
        raise sqlite3.OperationalError("busy")
    monkeypatch.setattr(db, "clear_all_data", fail)
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    app.checkbox(key="delete_confirm").check().run(timeout=30)
    app.text_input(key="delete_phrase").input("DELETE").run(timeout=30)
    app.button(key="clear_all_data").click().run(timeout=30)
    assert not app.exception and any("could not be cleared" in item.value for item in app.error)
    conn = db.connect(path)
    assert counts(conn) == (164, 2, 2)
    conn.close()
