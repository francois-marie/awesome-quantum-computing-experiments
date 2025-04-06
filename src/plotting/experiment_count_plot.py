from .base import BasePlot
import json
from pathlib import Path
import plotly
import plotly.graph_objects as go
import pandas as pd
import os
from .export_utils import export_figure_to_pdf

class ExperimentCountPlot(BasePlot):
    """Creates a stacked column chart showing experiment counts over time by platform."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['qec'])
        
    def load_data(self, csv_path: str):
        """Load and preprocess experiment count data."""
        data = pd.read_csv(csv_path)
        # Count experiments per year and platform
        experiment_counts = data.groupby(['Year', 'Platform']).size().reset_index(name='Count')

        # Compute the minimum year
        min_year = experiment_counts['Year'].min()

        # Add initial rows for each platform at min(Year) - 1 with 0 count
        platforms = experiment_counts['Platform'].unique()
        initial_rows = pd.DataFrame({
            'Year': [min_year - 1] * len(platforms),
            'Platform': platforms,
            'Count': [0]*len(platforms)
        })
        experiment_counts = pd.concat([initial_rows, experiment_counts], ignore_index=True)

        # Sort the DataFrame by Year before calculating cumulative counts
        experiment_counts = experiment_counts.sort_values(by='Year')

        # Fill missing years with cumulative counts from the previous year
        for platform in platforms:
            for year in range(min_year, experiment_counts['Year'].max() + 1):
                if not ((experiment_counts['Year'] == year) & (experiment_counts['Platform'] == platform)).any():
                    new_row = pd.DataFrame({
                        'Year': [year],
                        'Platform': [platform],
                        'Count': [0],
                    })
                    experiment_counts = pd.concat([experiment_counts, new_row], ignore_index=True)
        
        # Sort again after adding new rows
        experiment_counts = experiment_counts.sort_values(by='Year')

        # Calculate cumulative counts
        experiment_counts['Cumulative_Count'] = experiment_counts.groupby('Platform')['Count'].cumsum()

        # Convert Year to string to treat it as a categorical variable
        experiment_counts['Year_str'] = experiment_counts['Year'].astype(str)
        experiment_counts.sort_values(by='Year_str', key=int())

        return experiment_counts
        
    def create_plot(self):
        """Create the stacked column chart of experiment counts by year and platform."""
        # Create traces manually for better control
        traces = []
        for platform in self.data['Platform'].unique():
            platform_data = self.data[self.data['Platform'] == platform].sort_values('Year')
            trace = {
                'type': 'bar',
                'name': platform,
                'x': platform_data['Year_str'].tolist(),
                'y': platform_data['Cumulative_Count'].tolist(),
                'marker': {'color': self.PLATFORM_COLORS.get(platform)},
                'hovertemplate': '<b>%{x}</b><br>%{y} %{fullData.name} experiments<extra></extra>'
            }
            traces.append(trace)

        # Create layout with standardized settings
        layout = {
            'title': {
                'text': 'Cumulative Experiment Counts by Platform',
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            'xaxis': {
                'title': 'Year',
                'tickangle': -45,
                **self.PLOTLY_LAYOUT_DEFAULTS['xaxis']
            },
            'yaxis': {
                'title': 'Cumulative Experiment Counts',
                **self.PLOTLY_LAYOUT_DEFAULTS['yaxis']
            },
            'barmode': 'relative',
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
        self.export_to_multiple(export_name="experiment_counts")

def main():
    """Main function to create and save the plot."""
    plot = ExperimentCountPlot()
    plot.create_plot()

if __name__ == "__main__":
    main()
