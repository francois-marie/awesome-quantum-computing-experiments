"""Spider (radar) charts ranking platforms on every tracked metric.

One polar subplot per metric. Axes are the platforms that have data on that
metric; the radius is the rank (rank 1 on the outer ring). Two polygons per
metric: rank on the best value to date, and rank on the pace of improvement
over the last ``RATE_WINDOW`` years. Ranking logic lives in ``src/rankings.py``
and mirrors the interactive version on the website.
"""

from __future__ import annotations

import math

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..rankings import METRICS, Metric, Ranking, rankings
from .base import BasePlot

RATE_WINDOW = 10
BEST_COLOR = "#2563EB"
RATE_COLOR = "#F97316"


def _rate_label(metric: Metric, r: Ranking) -> str:
    if r.rate is None:
        return "no trend"
    if not math.isfinite(r.rate.doubling_time):
        return "flat"
    verb = "÷2" if metric.better == "min" else "×2"
    if r.rate.slope > 0:
        return f"{verb} every {r.rate.doubling_time:.1f} y"
    return f"worsening ({r.rate.doubling_time:.1f} y)"


def _fmt(metric: Metric, v: float) -> str:
    if metric.key == "qubit_count" or metric.aggregate == "count":
        return f"{int(v):,}"
    if metric.key == "qec_distance":
        return f"d = {int(v)}"
    if metric.key in ("t1", "t2"):
        return f"{v:.3g} s"
    return f"{v:.2e}"


class RankingsRadarPlot(BasePlot):
    """Small multiples of rank radars, one per metric."""

    def __init__(self, skip_export=False, window: float = RATE_WINDOW):
        super().__init__(skip_export=skip_export)
        self.window = window
        self.tables = [rankings(m, window=window, config=self.config) for m in METRICS]

    def create_plot(self):
        n = len(self.tables)
        cols = 2
        rows = math.ceil(n / cols)
        fig = make_subplots(
            rows=rows,
            cols=cols,
            specs=[[{"type": "polar"}] * cols for _ in range(rows)],
            subplot_titles=[t.metric.label for t in self.tables],
            horizontal_spacing=0.10,
            vertical_spacing=0.10,
        )

        for idx, table in enumerate(self.tables):
            metric = table.metric
            platforms = table.platforms
            k = len(platforms)
            by_platform = {r.platform: r for r in table.rows}
            ordered = [by_platform[p] for p in platforms]
            theta = platforms + [platforms[0]]

            best_r = [(k + 1 - r.best_rank) if r.best else 0 for r in ordered]
            rate_r = [(k + 1 - r.rate_rank) if r.rate else 0 for r in ordered]
            best_txt = [
                f"<b>{r.platform}</b><br>#{r.best_rank} best: {_fmt(metric, r.best.value)} ({int(r.best.year)})"
                if r.best else f"<b>{r.platform}</b><br>no data"
                for r in ordered
            ]
            rate_txt = [f"<b>{r.platform}</b><br>#{r.rate_rank} pace: {_rate_label(metric, r)}" for r in ordered]

            row, col = idx // cols + 1, idx % cols + 1
            fig.add_trace(go.Scatterpolar(
                r=best_r + best_r[:1], theta=theta, name="Best value (rank)",
                mode="lines+markers", fill="toself",
                line={"color": BEST_COLOR, "width": 2}, marker={"size": 6, "color": BEST_COLOR},
                fillcolor="rgba(37, 99, 235, 0.18)",
                text=best_txt + best_txt[:1], hovertemplate="%{text}<extra></extra>",
                legendgroup="best", showlegend=idx == 0,
            ), row=row, col=col)
            fig.add_trace(go.Scatterpolar(
                r=rate_r + rate_r[:1], theta=theta, name=f"Improvement rate, last {self.window:g} y (rank)",
                mode="lines+markers", fill="toself",
                line={"color": RATE_COLOR, "width": 2, "dash": "dash"}, marker={"size": 6, "color": RATE_COLOR},
                fillcolor="rgba(249, 115, 22, 0.08)",
                text=rate_txt + rate_txt[:1], hovertemplate="%{text}<extra></extra>",
                legendgroup="rate", showlegend=idx == 0,
            ), row=row, col=col)

            polar_key = "polar" if idx == 0 else f"polar{idx + 1}"
            fig.update_layout({polar_key: {
                "radialaxis": {
                    "range": [0, k], "tickvals": list(range(1, k + 1)),
                    "ticktext": [f"#{k + 1 - v}" for v in range(1, k + 1)],
                    "tickfont": {"size": 8, "color": "#999"}, "gridcolor": "#E5E5E5", "angle": 90,
                    "showline": False,
                },
                "angularaxis": {"tickfont": {"size": 10}, "gridcolor": "#E5E5E5", "rotation": 90, "direction": "clockwise"},
                "bgcolor": "white",
            }})

        fig.update_layout(
            title={"text": "Platform Rankings per Metric (outer ring = rank 1)",
                   "font": self.PLOTLY_LAYOUT_DEFAULTS["title"]["font"], "x": 0.5, "xanchor": "center"},
            font=self.PLOTLY_LAYOUT_DEFAULTS["font"],
            paper_bgcolor="white",
            legend={"orientation": "h", "x": 0.5, "xanchor": "center", "y": -0.03,
                    "font": {"size": 12}, "bgcolor": "rgba(255,255,255,0.8)"},
            margin={"t": 120, "b": 80, "l": 60, "r": 60},
            height=430 * rows + 160,
            width=self.plot_settings["export"]["width"],
        )
        fig.update_annotations(font={"size": 15}, yshift=26)
        self.fig = fig
        if not self.skip_export:
            self.export_to_multiple(export_name="rankings_radar")


def main():
    RankingsRadarPlot().create_plot()


if __name__ == "__main__":
    main()
