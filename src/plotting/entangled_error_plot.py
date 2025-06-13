from .base import BasePlot
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats

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

    def _calculate_fit(self, x, y):
        """Calculate linear fit in log space and return improvement rate."""
        if len(x) < 2 or len(y) < 2:  # Need at least 2 points for a fit
            return None, None, None
        
        # Convert to log space for fitting
        y_log = np.log10(y)
        
        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y_log)
        print(r_value)
        
        # Generate fit line points
        x_fit = np.array([min(x), max(x)])
        y_fit = 10**(slope * x_fit + intercept)
        
        # Calculate time to reduce error by factor of 10 (in years)
        # reduction_time = -1/slope if slope != 0 else float('inf')
        doubling_time = -np.log10(2) / slope if slope != 0 else float('inf')
        
        return x_fit, y_fit, doubling_time
        
    def create_plot(self):
        """Create the entangled state error evolution plot using Plotly."""
        # Create traces manually for better control
        traces = []
        for platform in sorted(self.data['Platform'].unique()):
            platform_data = self.data[self.data['Platform'] == platform].sort_values('Year')
            print(platform)
            
            # Data trace
            # Determine marker symbols based on 'Notes' column
            notes_list = platform_data['Notes'].fillna('').astype(str).tolist()
            marker_symbols = [
                'square' if 'gate' in note.lower() else 'circle' for note in notes_list
            ]
            trace = {
                'type': 'scatter',
                'x': platform_data['Year'].tolist(),
                'y': platform_data['Entangled State Error'].tolist(),
                'name': platform,
                # 'mode': 'lines+markers',
                'mode': 'markers',
                'line': {'color': self.PLATFORM_COLORS.get(platform), 'width': 3},
                'marker': {
                    'color': self.PLATFORM_COLORS.get(platform),
                    'size': 12,
                    'line': {'width': 2, 'color': 'white'},
                    'symbol': marker_symbols
                },
                'hovertemplate': "<b>%{text}</b><br>Error: %{y}<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
                'text': platform_data['Article Title'].tolist(),
                'customdata': platform_data['Link'].tolist()
            }
            traces.append(trace)
            
            # Calculate and add fit
            x_fit, y_fit, doubling_time = self._calculate_fit(
                platform_data['Year'].values,
                platform_data['Entangled State Error'].values
            )
            if x_fit is not None:
                trace_fit = {
                    'type': 'scatter',
                    'x': x_fit.tolist(),
                    'y': y_fit.tolist(),
                    'name': f'{platform} fit (×2 every {doubling_time:.1f}y)',
                    'mode': 'lines',
                    'line': {
                        'color': self.PLATFORM_COLORS.get(platform),
                        'width': 2,
                        'dash': 'dot'
                    },
                    'showlegend': True
                }
                traces.append(trace_fit)

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
