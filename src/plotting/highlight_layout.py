"""Portrait layout for highlight PNG exports (e.g. mobile Twitter)."""

from __future__ import annotations

import copy
import re
from typing import Any

import plotly.graph_objects as go
from plotly.subplots import make_subplots

_LEGEND_IDS = ("legend", "legend2", "legend3", "legend4")

_PLATFORM_ABBREVIATIONS = (
    ("Superconducting circuit", "SC circuit"),
    ("Superconducting", "SC"),
    ("Neutral atoms", "Neut. atoms"),
    ("Semiconductor", "Semi."),
    ("Semiconductor spins", "Semi. spins"),
)


def highlight_export_settings(plot_settings: dict[str, Any]) -> dict[str, int | float]:
    """Return width, height, and scale for highlight PNG export."""
    export = plot_settings.get("highlight_export", plot_settings["export"])
    return {
        "width": int(export["width"]),
        "height": int(export["height"]),
        "scale": float(export["scale"]),
    }


def legend_trace_indices(fig: go.Figure) -> list[int]:
    """Indices of traces that appear in the legend."""
    indices: list[int] = []
    for index, trace in enumerate(fig.data):
        if getattr(trace, "showlegend", True) is False:
            continue
        name = getattr(trace, "name", None)
        if name is None or str(name).strip() == "":
            continue
        indices.append(index)
    return indices


def shorten_legend_name(name: str) -> str:
    """Compact legend labels so multi-column layouts do not overlap."""
    text = str(name).strip()
    for long_label, short_label in _PLATFORM_ABBREVIATIONS:
        text = text.replace(long_label, short_label)
    fit_match = re.search(
        r"^(.*?) fit.*?\(.*?every ([\d.]+)y\)",
        text,
    )
    if fit_match:
        return f"{fit_match.group(1)} fit /{fit_match.group(2)}y"
    if len(text) > 28:
        return f"{text[:25]}..."
    return text


