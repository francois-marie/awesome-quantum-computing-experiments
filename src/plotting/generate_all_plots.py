from .qec_timeline_plot import QECTimelineScatterPlot
from .qec_platform_sunburst import QECPlatformSunburst
from .experiment_count_plot import ExperimentCountPlot
from .experiment_count_yearly_plot import ExperimentCountYearlyPlot
from .entangled_error_plot import EntangledErrorPlot
from .qubit_count_plot import QubitCountPlot
from .coherence_times_plot import CoherenceTimesPlot
from .nkd_plot import NKDPlot
from .qec_cumulative_plot import QECCumulativePlot
from .export_all_to_pdf import export_all_plots_to_pdf

def generate_all_plots(export_pdf=True):
    """
    Generate all QEC visualization plots.
    
    Args:
        export_pdf: Whether to export all plots to PDF format
    """
    # Generate timeline scatter plot
    timeline_plot = QECTimelineScatterPlot()
    timeline_plot.create_plot()
    
    # Generate platform sunburst
    sunburst_plot = QECPlatformSunburst()
    sunburst_plot.create_plot()
    
    # Generate experiment count plot
    experiment_count_plot = ExperimentCountPlot()
    experiment_count_plot.create_plot()
    
    # Generate experiment count yearly plot
    experiment_count_yearly_plot = ExperimentCountYearlyPlot()
    experiment_count_yearly_plot.create_plot()
    
    # Generate entangled error plot
    entangled_error_plot = EntangledErrorPlot()
    entangled_error_plot.create_plot()
    
    # Generate qubit count plot
    qubit_count_plot = QubitCountPlot()
    qubit_count_plot.create_plot()
    
    # Generate coherence times plot
    coherence_times_plot = CoherenceTimesPlot()
    coherence_times_plot.create_plot()
    
    # Generate NKD plot
    nkd_plot = NKDPlot()
    nkd_plot.create_plot()
    
    # Generate QEC cumulative growth plot
    qec_cumulative_growth_plot = QECCumulativePlot()
    qec_cumulative_growth_plot.create_plot()
    
    # Export all plots to PDF if requested
    if export_pdf:
        export_all_plots_to_pdf()

if __name__ == "__main__":
    generate_all_plots()
