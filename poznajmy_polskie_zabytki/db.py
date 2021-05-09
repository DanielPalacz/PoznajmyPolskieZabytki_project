import sqlite3
import pandas as pd

import click
from flask import current_app, g
from flask.cli import with_appcontext

sql_insert_into_zabytki = \
    "INSERT INTO zabytki VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

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


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def populate_db():
    db = get_db()
    df_data = pd.read_csv(current_app.config["INPUT"])
    df_size = len(df_data.index)
    c = db.cursor()
    for number in range(df_size):
        input_data = tuple(df_data.iloc[number])
        input_row = (df_data.index[number], *input_data)
        c.execute(sql_insert_into_zabytki, input_row)
    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Create new DB with zabytki table if not exists."""
    try:
        init_db()
        populate_db()
    except sqlite3.IntegrityError:
        click.echo("Initialized the database. "
                   "But due to 'IntegrityError' data population failed.")
    else:
        click.echo("Initialized the database. Data were automatically loaded.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
