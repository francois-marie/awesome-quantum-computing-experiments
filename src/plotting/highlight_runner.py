"""Generate PNG highlight plots for rows added in a PR."""

import importlib
import json
import sys
from pathlib import Path

import pandas as pd

from src.plotting.plot_mapping import HIGHLIGHT_PLOT_SPECS

HIGHLIGHT_OUTPUT_DIR = "out/png/highlights"


def _row_keys(identifiers: list[dict]) -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for ident in identifiers:
        title = str(ident.get("Article Title", "")).strip()
        year = str(ident.get("Year", "")).strip()
        if title:
            keys.add((title, year))
    return keys


def _match_processed_rows(plot_data: pd.DataFrame, identifiers: list[dict]) -> pd.DataFrame:
    """Match highlight identifiers against a plot's processed dataframe."""
    keys = _row_keys(identifiers)
    if not keys or plot_data is None or plot_data.empty:
        return pd.DataFrame()

    if "Article Title" not in plot_data.columns:
        return pd.DataFrame()

    def is_match(row: pd.Series) -> bool:
        title = str(row.get("Article Title", "")).strip()
        year = str(row.get("Year", "")).strip()
        return (title, year) in keys

    return plot_data[plot_data.apply(is_match, axis=1)]


def _instantiate_plot(module_name: str, class_name: str, highlight_rows: pd.DataFrame | None):
    module = importlib.import_module(f"src.plotting.{module_name}")
    plot_class = getattr(module, class_name)
    return plot_class(highlight_rows=highlight_rows)


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

        for module_name, class_name, export_name in specs:
            probe = _instantiate_plot(module_name, class_name, highlight_rows=None)
            matched = _match_processed_rows(probe.data, row_identifiers)

            if class_name in ("QECTimelineScatterPlot", "NKDPlot", "QECQubitCountPlot"):
                highlight_rows = raw_highlight
            else:
                highlight_rows = matched if not matched.empty else None

            if highlight_rows is None or (
                isinstance(highlight_rows, pd.DataFrame) and highlight_rows.empty
            ):
                continue

            plot = _instantiate_plot(module_name, class_name, highlight_rows=highlight_rows)
            plot._skip_export = True
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
        raise SystemExit(f"Usage: python -m src.plotting.highlight_runner <diff.json>")

    diff_json_path = sys.argv[1]
    generated = generate_highlights(diff_json_path)
    for export_name, path in generated:
        print(f"Generated highlight: {export_name} -> {path}")


if __name__ == "__main__":
    main()
