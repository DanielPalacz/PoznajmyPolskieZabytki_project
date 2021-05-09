import pytest
from bs4 import BeautifulSoup

from poznajmy_polskie_zabytki.db import get_db


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
    assert '<a href="/wygenerujesz">Wygeneruj wycieczkę</a>' in links
