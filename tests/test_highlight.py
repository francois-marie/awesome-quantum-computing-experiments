"""Tests for PR highlight overlay traces."""

import pandas as pd
import plotly.graph_objects as go
import pytest

from src.plotting.coherence_times_plot import (
    CoherenceTimesPlot,
    CoherenceTimesT1Plot,
    CoherenceTimesT2Plot,
)
from src.plotting.entangled_error_plot import EntangledErrorPlot
from src.plotting.highlight import add_highlight_trace, is_highlight_trace
from src.plotting.highlight_label import highlight_legend_label
from src.plotting.highlight_layout import (
    apply_highlight_portrait_layout,
    assign_column_legends,
    highlight_export_settings,
    legend_band_fraction,
    legend_trace_indices,
    shorten_legend_name,
)
from src.plotting.msd_error_evolution_plot import MSDErrorEvolutionPlot
from src.plotting.msd_plot import MSDPlot
from src.plotting.nkd_plot import NKDPlot
from src.plotting.qec_qubit_count_plot import QECQubitCountPlot
from src.plotting.qec_timeline_plot import QECTimelineScatterPlot
from src.plotting.qubit_count_plot import QubitCountPlot


def test_add_highlight_trace_marker_style():
    fig = go.Figure()
    df = pd.DataFrame({
        "Year": [2024],
        "Entangled State Error": [0.01],
        "Article Title": ["Test Paper"],
        "First Author": ["Smith"],
        "Link": ["https://arxiv.org/abs/test"],
    })
    add_highlight_trace(
        fig,
        df,
        "Year",
        "Entangled State Error",
        ["Article Title", "Link"],
        "<b>%{text}</b><extra></extra>",
    )
    assert len(fig.data) == 1
    trace = fig.data[0]
    assert trace.marker.symbol == "star"
    assert trace.marker.color == "red"
    assert trace.showlegend is False
    assert trace.name == "Smith et al."
    assert trace.text == ("Smith et al.",)
    assert trace.mode == "markers+text"


def test_add_highlight_trace_skips_empty():
    fig = go.Figure()
    add_highlight_trace(
        fig,
        pd.DataFrame(),
        "Year",
        "y",
        [],
        None,
    )
    assert len(fig.data) == 0


@pytest.mark.parametrize(
    "plot_class,highlight_df_factory",
    [
        (
            EntangledErrorPlot,
            lambda: pd.DataFrame({
                "Article Title": ["Highlight Paper"],
                "First Author": ["Doe"],
                "Link": ["https://arxiv.org/abs/hl"],
                "Year": [2024],
                "Platform": ["Ion traps"],
                "Entangled State Error": [0.001],
                "Notes": [""],
            }),
        ),
        (
            QubitCountPlot,
            lambda: pd.DataFrame({
                "Article Title": ["Highlight Paper"],
                "First Author": ["Doe"],
                "Link": ["https://arxiv.org/abs/hl"],
                "Year": [2024],
                "Platform": ["Ion traps"],
                "Number of qubits": [50],
                "Notes": [""],
            }),
        ),
        (
            CoherenceTimesPlot,
            lambda: pd.DataFrame({
                "Article Title": ["Highlight Paper"],
                "First Author": ["Doe"],
                "Link": ["https://arxiv.org/abs/hl"],
                "Year": [2024],
                "Platform": ["Ion traps"],
                "T1": [1e-4],
                "T2": [2e-4],
                "Code Name": ["Test"],
                "Notes": [""],
            }),
        ),
        (
            CoherenceTimesT1Plot,
            lambda: pd.DataFrame({
                "Article Title": ["Highlight Paper"],
                "First Author": ["Doe"],
                "Link": ["https://arxiv.org/abs/hl"],
                "Year": [2024],
                "Platform": ["Ion traps"],
                "T1": [1e-4],
                "T2": [None],
                "Code Name": ["Test"],
                "Notes": [""],
            }),
        ),
        (
            CoherenceTimesT2Plot,
            lambda: pd.DataFrame({
                "Article Title": ["Highlight Paper"],
                "First Author": ["Doe"],
                "Link": ["https://arxiv.org/abs/hl"],
                "Year": [2024],
                "Platform": ["Ion traps"],
                "T1": [None],
                "T2": [2e-4],
                "Code Name": ["Test"],
                "Notes": [""],
            }),
        ),
        (
            MSDPlot,
            lambda: pd.DataFrame({
                "Article Title": ["Highlight Paper"],
                "First Author": ["Doe"],
                "Link": ["https://arxiv.org/abs/hl"],
                "Year": [2024],
                "Platform": ["Ion traps"],
                "Fidelity": ["0.99"],
                "Acceptance Rate (%)": [80],
                "Magic State": ["T"],
                "QEC Code": [""],
                "Experiment Type": ["prep"],
            }),
        ),
        (
            MSDErrorEvolutionPlot,
            lambda: pd.DataFrame({
                "Article Title": ["Highlight Paper"],
                "First Author": ["Doe"],
                "Link": ["https://arxiv.org/abs/hl"],
                "Year": [2024],
                "Platform": ["Ion traps"],
                "Fidelity": ["0.99"],
                "Acceptance Rate (%)": [80],
                "Magic State": ["T"],
                "QEC Code": [""],
                "Experiment Type": ["prep"],
            }),
        ),
        (
            NKDPlot,
            lambda: pd.DataFrame({
                "Article Title": ["Highlight Paper"],
                "First Author": ["Doe"],
                "Link": ["https://arxiv.org/abs/hl"],
                "Year": [2024],
                "Platform": ["Ion traps"],
                "Code Parameters": ["[[9,1,3]]"],
                "Code Name": ["Surface Code"],
                "Notes": [""],
            }),
        ),
        (
            QECTimelineScatterPlot,
            lambda: pd.DataFrame({
                "Article Title": ["Highlight Paper"],
                "First Author": ["Doe"],
                "Link": ["https://arxiv.org/abs/hl"],
                "Year": [2024],
                "Platform": ["Ion traps"],
                "Code Parameters": ["[[9,1,3]]"],
                "Code Name": ["Surface Code"],
                "Notes": [""],
            }),
        ),
        (
            QECQubitCountPlot,
            lambda: pd.DataFrame({
                "Article Title": ["Highlight Paper"],
                "First Author": ["Doe"],
                "Link": ["https://arxiv.org/abs/hl"],
                "Year": [2024],
                "Platform": ["Ion traps"],
                "Code Parameters": ["[[9,1,3]]"],
                "Code Name": ["Surface Code"],
                "Notes": [""],
            }),
        ),
    ],
)
def test_highlight_plots_run_with_one_row(mocker, plot_class, highlight_df_factory):
    mocker.patch.object(plot_class, "export_to_multiple")
    highlight_df = highlight_df_factory()
    plot = plot_class(highlight_rows=highlight_df)
    plot.create_plot()
    assert plot.fig is not None
    highlight_traces = [t for t in plot.fig.data if is_highlight_trace(t)]
    assert len(highlight_traces) >= 1
    assert highlight_traces[0].name == "Doe et al."
    assert highlight_traces[0].showlegend is False


