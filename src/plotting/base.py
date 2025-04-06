from abc import ABC, abstractmethod
import yaml
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
import plotly.utils
import json
from pathlib import Path
import os
from .export_utils import export_figure_to_pdf, ensure_directory_exists, export_figure_to_png

class BasePlot(ABC):
    """Base class for all plotting classes."""
    
    def __init__(self, double_column=False):
        """Initialize plot settings and load config."""
        self.config = self.load_config()
        self.plot_settings = self.config['plot_settings']
        self.double_column = double_column
        self.fig = None  # Will store the Plotly figure for export
        
        # Load colors from config
        self.PLATFORM_COLORS = self.config['platform_colors']
        self.CODE_COLORS = self.config['code_colors']
        
        # Build Plotly layout defaults from config
        self.PLOTLY_LAYOUT_DEFAULTS = {
            'font': {
                'family': self.plot_settings['font']['family'],
                'size': self.plot_settings['font']['size'],
                'color': self.plot_settings['font']['color']
            },
            'plot_bgcolor': self.plot_settings['layout']['background']['plot'],
            'paper_bgcolor': self.plot_settings['layout']['background']['paper'],
            'margin': {
                't': self.plot_settings['layout']['margin']['top'],
                'b': self.plot_settings['layout']['margin']['bottom'],
                'l': self.plot_settings['layout']['margin']['left'],
                'r': self.plot_settings['layout']['margin']['right'],
                'pad': self.plot_settings['layout']['margin']['pad']
            },
            'hovermode': 'closest',
            'bargap': 0.15,
            'showlegend': True,
            'legend': {
                'x': self.plot_settings['layout']['legend']['position_x'],
                'y': self.plot_settings['layout']['legend']['position_y'],
                'bgcolor': self.plot_settings['layout']['legend']['bg_color'],
                'bordercolor': self.plot_settings['layout']['legend']['border_color'],
                'font': {'size': self.plot_settings['layout']['legend']['font_size']}
            },
            'xaxis': {
                'showgrid': True,
                'gridcolor': self.plot_settings['layout']['grid']['color'],
                'gridwidth': self.plot_settings['layout']['grid']['width'],
                'linecolor': self.plot_settings['layout']['axis']['line_color'],
                'linewidth': self.plot_settings['layout']['axis']['line_width'],
                'ticks': 'outside',
                'tickcolor': self.plot_settings['layout']['axis']['line_color'],
                'tickwidth': 1,
                'ticklen': self.plot_settings['layout']['axis']['tick_length'],
                'minor': {
                    'ticks': 'outside',
                    'ticklen': self.plot_settings['layout']['axis']['minor_tick_length'],
                    'tickwidth': 1,
                    'tickcolor': self.plot_settings['layout']['axis']['line_color']
                }
            },
            'yaxis': {
                'showgrid': True,
                'gridcolor': self.plot_settings['layout']['grid']['color'],
                'gridwidth': self.plot_settings['layout']['grid']['width'],
                'linecolor': self.plot_settings['layout']['axis']['line_color'],
                'linewidth': self.plot_settings['layout']['axis']['line_width'],
                'ticks': 'outside',
                'tickcolor': self.plot_settings['layout']['axis']['line_color'],
                'tickwidth': 1,
                'ticklen': self.plot_settings['layout']['axis']['tick_length'],
                'minor': {
                    'ticks': 'outside',
                    'ticklen': self.plot_settings['layout']['axis']['minor_tick_length'],
                    'tickwidth': 1,
                    'tickcolor': self.plot_settings['layout']['axis']['line_color']
                }
            },
            'title': {
                'font': {
                    'size': self.plot_settings['font']['title_size'],
                    'color': self.plot_settings['font']['color']
                },
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.95,
                'yanchor': 'top'
            },
            'shapes': [{
                'type': 'rect',
                'xref': 'paper',
                'yref': 'paper',
                'x0': 0,
                'y0': 0,
                'x1': 1,
                'y1': 1,
                'line': {
                    'color': self.plot_settings['layout']['axis']['line_color'],
                    'width': 1
                }
            }]
        }
        
    def load_data(self, csv_path: str) -> pd.DataFrame:
        """Load data from CSV file and ensure numeric types."""
        data = pd.read_csv(csv_path)
        # Convert year to numeric, handling errors
        data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
        return data
        
    @abstractmethod
    def create_plot(self):
        """Create the plot. Must be implemented by child classes."""
        pass
        
    def save_plot(self, filename: str):
        """Save the plot to the configured output directory."""
        output_path = Path(self.config['paths']['output']['plots']) / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(
            output_path,
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none',
            dpi=300
        )
        # save also as pdf
        plt.savefig(output_path.with_suffix('.pdf'), bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close()

    def setup_plot(self, title: str, xlabel: str, ylabel: str):
        """Set up the basic plot parameters."""
        plt.figure()
        plt.title(title, fontsize=self.plot_settings['fontsize']['title'])
        plt.xlabel(xlabel, fontsize=self.plot_settings['fontsize']['label'])
        plt.ylabel(ylabel, fontsize=self.plot_settings['fontsize']['label'])
        
        # Configure ticks
        plt.tick_params(
            axis='both',
            which='major',
            labelsize=self.plot_settings['fontsize']['tick']
        )
        plt.tick_params(
            axis='both',
            which='minor',
            labelsize=self.plot_settings['fontsize']['tick']
        )

    def load_config(self):
        """Load configuration from YAML file."""
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
            
    def export_to_js(self, data, layout, element_id, filename):
        """
        Export a Plotly figure to JavaScript file.
        
        Args:
            data: The data component of the Plotly figure
            layout: The layout component of the Plotly figure
            element_id: The HTML element ID where the plot will be rendered
            filename: The output filename (without extension)
        """
        # Ensure the output directory exists
        output_dir = Path(self.config['paths']['output']['plots']).parent / 'js'
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{filename}.js"
        
        # Convert Plotly objects to JSON-serializable format
        if isinstance(data, (list, tuple)) and len(data) > 0 and hasattr(data[0], 'to_plotly_json'):
            # Handle list of Plotly traces
            data_json = json.dumps([trace.to_plotly_json() for trace in data], indent=2)
        else:
            # Handle regular JSON data or Plotly data
            data_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder, indent=2)
            
        # Convert layout to JSON
        if hasattr(layout, 'to_plotly_json'):
            layout_json = json.dumps(layout.to_plotly_json(), indent=2)
        else:
            layout_json = json.dumps(layout, cls=plotly.utils.PlotlyJSONEncoder, indent=2)
        
        # Generate JavaScript code
        js_code = f"""// {filename.replace('_', ' ').title()} Plot
const {filename.replace('-', '_')}Data = {data_json};

const {filename.replace('-', '_')}Layout = {layout_json};

Plotly.newPlot('{element_id}', {filename.replace('-', '_')}Data, {filename.replace('-', '_')}Layout);
"""
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write(js_code)
            
        return output_path
        
    def export_to_pdf(self, fig, filename):
        """
        Export a Plotly figure to PDF.
        
        Args:
            fig: A Plotly figure object
            filename: The output filename (without extension)
        """
        return export_figure_to_pdf(
            fig, 
            filename, 
            output_dir='out/pdf',
            width=self.plot_settings['export']['width'],
            height=self.plot_settings['export']['height'],
            scale=self.plot_settings['export']['scale']
        ) 
            
    def export_to_png(self, fig, filename):
        """
        Export a Plotly figure to PNG.
        
        Args:
            fig: A Plotly figure object
            filename: The output filename (without extension)
        """
        return export_figure_to_png(
            fig, 
            filename, 
            output_dir='out/png',
            width=self.plot_settings['export']['width'],
            height=self.plot_settings['export']['height'],
            scale=self.plot_settings['export']['scale']
        ) 

    def export_to_multiple(self, export_name:str, element_id=None):
        
        # Export to PDF
        self.export_to_pdf(self.fig, export_name)

        # Export to PNG
        self.export_to_png(self.fig, export_name)
        
        # Export to JavaScript - make a copy of the figure to avoid inheriting
        # any modifications made during PDF/PNG export
        fig_dict = self.fig.to_dict()
        
        # Ensure hovermode is set correctly for the JS export
        if 'layout' in fig_dict and fig_dict['layout'].get('hovermode') is False:
            fig_dict['layout']['hovermode'] = 'closest'
            
        self.export_to_js(
            fig_dict['data'], 
            fig_dict['layout'], 
            element_id if element_id else export_name.replace('_', '-'),
            export_name
        )


