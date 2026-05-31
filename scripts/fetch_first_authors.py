#!/usr/bin/env python3
"""Populate the First Author column in experiment CSVs via arXiv and Crossref."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FIRST_AUTHOR_COLUMN = "First Author"
ARTICLE_TITLE_COLUMN = "Article Title"
LINK_COLUMN = "Link"
USER_AGENT = (
    "awesome-quantum-computing-experiments/1.0 "
    "(mailto:fm.le.regent@gmail.com)"
)
DEFAULT_CSV_PATHS = (
    "data/qubit_count.csv",
    "data/physical_qubits.csv",
    "data/qec_exp.csv",
    "data/msd_exp.csv",
    "data/entangled_state_error_exp.csv",
)

_ARXIV_ABS_RE = re.compile(
    r"arxiv\.org/abs/([^?#\s]+)",
    re.IGNORECASE,
)
_ARXIV_DOI_RE = re.compile(
    r"10\.48550/arXiv\.([^/?#\s]+)",
    re.IGNORECASE,
)
_DOI_LINK_RE = re.compile(
    r"doi\.org/([^?#\s]+)",
    re.IGNORECASE,
)
_NATURE_ARTICLE_RE = re.compile(
    r"nature\.com/articles/([^?#/]+)",
    re.IGNORECASE,
)
_SCIENCE_DOI_RE = re.compile(
    r"science\.org/doi/([^?#\s]+)",
    re.IGNORECASE,
)
_APS_DOI_RE = re.compile(
    r"10\.1103/[^?#\s]+",
    re.IGNORECASE,
)
_ARXIV_REQUEST_DELAY_S = 3.0
_HTTP_MAX_ATTEMPTS = 5
_ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def extract_arxiv_id(link: str) -> str | None:
    """Return an arXiv identifier from an abs URL or 10.48550/arXiv.* DOI link."""
    if not link:
        return None
    match = _ARXIV_ABS_RE.search(link)
    if match:
        return match.group(1).rstrip("/")
    match = _ARXIV_DOI_RE.search(link)
    if match:
        return match.group(1).rstrip("/")
    return None


def extract_doi(link: str) -> str | None:
    """Return a DOI from a doi.org link or a derivable nature.com/articles URL."""
    if not link:
        return None
    match = _DOI_LINK_RE.search(link)
    if match:
        return match.group(1).rstrip("/")
    match = _NATURE_ARTICLE_RE.search(link)
    if match:
        return f"10.1038/{match.group(1).rstrip('/')}"
    match = _SCIENCE_DOI_RE.search(link)
    if match:
        return match.group(1).rstrip("/")
    match = _APS_DOI_RE.search(link)
    if match:
        return match.group(0).rstrip("/")
    return None


def last_name(full_name: str) -> str:
    """Return the surname (last whitespace-delimited token)."""
    stripped = full_name.strip()
    if not stripped:
        raise ValueError("full_name must not be empty")
    parts = stripped.split()
    return parts[-1]


def parse_arxiv_author_from_xml(xml_text: str) -> str:
    """Parse the first author last name from arXiv Atom API XML."""
    root = ET.fromstring(xml_text)
    entry = root.find("atom:entry", _ATOM_NS)
    if entry is None:
        raise ValueError("no arXiv entry in response")
    author = entry.find("atom:author", _ATOM_NS)
    if author is None:
        raise ValueError("no author in arXiv entry")
    name_el = author.find("atom:name", _ATOM_NS)
    if name_el is None or not (name_el.text or "").strip():
        raise ValueError("empty author name in arXiv entry")
    return last_name(name_el.text)


def parse_crossref_author_from_json(json_text: str) -> str:
    """Parse the first author family name from a Crossref works JSON response."""
    payload = json.loads(json_text)
    message = payload.get("message")
    if not isinstance(message, dict):
        raise ValueError("missing message in Crossref response")
    authors = message.get("author")
    if not authors or not isinstance(authors, list):
        raise ValueError("no authors in Crossref response")
    first = authors[0]
    if not isinstance(first, dict):
        raise ValueError("invalid first author in Crossref response")
    family = first.get("family")
    if not family or not str(family).strip():
        raise ValueError("empty family name in Crossref response")
    return str(family).strip()


def _http_get(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT},
    )
    last_error: urllib.error.HTTPError | None = None
    for attempt in range(_HTTP_MAX_ATTEMPTS):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset)
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code == 429 and attempt < _HTTP_MAX_ATTEMPTS - 1:
                time.sleep(_ARXIV_REQUEST_DELAY_S * (attempt + 1))
                continue
            raise
    if last_error is not None:
        raise last_error
    raise RuntimeError("_http_get failed without an HTTP error")


def fetch_arxiv_author(arxiv_id: str) -> str:
    """Fetch the first author's last name for an arXiv id via the export API."""
    time.sleep(_ARXIV_REQUEST_DELAY_S)
    encoded_id = urllib.request.quote(arxiv_id, safe="/")
    url = f"https://export.arxiv.org/api/query?id_list={encoded_id}"
    xml_text = _http_get(url)
    return parse_arxiv_author_from_xml(xml_text)


