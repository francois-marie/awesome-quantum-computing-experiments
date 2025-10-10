import json
import os
import re
from .base import BasePlot
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class MSDPlot(BasePlot):
    """Creates the Magic State Distillation fidelity vs acceptance rate plot."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['msd'])
        
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
        
        # Convert acceptance rate to numeric
        data["Acceptance Rate (%)"] = pd.to_numeric(
            data["Acceptance Rate (%)"], errors="coerce"
        )
        
        # Filter out rows without both error and acceptance rate
        data = data.dropna(subset=['Error_Value', 'Acceptance Rate (%)'])
        
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

    def create_plot(self):
        """Create the MSD fidelity vs acceptance rate plot using Plotly."""
        traces = []
        
        # Calculate the minimum error for y-axis range
        min_error = self.data['Error_Value'].min()
        # Use a slightly lower value for better visualization
        y_min = max(0.0001, min_error * 0.5)  # Don't go below 0.0001 for log scale

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
        
        # Create legend entries for platforms (without showing data)
        platform_legend_rank = 1
        for platform in sorted(self.data['Platform'].unique()):
            normalized_platform = self._normalize_platform_name(platform)
            platform_color = self.PLATFORM_COLORS.get(normalized_platform, '#000000')
            
            platform_legend_trace = {
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
                'legendgroup': 'platform_legend',
                'legendrank': platform_legend_rank
            }
            traces.append(platform_legend_trace)
            platform_legend_rank += 1
        
        # Add legend section header for Magic State
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
        
        # Create legend entries for magic states
        magic_state_legend_rank = 101
        unique_magic_states = sorted([state for state in self.data['Magic State'].dropna().unique() if state.strip()])
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
        
        # Create actual data traces (without showing in legend)
        for platform in sorted(self.data['Platform'].unique()):
            platform_data = self.data[self.data['Platform'] == platform].sort_values('Year')
            # Normalize platform name to match color configuration
            normalized_platform = self._normalize_platform_name(platform)
            platform_color = self.PLATFORM_COLORS.get(normalized_platform, '#000000')  # Default to black if color not found
            
            if platform_data.empty:
                continue
            
            # Group by magic state to create separate traces with different markers
            for magic_state in platform_data['Magic State'].dropna().unique():
                if pd.isna(magic_state) or magic_state.strip() == '':
                    continue
                    
                state_data = platform_data[platform_data['Magic State'] == magic_state]
                marker_symbol = self._get_marker_symbol(magic_state)
                
                # Create main data trace for this magic state (don't show in legend)
                trace = {
                    'type': 'scatter',
                    'x': state_data['Acceptance Rate (%)'].tolist(),
                    'y': state_data['Error_Value'].tolist(),
                    'name': f'{platform} ({magic_state})',
                    'mode': 'markers',
                    'marker': {
                        'color': platform_color,
                        'symbol': marker_symbol,
                        'size': 12,
                        'line': {'width': 2, 'color': 'white'}
                    },
                    'hovertemplate': "<b>%{text}</b><br>Error: %{y:.4f}<br>Acceptance Rate: %{x}%<br>Magic State: %{customdata[0]}<br>QEC Code: %{customdata[1]}<br>Experiment Type: %{customdata[2]}<br>Year: %{customdata[3]}<br><a href='%{customdata[4]}' target='_blank'>Link</a><extra></extra>",
                    'text': state_data['Article Title'].tolist(),
                    'customdata': list(zip(
                        state_data['Magic State'].fillna('').tolist(),
                        state_data['QEC Code'].fillna('').tolist(),
                        state_data['Experiment Type'].fillna('').tolist(),
                        state_data['Year'].tolist(),
                        state_data['Link'].tolist()
                    )),
                    'showlegend': False,  # Don't show data traces in legend
                    'legendgroup': f'data_{platform}_{magic_state}'
                }
                traces.append(trace)
                
                # Add error bars if confidence intervals exist
                has_error_bars = (
                    state_data['Error_Lower'].notna().any() and 
                    state_data['Error_Upper'].notna().any()
                )
                
                if has_error_bars:
                    # Filter data with valid error bars
                    error_data = state_data[
                        state_data['Error_Lower'].notna() & 
                        state_data['Error_Upper'].notna()
                    ]
                    
                    if not error_data.empty:
                        error_trace = {
                            'type': 'scatter',
                            'x': error_data['Acceptance Rate (%)'].tolist(),
                            'y': error_data['Error_Value'].tolist(),
                            'error_y': {
                                'type': 'data',
                                'symmetric': False,
                                'array': (error_data['Error_Upper'] - error_data['Error_Value']).tolist(),
                                'arrayminus': (error_data['Error_Value'] - error_data['Error_Lower']).tolist(),
                                'color': platform_color,  # Use the same platform color for error bars
                                'thickness': 2,
                                'width': 4
                            },
                            'mode': 'markers',
                            'marker': {
                                'color': platform_color,  # Ensure marker color also matches
                                'opacity': 0
                            },
                            'showlegend': False,
                            'hoverinfo': 'skip'
                        }
                        traces.append(error_trace)

        # Create layout with standardized settings
        layout = {
            'title': {
                'text': 'Magic State Preparation: Error vs Acceptance Rate',
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            'xaxis': {
                'title': {'text': 'Acceptance Rate (%)'},
                'range': [0, 105],
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
        
        self.export_to_multiple(export_name="msd_plot")

def main():
    """Main function to create and save the plot."""
    plot = MSDPlot()
    plot.create_plot()

if __name__ == "__main__":
    main() 