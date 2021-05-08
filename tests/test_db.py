import sqlite3
import pytest

from poznajmy_polskie_zabytki.db import get_db, populate_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
        c = db.cursor()
        c.execute("SELECT * from zabytki")
        record = [el for el in c.fetchone()]
        assert record[1] == "PL.1.9.ZIPOZ.NID_N_02_ZZ.23316"
        assert record[12] == "Dąbrowa Bolesławiecka"

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "Cannot operate on a closed database" in str(e.value)


def test_db_schema(app, zabytki_info_fixt):
    with app.app_context():
        c = get_db().cursor()
        # table name check
        table_name = c.execute("select name from sqlite_master where type = 'table'").fetchone()[0]

        assert "zabytki" == table_name
        # amount of colums check
        result = c.execute("PRAGMA table_info('zabytki')").fetchall()
        zabytki_table_info = ([tuple(el) for el in result])
        assert len(zabytki_table_info) == 15

        # name of teh particular columns check
        for column_info in zabytki_table_info:
            assert column_info[1] in zabytki_info_fixt


@pytest.mark.skip
def test_populatedb(app_without_db_content):
    with app_without_db_content.app_context():
        populate_db()
        c = get_db().cursor()
        # amount of records:
        quantity = c.execute("SELECT count(1) from zabytki").fetchone()[0]
        assert quantity == 78616


def test_init_db_command(runner, monkeypatch):
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("poznajmy_polskie_zabytki.db.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
