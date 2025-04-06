"""
Script to export all Plotly figures to PDF format.
"""
import os
import importlib
import plotly.graph_objects as go
from pathlib import Path
from .export_utils import export_figure_to_pdf, ensure_directory_exists

# Dictionary mapping module names to their class names
PLOT_MODULES = {
    'experiment_count_plot': 'ExperimentCountPlot',
    'experiment_count_yearly_plot': 'ExperimentCountYearlyPlot',
    'qec_platform_sunburst': 'QECPlatformSunburst',
    'qec_timeline_plot': 'QECTimelineScatterPlot',
    'entangled_error_plot': 'EntangledErrorPlot',
    'qubit_count_plot': 'QubitCountPlot',
    'coherence_times_plot': 'CoherenceTimesPlot',
    'nkd_plot': 'NKDPlot'
}

def export_all_plots_to_pdf(output_dir='out/pdf'):
    """
    Export all plots to PDF format.
    
    Args:
        output_dir: Directory to save the PDF files
    """
    # Ensure the output directory exists
    ensure_directory_exists(output_dir)
    
    exported_files = []
    
    # Process each plot module
    for module_name, class_name in PLOT_MODULES.items():
        try:
            # Import the module
            module_path = f'.{module_name}'
            module = importlib.import_module(module_path, package='src.plotting')
            
            # Check if the class exists in the module
            if hasattr(module, class_name):
                # Create an instance of the plot class
                plot_class = getattr(module, class_name)
                plot_instance = plot_class()
                
                # Create the plot
                plot_instance.create_plot()
                
                # Check if the module already exports to PDF
                if 'export_figure_to_pdf' not in str(module.__dict__):
                    # Try to get the figure from the instance
                    if hasattr(plot_instance, 'fig'):
                        fig = plot_instance.fig
                        try:
                            export_figure_to_pdf(
                                fig, 
                                module_name, 
                                output_dir=output_dir,
                                width=1000,
                                height=800
                            )
                        except Exception as e:
                            pass
                
                exported_files.append(module_name)
            
        except Exception as e:
            pass
    
    return exported_files

def main():
    """Main function to export all plots to PDF."""
    export_all_plots_to_pdf()

if __name__ == "__main__":
    main() 