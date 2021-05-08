
import os
import tempfile

import pytest

from poznajmy_polskie_zabytki import create_app
from poznajmy_polskie_zabytki.db import get_db
from poznajmy_polskie_zabytki.db import init_db

_data_sql = None
# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), "supported_data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")

zabytki_info = (
 "id",
 "inspire_id",
 "forma_ochrony",
 "dokladnosc_polozenia",
 "nazwa",
 "chronologia",
 "funkcja",
 "wykaz_dokumentow",
 "data_wpisu",
 "wojewodztwo",
 "powiat",
 "gmina",
 "miejscowosc",
 "ulica",
 "nr_adresowy")


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # create the database and load test data
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def app_without_db_content():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # create the database and load test data
    with app.app_context():
        init_db()

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app_without_db_content):
    """A test runner for the app's Click commands."""
    return app_without_db_content.test_cli_runner()


@pytest.fixture
def zabytki_info_fixt():
    """Returning info about zabytki table."""
    return zabytki_info
