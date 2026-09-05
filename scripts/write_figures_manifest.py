#!/usr/bin/env python3
"""Write ``out/figures/manifest.json``: a hash of every data CSV plus the figure list.

The website is rebuilt from commits that touch ``out/figures``; committing this
manifest guarantees such a commit exists after any data change, even one that
leaves every figure unchanged (e.g. a title typo fix that only affects tables).
"""

import hashlib
import json
from pathlib import Path

import yaml

FIGURES = Path("out/figures")


def main() -> None:
    config = yaml.safe_load(Path("config.yaml").read_text())
    data = {
        key: hashlib.sha256(Path(path).read_bytes()).hexdigest()
        for key, path in sorted(config["paths"]["data"].items())
    }
    figures = sorted(p.stem for p in FIGURES.glob("*.json") if p.name != "manifest.json")
    FIGURES.mkdir(parents=True, exist_ok=True)
    (FIGURES / "manifest.json").write_text(json.dumps({"data": data, "figures": figures}, indent=2) + "\n")


if __name__ == "__main__":
    main()
