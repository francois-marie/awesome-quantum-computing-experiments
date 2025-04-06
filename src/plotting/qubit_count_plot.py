from .base import BasePlot
import plotly.graph_objects as go
import pandas as pd

class QubitCountPlot(BasePlot):
    """Creates the physical qubit count evolution plot."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['qubit_count'])
        
    def load_data(self, csv_path: str):
        """Load and preprocess qubit count data."""
        data = super().load_data(csv_path)
        data["Number of qubits"] = pd.to_numeric(
            data["Number of qubits"], errors="coerce"
        )
        return data
        
    def create_plot(self):
        """Create the physical qubit count evolution plot using Plotly."""
        # Create traces manually for better control
        traces = []
        for platform in sorted(self.data['Platform'].unique()):
            platform_data = self.data[self.data['Platform'] == platform].sort_values('Year')
            trace = {
                'type': 'scatter',
                'x': platform_data['Year'].tolist(),
                'y': platform_data['Number of qubits'].tolist(),
                'name': platform,
                'mode': 'lines+markers',
                'line': {'color': self.PLATFORM_COLORS.get(platform), 'width': 3},  # Thicker lines
                'marker': {
                    'color': self.PLATFORM_COLORS.get(platform),
                    'size': 12,  # Larger markers
                    'line': {'width': 2, 'color': 'white'}  # Add white border
                },
                'hovertemplate': "<b>%{text}</b><br>Qubits: %{y}<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
                'text': platform_data['Article Title'].tolist(),
                'customdata': platform_data['Link'].tolist()
            }
            traces.append(trace)

        # Create layout with standardized settings
        layout = {
            'title': {
                'text': 'Physical Qubit Count Evolution',
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            'xaxis': {
                'title': {'text': 'Year'},
                **self.PLOTLY_LAYOUT_DEFAULTS['xaxis']
            },
            'yaxis': {
                'title': {'text': 'Physical Qubit Count'},
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
            'width': self.plot_settings['export']['width'],
            'height': self.plot_settings['export']['height']
        }
        
        # Create a Plotly figure for export
        self.fig = go.Figure(data=traces, layout=layout)
        self.export_to_multiple(export_name="qubit_count_plot")

def main():
    """Main function to create and save the plot."""
    plot = QubitCountPlot()
    plot.create_plot()

if __name__ == "__main__":
    main() 