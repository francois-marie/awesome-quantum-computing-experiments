"""
Utility functions for exporting Plotly figures to various formats.
"""
import os
from pathlib import Path
import plotly.graph_objects as go
from plotly.io import write_image, to_image
import plotly.io as pio

def ensure_directory_exists(directory_path):
    """Ensure the specified directory exists, creating it if necessary."""
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def _prepare_figure_for_export(fig):
    """
    Prepare a Plotly figure for export by updating its layout and text elements.
    
    Args:
        fig: A Plotly figure object or dictionary
    
    Returns:
        A Plotly Figure object ready for export
    """
    # Convert dictionary to Figure object if needed
    if isinstance(fig, dict):
        fig = go.Figure(fig)
    
    # Update layout to use static text rendering
    fig.update_layout(
        font_family="Arial",  # Use a standard font
        title_font_family="Arial",
        uniformtext_mode='hide',  # Hide text that doesn't fit
        uniformtext_minsize=8,  # Minimum font size
        separators='. ',  # Use period for decimals and space for thousands
        showlegend=True,
        modebar_remove=["toImage", "sendDataToCloud"],  # Remove unnecessary modebar buttons
        hovermode=False  # Disable hover to prevent MathJax loading
    )
    
    # Ensure all text elements use standard fonts
    for trace in fig.data:
        if hasattr(trace, 'textfont'):
            trace.textfont.family = "Arial"
        if hasattr(trace, 'hoverlabel'):
            trace.hoverlabel.font.family = "Arial"
    
    return fig

def _export_figure(fig, output_path, format, width=800, height=600, scale=2):
    """
    Export a Plotly figure to the specified format.
    
    Args:
        fig: A Plotly Figure object
        output_path: Full path to save the exported file
        format: Export format ('pdf' or 'png')
        width: Width of the figure in pixels
        height: Height of the figure in pixels
        scale: Scale factor for the image (higher values = higher resolution)
    
    Returns:
        Path to the saved file
    """
    # Configure renderer
    pio.kaleido.scope.mathjax = None  # Disable MathJax in Kaleido
    
    # Export the figure
    write_image(
        fig, 
        output_path, 
        format=format, 
        width=width, 
        height=height, 
        scale=scale,
        engine='kaleido',
        validate=True
    )
    
    return output_path

def export_figure_to_pdf(fig, filename, output_dir='out/pdf', width=800, height=600, scale=2):
    """
    Export a Plotly figure to PDF format.
    
    Args:
        fig: A Plotly figure object or dictionary
        filename: Name of the output file (without extension)
        output_dir: Directory to save the PDF file
        width: Width of the figure in pixels
        height: Height of the figure in pixels
        scale: Scale factor for the image (higher values = higher resolution)
    
    Returns:
        Path to the saved PDF file
    """
    ensure_directory_exists(output_dir)
    output_path = os.path.join(output_dir, f"{filename}.pdf")
    prepared_fig = _prepare_figure_for_export(fig)
    return _export_figure(prepared_fig, output_path, 'pdf', width, height, scale)

def export_all_figures(figures_dict, output_dir='out/pdf'):
    """
    Export multiple Plotly figures to PDF format.
    
    Args:
        figures_dict: Dictionary mapping filenames to Plotly figures
        output_dir: Directory to save the PDF files
    
    Returns:
        List of paths to the saved PDF files
    """
    output_paths = []
    
    for filename, fig_info in figures_dict.items():
        fig = fig_info.get('figure')
        width = fig_info.get('width', 800)
        height = fig_info.get('height', 600)
        
        output_path = export_figure_to_pdf(
            fig, 
            filename, 
            output_dir=output_dir,
            width=width,
            height=height
        )
        output_paths.append(output_path)
    
    return output_paths 

def export_figure_to_png(fig, filename, output_dir='out/png', width=800, height=600, scale=2):
    """
    Export a Plotly figure to PNG format.
    
    Args:
        fig: A Plotly figure object or dictionary
        filename: Name of the output file (without extension)
        output_dir: Directory to save the PNG file
        width: Width of the figure in pixels
        height: Height of the figure in pixels
        scale: Scale factor for the image (higher values = higher resolution)
    
    Returns:
        Path to the saved PNG file
    """
    ensure_directory_exists(output_dir)
    output_path = os.path.join(output_dir, f"{filename}.png")
    prepared_fig = _prepare_figure_for_export(fig)
    return _export_figure(prepared_fig, output_path, 'png', width, height, scale)
