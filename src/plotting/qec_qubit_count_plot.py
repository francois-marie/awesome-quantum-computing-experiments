from .base import BasePlot
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats
import re

class QECQubitCountPlot(BasePlot):
    """Creates the QEC experiment qubit count evolution plot."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['qec'])
        
    def _extract_max_n(self, code_params):
        """Extract the maximum n value from code parameters string."""
        if pd.isna(code_params):
            return None
            
        # Pattern to match [n,k,d] or [[n,k,d]] format, possibly with spaces
        pattern = r'[\[]{1,2}(\d+),\s*\d+,\s*\d+[\]]{1,2}'
        matches = re.findall(pattern, str(code_params))
        
        if not matches:
            return None
            
        # Convert all matches to integers and take the maximum
        n_values = [int(n) for n in matches]
        return max(n_values)
        
    def load_data(self, csv_path: str):
        """Load and preprocess QEC experiment data."""
        data = super().load_data(csv_path)
        
        # Extract maximum n value from Code Parameters for each experiment
        data['Data Qubits'] = data['Code Parameters'].apply(self._extract_max_n)
        return data

    def _calculate_fit(self, x, y):
        """Calculate linear fit in log space and return growth rate."""
        if len(x) < 2 or len(y) < 2:  # Need at least 2 points for a fit
            return None, None, None
        
        # Convert to log space for fitting
        y_log = np.log10(y)
        
        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y_log)
        
        # Generate fit line points
        x_fit = np.array([min(x), max(x)])
        y_fit = 10**(slope * x_fit + intercept)
        
        # Calculate doubling time (in years)
        doubling_time = np.log10(2) / slope if slope != 0 else float('inf')
        
        return x_fit, y_fit, doubling_time
        
    def create_plot(self):
        """Create the QEC experiment qubit count evolution plot using Plotly."""
        # Create traces manually for better control
        traces = []
        
        # Group by platform and year, get the maximum qubit count for each group
        grouped_data = self.data.groupby(['Platform', 'Year'])['Data Qubits'].max().reset_index()
        
        for platform in sorted(grouped_data['Platform'].unique()):
            platform_data = grouped_data[grouped_data['Platform'] == platform].sort_values('Year')
            
            # Skip if no valid qubit counts
            if platform_data['Data Qubits'].isna().all():
                continue
                
            # Data trace
            trace = {
                'type': 'scatter',
                'x': platform_data['Year'].tolist(),
                'y': platform_data['Data Qubits'].tolist(),
                'name': platform,
                'mode': 'lines+markers',
                'line': {'color': self.PLATFORM_COLORS.get(platform), 'width': 3},
                'marker': {
                    'color': self.PLATFORM_COLORS.get(platform),
                    'size': 12,
                    'line': {'width': 2, 'color': 'white'}
                },
                'hovertemplate': "<b>%{y}</b> data qubits<br>Year: %{x}<br>Platform: " + platform + "<extra></extra>"
            }
            traces.append(trace)
            
            # Calculate and add fit if we have enough valid data points
            valid_data = platform_data.dropna(subset=['Data Qubits'])
            if len(valid_data) >= 2:
                x_fit, y_fit, doubling_time = self._calculate_fit(
                    valid_data['Year'].values,
                    valid_data['Data Qubits'].values
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
                'text': 'QEC Data Qubit Count Evolution',
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            'xaxis': {
                'title': {'text': 'Year'},
                **self.PLOTLY_LAYOUT_DEFAULTS['xaxis']
            },
            'yaxis': {
                'title': {'text': 'Number of Data Qubits'},
                'type': 'linear',
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
        self.export_to_multiple(export_name="qec_data_qubit_count_plot")

def main():
    """Main function to create and save the plot."""
    plot = QECQubitCountPlot()
    plot.create_plot()

if __name__ == "__main__":
    main() 