def assign_column_legends(fig: go.Figure, columns: int) -> int:
    """
    Distribute legend entries across legend, legend2, (legend3).

    Returns rows per column (column-first fill).
    """
    indices = legend_trace_indices(fig)
    if not indices:
        return 0

    column_count = min(max(columns, 1), len(_LEGEND_IDS))
    rows_per_column = (len(indices) + column_count - 1) // column_count

    for slot, index in enumerate(indices):
        column_index = min(slot // rows_per_column, column_count - 1)
        fig.data[index].legend = _LEGEND_IDS[column_index]
        shortened = shorten_legend_name(str(fig.data[index].name))
        fig.data[index].name = shortened

    return rows_per_column


def column_count_for_traces(trace_count: int, configured_columns: int) -> int:
    """Use at most two widely spaced columns (best supported in PNG export)."""
    if trace_count > 10:
        return min(configured_columns, 2)
    return 1


def legend_band_fraction(
    rows_per_column: int,
    legend_font_size: int,
    figure_height: int,
) -> float:
    """Paper fraction for the bottom subplot row reserved for the legend."""
    if rows_per_column <= 0:
        return 0.18
    row_pixels = int(legend_font_size * 1.55) + 8
    band_pixels = rows_per_column * row_pixels + 32
    fraction = band_pixels / figure_height
    return min(0.42, max(0.2, fraction))


def _axis_title_text(axis_layout: Any) -> str | None:
    if axis_layout is None or axis_layout.title is None:
        return None
    title = axis_layout.title
    if isinstance(title, str):
        return title
    return title.get("text") if isinstance(title, dict) else title.text


def tighten_xaxis_year_range(fig: go.Figure, row: int, col: int) -> None:
    """Shrink x-axis to data extent on a subplot axis."""
    years: list[float] = []
    for trace in fig.data:
        x_values = getattr(trace, "x", None)
        if x_values is None:
            continue
        for value in x_values:
            try:
                years.append(float(value))
            except (TypeError, ValueError):
                continue
    if not years:
        return
    year_min = min(years)
    year_max = max(years)
    span = year_max - year_min
    padding = max(1.0, span * 0.02)
    fig.update_xaxes(
        range=[year_min - padding, year_max + padding],
        fixedrange=True,
        row=row,
        col=col,
    )


def _legend_column_positions(column_count: int, highlight_legend: dict) -> list[float]:
    if column_count == 1:
        return [0.5]
    if column_count >= 4:
        return [
            float(highlight_legend.get("column_x_1", 0.03)),
            float(highlight_legend.get("column_x_2", 0.26)),
            float(highlight_legend.get("column_x_3", 0.49)),
            float(highlight_legend.get("column_x_4", 0.72)),
        ]
    if column_count >= 3:
        return [
            float(highlight_legend.get("column_x_1", 0.04)),
            float(highlight_legend.get("column_x_2", 0.35)),
            float(highlight_legend.get("column_x_3", 0.67)),
        ]
    return [
        float(highlight_legend.get("column_x_left", 0.04)),
        float(highlight_legend.get("column_x_right", 0.54)),
    ]


def apply_highlight_portrait_layout(
    fig: go.Figure,
    plot_settings: dict[str, Any],
) -> go.Figure:
    """
    Build a portrait figure: plot on top, multi-column legend band below.

    Highlight PNGs only.
    """
    export = highlight_export_settings(plot_settings)
    layout_settings = plot_settings["layout"]
    highlight_legend = layout_settings.get("highlight_legend", layout_settings["legend"])
    margins = layout_settings.get("highlight_margin", layout_settings["margin"])

    highlight_font = layout_settings.get("highlight_font", plot_settings["font"])
    body_size = highlight_font["size"]
    title_size = highlight_font["title_size"]
    tick_size = highlight_font["tick_size"]
    legend_size = highlight_font.get(
        "legend_size",
        highlight_legend["font_size"],
    )

    working = copy.deepcopy(fig)
    configured_columns = int(highlight_legend.get("columns", 2))
    trace_count = len(legend_trace_indices(working))
    column_count = column_count_for_traces(trace_count, configured_columns)
    rows_per_column = assign_column_legends(working, column_count)
    band = legend_band_fraction(
        rows_per_column,
        legend_size,
        export["height"],
    )
    legend_y = band * 0.5
    column_positions = _legend_column_positions(column_count, highlight_legend)

    subplot = make_subplots(
        rows=2,
        cols=1,
        row_heights=[1.0 - band, band],
        vertical_spacing=0.08,
    )

    for trace in working.data:
        subplot.add_trace(trace, row=1, col=1)

    orig = fig.layout
    axis_font = {
        "title_font": dict(size=body_size),
        "tickfont": dict(size=tick_size),
        "automargin": True,
    }

    subplot.update_xaxes(
        title_text=_axis_title_text(orig.xaxis) or "Year",
        showgrid=orig.xaxis.showgrid,
        gridcolor=orig.xaxis.gridcolor,
        row=1,
        col=1,
        **axis_font,
    )
    yaxis_type = orig.yaxis.type if orig.yaxis.type is not None else "linear"
    subplot.update_yaxes(
        title_text=_axis_title_text(orig.yaxis),
        type=yaxis_type,
        showgrid=orig.yaxis.showgrid,
        gridcolor=orig.yaxis.gridcolor,
        row=1,
        col=1,
        **axis_font,
    )
    subplot.update_xaxes(visible=False, row=2, col=1)
    subplot.update_yaxes(visible=False, row=2, col=1)

    title_dict = None
    if orig.title is not None:
        title_text = orig.title.text if hasattr(orig.title, "text") else orig.title
        title_dict = dict(
            text=title_text,
            font=dict(
                size=title_size,
                color=plot_settings["font"]["color"],
            ),
            x=0.5,
            xanchor="center",
        )

    legend_xanchor = "center" if column_count == 1 else "left"

    legend_common = {
        "orientation": "v",
        "xref": "paper",
        "yref": "paper",
        "y": legend_y,
        "yanchor": "middle",
        "xanchor": legend_xanchor,
        "bgcolor": "rgba(255, 255, 255, 0)",
        "borderwidth": 0,
        "font": dict(size=legend_size),
        "traceorder": "normal",
        "itemsizing": "constant",
        "itemwidth": 30,
        "tracegroupgap": 3,
    }

    layout_update: dict[str, Any] = {
        "width": export["width"],
        "height": export["height"],
        "title": title_dict,
        "font": {
            "family": plot_settings["font"]["family"],
            "size": body_size,
            "color": plot_settings["font"]["color"],
        },
        "plot_bgcolor": orig.plot_bgcolor,
        "paper_bgcolor": orig.paper_bgcolor,
        "margin": {
            "t": margins["top"],
            "b": 4,
            "l": margins["left"],
            "r": margins["right"],
            "pad": margins["pad"],
        },
        "showlegend": True,
        "legend": {**legend_common, "x": column_positions[0]},
        "legend2": dict(visible=False),
        "legend3": dict(visible=False),
        "legend4": dict(visible=False),
        "hovermode": orig.hovermode,
    }

    if column_count >= 2:
        layout_update["legend2"] = {**legend_common, "x": column_positions[1]}
    if column_count >= 3:
        layout_update["legend3"] = {**legend_common, "x": column_positions[2]}
    if column_count >= 4:
        layout_update["legend4"] = {**legend_common, "x": column_positions[3]}

    subplot.update_layout(**layout_update)

    tighten_xaxis_year_range(subplot, row=1, col=1)
    return subplot
