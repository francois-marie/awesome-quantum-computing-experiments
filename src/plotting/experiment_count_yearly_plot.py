from .base import BasePlot
import json
from pathlib import Path
import plotly
import plotly.graph_objects as go
import pandas as pd
import os
from .export_utils import export_figure_to_pdf

class ExperimentCountYearlyPlot(BasePlot):
    """Creates a stacked column chart showing yearly experiment counts by platform."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['qec'])
        
    def load_data(self, csv_path: str):
        """Load and preprocess experiment count data."""
        data = pd.read_csv(csv_path)
        # Count experiments per year and platform
        experiment_counts = data.groupby(['Year', 'Platform']).size().reset_index(name='Count')

        # Get all unique years and platforms
        years = range(experiment_counts['Year'].min(), experiment_counts['Year'].max() + 1)
        platforms = experiment_counts['Platform'].unique()

        # Create a complete DataFrame with all year-platform combinations
        complete_index = pd.MultiIndex.from_product([years, platforms], names=['Year', 'Platform'])
        experiment_counts = (experiment_counts
            .set_index(['Year', 'Platform'])
            .reindex(complete_index, fill_value=0)
            .reset_index())

        # Convert Year to string to treat it as a categorical variable
        experiment_counts['Year_str'] = experiment_counts['Year'].astype(str)
        experiment_counts = experiment_counts.sort_values(['Platform', 'Year'])

        return experiment_counts
        
    def create_plot(self):
        """Create the stacked column chart of yearly experiment counts by platform."""
        # Create traces manually for better control
        traces = []
        for platform in sorted(self.data['Platform'].unique()):
            platform_data = self.data[self.data['Platform'] == platform].sort_values('Year')
            trace = {
                'type': 'bar',
                'name': platform,
                'x': platform_data['Year_str'].tolist(),
                'y': platform_data['Count'].tolist(),
                'marker': {'color': self.PLATFORM_COLORS.get(platform)},
                'hovertemplate': '<b>%{x}</b><br>%{y} %{fullData.name} experiments<extra></extra>'
            }
            traces.append(trace)

        # Create layout with standardized settings
        layout = {
            'title': {
                'text': 'Yearly Experiment Counts by Platform',
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            'xaxis': {
                'title': 'Year',
                'tickangle': -45,
                **self.PLOTLY_LAYOUT_DEFAULTS['xaxis']
            },
            'yaxis': {
                'title': 'Number of Experiments',
                **self.PLOTLY_LAYOUT_DEFAULTS['yaxis']
            },
            'barmode': 'stack',
            'bargap': self.PLOTLY_LAYOUT_DEFAULTS['bargap'],
            'showlegend': True,
            'legend': {
                'title': {'text': 'Platform'},
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
        self.export_to_multiple(export_name="experiment_counts_yearly")
        
def main():
    """Main function to create and save the plot."""
    plot = ExperimentCountYearlyPlot()
    plot.create_plot()

if __name__ == "__main__":
    main()
