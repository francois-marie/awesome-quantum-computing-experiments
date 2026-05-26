"""Generate PNG highlight plots for rows added in a PR."""

import importlib
import json
import logging
import sys
from pathlib import Path

import pandas as pd

from src.plotting.plot_mapping import HIGHLIGHT_PLOT_SPECS

HIGHLIGHT_OUTPUT_DIR = "out/png/highlights"
logger = logging.getLogger(__name__)


def _row_keys(identifiers: list[dict]) -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for ident in identifiers:
        title = str(ident.get("Article Title", "")).strip()
        year = str(ident.get("Year", "")).strip()
        if title:
            keys.add((title, year))
    return keys


def _match_processed_rows(
    plot_data: pd.DataFrame,
    identifiers: list[dict],
    module_name: str,
) -> pd.DataFrame:
    """Match highlight identifiers against a plot's processed dataframe."""
    keys = _row_keys(identifiers)
    if not keys or plot_data is None or plot_data.empty:
        return pd.DataFrame()

    if "Article Title" not in plot_data.columns:
        logger.warning(
            "Plot module %s has no Article Title column; cannot match highlight rows",
            module_name,
        )
        return pd.DataFrame()

    def is_match(row: pd.Series) -> bool:
        title = str(row.get("Article Title", "")).strip()
        year = str(row.get("Year", "")).strip()
        return (title, year) in keys

    return plot_data[plot_data.apply(is_match, axis=1)]


def _instantiate_plot(
    module_name: str,
    class_name: str,
    highlight_rows: pd.DataFrame | None,
    skip_export: bool,
):
    module = importlib.import_module(f"src.plotting.{module_name}")
    plot_class = getattr(module, class_name)
    return plot_class(highlight_rows=highlight_rows, skip_export=skip_export)


def _resolve_highlight_rows(
    match_strategy: str,
    raw_highlight: pd.DataFrame,
    matched: pd.DataFrame,
) -> pd.DataFrame | None:
    if match_strategy == "raw":
        return raw_highlight if not raw_highlight.empty else None
    if match_strategy == "processed_match":
        return matched if not matched.empty else None
    raise ValueError(f"Unknown highlight match_strategy: {match_strategy}")


def generate_highlights(diff_json_path: str) -> list[tuple[str, str]]:
    """
    Generate highlight PNGs from a diff JSON file.

    Returns:
        List of (export_name, output_path) tuples for generated PNGs.
    """
    with open(diff_json_path, encoding="utf-8") as handle:
        diff_data: dict[str, list[dict]] = json.load(handle)

    if not diff_data:
        return []

    Path(HIGHLIGHT_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    generated: list[tuple[str, str]] = []

    for csv_path, row_identifiers in diff_data.items():
        specs = HIGHLIGHT_PLOT_SPECS.get(csv_path, [])
        raw_highlight = pd.DataFrame(row_identifiers)

        for module_name, class_name, export_name, match_strategy in specs:
            probe = _instantiate_plot(
                module_name,
                class_name,
                highlight_rows=None,
                skip_export=False,
            )
            matched = _match_processed_rows(probe.data, row_identifiers, module_name)
            highlight_rows = _resolve_highlight_rows(
                match_strategy,
                raw_highlight,
                matched,
            )

            if highlight_rows is None or highlight_rows.empty:
                continue

            plot = _instantiate_plot(
                module_name,
                class_name,
                highlight_rows=highlight_rows,
                skip_export=True,
            )
            plot.create_plot()

            if plot.fig is None:
                continue

            output_path = plot.export_to_png(
                plot.fig,
                export_name,
                output_dir=HIGHLIGHT_OUTPUT_DIR,
            )
            if output_path:
                generated.append((export_name, str(output_path)))

    return generated


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python -m src.plotting.highlight_runner <diff.json>"
        )

    diff_json_path = sys.argv[1]
    generated = generate_highlights(diff_json_path)
    for export_name, path in generated:
        print(f"Generated highlight: {export_name} -> {path}")


if __name__ == "__main__":
    main()
