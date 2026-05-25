#!/usr/bin/env python3
"""Emit JSON of CSV rows present in head but not in base (for PR highlight workflow)."""

import argparse
import csv
import io
import json
import subprocess
import sys
from pathlib import Path


def _is_missing_path_at_ref(stderr: str, csv_path: str) -> bool:
    """True when git show failed because the path is absent at that ref."""
    return (
        f"path '{csv_path}' does not exist in" in stderr
        or f"path '{csv_path}' exists on disk, but not in" in stderr
    )


def _run_git_show(ref: str, csv_path: str, repo_root: str | None) -> str | None:
    """
    Return file contents at ref, or None if the path did not exist at that ref.

    Raises:
        subprocess.CalledProcessError: For invalid refs or other git failures.
    """
    cmd = ["git"]
    if repo_root is not None:
        cmd.extend(["-C", repo_root])
    cmd.extend(["show", f"{ref}:{csv_path}"])
    result = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return result.stdout

    stderr = result.stderr or ""
    if _is_missing_path_at_ref(stderr, csv_path):
        return None

    raise subprocess.CalledProcessError(
        result.returncode,
        cmd,
        output=result.stdout,
        stderr=stderr,
    )


def _read_csv_rows(content: str) -> list[dict[str, str]]:
    reader = csv.DictReader(io.StringIO(content))
    return [dict(row) for row in reader]


def _row_tuple(row: dict[str, str]) -> tuple[tuple[str, str], ...]:
    return tuple(sorted(row.items()))


def _added_rows(base_content: str | None, head_content: str) -> list[dict[str, str]]:
    base_rows = _read_csv_rows(base_content) if base_content else []
    head_rows = _read_csv_rows(head_content)

    base_tuples = {_row_tuple(row) for row in base_rows}
    added: list[dict[str, str]] = []
    seen: set[tuple[tuple[str, str], ...]] = set()

    for row in head_rows:
        row_t = _row_tuple(row)
        if row_t in base_tuples or row_t in seen:
            continue
        if not row.get("Article Title", "").strip():
            continue
        seen.add(row_t)
        added.append(row)

    return added


def diff_csv_rows(
    base_ref: str,
    head_ref: str,
    csv_paths: list[str],
    repo_root: str | None,
) -> dict[str, list[dict[str, str]]]:
    """Return mapping of csv_path -> rows added between base and head."""
    result: dict[str, list[dict[str, str]]] = {}

    for csv_path in csv_paths:
        base_content = _run_git_show(base_ref, csv_path, repo_root)
        head_content = _run_git_show(head_ref, csv_path, repo_root)
        if head_content is None:
            raise FileNotFoundError(f"CSV not found at head ref {head_ref}: {csv_path}")

        added = _added_rows(base_content, head_content)
        if added:
            result[csv_path] = added

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Diff CSV rows added between two git refs."
    )
    parser.add_argument("base_ref", help="Base git ref (e.g. origin/main)")
    parser.add_argument("head_ref", help="Head git ref (e.g. HEAD or commit SHA)")
    parser.add_argument(
        "csv_paths",
        nargs="+",
        help="CSV file paths relative to repo root",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Git repository root (default: current directory)",
    )
    args = parser.parse_args()

    resolved_paths = [str(Path(p)) for p in args.csv_paths]
    diff = diff_csv_rows(
        args.base_ref,
        args.head_ref,
        resolved_paths,
        repo_root=args.repo_root,
    )
    json.dump(diff, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
