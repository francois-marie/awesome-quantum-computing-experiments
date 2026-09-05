"""Q-day plots: platform trends against the requirements of resource estimates.

Per platform with at least one target in ``data/qday_targets.csv``:

* ``qday_qubits_<platform>``: demonstrated qubit count, all-time exponential
  trend extended to the last crossing, one dotted line per target with the
  crossing year in the legend, and an X marker where the trend meets it.
* ``qday_error_<platform>``: same for the entangled-state error, for targets
  that state a physical error rate.

Plus ``qday_summary``: every target on a timeline, with the qubit-count
crossing, the error crossing and the resulting Q-day estimate.
"""

from __future__ import annotations

import math
import re

import plotly.graph_objects as go

from ..qday import Crossing, PlatformTrend, crossings, export_json, load_targets, platform_trend
from ..rankings import Fit
from .base import BasePlot

TARGET_COLORS = ["#DC2626", "#DB2777", "#EA580C", "#7C3AED", "#0891B2", "#65A30D"]


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def _short_qubits(n: float) -> str:
    if n >= 1e6:
        return f"{n / 1e6:g}M"
    if n >= 1e3:
        return f"{n / 1e3:g}k"
    return f"{n:g}"


def _year_label(y: float | None) -> str:
    return f"→ {int(round(y))}" if y is not None and math.isfinite(y) else "→ never (trend flat)"


class QDayPlotBase(BasePlot):
    def __init__(self, skip_export=False):
        super().__init__(skip_export=skip_export)
        self.rows = crossings(self.config)
        self.platforms = sorted({r.platform for r in self.rows})
        self.trends = {p: platform_trend(p, self.config) for p in self.platforms}

    def _layout(self, title: str, ytitle: str, log: bool = True) -> dict:
        return {
            "title": {"text": title, "font": self.PLOTLY_LAYOUT_DEFAULTS["title"]["font"]},
            "xaxis": {"title": {"text": "Year"}, **self.PLOTLY_LAYOUT_DEFAULTS["xaxis"]},
            "yaxis": {"title": {"text": ytitle}, **({"type": "log"} if log else {}), **self.PLOTLY_LAYOUT_DEFAULTS["yaxis"]},
            "showlegend": True,
            "legend": {**self.PLOTLY_LAYOUT_DEFAULTS["legend"]},
            "font": self.PLOTLY_LAYOUT_DEFAULTS["font"],
            "plot_bgcolor": self.PLOTLY_LAYOUT_DEFAULTS["plot_bgcolor"],
            "paper_bgcolor": self.PLOTLY_LAYOUT_DEFAULTS["paper_bgcolor"],
            "margin": self.PLOTLY_LAYOUT_DEFAULTS["margin"],
            "hovermode": self.PLOTLY_LAYOUT_DEFAULTS["hovermode"],
            "height": self.plot_settings["export"]["height"],
            "width": self.plot_settings["export"]["width"],
        }

    def _metric_figure(self, platform: str, kind: str) -> go.Figure | None:
        trend: PlatformTrend = self.trends[platform]
        pts = trend.qubits_points if kind == "qubits" else trend.error_points
        f: Fit | None = trend.qubits_fit if kind == "qubits" else trend.error_fit
        rows = [r for r in self.rows if r.platform == platform and (kind == "qubits" or r.physical_error is not None)]
        if not pts or not rows:
            return None
        color = self.PLATFORM_COLORS.get(platform) or self.PLATFORM_COLORS.get(platform.rstrip("s")) or "#2563EB"
        years = [r.qubits_year if kind == "qubits" else r.error_year for r in rows]
        x_end = max([y for y in years if y is not None] + [max(p.year for p in pts)]) + 1
        x_start = min(p.year for p in pts) - 1

        traces = [{
            "type": "scatter", "mode": "markers", "name": f"Demonstrated ({platform})",
            "x": [p.year for p in pts], "y": [p.value for p in pts],
            "marker": {"color": color, "size": 11, "line": {"width": 2, "color": "white"}},
            "text": [p.title for p in pts], "customdata": [p.link for p in pts],
            "hovertemplate": "<b>%{text}</b><br>" + ("Qubits" if kind == "qubits" else "Error") +
                             ": %{y}<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
        }]
        if f is not None:
            xs = [x_start, x_end]
            ys = [10 ** (f.slope * x + f.intercept) for x in xs]
            verb = "×2" if kind == "qubits" else "÷2"
            traces.append({
                "type": "scatter", "mode": "lines", "name": f"Trend fit ({verb} every {f.doubling_time:.1f}y)",
                "x": xs, "y": ys, "line": {"color": color, "width": 2, "dash": "dash"},
            })
        for i, (r, y) in enumerate(zip(rows, years)):
            c = TARGET_COLORS[i % len(TARGET_COLORS)]
            level = r.physical_qubits if kind == "qubits" else r.physical_error
            req = _short_qubits(level) if kind == "qubits" else f"{level:g}"
            label = f"{r.target}: {r.problem} ({req}) {_year_label(y)}"
            traces.append({
                "type": "scatter", "mode": "lines", "name": label, "legendgroup": f"target{i}",
                "x": [x_start, x_end], "y": [level, level],
                "line": {"color": c, "width": 1.5, "dash": "dot"},
                "hovertemplate": f"<b>{r.target}</b><br>{r.problem}<br>Requirement: {level:g}<br>Runtime: {r.runtime or 'n/a'}"
                                 f"<br><a href='{r.link}' target='_blank'>Paper</a><extra></extra>",
            })
            if y is not None and math.isfinite(y):
                traces.append({
                    "type": "scatter", "mode": "markers", "name": f"{r.target} crossing", "legendgroup": f"target{i}",
                    "showlegend": False, "x": [y], "y": [level],
                    "marker": {"color": c, "size": 13, "symbol": "x"},
                    "hovertemplate": f"<b>{r.target}</b> met in {int(round(y))}<extra></extra>",
                })
        title = (f"{platform}: physical qubit count vs. requirements" if kind == "qubits"
                 else f"{platform}: entangled state error vs. requirements")
        ytitle = "Physical Qubit Count" if kind == "qubits" else "Entanglement Error"
        return go.Figure(data=traces, layout=self._layout(title, ytitle))


