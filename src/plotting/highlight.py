"""Red-star overlay trace for highlighted papers in plots."""

import pandas as pd
import numpy as np
import plotly.graph_objects as go

from src.plotting.highlight_label import highlight_legend_label

HIGHLIGHT_MARKER_SIZE = 22
HIGHLIGHT_LABEL_FONT_SIZE = 16


def is_highlight_trace(trace: go.Scatter) -> bool:
    """True when trace is a red-star highlight overlay."""
    marker = getattr(trace, "marker", None)
    if marker is None:
        return False
    mode = getattr(trace, "mode", None)
    return (
        mode in ("markers", "markers+text")
        and getattr(marker, "symbol", None) == "star"
        and getattr(marker, "color", None) == "red"
    )


def _trace_axis_values(values) -> list[float]:
    if values is None:
        return []
    parsed: list[float] = []
    for value in list(values):
        try:
            parsed.append(float(value))
        except (TypeError, ValueError):
            continue
    return parsed


def _axis_data_bounds(fig: go.Figure) -> tuple[list[float], list[float]]:
    x_values: list[float] = []
    y_values: list[float] = []
    for trace in fig.data:
        x_values.extend(_trace_axis_values(getattr(trace, "x", None)))
        y_values.extend(_trace_axis_values(getattr(trace, "y", None)))
    return x_values, y_values


def _normalized_axis_fraction(
    value: float,
    bounds: list[float],
    log_scale: bool,
) -> float:
    if not bounds:
        return 0.5
    low = min(bounds)
    high = max(bounds)
    if high == low:
        return 0.5
    if log_scale and low > 0 and high > 0 and value > 0:
        low_log = np.log10(low)
        high_log = np.log10(high)
        if high_log == low_log:
            return 0.5
        return (np.log10(value) - low_log) / (high_log - low_log)
    return (value - low) / (high - low)


def _highlight_textposition(
    fig: go.Figure,
    x_value: float,
    y_value: float,
) -> str:
    x_bounds, y_bounds = _axis_data_bounds(fig)
    x_bounds = [*x_bounds, x_value]
    y_bounds = [*y_bounds, y_value]
    yaxis_type = getattr(fig.layout.yaxis, "type", None)
    y_log = yaxis_type == "log"
    x_frac = _normalized_axis_fraction(x_value, x_bounds, False)
    y_frac = _normalized_axis_fraction(y_value, y_bounds, y_log)

    if x_frac > 0.72 and y_frac < 0.28:
        return "top left"
    if x_frac > 0.72:
        return "middle left"
    if y_frac > 0.72:
        return "middle right"
    if y_frac < 0.28:
        return "top center"
    return "middle right"


def add_highlight_trace(
    fig: go.Figure,
    df_highlight: pd.DataFrame,
    x_col: str,
    y_col: str,
    hover_cols: list[str],
    hovertemplate: str | None,
) -> None:
    """
    Append red-star scatter trace(s) for highlighted rows.

    Labels (First Author et al.) are drawn next to each star, not in the legend.

    Args:
        fig: Plotly figure to annotate.
        df_highlight: Rows to highlight (must include x_col and y_col).
        x_col: Column name for x coordinates.
        y_col: Column name for y coordinates.
        hover_cols: Columns for hover text (index 0) and customdata (index 1) when present.
        hovertemplate: Optional Plotly hover template.
    """
    if df_highlight is None or df_highlight.empty:
        return

    plot_df = df_highlight.dropna(subset=[x_col, y_col])
    if plot_df.empty:
        return

    text_col = hover_cols[0] if len(hover_cols) > 0 else None
    custom_col = hover_cols[1] if len(hover_cols) > 1 else None

    for _, row in plot_df.iterrows():
        hover_text = None
        if text_col and text_col in row.index:
            hover_text = [row[text_col]]
        customdata = None
        if custom_col and custom_col in row.index:
            customdata = [row[custom_col]]

        label = highlight_legend_label(row)
        textposition = _highlight_textposition(
            fig,
            float(row[x_col]),
            float(row[y_col]),
        )
        resolved_hovertemplate = hovertemplate
        if hovertemplate and hover_text and "%{text}" in hovertemplate:
            resolved_hovertemplate = hovertemplate.replace("%{text}", "%{hovertext}")

        fig.add_trace(
            go.Scatter(
                x=[row[x_col]],
                y=[row[y_col]],
                mode="markers+text",
                name=label,
                showlegend=False,
                marker=dict(
                    symbol="star",
                    color="red",
                    size=HIGHLIGHT_MARKER_SIZE,
                    line=dict(color="black", width=1),
                ),
                text=[label],
                textposition=textposition,
                textfont=dict(size=HIGHLIGHT_LABEL_FONT_SIZE, color="black"),
                cliponaxis=False,
                hovertext=hover_text,
                customdata=customdata,
                hovertemplate=resolved_hovertemplate,
                legendrank=1000,
            )
        )
