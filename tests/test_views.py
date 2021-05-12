import pytest
from bs4 import BeautifulSoup


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("content-type", "") == "text/html; charset=utf-8"


def test_index_links(client):
    response = client.get("/")
    soup = BeautifulSoup(response.get_data(), "html.parser")
    links = [repr(link) for link in soup.find_all("a")]
    assert '<a href="/">Poznajmy polskie zabytki</a>' in links
    assert '<a href="/wyszukaj">Wyszukaj zabytki</a>' in links
    assert '<a href="/wygeneruj">Wygeneruj wycieczkę</a>' in links


def test_wyszukaj_main(client):
    response = client.get("/wyszukaj/")
    soup = BeautifulSoup(response.get_data(), "html.parser")
    input_tags = soup.find_all("input")
    assert len(input_tags) == 5
    for input_tag in input_tags:
        assert input_tag.get("name") in ["miasto", "gmina", "powiat", "dowolneslowo", None]
    for p in soup.find_all("p"):
        assert p.text in ["Super:) Poznajemy razem polskie zabytki.", "Wyszukiwarka zabytków:"]


def test_wyszukaj_main_without_parameters(client):
    response = client.get("/wyszukaj/?miasto=&gmina=&powiat=&dowolneslowo=")
    soup = BeautifulSoup(response.get_data(), "html.parser")
    input_tags = soup.find_all("input")
    assert len(input_tags) == 5
    for input_tag in input_tags:
        assert input_tag.get("name") in ["miasto", "gmina", "powiat", "dowolneslowo", None]
    for p in soup.find_all("p"):
        assert p.text in ["Super:) Poznajemy razem polskie zabytki.", "Wyszukiwarka zabytków:"]


def test_wyszukaj_sql_injection_filtering(client):
    response = client.get("/wyszukaj/?miasto=Koniusza'+or+True+or+miejscowosc%3D'Koniusza&gmina=&powiat=&dowolneslowo=")
    assert response.status_code == 200, "Sql injection filtering not implemented"


@pytest.mark.skip
def test_wyszukaj_with_parameters(client_full_dbload):
    response = client_full_dbload.get("/wyszukaj/?miasto=Koniusza&gmina=&powiat=&dowolneslowo=dzwonnica")
    soup = BeautifulSoup(response.get_data(), "html.parser")
    monuments_text = soup.text
    assert "Zabytki znalezione (2):" in monuments_text
    assert """1\ndzwonnica\nXVIII w.\ndzwonnica\nmałopolskie\nproszowicki\nKoniusza\nKoniusza\n-""" in monuments_text
    assert len(soup.find_all("tr")) == 3


def test_wygeneruj_main(client):
    response = client.get("/wygeneruj/")
    assert response.status_code == 200
    soup = BeautifulSoup(response.get_data(), "html.parser")
    input_tags = soup.find_all("input")
    assert len(input_tags) == 5
    for input_tag in input_tags:
        assert input_tag.get("name") in ["miasto", "gmina", "powiat", "wojewodztwo", None]
        assert input_tag.get("placeholder") in ["..wpisz miejscowość..",
                                                "..wpisz gminę..",
                                                "..wpisz powiat..",
                                                "..wpisz wojewodztwo..", None]
    for p in soup.find_all("p"):
        assert p.text in ["Super:) Wygenerujemy zaraz wycieczkę (i poznamy polskie zabytki).", "Generator wycieczek:"]


def test_wygeneruj_main_without_parameters(client):
    response = client.get("/wygeneruj/?miasto=&gmina=&powiat=&wojewodztwo=")
    assert response.status_code == 200
    soup = BeautifulSoup(response.get_data(), "html.parser")
    input_tags = soup.find_all("input")
    assert len(input_tags) == 5
    for input_tag in input_tags:
        assert input_tag.get("name") in ["miasto", "gmina", "powiat", "wojewodztwo", None]
        assert input_tag.get("placeholder") in ["..wpisz miejscowość..",
                                                "..wpisz gminę..",
                                                "..wpisz powiat..",
                                                "..wpisz wojewodztwo..", None]
    for p in soup.find_all("p"):
        assert p.text in ["Super:) Wygenerujemy zaraz wycieczkę (i poznamy polskie zabytki).", "Generator wycieczek:"]


def test_wygeneruj_sql_injection_filtering(client):
    response = client.get("/wygeneruj/?miasto=Koniusza'+or+True&gmina=&powiat=&wojewodztwo=")
    assert response.status_code == 200, "Sql injection filtering not implemented"
