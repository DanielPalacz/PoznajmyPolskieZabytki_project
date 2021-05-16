from poznajmy_polskie_zabytki.views import _create_sql_query


def test_no_parameters():
    query = _create_sql_query()
    assert query == ""
    def_params = _create_sql_query.__kwdefaults__
    assert [] == [val for val in def_params.values() if val != ""]


def test_only_keyword_parameters():
    try:
        _create_sql_query(1)
    except TypeError:
        pass


def test_only_city():
    query = _create_sql_query(city="Warszawa")
    assert query == "SELECT * from zabytki where miejscowosc='Warszawa' order by powiat, gmina, miejscowosc, ulica"


def test_only_parish():
    query = _create_sql_query(parish="Wolbrom")
    assert query == "SELECT * from zabytki where gmina like '%Wolbrom%' order by powiat, gmina, miejscowosc, ulica"


def test_only_county():
    query = _create_sql_query(county="olkuski")
    assert query == "SELECT * from zabytki where powiat='olkuski' order by powiat, gmina, miejscowosc, ulica"


def test_only_voivodeship():
    query = _create_sql_query(voivodeship="mazowieckie")
    assert query == "SELECT * from zabytki where wojewodztwo='mazowieckie' order by powiat, gmina, miejscowosc, ulica"


def test_only_keyword():
    query = _create_sql_query(keyword="dzwonnica")
    assert query == "SELECT * from zabytki where ( " \
                    "nazwa like '%dzwonnica%' or " \
                    "funkcja like '%dzwonnica%' or " \
                    "wojewodztwo like '%dzwonnica%' or " \
                    "chronologia like '%dzwonnica%' or " \
                    "ulica like '%dzwonnica%' )" \
                    " order by powiat, gmina, miejscowosc, ulica"


def test_city_and_parish():
    query = _create_sql_query(city="Koniusza", parish="Koniusza")
    assert query == "SELECT * from zabytki where miejscowosc='Koniusza' and gmina like '%Koniusza%'" \
                    " order by powiat, gmina, miejscowosc, ulica"


def test_city_and_parish_and_county():
    query = _create_sql_query(city="Koniusza", parish="Koniusza", county="proszowicki")
    assert query == "SELECT * from zabytki where " \
                    "miejscowosc='Koniusza' and " \
                    "gmina like '%Koniusza%' and " \
                    "powiat='proszowicki'" \
                    " order by powiat, gmina, miejscowosc, ulica"


def test_city_and_parish_and_county_and_keyword():
    query = _create_sql_query(city="Koniusza", parish="Koniusza", county="proszowicki", keyword="dzwonnica")
    assert query == "SELECT * from zabytki where " \
                    "miejscowosc='Koniusza' and " \
                    "gmina like '%Koniusza%' and " \
                    "powiat='proszowicki' and " \
                    "( " \
                        "nazwa like '%dzwonnica%' or " \
                        "funkcja like '%dzwonnica%' or " \
                        "wojewodztwo like '%dzwonnica%' or " \
                        "chronologia like '%dzwonnica%' or " \
                        "ulica like '%dzwonnica%' " \
                    ")" \
                    " order by powiat, gmina, miejscowosc, ulica"
