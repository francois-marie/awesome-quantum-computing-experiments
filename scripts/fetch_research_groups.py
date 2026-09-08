#!/usr/bin/env python3
"""Resolve every paper in ``data/*.csv`` to a research group via OpenAlex.

Writes ``data/research_groups.csv`` with one row per unique paper link:

    Link, Research Group, Institutions, Org Type, Country, Source

* ``Research Group``: first-author institution (short name), or the manual
  value from the ``Research Group`` column of ``qec_exp.csv`` when present.
* ``Institutions``: all distinct author institutions, ``; `` separated.
* ``Org Type``: ``industry`` when the first author is at a company,
  ``academic`` when no company appears, ``mixed`` otherwise.
* ``Source``: ``manual``, ``openalex``, ``openalex-noaff`` (the work exists
  but carries no author affiliations) or ``unresolved`` (no matching work).

The script is idempotent: existing rows whose ``Source`` is ``manual`` are
kept verbatim, and resolved rows are only refetched with ``--refresh``.
OpenAlex needs no API key; a contact e-mail is passed for the polite pool.

Usage:
    python scripts/fetch_research_groups.py [--refresh] [--limit N]
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

import yaml

OUT = Path("data/research_groups.csv")
FIELDS = ["Link", "Research Group", "Institutions", "Org Type", "Country", "Source"]
MAILTO = "fm.le.regent@gmail.com"
API = "https://api.openalex.org"
RATE_STATE: dict[str, bool] = {}

COMPANY_HINTS = re.compile(
    r"\b(google|ibm|microsoft|amazon|aws|quantinuum|honeywell|ionq|quera|atom computing|pasqal|rigetti|"
    r"alice\s*&\s*bob|psiquantum|xanadu|intel|nvidia|iqm|oxford ionics|infleqtion|coldquanta|"
    r"planqc|alpine quantum|aqt|q-ctrl|quantware|nord quantique|photonic inc|diraq|silicon quantum computing)\b",
    re.I,
)

SHORT_NAMES = {
    "Google (United States)": "Google Quantum AI",
    "IBM (United States)": "IBM Research",
    "Microsoft (United States)": "Microsoft",
    "Amazon (United States)": "Amazon (AWS)",
    "Harvard University": "Harvard",
    "Massachusetts Institute of Technology": "MIT",
    "California Institute of Technology": "Caltech",
    "ETH Zurich": "ETH Zurich",
    "Delft University of Technology": "Delft",
    "University of Innsbruck": "Innsbruck",
    "University of Maryland, College Park": "Maryland",
    "University of California, Santa Barbara": "UCSB",
    "University of Science and Technology of China": "USTC",
    "University of Waterloo": "Waterloo",
    "Yale University": "Yale",
    "National Institute of Standards and Technology": "NIST",
}


ACADEMIC_HINTS = re.compile(
    r"\b(universit|institute|institut|college|school|eth|cnrs|cea|nist|jila|mit|caltech|ucsb|usTC|qutech|delft|harvard|yale|"
    r"innsbruck|maryland|waterloo|iqc|southampton|bristol|durham|sheffield|los alamos|academy|laborator|max planck|riken|nrc)\b",
    re.I,
)


def infer_org_type(group: str, institutions: str) -> str:
    """Fallback classification from names when OpenAlex has no affiliations."""
    text = f"{group} {institutions}"
    company = bool(COMPANY_HINTS.search(text))
    academic = bool(ACADEMIC_HINTS.search(text))
    if company and academic:
        return "mixed"
    if company:
        return "industry"
    if academic:
        return "academic"
    return ""


def load_yaml(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def paper_links(config: dict) -> tuple[list[str], dict[str, str]]:
    """Unique links across all CSVs plus manual group names from qec_exp.csv."""
    links: list[str] = []
    manual: dict[str, str] = {}
    for key, path in config["paths"]["data"].items():
        if key == "research_groups":
            continue
        with open(path, newline="") as f:
            for row in csv.DictReader(f):
                link = (row.get("Link") or "").strip()
                if not link:
                    continue
                if link not in links:
                    links.append(link)
                group = (row.get("Research Group") or "").strip()
                if group and group.lower() not in {"unknown", "research group"}:
                    manual.setdefault(link, group)
    return links, manual


def doi_from_link(link: str) -> str | None:
    m = re.search(r"doi\.org/(10\.\S+)", link)
    if m:
        return m.group(1).rstrip("/")
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([\w.\-]+?)(?:v\d+)?(?:\.pdf)?$", link)
    if m:
        return f"10.48550/arXiv.{m.group(1)}"
    m = re.search(r"nature\.com/articles/([\w\-]+)", link)
    if m:
        return f"10.1038/{m.group(1)}"
    m = re.search(r"science\.org/doi/(10\.\S+)", link)
    if m:
        return m.group(1)
    m = re.search(r"journals\.aps\.org/\w+/abstract/(10\.\S+)", link)
    if m:
        return m.group(1)
    return None


def get(url: str) -> dict | None:
    sep = "&" if "?" in url else "?"
    req = urllib.request.Request(f"{url}{sep}mailto={MAILTO}", headers={"User-Agent": f"aqce/1.0 ({MAILTO})"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:  # type: ignore[attr-defined]
            if e.code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            return None
        except Exception:
            time.sleep(2)
    # Three 429s or errors in a row: treat as rate limited and stop querying.
    RATE_STATE["rate limited"] = True
    return None


def has_institutions(work: dict | None) -> bool:
    return bool(work) and any(a.get("institutions") for a in work.get("authorships") or [])


def find_work(link: str, title: str | None) -> dict | None:
    """Resolve by DOI first; if that version carries no affiliations (typical
    for arXiv-only records) look for another version of the same title."""
    doi = doi_from_link(link)
    work = None
    if doi:
        work = get(f"{API}/works/https://doi.org/{urllib.parse.quote(doi, safe='')}?select=id,title,authorships,publication_year")
        if has_institutions(work):
            return work
    if title:
        query = re.sub(r"[^\w\s-]", " ", title)[:200]
        res = get(f"{API}/works?search={urllib.parse.quote(query)}&per-page=5&select=id,title,authorships,publication_year")
        norm = lambda s: re.sub(r"\W+", " ", (s or "").lower()).strip()
        b = norm(title)
        for cand in (res or {}).get("results", []):
            a = norm(cand.get("title"))
            if a and (a == b or a in b or b in a) and has_institutions(cand):
                return cand
    return work


def summarise(work: dict) -> dict[str, str]:
    authorships = work.get("authorships") or []
    institutions: list[tuple[str, str, str]] = []  # (name, type, country)
    for a in authorships:
        for inst in a.get("institutions") or []:
            institutions.append((inst.get("display_name") or "", inst.get("type") or "", inst.get("country_code") or ""))
    first = [i for i in (authorships[0].get("institutions") if authorships else []) or []]
    first_names = [i.get("display_name") or "" for i in first]
    first_types = [i.get("type") or "" for i in first]

    def is_company(name: str, typ: str) -> bool:
        return typ == "company" or bool(COMPANY_HINTS.search(name))

    any_company = any(is_company(n, t) for n, t, _ in institutions)
    first_company = any(is_company(n, t) for n, t in zip(first_names, first_types))
    if not institutions:
        org_type = ""
    elif first_company and all(is_company(n, t) for n, t, _ in institutions):
        org_type = "industry"
    elif first_company:
        org_type = "industry"
    elif any_company:
        org_type = "mixed"
    else:
        org_type = "academic"

    counts = Counter(n for n, _, _ in institutions if n)
    group = first_names[0] if first_names else (counts.most_common(1)[0][0] if counts else "")
    group = SHORT_NAMES.get(group, group)
    country = Counter(c for _, _, c in institutions if c).most_common(1)
    return {
        "Research Group": group,
        "Institutions": "; ".join(dict.fromkeys(n for n, _, _ in institutions if n)),
        "Org Type": org_type,
        "Country": country[0][0] if country else "",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", action="store_true", help="re-query OpenAlex for already resolved rows")
    ap.add_argument("--limit", type=int, default=0, help="stop after N lookups (for testing)")
    ap.add_argument("--offline", action="store_true", help="no network: rewrite the CSV, filling Org Type from names")
    args = ap.parse_args()

    config = load_yaml("config.yaml")
    links, manual = paper_links(config)
    titles: dict[str, str] = {}
    for key, path in config["paths"]["data"].items():
        if key == "research_groups":
            continue
        with open(path, newline="") as f:
            for row in csv.DictReader(f):
                if row.get("Link"):
                    titles.setdefault(row["Link"].strip(), row.get("Article Title", ""))

    existing: dict[str, dict[str, str]] = {}
    if OUT.exists():
        with open(OUT, newline="") as f:
            existing = {r["Link"]: r for r in csv.DictReader(f)}

    rows: list[dict[str, str]] = []
    lookups = 0
    unresolved = 0
    for link in links:
        prev = existing.get(link)
        if prev and prev.get("Source") == "manual":
            rows.append(prev)
            continue
        if prev and prev.get("Source") == "openalex-noaff" and not args.refresh:
            rows.append(prev)
            continue
        if prev and prev.get("Source") == "openalex" and prev.get("Institutions") and not args.refresh:
            rows.append(prev)
            continue
        if args.offline or RATE_STATE.get("rate limited") or (args.limit and lookups >= args.limit):
            rows.append(prev or {"Link": link, "Research Group": manual.get(link, ""), "Institutions": "", "Org Type": "", "Country": "", "Source": "unresolved"})
            continue
        lookups += 1
        work = find_work(link, titles.get(link))
        time.sleep(0.15)
        if work:
            info = summarise(work)
            if manual.get(link):
                info["Research Group"] = manual[link]
            source = "openalex" if info["Institutions"] else "openalex-noaff"
            rows.append({"Link": link, **info, "Source": source})
            tag = "ok" if source == "openalex" else "noaff"
            print(f"{tag:6}{info['Research Group'] or '?':30.30} {info['Org Type']:8} {link}")
        else:
            unresolved += 1
            rows.append({"Link": link, "Research Group": manual.get(link, ""), "Institutions": "", "Org Type": "", "Country": "", "Source": "unresolved"})
            print(f"MISS {link}", file=sys.stderr)

    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for r in rows:
            if not r.get("Org Type"):
                r["Org Type"] = infer_org_type(r.get("Research Group", ""), r.get("Institutions", ""))
            w.writerow({k: r.get(k, "") for k in FIELDS})
    tally = Counter(r.get("Source", "") for r in rows)
    pending = sum(
        1
        for r in rows
        if r.get("Source") == "unresolved"
        or (r.get("Source") == "openalex" and not r.get("Institutions"))
    )
    print(f"\n{len(rows)} papers, {lookups} lookups this run -> {OUT}")
    for key in ("manual", "openalex", "openalex-noaff", "unresolved"):
        if tally.get(key):
            print(f"  {key:15} {tally[key]}")
    if RATE_STATE.get("rate limited"):
        print("OpenAlex rate limit hit (HTTP 429): remaining papers left untouched, rerun later.", file=sys.stderr)
    elif pending:
        print(f"{pending} paper(s) still to query: rerun `make groups`.")
    else:
        print("Nothing left to query: every paper is resolved or a known dead end.")
        print("Use --refresh to re-query everything, and fill dead ends by hand in the CSV.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
