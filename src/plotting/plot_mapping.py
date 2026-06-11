"""CSV-to-plot module mapping shared by CI workflows and highlight runner."""

CSV_TO_PLOT_MODULES: dict[str, list[str]] = {
    "data/qec_exp.csv": [
        "qec_timeline_plot",
        "qec_platform_sunburst",
        "experiment_count_plot",
        "experiment_count_yearly_plot",
        "nkd_plot",
        "qec_cumulative_plot",
        "qec_qubit_count_plot",
    ],
    "data/msd_exp.csv": [
        "msd_plot",
        "msd_error_evolution_plot",
    ],
    "data/entangled_state_error_exp.csv": [
        "entangled_error_plot",
    ],
    "data/qubit_count.csv": [
        "qubit_count_plot",
    ],
    "data/physical_qubits.csv": [
        "coherence_times_plot",
    ],
}

SHARED_PLOT_TRIGGER_PATHS: list[str] = [
    "config.yaml",
    "src/plotting/base.py",
    "src/plotting/export_utils.py",
]

# (module_name, class_name, png_export_name, match_strategy)
# match_strategy: "raw" uses diff rows as-is; "processed_match" joins on plot.data
HIGHLIGHT_PLOT_SPECS: dict[str, list[tuple[str, str, str, str]]] = {
    "data/qec_exp.csv": [
        ("qec_timeline_plot", "QECTimelineScatterPlot", "qec_timeline_aggregated", "raw"),
        ("nkd_plot", "NKDPlot", "nkd_plot_aggregated", "raw"),
        ("qec_qubit_count_plot", "QECQubitCountPlot", "qec_data_qubit_count_plot", "raw"),
    ],
    "data/msd_exp.csv": [
        ("msd_plot", "MSDPlot", "msd_plot", "processed_match"),
        ("msd_error_evolution_plot", "MSDErrorEvolutionPlot", "msd_error_evolution_plot", "processed_match"),
    ],
    "data/entangled_state_error_exp.csv": [
        ("entangled_error_plot", "EntangledErrorPlot", "entangled_error_plot", "processed_match"),
    ],
    "data/qubit_count.csv": [
        ("qubit_count_plot", "QubitCountPlot", "qubit_count_plot", "processed_match"),
    ],
    "data/physical_qubits.csv": [
        ("coherence_times_plot", "CoherenceTimesT1Plot", "coherence_times_t1_plot", "processed_match"),
        ("coherence_times_plot", "CoherenceTimesT2Plot", "coherence_times_t2_plot", "processed_match"),
    ],
}


def plot_modules_for_csvs(csv_paths: list[str]) -> list[str]:
    """Return sorted unique plot module names affected by the given CSV paths."""
    modules: set[str] = set()
    for csv_path in csv_paths:
        modules.update(CSV_TO_PLOT_MODULES.get(csv_path, []))
    return sorted(modules)
