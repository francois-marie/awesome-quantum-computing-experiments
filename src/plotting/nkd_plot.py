from .base import BasePlot
import plotly.graph_objects as go
import pandas as pd
import re
from typing import Tuple, List

class NKDPlot(BasePlot):
    """Creates the [n,k,d] parameter space plot."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['qec'])
        
    def parse_code_parameters(self, params: str) -> Tuple[List[int], List[int], List[int]]:
        """
        Parse code parameters from string format.
        
        Args:
            params: String containing code parameters in format like [[n,k,d]] or [n,k,d]
            
        Returns:
            Tuple of lists (n_values, k_values, d_values)
        """
        if pd.isna(params):
            return [], [], []
            
        # Initialize lists to store parsed values
        n_values, k_values, d_values = [], [], []
        
        # Split by comma outside brackets
        param_groups = re.findall(r'(\[+\d+,\d+,\d+\]+)', params)
        
        for param in param_groups:
            # Extract n, k, d values
            match = re.search(r'\[+(\d+),(\d+),(\d+)\]+', param)
            if match:
                n = int(match.group(1))
                k = int(match.group(2))
                d = int(match.group(3))
                
                # For single brackets [n,k,d], set d=1 (distance is 1)
                # For double brackets [[n,k,d]], use the provided d
                if param.count('[') == 1:
                    d = 1
                    
                n_values.append(n)
                k_values.append(k)
                d_values.append(d)
                
        return n_values, k_values, d_values
        
    def load_data(self, csv_path: str):
        """Load and preprocess QEC data for NKD analysis."""
        data = super().load_data(csv_path)
        
        # Filter out rows without code parameters
        data = data.dropna(subset=['Code Parameters'])
        
        # Parse code parameters
        parsed_params = data['Code Parameters'].apply(self.parse_code_parameters)
        
        # Create expanded DataFrame with one row per n,k,d triple
        expanded_data = []
        
        for idx, row in data.iterrows():
            n_values, k_values, d_values = parsed_params[idx]
            
            # Skip if no valid parameters
            if not n_values:
                continue
                
            for n, k, d in zip(n_values, k_values, d_values):
                new_row = row.copy()
                new_row['n'] = n
                new_row['k'] = k
                new_row['d'] = d
                expanded_data.append(new_row)
                
        if expanded_data:
            return pd.DataFrame(expanded_data)
        else:
            return pd.DataFrame(columns=data.columns.tolist() + ['n', 'k', 'd'])
        
    def create_plot(self):
        """Create the NKD parameter space plot using Plotly."""
        # Get unique codes for marker mapping
        unique_codes = sorted(self.data['Code Name'].unique())
        markers = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down', 'star', 'hexagon']
        code_to_marker = {code: markers[i % len(markers)] for i, code in enumerate(unique_codes)}
        
        # Get unique k values for color mapping
        unique_k = sorted(self.data['k'].unique())
        k_to_color = {k: list(self.CODE_COLORS.values())[i % len(self.CODE_COLORS)] for i, k in enumerate(unique_k)}
        
        # Create traces manually for better control
        traces = []
        for code in unique_codes:
            code_data = self.data[self.data['Code Name'] == code]
            
            for k_val in unique_k:
                k_data = code_data[code_data['k'] == k_val]
                
                if not k_data.empty:
                    # Create hover text with article title, platform, code, etc.
                    hover_text = k_data.apply(
                        lambda row: f"<b>{row['Article Title']}</b><br>" +
                                  f"Platform: {row['Platform']}<br>" +
                                  f"Code: {row['Code Name']}<br>" +
                                  f"Parameters: {row['Code Parameters']}<br>" +
                                  f"n={row['n']}, k={row['k']}, d={row['d']}<br>" +
                                  f"Year: {row['Year']}", 
                        axis=1
                    ).tolist()
                    
                    trace = {
                        'type': 'scatter',
                        'x': k_data['n'].tolist(),
                        'y': k_data['d'].tolist(),
                        'mode': 'markers',
                        'name': f"{code} (k={k_val})",
                        'marker': {
                            'symbol': code_to_marker[code],
                            'color': k_to_color[k_val],
                            'size': 12,
                            'line': {'width': 2, 'color': 'grey'},
                            'opacity': 0.8
                        },
                        'hovertemplate': '%{customdata}<extra></extra>',
                        'customdata': hover_text
                    }
                    traces.append(trace)
        
        # Create layout with standardized settings
        layout = {
            'title': {
                'text': 'Quantum Error Correction Code Parameters',
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            'xaxis': {
                'title': {'text': 'Number of Physical Qubits (n)'},
                'type': 'linear',
                **self.PLOTLY_LAYOUT_DEFAULTS['xaxis']
            },
            'yaxis': {
                'title': {'text': 'Distance (d)'},
                'type': 'linear',
                **self.PLOTLY_LAYOUT_DEFAULTS['yaxis']
            },
            'showlegend': True,
            'legend': {
                'title': {'text': 'Code Parameters'},
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
        
        # Export to multiple formats
        self.export_to_multiple(export_name="nkd_plot")

def main():
    """Main function to create and save the plot."""
    plot = NKDPlot()
    plot.create_plot()

if __name__ == "__main__":
    main()