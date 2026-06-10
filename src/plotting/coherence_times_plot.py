from .base import BasePlot
from .highlight import add_highlight_trace
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats
import json
import os


def _validate_coherence_metric(coherence_metric: str | None) -> str | None:
    if coherence_metric is None:
        return None
    metric = str(coherence_metric).strip().upper()
    if metric not in ("T1", "T2"):
        raise ValueError(
            f"coherence_metric must be 'T1', 'T2', or None, got: {coherence_metric}"
        )
    return metric


class CoherenceTimesPlot(BasePlot):
    """Creates physical qubit coherence times plot (T1, T2, or both)."""

    def __init__(
        self,
        highlight_rows=None,
        skip_export=False,
        coherence_metric=None,
    ):
        super().__init__(skip_export=skip_export)
        self.coherence_metric = _validate_coherence_metric(coherence_metric)
        self.data = self.load_data(self.config["paths"]["data"]["physical_qubits"])
        self.fitting_stats = []
        self.highlight_rows = self._preprocess_rows(highlight_rows)

    def _preprocess_rows(self, df):
        if df is None:
            return None
        if isinstance(df, list):
            df = pd.DataFrame(df)
        if df.empty:
            return None
        data = df.copy()
        data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
        data["T1"] = pd.to_numeric(data["T1"], errors="coerce")
        data["T2"] = pd.to_numeric(data["T2"], errors="coerce")
        return data

    def load_data(self, csv_path: str):
        """Load and preprocess coherence times data."""
        data = super().load_data(csv_path)
        data["T1"] = pd.to_numeric(data["T1"], errors="coerce")
        data["T2"] = pd.to_numeric(data["T2"], errors="coerce")
        return data

    def _plot_title(self) -> str:
        if self.coherence_metric == "T1":
            return "Physical Qubit T1 Coherence Times"
        if self.coherence_metric == "T2":
            return "Physical Qubit T2 Coherence Times"
        return "Physical Qubit Coherence Times Evolution"

    def _export_name(self) -> str:
        if self.coherence_metric == "T1":
            return "coherence_times_t1_plot"
        if self.coherence_metric == "T2":
            return "coherence_times_t2_plot"
        return "coherence_times_plot"

    def _calculate_fit(self, x, y, metric_type, platform):
        """Calculate linear fit in log space and return slope."""
        if len(x) < 2 or len(y) < 2:
            return None, None, None

        y_log = np.log10(y)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y_log)

        self.fitting_stats.append({
            "metric": f"Coherence Time ({metric_type})",
            "platform": platform,
            "r_squared": r_value**2,
            "slope": slope,
            "std_err": std_err,
            "p_value": p_value,
            "doubling_time": np.log10(2) / slope if slope != 0 else float("inf"),
        })

        x_fit = np.array([min(x), max(x)])
        y_fit = 10 ** (slope * x_fit + intercept)
        doubling_time = np.log10(2) / slope if slope != 0 else float("inf")

        return x_fit, y_fit, doubling_time

    def _t1_traces_for_platform(self, platform: str, platform_data: pd.DataFrame) -> list[dict]:
        traces: list[dict] = []
        platform_color = self.PLATFORM_COLORS.get(platform)
        t1_data = platform_data[platform_data["T1"].notna()]
        if t1_data.empty:
            return traces

        traces.append({
            "type": "scatter",
            "x": t1_data["Year"].tolist(),
            "y": t1_data["T1"].tolist(),
            "name": f"{platform} (T1)",
            "mode": "markers",
            "line": {"color": platform_color, "width": 3},
            "marker": {
                "color": platform_color,
                "symbol": "circle",
                "size": 12,
                "line": {"width": 2, "color": "white"},
            },
            "hovertemplate": (
                "<b>%{text}</b><br>T1: %{y} s<br>Year: %{x}<br>"
                "<a href='%{customdata}' target='_blank'>Link</a><extra></extra>"
            ),
            "text": t1_data["Article Title"].tolist(),
            "customdata": t1_data["Link"].tolist(),
        })

        x_fit, y_fit, doubling_time = self._calculate_fit(
            t1_data["Year"].values,
            t1_data["T1"].values,
            "T1",
            platform,
        )
        if x_fit is not None:
            traces.append({
                "type": "scatter",
                "x": x_fit.tolist(),
                "y": y_fit.tolist(),
                "name": f"{platform} T1 fit (x2 every {doubling_time:.1f}y)",
                "mode": "lines",
                "line": {"color": platform_color, "width": 2, "dash": "dot"},
                "showlegend": True,
            })
        return traces

    def _t2_traces_for_platform(self, platform: str, platform_data: pd.DataFrame) -> list[dict]:
        traces: list[dict] = []
        platform_color = self.PLATFORM_COLORS.get(platform)
        t2_data = platform_data[platform_data["T2"].notna()]
        if t2_data.empty:
            return traces

        traces.append({
            "type": "scatter",
            "x": t2_data["Year"].tolist(),
            "y": t2_data["T2"].tolist(),
            "name": f"{platform} (T2)",
            "mode": "markers",
            "line": {"color": platform_color, "dash": "dash", "width": 3},
            "marker": {
                "color": platform_color,
                "symbol": "circle-open",
                "size": 12,
                "line": {"width": 2, "color": platform_color},
            },
            "hovertemplate": (
                "<b>%{text}</b><br>T2: %{y} s<br>Year: %{x}<br>"
                "<a href='%{customdata}' target='_blank'>Link</a><extra></extra>"
            ),
            "text": t2_data["Article Title"].tolist(),
            "customdata": t2_data["Link"].tolist(),
        })

        x_fit, y_fit, doubling_time = self._calculate_fit(
            t2_data["Year"].values,
            t2_data["T2"].values,
            "T2",
            platform,
        )
        if x_fit is not None:
            traces.append({
                "type": "scatter",
                "x": x_fit.tolist(),
                "y": y_fit.tolist(),
                "name": f"{platform} T2 fit (x2 every {doubling_time:.1f}y)",
                "mode": "lines",
                "line": {"color": platform_color, "width": 2, "dash": "dashdot"},
                "showlegend": True,
            })
        return traces

    def _add_highlights(self) -> None:
        if self.highlight_rows is None or self.highlight_rows.empty:
            return
        if self.coherence_metric in (None, "T1"):
            t1_highlight = self.highlight_rows[self.highlight_rows["T1"].notna()]
            if not t1_highlight.empty:
                add_highlight_trace(
                    self.fig,
                    t1_highlight,
                    "Year",
                    "T1",
                    ["Article Title", "Link"],
                    "<b>%{text}</b><br>T1: %{y} s<br>Year: %{x}<br>"
                    "<a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
                )
        if self.coherence_metric in (None, "T2"):
            t2_highlight = self.highlight_rows[self.highlight_rows["T2"].notna()]
            if not t2_highlight.empty:
                add_highlight_trace(
                    self.fig,
                    t2_highlight,
                    "Year",
                    "T2",
                    ["Article Title", "Link"],
                    "<b>%{text}</b><br>T2: %{y} s<br>Year: %{x}<br>"
                    "<a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
                )

    def create_plot(self):
        """Create the physical qubit coherence times plot using Plotly."""
        traces: list[dict] = []
        include_t1 = self.coherence_metric in (None, "T1")
        include_t2 = self.coherence_metric in (None, "T2")

        for platform in sorted(self.data["Platform"].unique()):
            platform_data = self.data[self.data["Platform"] == platform].sort_values(
                "Year"
            )
            if include_t1:
                traces.extend(self._t1_traces_for_platform(platform, platform_data))
            if include_t2:
                traces.extend(self._t2_traces_for_platform(platform, platform_data))

        layout = {
            "title": {
                "text": self._plot_title(),
                "font": self.PLOTLY_LAYOUT_DEFAULTS["title"]["font"],
            },
            "xaxis": {
                "title": {"text": "Year"},
                **self.PLOTLY_LAYOUT_DEFAULTS["xaxis"],
            },
            "yaxis": {
                "title": {"text": "Coherence Time (s)"},
                "type": "log",
                **self.PLOTLY_LAYOUT_DEFAULTS["yaxis"],
            },
            "showlegend": True,
            "legend": {**self.PLOTLY_LAYOUT_DEFAULTS["legend"]},
            "font": self.PLOTLY_LAYOUT_DEFAULTS["font"],
            "plot_bgcolor": self.PLOTLY_LAYOUT_DEFAULTS["plot_bgcolor"],
            "paper_bgcolor": self.PLOTLY_LAYOUT_DEFAULTS["paper_bgcolor"],
            "margin": self.PLOTLY_LAYOUT_DEFAULTS["margin"],
            "hovermode": self.PLOTLY_LAYOUT_DEFAULTS["hovermode"],
            "width": self.plot_settings["export"]["width"],
            "height": self.plot_settings["export"]["height"],
        }

        self.fig = go.Figure(data=traces, layout=layout)
        self._add_highlights()

        if not self.skip_export:
            self.export_to_multiple(export_name=self._export_name())

    def save_fitting_stats(self, output_dir: str):
        """Save fitting statistics to a JSON file."""
        if not self.fitting_stats:
            return

        os.makedirs(output_dir, exist_ok=True)
        suffix = ""
        if self.coherence_metric == "T1":
            suffix = "_t1"
        elif self.coherence_metric == "T2":
            suffix = "_t2"
        filename = os.path.join(
            output_dir,
            f"coherence_times{suffix}_fitting_stats.json",
        )
        with open(filename, "w", encoding="utf-8") as handle:
            json.dump(self.fitting_stats, handle)


class CoherenceTimesT1Plot(CoherenceTimesPlot):
    """Coherence times plot for T1 only."""

    def __init__(self, highlight_rows=None, skip_export=False):
        super().__init__(
            highlight_rows=highlight_rows,
            skip_export=skip_export,
            coherence_metric="T1",
        )


class CoherenceTimesT2Plot(CoherenceTimesPlot):
    """Coherence times plot for T2 only."""

    def __init__(self, highlight_rows=None, skip_export=False):
        super().__init__(
            highlight_rows=highlight_rows,
            skip_export=skip_export,
            coherence_metric="T2",
        )


def main():
    """Main function to create and save the combined plot."""
    plot = CoherenceTimesPlot()
    plot.create_plot()
    plot.save_fitting_stats("out/fitting_stats")


if __name__ == "__main__":
    main()