def test_highlight_legend_label_first_author():
    row = pd.Series({
        "First Author": "Hughes",
        "Article Title": "Trapped-ion two-qubit gates with high fidelity",
    })
    assert highlight_legend_label(row) == "Hughes et al."


def test_highlight_legend_label_title_when_no_first_author():
    row = pd.Series({
        "Link": "https://doi.org/10.48550/arXiv.2403.12021",
        "Article Title": "Example paper on gates",
    })
    assert highlight_legend_label(row) == "Example et al."


def test_highlight_legend_label_research_group():
    row = pd.Series({
        "Link": "https://example.com/paper",
        "Article Title": "Some experiment",
        "Research Group": "Yale (Schoelkopf)",
    })
    assert highlight_legend_label(row) == "Schoelkopf et al."


def test_highlight_legend_label_title_fallback():
    row = pd.Series({
        "Link": "",
        "First Author": "",
        "Article Title": "Trapped-ion two-qubit gates with high fidelity",
    })
    assert highlight_legend_label(row) == "Trapped-ion et al."


def test_shorten_legend_name_fit():
    name = "Superconducting circuit fit (x2 every 2.6y)"
    assert shorten_legend_name(name) == "SC circuit fit /2.6y"


def test_assign_column_legends_splits_traces():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1], y=[1], name="A"))
    fig.add_trace(go.Scatter(x=[2], y=[2], name="B"))
    fig.add_trace(go.Scatter(x=[3], y=[3], name="C"))
    rows = assign_column_legends(fig, 2)
    assert rows == 2
    assert fig.data[2].legend == "legend2"


def test_legend_trace_indices_excludes_hidden():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1], y=[1], name="Visible"))
    fig.add_trace(go.Scatter(x=[2], y=[2], name="Hidden", showlegend=False))
    assert legend_trace_indices(fig) == [0]


def test_legend_band_fraction_scales_with_rows():
    small = legend_band_fraction(3, 18, 900)
    large = legend_band_fraction(9, 18, 900)
    assert large > small
    assert 0.14 <= small <= 0.42


def test_highlight_portrait_export_settings():
    plot = QubitCountPlot(skip_export=True)
    dims = highlight_export_settings(plot.plot_settings)
    assert dims["width"] < dims["height"]
    assert dims["width"] == 780
    assert dims["height"] == 1040


def test_apply_highlight_portrait_layout():
    highlight_df = pd.DataFrame({
        "Article Title": ["Highlight Paper"],
        "First Author": ["Doe"],
        "Link": ["https://arxiv.org/abs/hl"],
        "Year": [2024],
        "Platform": ["Ion traps"],
        "Number of qubits": [50],
        "Notes": [""],
    })
    plot = QubitCountPlot(highlight_rows=highlight_df, skip_export=True)
    plot.create_plot()
    highlight_fig = apply_highlight_portrait_layout(
        plot.fig,
        plot.plot_settings,
    )
    assert highlight_fig.layout.width == 780
    assert highlight_fig.layout.height == 1040
    assert highlight_fig.layout.margin.b <= 20
    assert highlight_fig.layout.margin.r <= 20
    assert highlight_fig.layout.font.size == 23
    assert highlight_fig.layout.legend.font.size == 18
    assert highlight_fig.layout.legend.orientation == "v"
    assert highlight_fig.layout.legend.yanchor == "middle"
    assert highlight_fig.layout.legend.xanchor == "center"
    assert highlight_fig.layout.legend2.visible is False
    assert len(highlight_fig.data) >= 1
    assert highlight_fig.layout.xaxis.range is not None
    assert len(legend_trace_indices(plot.fig)) >= 1
    highlight_traces = [t for t in plot.fig.data if is_highlight_trace(t)]
    assert highlight_traces
    assert highlight_traces[0].showlegend is False
    assert highlight_traces[0].text == ("Doe et al.",)
