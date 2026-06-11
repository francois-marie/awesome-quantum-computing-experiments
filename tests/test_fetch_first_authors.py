"""Tests for first-author resolution helpers and parsers."""

import pytest

from scripts.fetch_first_authors import (
    extract_arxiv_id,
    extract_doi,
    fetch_arxiv_author,
    fetch_crossref_author,
    last_name,
    parse_arxiv_author_from_xml,
    parse_crossref_author_from_json,
    resolve_first_author,
)

ARXIV_FIXTURE = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <author><name>John Q. Public</name></author>
  </entry>
</feed>
"""

CROSSREF_FIXTURE = """{
  "message": {
    "author": [
      {"given": "Jane", "family": "Doe"},
      {"given": "Bob", "family": "Smith"}
    ]
  }
}
"""


@pytest.mark.parametrize(
    ("link", "expected"),
    [
        ("https://arxiv.org/abs/1108.4842", "1108.4842"),
        ("https://arxiv.org/abs/quant-ph/9802018", "quant-ph/9802018"),
        ("https://doi.org/10.48550/arXiv.2411.11708", "2411.11708"),
        ("http://arxiv.org/abs/cond-mat/0306492/", "cond-mat/0306492"),
        ("https://www.nature.com/articles/s41586-019-1666-5", None),
        ("", None),
    ],
)
def test_extract_arxiv_id(link: str, expected: str | None) -> None:
    assert extract_arxiv_id(link) == expected


@pytest.mark.parametrize(
    ("link", "expected"),
    [
        ("https://doi.org/10.1038/nature03074", "10.1038/nature03074"),
        ("https://doi.org/10.1103/PhysRevX.11.041058", "10.1103/PhysRevX.11.041058"),
        ("https://www.nature.com/articles/35005011", "10.1038/35005011"),
        ("https://www.nature.com/articles/ncomms7979", "10.1038/ncomms7979"),
        (
            "https://www.science.org/doi/10.1126/science.1130886",
            "10.1126/science.1130886",
        ),
        (
            "https://journals.aps.org/pra/abstract/10.1103/PhysRevA.92.022336",
            "10.1103/PhysRevA.92.022336",
        ),
        ("https://arxiv.org/abs/1711.11092", None),
        ("", None),
    ],
)
def test_extract_doi(link: str, expected: str | None) -> None:
    assert extract_doi(link) == expected


def test_last_name_returns_surname() -> None:
    assert last_name("John Q. Public") == "Public"
    assert last_name("Marie Curie") == "Curie"


def test_last_name_rejects_empty() -> None:
    with pytest.raises(ValueError):
        last_name("   ")


def test_parse_arxiv_author_from_xml() -> None:
    assert parse_arxiv_author_from_xml(ARXIV_FIXTURE) == "Public"


def test_parse_crossref_author_from_json() -> None:
    assert parse_crossref_author_from_json(CROSSREF_FIXTURE) == "Doe"


def test_fetch_arxiv_author_uses_http(mocker) -> None:
    mocker.patch(
        "scripts.fetch_first_authors._http_get",
        return_value=ARXIV_FIXTURE,
    )
    assert fetch_arxiv_author("1108.4842") == "Public"


def test_fetch_crossref_author_uses_http(mocker) -> None:
    mocker.patch(
        "scripts.fetch_first_authors._http_get",
        return_value=CROSSREF_FIXTURE,
    )
    assert fetch_crossref_author("10.1038/nature03074") == "Doe"


def test_resolve_first_author_prefers_arxiv(mocker) -> None:
    mocker.patch(
        "scripts.fetch_first_authors.fetch_arxiv_author",
        return_value="Knill",
    )
    crossref = mocker.patch("scripts.fetch_first_authors.fetch_crossref_author")
    author = resolve_first_author(
        "https://arxiv.org/abs/quant-ph/9802018",
        {},
        {},
    )
    assert author == "Knill"
    crossref.assert_not_called()


def test_resolve_first_author_falls_back_to_crossref(mocker) -> None:
    mocker.patch(
        "scripts.fetch_first_authors.fetch_crossref_author",
        return_value="Monroe",
    )
    author = resolve_first_author(
        "https://doi.org/10.1038/nature05146",
        {},
        {},
    )
    assert author == "Monroe"
