"""Tests for CSV row diff script used in PR highlight workflow."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.diff_csv_rows import _added_rows, _row_key, diff_csv_rows


def test_row_key_uses_title_and_year():
    row = {"Article Title": "My Paper", "Year": "2024", "Link": "http://x"}
    assert _row_key(row) == ("My Paper", "2024")


def test_added_rows_finds_new_rows():
    base = "Article Title,Year,Link\nOld Paper,2023,http://a\n"
    head = (
        "Article Title,Year,Link\n"
        "Old Paper,2023,http://a\n"
        "New Paper,2024,http://b\n"
    )
    added = _added_rows(base, head)
    assert len(added) == 1
    assert added[0]["Article Title"] == "New Paper"
    assert added[0]["Year"] == "2024"


def test_added_rows_treats_edited_row_as_add():
    base = "Article Title,Year,Link\nSame Title,2024,http://old\n"
    head = "Article Title,Year,Link\nSame Title,2024,http://new\n"
    added = _added_rows(base, head)
    assert len(added) == 1
    assert added[0]["Link"] == "http://new"


def test_diff_csv_rows_in_temp_git_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    data_dir = repo / "data"
    data_dir.mkdir()

    csv_path = data_dir / "sample.csv"
    csv_path.write_text(
        "Article Title,Year,Link\nBase Paper,2023,http://base\n",
        encoding="utf-8",
    )

    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "base"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    base_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    csv_path.write_text(
        "Article Title,Year,Link\n"
        "Base Paper,2023,http://base\n"
        "Added Paper,2024,http://added\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "add row"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    head_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    result = diff_csv_rows(base_sha, head_sha, ["data/sample.csv"], repo_root=str(repo))
    assert "data/sample.csv" in result
    assert len(result["data/sample.csv"]) == 1
    assert result["data/sample.csv"][0]["Article Title"] == "Added Paper"


def test_diff_csv_rows_cli_stdout(tmp_path):
    repo = tmp_path / "repo2"
    repo.mkdir()
    data_dir = repo / "data"
    data_dir.mkdir()
    csv_path = data_dir / "sample.csv"
    csv_path.write_text("Article Title,Year\nFirst,2023\n", encoding="utf-8")

    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "initial"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    base_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    csv_path.write_text(
        "Article Title,Year\nFirst,2023\nSecond,2024\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "add row"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    head_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    script = Path(__file__).resolve().parents[1] / "scripts" / "diff_csv_rows.py"
    proc = subprocess.run(
        [
            sys.executable,
            str(script),
            base_sha,
            head_sha,
            "data/sample.csv",
            "--repo-root",
            str(repo),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    output = json.loads(proc.stdout)
    assert "data/sample.csv" in output
    assert output["data/sample.csv"][0]["Article Title"] == "Second"
