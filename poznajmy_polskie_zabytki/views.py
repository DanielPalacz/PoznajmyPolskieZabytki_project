
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


def _create_sql_query(*, city="", parish="", county="", keyword="", voivodeship="") -> str:
    if city or parish or county or keyword or voivodeship:
        sql_query = "SELECT * from zabytki where"
    else:
        return ""
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
    if voivodeship:
        if city or parish or county:
            sql_query += " and"
        sql_query += " wojewodztwo='" + voivodeship + "'"
    if keyword:
        if city or parish or county:
            sql_query += " and"
        sql_query += " ( nazwa like '%" + keyword + "%'" + " or funkcja like '%" + keyword + "%'"
        sql_query += " or wojewodztwo like '%" + keyword + "%'" + " or chronologia like '%" + keyword + "%' )"
    sql_query += " order by powiat, gmina, miejscowosc, ulica"
    return sql_query


def _get_query_params(r):
    city = r.args.get("miasto", "").replace("'", "")
    parish = r.args.get("gmina", "").replace("'", "")
    county = r.args.get("powiat", "").replace("'", "")
    voivodeship = r.args.get("wojewodztwo", "").replace("'", "")
    keyword = request.args.get("dowolneslowo", "").replace("'", "")
    return city, parish, county, keyword, voivodeship


def _generate_trip(monuments=None):
    pass


def _generate_pdf_report(monuments=None):
    pass


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/wyszukaj/')
def wyszukaj():
    city, parish, county, keyword, voivodeship = _get_query_params(request)
    if city or parish or county or keyword:
        try:
            db = get_db()
            sql_query = _create_sql_query(city=city, parish=parish, county=county, keyword=keyword)
            output = db.execute(sql_query).fetchall()
        except sqlite3.Error:
            abort(500)
        items = [tuple([id_temp+1]) + tuple(item) for id_temp, item in enumerate(output)]
        return render_template("search.html", city=city, items=items, quantity=len(items))
    else:
        return render_template('search_main.html')


@bp.route('/wygeneruj/')
def wygeneruj():
    city, parish, county, keyword, voivodeship = _get_query_params(request)
    if city or parish or county or voivodeship:
        params = [":".join(x) for x in
                  [["miasto", city], ["gmina", parish], ["powiat", county], ["wojewodztwo", voivodeship]] if x[1]]
        try:
            db = get_db()
            sql_query = _create_sql_query(city=city, parish=parish, county=county, voivodeship=voivodeship)
            output = db.execute(sql_query).fetchall()
            items = [tuple(item) for item in output]
            quantity = len(items)
            trip_msg = " !!! Wycieczka nie może być wygenerowana (funcjonalność nie jest zaimplementowana jeszcze)."
            return render_template("generate.html", params=params, trip=trip_msg)
        except sqlite3.Error:
            abort(500)

    return render_template('generate_main.html')