def fetch_crossref_author(doi: str) -> str:
    """Fetch the first author's family name for a DOI via Crossref."""
    encoded_doi = urllib.request.quote(doi, safe="")
    url = f"https://api.crossref.org/works/{encoded_doi}"
    json_text = _http_get(url)
    return parse_crossref_author_from_json(json_text)


def resolve_first_author(
    link: str,
    arxiv_cache: dict[str, str],
    crossref_cache: dict[str, str],
) -> str | None:
    """Resolve first author last name from link; use caches to avoid duplicate API calls."""
    arxiv_id = extract_arxiv_id(link)
    if arxiv_id is not None:
        if arxiv_id in arxiv_cache:
            return arxiv_cache[arxiv_id]
        author = fetch_arxiv_author(arxiv_id)
        arxiv_cache[arxiv_id] = author
        return author

    doi = extract_doi(link)
    if doi is not None:
        if doi in crossref_cache:
            return crossref_cache[doi]
        author = fetch_crossref_author(doi)
        crossref_cache[doi] = author
        return author

    return None


def _insert_first_author_column(fieldnames: list[str]) -> list[str]:
    if FIRST_AUTHOR_COLUMN in fieldnames:
        return fieldnames
    if ARTICLE_TITLE_COLUMN not in fieldnames:
        raise ValueError(
            f"CSV must contain '{ARTICLE_TITLE_COLUMN}' to insert '{FIRST_AUTHOR_COLUMN}'"
        )
    out: list[str] = []
    for name in fieldnames:
        out.append(name)
        if name == ARTICLE_TITLE_COLUMN:
            out.append(FIRST_AUTHOR_COLUMN)
    return out


def _process_csv(
    csv_path: Path,
    arxiv_cache: dict[str, str],
    crossref_cache: dict[str, str],
) -> tuple[int, int, list[str]]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"no header row in {csv_path}")
        fieldnames = _insert_first_author_column(list(reader.fieldnames))
        rows = list(reader)

    resolved = 0
    unresolved = 0
    unresolved_lines: list[str] = []

    for index, row in enumerate(rows, start=2):
        existing = (row.get(FIRST_AUTHOR_COLUMN) or "").strip()
        if existing:
            continue
        link = (row.get(LINK_COLUMN) or "").strip()
        title = (row.get(ARTICLE_TITLE_COLUMN) or "").strip()
        if not link:
            unresolved += 1
            unresolved_lines.append(
                f"{csv_path}:{index}: missing link | {title!r}"
            )
            row[FIRST_AUTHOR_COLUMN] = ""
            continue
        try:
            author = resolve_first_author(link, arxiv_cache, crossref_cache)
        except (urllib.error.URLError, ValueError, ET.ParseError) as exc:
            unresolved += 1
            unresolved_lines.append(
                f"{csv_path}:{index}: {link} | {title!r} | {exc}"
            )
            row[FIRST_AUTHOR_COLUMN] = ""
            continue
        if author is None:
            unresolved += 1
            unresolved_lines.append(
                f"{csv_path}:{index}: unclassified link | {link} | {title!r}"
            )
            row[FIRST_AUTHOR_COLUMN] = ""
            continue
        row[FIRST_AUTHOR_COLUMN] = author
        resolved += 1

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_ALL,
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})

    return resolved, unresolved, unresolved_lines


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Populate First Author (last name) in experiment CSVs.",
    )
    parser.add_argument(
        "csv_paths",
        nargs="*",
        default=list(DEFAULT_CSV_PATHS),
        help="CSV files to update (default: all five data/*.csv files)",
    )
    args = parser.parse_args(argv)

    arxiv_cache: dict[str, str] = {}
    crossref_cache: dict[str, str] = {}
    total_resolved = 0
    total_unresolved = 0
    all_unresolved: list[str] = []

    for path_str in args.csv_paths:
        csv_path = Path(path_str)
        if not csv_path.is_file():
            print(f"skip missing file: {csv_path}", file=sys.stderr)
            continue
        resolved, unresolved, lines = _process_csv(
            csv_path,
            arxiv_cache,
            crossref_cache,
        )
        total_resolved += resolved
        total_unresolved += unresolved
        all_unresolved.extend(lines)
        print(
            f"{csv_path}: resolved {resolved}, still blank {unresolved}",
            file=sys.stderr,
        )

    print(
        f"total: resolved {total_resolved}, still blank {total_unresolved}",
        file=sys.stderr,
    )
    if all_unresolved:
        print("\nUnresolved rows (fill First Author manually):", file=sys.stderr)
        for line in all_unresolved:
            print(line, file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
