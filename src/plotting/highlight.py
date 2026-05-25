"""Red-star overlay trace for newly added papers in PR highlight plots."""

import pandas as pd
import plotly.graph_objects as go


def add_highlight_trace(
    fig: go.Figure,
    df_highlight: pd.DataFrame,
    x_col: str,
    y_col: str,
    hover_cols: list[str],
    hovertemplate: str | None,
) -> None:
    """
    Append a red-star scatter trace marking rows new in the current PR.

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

    fig.add_trace(
        go.Scatter(
            x=plot_df[x_col].tolist(),
            y=plot_df[y_col].tolist(),
            mode="markers",
            name="New in this PR",
            marker=dict(
                symbol="star",
                color="red",
                size=18,
                line=dict(color="black", width=1),
            ),
            text=plot_df[text_col].tolist() if text_col and text_col in plot_df.columns else None,
            customdata=plot_df[custom_col].tolist()
            if custom_col and custom_col in plot_df.columns
            else None,
            hovertemplate=hovertemplate,
            legendrank=1000,
        )
    )
