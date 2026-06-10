#!/usr/bin/env python3
"""Build sticky PR comment body for highlight plot previews."""

import json
import sys
from pathlib import Path


def build_comment(
    diff_json_path: str,
    output_path: str,
    repo: str,
    pr_number: str,
    head_sha: str,
    highlights_dir: str,
) -> None:
    with open(diff_json_path, encoding="utf-8") as handle:
        diff = json.load(handle)

    cdn_base = (
        f"https://cdn.jsdelivr.net/gh/{repo}@gh-pages-assets/previews/pr-{pr_number}"
    )
    highlight_path = Path(highlights_dir)
    png_files = sorted(highlight_path.glob("*.png")) if highlight_path.exists() else []

    lines = [
        "## Highlight plots for new papers in this PR",
        "",
        "Red-star overlays mark rows added vs the base branch. "
        f"Append `?v={head_sha}` if jsDelivr serves a stale cached image.",
        "",
    ]

    if png_files:
        lines.append("### Plot images")
        lines.append("")
        for png in png_files:
            url = f"{cdn_base}/{png.name}?v={head_sha}"
            lines.append(f"- **{png.stem}**: [PNG]({url})")
            lines.append(f"  ![{png.stem}]({url})")
        lines.append("")

    lines.append("### Tweet draft")
    lines.append("")
    for rows in diff.values():
        for row in rows:
            title = row.get("Article Title", "Unknown")
            year = row.get("Year", "")
            platform = row.get("Platform", "")
            link = row.get("Link", "")
            lines.append(f"- **{title}** ({year}, {platform}) - {link}")
    lines.append("")
    lines.append(
        "> Copy an image URL above into your tweet to showcase "
        "where the new paper lands on the timeline."
    )

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 7:
        raise SystemExit(
            "Usage: build_pr_highlight_comment.py "
            "<diff.json> <output.md> <repo> <pr_number> <head_sha> <highlights_dir>"
        )
    build_comment(
        diff_json_path=sys.argv[1],
        output_path=sys.argv[2],
        repo=sys.argv[3],
        pr_number=sys.argv[4],
        head_sha=sys.argv[5],
        highlights_dir=sys.argv[6],
    )


if __name__ == "__main__":
    main()
