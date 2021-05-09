
import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
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
        db = get_db()
        c = db.cursor()
        sql_query = f"SELECT * from zabytki where miejscowosc='{city}'"
        output = c.execute(sql_query).fetchall()
        print()
        for x in output:
            print(tuple(x))
        print()
        items = [tuple(item) for item in output]
        quantity = len(items)
        return render_template("search.html", city=city, items=items, quantity=quantity)
        # return f"Not implemented, but query parameter is: '{city}' and ..."
    else:
        return render_template('search_main.html')
