from .base import BasePlot
import plotly.graph_objects as go
import pandas as pd
from .export_utils import export_figure_to_pdf

class QECCumulativePlot(BasePlot):
    """Creates a stacked area chart showing cumulative QEC implementations."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['qec'])
        
    def load_data(self, csv_path: str):
        """Load and preprocess QEC data for cumulative analysis."""
        data = super().load_data(csv_path)
        
        # Sort data by year and prepare cumulative counts
        yearly_counts = pd.crosstab(data['Year'], data['Code Name'])
        
        # Add missing years
        min_year = yearly_counts.index.min()
        max_year = yearly_counts.index.max()
        all_years = range(min_year, max_year + 1)
        yearly_counts = yearly_counts.reindex(all_years, fill_value=0)
        
        # Calculate cumulative counts
        cumulative_counts = yearly_counts.cumsum()
        
        return cumulative_counts
        
    def create_plot(self):
        """Create the stacked area chart of cumulative QEC implementations."""
        
        # Create traces manually for better control
        traces = []
        for code_name in self.data.columns:
            trace = {
                'type': 'scatter',
                'x': self.data.index.tolist(),
                'y': self.data[code_name].tolist(),
                'name': code_name,
                'stackgroup': 'one',  # Enable stacking
                'mode': 'lines',  # Only show lines, no markers or text
                'line': {'width': 0.5},  # Thin line borders for publication
                'fillcolor': self._get_rgba_color(code_name, 0.5),  # Convert hex to rgba with opacity
                'line': {'color': self._get_rgba_color(code_name, 0.8)},  # Convert hex to rgba with opacity
                'showlegend': True,
                'hoverinfo': 'x+y+name',  # Show x, y values and name on hover
                'hovertemplate': "%{y} %{fullData.name} experiments in %{x}<extra></extra>"
            }
            traces.append(trace)

        # Create layout with standardized settings for publication
        layout = {
            'title': {
                'text': 'Cumulative Growth of QEC Implementations Over Time',
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            'xaxis': {
                'title': 'Year',
                **self.PLOTLY_LAYOUT_DEFAULTS['xaxis']
            },
            'yaxis': {
                'title': 'Cumulative Number of Implementations',
                **self.PLOTLY_LAYOUT_DEFAULTS['yaxis']
            },
            'showlegend': True,
            'legend': {
                'title': {'text': 'QEC Code Type'},
                **self.PLOTLY_LAYOUT_DEFAULTS['legend']
            },
            'font': self.PLOTLY_LAYOUT_DEFAULTS['font'],
            'plot_bgcolor': self.PLOTLY_LAYOUT_DEFAULTS['plot_bgcolor'],
            'paper_bgcolor': self.PLOTLY_LAYOUT_DEFAULTS['paper_bgcolor'],
            'margin': self.PLOTLY_LAYOUT_DEFAULTS['margin'],
            'hovermode': self.PLOTLY_LAYOUT_DEFAULTS['hovermode'],
            'height': self.plot_settings['export']['height'],
            'width': self.plot_settings['export']['width']
        }
        
        # Create a Plotly figure for export
        self.fig = go.Figure(data=traces, layout=layout)
        self.export_to_multiple(export_name="qec_cumulative_growth")

    def _get_rgba_color(self, code_name, opacity):
        """Convert hex color to rgba with opacity."""
        hex_color = self.CODE_COLORS.get(code_name, '#808080')
        # Remove the '#' and convert to RGB
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return f'rgba({r}, {g}, {b}, {opacity})'  # 0.8 opacity

def main():
    """Main function to create and save the plot."""
    plot = QECCumulativePlot()
    plot.create_plot()

if __name__ == "__main__":
    main() 