import json
import os
from .base import BasePlot
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats

class QubitCountPlot(BasePlot):
    """Creates the physical qubit count evolution plot."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['qubit_count'])
        self.fitting_stats = []
        
    def load_data(self, csv_path: str):
        """Load and preprocess qubit count data."""
        data = super().load_data(csv_path)
        data["Number of qubits"] = pd.to_numeric(
            data["Number of qubits"], errors="coerce"
        )
        return data

    def _calculate_fit(self, x, y, platform):
        """Calculate linear fit in log space and return growth rate."""
        if len(x) < 2 or len(y) < 2:  # Need at least 2 points for a fit
            return None, None, None
        
        # Convert to log space for fitting
        y_log = np.log10(y)
        
        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y_log)
        
        # Store fitting statistics
        self.fitting_stats.append({
            'metric': 'Physical Qubit Count',
            'platform': platform,
            'r_squared': r_value**2,
            'slope': slope,
            'std_err': std_err,
            'p_value': p_value,
            'doubling_time': np.log10(2) / slope if slope != 0 else float('inf')
        })
        
        # Generate fit line points
        x_fit = np.array([min(x), max(x)])
        y_fit = 10**(slope * x_fit + intercept)
        
        # Calculate doubling time (in years)
        doubling_time = np.log10(2) / slope if slope != 0 else float('inf')
        
        return x_fit, y_fit, doubling_time
        
    def create_plot(self):
        """Create the physical qubit count evolution plot using Plotly."""
        # Create traces manually for better control
        traces = []
        for platform in sorted(self.data['Platform'].unique()):
            platform_data = self.data[self.data['Platform'] == platform].sort_values('Year')
            
            # Data trace
            trace = {
                'type': 'scatter',
                'x': platform_data['Year'].tolist(),
                'y': platform_data['Number of qubits'].tolist(),
                'name': platform,
                # 'mode': 'lines+markers',
                'mode': 'markers',
                'line': {'color': self.PLATFORM_COLORS.get(platform), 'width': 3},
                'marker': {
                    'color': self.PLATFORM_COLORS.get(platform),
                    'size': 12,
                    'line': {'width': 2, 'color': 'white'}
                },
                'hovertemplate': "<b>%{text}</b><br>Qubits: %{y}<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
                'text': platform_data['Article Title'].tolist(),
                'customdata': platform_data['Link'].tolist()
            }
            traces.append(trace)
            
            # Calculate and add fit
            x_fit, y_fit, doubling_time = self._calculate_fit(
                platform_data['Year'].values,
                platform_data['Number of qubits'].values,
                platform
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

    def save_fitting_stats(self, output_dir: str):
        """Save fitting statistics to a JSON file."""
        if not self.fitting_stats:
            # print("No fitting statistics to save.")
            return
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save fitting statistics to file
        filename = os.path.join(output_dir, 'qubit_count_fitting_stats.json')
        with open(filename, 'w') as f:
            json.dump(self.fitting_stats, f)
        # print(f"Fitting statistics saved to {filename}")

def main():
    """Main function to create and save the plot."""
    plot = QubitCountPlot()
    plot.create_plot()
    plot.save_fitting_stats("out/fitting_stats")

if __name__ == "__main__":
    main() 