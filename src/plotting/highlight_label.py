"""Labels for highlight star traces and on-plot annotations."""

from __future__ import annotations

import re

import pandas as pd

FIRST_AUTHOR_COLUMN = "First Author"

_RESEARCH_GROUP_AUTHOR = re.compile(r"\(([^)]+)\)")

_TITLE_PREFIX_SKIP = frozenset({
    "a",
    "an",
    "the",
    "experimental",
    "demonstration",
    "observation",
    "realization",
    "implementation",
    "evidence",
    "towards",
    "toward",
    "high",
    "fast",
    "robust",
    "deterministic",
})


def research_group_author_et_al(row: pd.Series) -> str | None:
    """Build 'Name et al.' from Research Group when parenthetical name exists."""
    group = row.get("Research Group")
    if group is None or (isinstance(group, float) and pd.isna(group)):
        return None
    text = str(group).strip()
    if not text:
        return None
    match = _RESEARCH_GROUP_AUTHOR.search(text)
    if match:
        name = match.group(1).strip()
        if name:
            return f"{name} et al."
    lead = text.split("/")[0].split(",")[0].strip()
    if lead:
        return f"{lead} et al."
    return None


def title_author_et_al(row: pd.Series) -> str:
    """First meaningful title word plus 'et al.' when no research group is available."""
    title = str(row.get("Article Title", "")).strip()
    if not title:
        return "Highlighted paper"
    for word in title.split():
        token = word.strip(".,;:\"'()[]")
        if len(token) > 2 and token.lower() not in _TITLE_PREFIX_SKIP:
            return f"{token} et al."
    first = title.split()[0].strip(".,;:\"'()[]")
    return f"{first} et al." if first else "Highlighted paper"


def first_author_et_al(row: pd.Series) -> str | None:
    """Build 'LastName et al.' from the First Author column when present."""
    author = row.get(FIRST_AUTHOR_COLUMN)
    if author is None or (isinstance(author, float) and pd.isna(author)):
        return None
    text = str(author).strip()
    if not text:
        return None
    return f"{text} et al."


def highlight_legend_label(row: pd.Series) -> str:
    """
    Label for a highlight: First Author et al., research group, or title fallback.

    arXiv and DOI are intentionally omitted for social PNG exports.
    """
    author_label = first_author_et_al(row)
    if author_label:
        return author_label
    group_label = research_group_author_et_al(row)
    if group_label:
        return group_label
    return title_author_et_al(row)
