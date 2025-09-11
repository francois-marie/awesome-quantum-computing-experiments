import json
import os
from .base import BasePlot
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats

class MSDErrorEvolutionPlot(BasePlot):
    """Creates the Magic State error evolution over time plot."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['msd'])
        self.fitting_stats = []
        
    def load_data(self, csv_path: str):
        """Load and preprocess MSD data."""
        data = super().load_data(csv_path)
        
        # Parse fidelity values with confidence intervals
        data['Fidelity_Value'] = data['Fidelity'].apply(self._parse_fidelity)
        data['Fidelity_Lower'] = data['Fidelity'].apply(self._parse_fidelity_lower)
        data['Fidelity_Upper'] = data['Fidelity'].apply(self._parse_fidelity_upper)
        
        # Calculate error = 1 - fidelity
        data['Error_Value'] = 1 - data['Fidelity_Value']
        data['Error_Lower'] = 1 - data['Fidelity_Upper']  # Note: Upper fidelity becomes lower error
        data['Error_Upper'] = 1 - data['Fidelity_Lower']  # Note: Lower fidelity becomes upper error
        
        # Convert year to numeric
        data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
        
        # Filter out rows without both error and year
        data = data.dropna(subset=['Error_Value', 'Year'])
        
        return data

    def _parse_fidelity(self, fidelity_str):
        """Extract the main fidelity value from strings like '0.996-6+3'."""
        if pd.isna(fidelity_str) or fidelity_str == '':
            return None
        
        # Handle various fidelity formats
        fidelity_str = str(fidelity_str).strip()
        
        # Pattern for formats like "0.996-6+3" or "0.996"
        if '-' in fidelity_str and '+' in fidelity_str:
            return float(fidelity_str.split('-')[0])
        else:
            try:
                return float(fidelity_str)
            except ValueError:
                return None

    def _parse_fidelity_lower(self, fidelity_str):
        """Extract the lower bound from fidelity confidence intervals."""
        if pd.isna(fidelity_str) or fidelity_str == '':
            return None
            
        fidelity_str = str(fidelity_str).strip()
        
        if '-' in fidelity_str and '+' in fidelity_str:
            parts = fidelity_str.split('-')
            if len(parts) >= 2:
                base_value = float(parts[0])
                error_part = parts[1].split('+')[0]
                # Handle different decimal place errors (e.g., "-6" means -0.006 for 0.996)
                error_magnitude = len(str(base_value).split('.')[-1])
                error_value = float(error_part) / (10 ** error_magnitude)
                return base_value - error_value
        
        # If no confidence interval, return the base value
        try:
            return float(fidelity_str)
        except ValueError:
            return None

    def _parse_fidelity_upper(self, fidelity_str):
        """Extract the upper bound from fidelity confidence intervals."""
        if pd.isna(fidelity_str) or fidelity_str == '':
            return None
            
        fidelity_str = str(fidelity_str).strip()
        
        if '-' in fidelity_str and '+' in fidelity_str:
            parts = fidelity_str.split('+')
            if len(parts) >= 2:
                base_part = fidelity_str.split('-')[0]
                base_value = float(base_part)
                error_value_str = parts[1]
                # Handle different decimal place errors
                error_magnitude = len(str(base_value).split('.')[-1])
                error_value = float(error_value_str) / (10 ** error_magnitude)
                return base_value + error_value
        
        # If no confidence interval, return the base value
        try:
            return float(fidelity_str)
        except ValueError:
            return None

    def _normalize_platform_name(self, platform_name):
        """Normalize platform names to match color configuration keys."""
        platform_mapping = {
            'Trapped-ion': 'Ion traps',
            'Superconducting qubits': 'Superconducting circuits',
            'Neutral atoms': 'Neutral atoms',
            'Ion traps': 'Ion traps',
            'Superconducting circuits': 'Superconducting circuits'
        }
        return platform_mapping.get(platform_name, platform_name)

    def _clean_magic_state_name(self, magic_state):
        """Clean magic state name by removing | and > characters."""
        if pd.isna(magic_state):
            return magic_state
        return str(magic_state).replace('|', '').replace('>', '')

    def _get_marker_symbol(self, magic_state):
        """Get marker symbol based on magic state."""
        # Clean the magic state name for consistent mapping
        clean_state = self._clean_magic_state_name(magic_state)
        magic_state_markers = {
            'H': 'circle',
            'T': 'square', 
            'M': 'diamond',
            'CZ': 'triangle-up'
        }
        return magic_state_markers.get(clean_state, 'circle')

    def _calculate_fit(self, x, y, platform):
        """Calculate linear fit in log space and return improvement rate."""
        if len(x) < 2 or len(y) < 2:  # Need at least 2 points for a fit
            return None, None, None
        
        # Convert to log space for fitting
        y_log = np.log10(y)
        
        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y_log)
        
        # Store fitting statistics
        self.fitting_stats.append({
            'metric': 'Magic State Error',
            'platform': platform,
            'r_squared': r_value**2,
            'slope': slope,
            'std_err': std_err,
            'p_value': p_value,
            'halving_time': -np.log10(2) / slope if slope != 0 else float('inf')
        })
        
        # Generate fit line points
        x_fit = np.array([min(x), max(x)])
        y_fit = 10**(slope * x_fit + intercept)
        
        # Calculate halving time (in years)
        halving_time = -np.log10(2) / slope if slope != 0 else float('inf')
        
        return x_fit, y_fit, halving_time

    def create_plot(self):
        """Create the Magic State error evolution plot using Plotly."""
        traces = []
        
        # Add legend section header for Platform
        traces.append({
            'type': 'scatter',
            'x': [None],
            'y': [None],
            'name': '𝐏𝐥𝐚𝐭𝐟𝐨𝐫𝐦',
            'mode': 'markers',
            'marker': {
                'color': 'rgba(0,0,0,0)',
                'size': 0,
                'symbol': 'circle'
            },
            'showlegend': True,
            'legendgroup': 'header_platform',
            'legendrank': 0
        })
        
        # Create data traces and fits for each platform
        platform_legend_rank = 1
        for i, platform in enumerate(sorted(self.data['Platform'].unique())):
            platform_data = self.data[self.data['Platform'] == platform].sort_values('Year')
            # Normalize platform name to match color configuration
            normalized_platform = self._normalize_platform_name(platform)
            platform_color = self.PLATFORM_COLORS.get(normalized_platform, '#000000')
            
            if platform_data.empty:
                continue
            
            # Determine marker symbols based on magic states
            magic_states = platform_data['Magic State'].fillna('').astype(str).tolist()
            marker_symbols = [self._get_marker_symbol(state) for state in magic_states]
            
            # Data trace
            trace = {
                'type': 'scatter',
                'x': platform_data['Year'].tolist(),
                'y': platform_data['Error_Value'].tolist(),
                'name': platform,
                'mode': 'markers',
                'marker': {
                    'color': platform_color,
                    'size': 12,
                    'line': {'width': 2, 'color': 'white'},
                    'symbol': marker_symbols
                },
                'hovertemplate': "<b>%{text}</b><br>Error: %{y:.4f}<br>Year: %{x}<br>Magic State: %{customdata[0]}<br>QEC Code: %{customdata[1]}<br>Experiment Type: %{customdata[2]}<br>Acceptance Rate: %{customdata[3]}%<br><a href='%{customdata[4]}' target='_blank'>Link</a><extra></extra>",
                'text': platform_data['Article Title'].tolist(),
                'customdata': list(zip(
                    platform_data['Magic State'].fillna('').tolist(),
                    platform_data['QEC Code'].fillna('').tolist(),
                    platform_data['Experiment Type'].fillna('').tolist(),
                    platform_data['Acceptance Rate (%)'].fillna('').tolist(),
                    platform_data['Link'].tolist()
                )),
                'legendgroup': platform,
                'showlegend': False
            }
            
            # Add error bars if confidence intervals exist
            has_error_bars = (
                platform_data['Error_Lower'].notna().any() and 
                platform_data['Error_Upper'].notna().any()
            )
            
            if has_error_bars:
                # Filter data with valid error bars
                error_data = platform_data[
                    platform_data['Error_Lower'].notna() & 
                    platform_data['Error_Upper'].notna()
                ]
                
                if not error_data.empty:
                    trace['error_y'] = {
                        'type': 'data',
                        'symmetric': False,
                        'array': (error_data['Error_Upper'] - error_data['Error_Value']).tolist(),
                        'arrayminus': (error_data['Error_Value'] - error_data['Error_Lower']).tolist(),
                        'color': platform_color,
                        'thickness': 2,
                        'width': 4
                    }
            
            # Platform legend trace
            legend_trace = {
                'type': 'scatter',
                'x': [None],
                'y': [None],
                'name': platform,
                'mode': 'markers',
                'marker': {
                    'color': platform_color,
                    'size': 12,
                    'line': {'width': 2, 'color': 'white'},
                    'symbol': 'circle'
                },
                'showlegend': True,
                'legendgroup': platform,
                'legendrank': platform_legend_rank
            }
            traces.append(trace)
            traces.append(legend_trace)
            platform_legend_rank += 1
            
            # Calculate and add fit if enough points
            if len(platform_data) >= 2:
                x_fit, y_fit, halving_time = self._calculate_fit(
                    platform_data['Year'].values,
                    platform_data['Error_Value'].values,
                    platform
                )
                if x_fit is not None:
                    trace_fit = {
                        'type': 'scatter',
                        'x': x_fit.tolist(),
                        'y': y_fit.tolist(),
                        'name': f'{platform} fit (÷2 every {halving_time:.1f}y)',
                        'mode': 'lines',
                        'line': {
                            'color': platform_color,
                            'width': 2,
                            'dash': 'dot'
                        },
                        'showlegend': True,
                        'legendrank': platform_legend_rank
                    }
                    traces.append(trace_fit)
                    platform_legend_rank += 1

        # Add legend section for magic state markers
        traces.append({
            'type': 'scatter',
            'x': [None],
            'y': [None],
            'name': '𝐌𝐚𝐠𝐢𝐜 𝐒𝐭𝐚𝐭𝐞',
            'mode': 'markers',
            'marker': {
                'color': 'rgba(0,0,0,0)',
                'size': 0,
                'symbol': 'circle'
            },
            'showlegend': True,
            'legendgroup': 'header_magic_state',
            'legendrank': 100
        })
        
        # Add magic state legend entries
        magic_state_legend_rank = 101
        unique_magic_states = sorted([state for state in self.data['Magic State'].dropna().unique() if str(state).strip()])
        for magic_state in unique_magic_states:
            clean_magic_state = self._clean_magic_state_name(magic_state)
            marker_symbol = self._get_marker_symbol(magic_state)
            
            magic_state_legend_trace = {
                'type': 'scatter',
                'x': [None],
                'y': [None],
                'name': clean_magic_state,
                'mode': 'markers',
                'marker': {
                    'color': 'gray',
                    'size': 12,
                    'symbol': marker_symbol,
                    'line': {'width': 2, 'color': 'white'}
                },
                'showlegend': True,
                'legendgroup': 'magic_state_legend',
                'legendrank': magic_state_legend_rank
            }
            traces.append(magic_state_legend_trace)
            magic_state_legend_rank += 1

        # Create layout with standardized settings
        layout = {
            'title': {
                'text': 'Magic State Error Evolution Over Time',
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            'xaxis': {
                'title': {'text': 'Year'},
                **self.PLOTLY_LAYOUT_DEFAULTS['xaxis']
            },
            'yaxis': {
                'title': {
                    'text': 'Error (1 - Fidelity)',
                    'font': self.PLOTLY_LAYOUT_DEFAULTS['font']
                },
                'type': 'log',
                'dtick': 'D1',  # Force log scale ticks
                'showgrid': True,
                'gridcolor': '#E5E5E5',
                'showline': True,
                'linecolor': '#2F3136',
                'tickfont': self.PLOTLY_LAYOUT_DEFAULTS['font']
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
        
        self.export_to_multiple(export_name="msd_error_evolution_plot")

    def save_fitting_stats(self, output_dir: str):
        """Save fitting statistics to a JSON file."""
        if not self.fitting_stats:
            return
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save fitting statistics to file
        filename = os.path.join(output_dir, 'msd_error_evolution_fitting_stats.json')
        with open(filename, 'w') as f:
            json.dump(self.fitting_stats, f)

def main():
    """Main function to create and save the plot."""
    plot = MSDErrorEvolutionPlot()
    plot.create_plot()
    plot.save_fitting_stats("out/fitting_stats")

if __name__ == "__main__":
    main() 