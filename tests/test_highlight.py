"""Tests for PR highlight overlay traces."""

import pandas as pd
import plotly.graph_objects as go
import pytest

from src.plotting.coherence_times_plot import CoherenceTimesPlot
from src.plotting.entangled_error_plot import EntangledErrorPlot
from src.plotting.highlight import add_highlight_trace
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
    assert trace.name == "New in this PR"


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
            MSDPlot,
            lambda: pd.DataFrame({
                "Article Title": ["Highlight Paper"],
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
    highlight_traces = [
        t for t in plot.fig.data if getattr(t, "name", None) == "New in this PR"
    ]
    assert len(highlight_traces) >= 1
