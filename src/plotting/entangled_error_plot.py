from .base import BasePlot
import plotly.graph_objects as go
import pandas as pd

class EntangledErrorPlot(BasePlot):
    """Creates the entangled state error evolution plot."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['entangled'])
        
    def load_data(self, csv_path: str):
        """Load and preprocess entangled error data."""
        data = super().load_data(csv_path)
        data["Entangled State Error"] = pd.to_numeric(
            data["Entangled State Error"], errors="coerce"
        )
        return data
        
    def create_plot(self):
        """Create the entangled state error evolution plot using Plotly."""
        # Create traces manually for better control
        traces = []
        for platform in sorted(self.data['Platform'].unique()):
            platform_data = self.data[self.data['Platform'] == platform].sort_values('Year')
            trace = {
                'type': 'scatter',
                'x': platform_data['Year'].tolist(),
                'y': platform_data['Entangled State Error'].tolist(),
                'name': platform,
                'mode': 'lines+markers',
                'line': {'color': self.PLATFORM_COLORS.get(platform), 'width': 3},
                'marker': {
                    'color': self.PLATFORM_COLORS.get(platform),
                    'size': 12,
                    'line': {'width': 2, 'color': 'white'}
                },
                'hovertemplate': "<b>%{text}</b><br>Error: %{y}<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
                'text': platform_data['Article Title'].tolist(),
                'customdata': platform_data['Link'].tolist()
            }
            traces.append(trace)

        # Create layout with standardized settings
        layout = {
            'title': {
                'text': 'Entangled State Error vs. Year',
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            'xaxis': {
                'title': {'text': 'Year'},
                **self.PLOTLY_LAYOUT_DEFAULTS['xaxis']
            },
            'yaxis': {
                'title': {'text': 'Entangled State Error'},
                'type': 'log',
                **self.PLOTLY_LAYOUT_DEFAULTS['yaxis']
            },
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
        self.export_to_multiple(export_name="entangled_error_plot")

def main():
    """Main function to create and save the plot."""
    plot = EntangledErrorPlot()
    plot.create_plot()

if __name__ == "__main__":
    main()
