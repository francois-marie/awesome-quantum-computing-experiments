from .base import BasePlot
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats

class CoherenceTimesPlot(BasePlot):
    """Creates the physical qubit coherence times plot."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['physical_qubits'])
        
    def load_data(self, csv_path: str):
        """Load and preprocess coherence times data."""
        data = super().load_data(csv_path)
        # Convert T1 and T2 to numeric, handling any non-numeric values
        data["T1"] = pd.to_numeric(data["T1"], errors="coerce")
        data["T2"] = pd.to_numeric(data["T2"], errors="coerce")
        return data

    def _calculate_fit(self, x, y):
        """Calculate linear fit in log space and return slope."""
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
        """Create the physical qubit coherence times plot using Plotly."""
        # Create traces manually for better control
        traces = []
        for platform in sorted(self.data['Platform'].unique()):
            platform_data = self.data[self.data['Platform'] == platform].sort_values('Year')
            platform_color = self.PLATFORM_COLORS.get(platform)
            
            # Add T1 trace and fit
            t1_data = platform_data[platform_data['T1'].notna()]
            if not t1_data.empty:
                # Data trace
                trace_t1 = {
                    'type': 'scatter',
                    'x': t1_data['Year'].tolist(),
                    'y': t1_data['T1'].tolist(),
                    'name': f'{platform} (T1)',
                    'mode': 'lines+markers',
                    'line': {'color': platform_color, 'width': 3},
                    'marker': {
                        'color': platform_color, 
                        'symbol': 'circle',
                        'size': 12,
                        'line': {'width': 2, 'color': 'white'}
                    },
                    'hovertemplate': "<b>%{text}</b><br>T1: %{y} s<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
                    'text': t1_data['Article Title'].tolist(),
                    'customdata': t1_data['Link'].tolist()
                }
                traces.append(trace_t1)
                
                # Calculate and add fit
                x_fit, y_fit, doubling_time = self._calculate_fit(
                    t1_data['Year'].values,
                    t1_data['T1'].values
                )
                if x_fit is not None:
                    trace_t1_fit = {
                        'type': 'scatter',
                        'x': x_fit.tolist(),
                        'y': y_fit.tolist(),
                        'name': f'{platform} T1 fit (×2 every {doubling_time:.1f}y)',
                        'mode': 'lines',
                        'line': {'color': platform_color, 'width': 2, 'dash': 'dot'},
                        'showlegend': True
                    }
                    traces.append(trace_t1_fit)
            
            # Add T2 trace and fit
            t2_data = platform_data[platform_data['T2'].notna()]
            if not t2_data.empty:
                # Data trace
                trace_t2 = {
                    'type': 'scatter',
                    'x': t2_data['Year'].tolist(),
                    'y': t2_data['T2'].tolist(),
                    'name': f'{platform} (T2)',
                    'mode': 'lines+markers',
                    'line': {'color': platform_color, 'dash': 'dash', 'width': 3},
                    'marker': {
                        'color': platform_color, 
                        'symbol': 'circle-open',
                        'size': 12,
                        'line': {'width': 2, 'color': platform_color}
                    },
                    'hovertemplate': "<b>%{text}</b><br>T2: %{y} s<br>Year: %{x}<br><a href='%{customdata}' target='_blank'>Link</a><extra></extra>",
                    'text': t2_data['Article Title'].tolist(),
                    'customdata': t2_data['Link'].tolist()
                }
                traces.append(trace_t2)
                
                # Calculate and add fit
                x_fit, y_fit, doubling_time = self._calculate_fit(
                    t2_data['Year'].values,
                    t2_data['T2'].values
                )
                if x_fit is not None:
                    trace_t2_fit = {
                        'type': 'scatter',
                        'x': x_fit.tolist(),
                        'y': y_fit.tolist(),
                        'name': f'{platform} T2 fit (×2 every {doubling_time:.1f}y)',
                        'mode': 'lines',
                        'line': {'color': platform_color, 'width': 2, 'dash': 'dashdot'},
                        'showlegend': True
                    }
                    traces.append(trace_t2_fit)

        # Create layout with standardized settings
        layout = {
            'title': {
                'text': 'Physical Qubit Coherence Times Evolution',
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            'xaxis': {
                'title': {'text': 'Year'},
                **self.PLOTLY_LAYOUT_DEFAULTS['xaxis']
            },
            'yaxis': {
                'title': {'text': 'Coherence Time (s)'},
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
        self.export_to_multiple(export_name="coherence_times_plot")


def main():
    """Main function to create and save the plot."""
    plot = CoherenceTimesPlot()
    plot.create_plot()

if __name__ == "__main__":
    main() 