
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


def create_sql_query(*, city="", parish="", county="", keyword="") -> str:
    sql_query = "SELECT * from zabytki where"
    if city:
        sql_query += " miejscowosc='" + city + "'"
    if parish:
        if city:
            sql_query += " and"
        sql_query += " gmina like '%" + parish + "%'"
    if county:
        if city or parish:
            sql_query += " and"
        sql_query += " powiat='" + county + "'"
    if keyword:
        if city or parish or county:
            sql_query += " and"
        sql_query += " ( nazwa like '%" + keyword + "%'" + " or funkcja like '%" + keyword + "%'"
        sql_query += " or wojewodztwo like '%" + keyword + "%'" + " or chronologia like '%" + keyword + "%' )"
    return sql_query


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/wyszukaj/')
def wyszukaj():
    city = request.args.get("miasto", "")
    parish = request.args.get("gmina", "")
    county = request.args.get("powiat", "")
    keyword = request.args.get("dowolneslowo", "")
    if city or parish or county or keyword:
        try:
            db = get_db()
            sql_query = create_sql_query(city=city, parish=parish, county=county, keyword=keyword)
            output = db.execute(sql_query).fetchall()
        except sqlite3.Error:
            abort(500)
        items = [tuple([id_temp+1]) + tuple(item) for id_temp, item in enumerate(output)]
        return render_template("search.html", city=city, items=items, quantity=len(items))
    else:
        return render_template('search_main.html')