class QDayPlatformPlots(QDayPlotBase):
    """One qubit-count figure and one error figure per platform with targets."""

    def create_plot(self):
        self.figures = {}
        for platform in self.platforms:
            for kind in ("qubits", "error"):
                fig = self._metric_figure(platform, kind)
                if fig is None:
                    continue
                name = f"qday_{kind}_{slug(platform)}"
                self.figures[name] = fig
                self.fig = fig
                if not self.skip_export:
                    self.export_to_multiple(export_name=name)


class QDaySummaryPlot(QDayPlotBase):
    """Timeline of crossing years per target: qubits, error and the resulting Q-day."""

    def create_plot(self):
        rows: list[Crossing] = sorted(self.rows, key=lambda r: (r.platform, r.qday_year or r.qubits_year or 9e9))
        labels = [f"{r.platform} · {r.target} · {r.problem}" for r in rows]

        def trace(name, attr, symbol, color, size):
            xs, ys, texts = [], [], []
            for r, lab in zip(rows, labels):
                y = getattr(r, attr)
                if y is None or not math.isfinite(y):
                    continue
                xs.append(round(y, 1)); ys.append(lab)
                texts.append(f"<b>{r.target}</b><br>{r.problem} on {r.platform}<br>{name}: {int(round(y))}")
            return {
                "type": "scatter", "mode": "markers", "name": name, "x": xs, "y": ys, "text": texts,
                "marker": {"symbol": symbol, "size": size, "color": color, "line": {"width": 1.5, "color": "white"}},
                "hovertemplate": "%{text}<extra></extra>",
            }

        traces = []
        for r, lab in zip(rows, labels):
            ys = [y for y in (r.qubits_year, r.error_year) if y is not None and math.isfinite(y)]
            if len(ys) == 2 and abs(ys[0] - ys[1]) > 0.05:
                traces.append({
                    "type": "scatter", "mode": "lines", "name": "range", "showlegend": False, "hoverinfo": "skip",
                    "x": [round(min(ys), 1), round(max(ys), 1)], "y": [lab, lab],
                    "line": {"color": "#BDBDBD", "width": 2},
                })
        traces += [
            trace("Qubit count met", "qubits_year", "circle", "#2563EB", 12),
            trace("Error rate met", "error_year", "square", "#EA580C", 12),
            trace("Q-day estimate (both met)", "qday_year", "star", "#DC2626", 18),
        ]
        layout = self._layout("Q-day estimates: when platform trends meet published requirements", "", log=False)
        layout["xaxis"]["title"] = {"text": "Year"}
        layout["yaxis"] = {"type": "category", "categoryorder": "array", "categoryarray": labels[::-1],
                           "automargin": True, **{k: v for k, v in self.PLOTLY_LAYOUT_DEFAULTS["yaxis"].items() if k != "showgrid"}}
        layout["margin"] = {**layout["margin"], "l": 320}
        self.fig = go.Figure(data=traces, layout=layout)
        if not self.skip_export:
            self.export_to_multiple(export_name="qday_summary")


def main():
    export_json()
    QDayPlatformPlots().create_plot()
    QDaySummaryPlot().create_plot()


if __name__ == "__main__":
    main()
