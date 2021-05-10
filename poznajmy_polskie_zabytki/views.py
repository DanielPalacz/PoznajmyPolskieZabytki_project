
import functools
import sqlite3

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import abort
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


from poznajmy_polskie_zabytki.db import get_db

bp = Blueprint("views", __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/wyszukaj/')
def wyszukaj():
    if tuple(request.args):
        city = request.args.get("miasto")
        try:
            db = get_db()
            c = db.cursor()
            sql_query = f"SELECT * from zabytki where miejscowosc='{city}'"
            output = c.execute(sql_query).fetchall()
        except sqlite3.Error:
            abort(500)
        items = [tuple([id_temp+1]) + tuple(item) for id_temp, item in enumerate(output)]
        return render_template("search.html", city=city, items=items, quantity=len(items))
    else:
        return render_template('search_main.html')
