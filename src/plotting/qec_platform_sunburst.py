from .base import BasePlot
import json
from pathlib import Path
import plotly
import plotly.graph_objects as go
import pandas as pd
import os
from .export_utils import export_figure_to_pdf

class QECPlatformSunburst(BasePlot):
    """Creates a sunburst chart showing QEC code distribution across platforms."""
    
    def __init__(self, double_column=False):
        super().__init__(double_column)
        self.data = self.load_data(self.config['paths']['data']['qec'])
        
    def prepare_sunburst_data(self):
        """Prepare data for the sunburst chart."""
        # Count experiments by code name and platform
        code_platform_counts = self.data.groupby(['Code Name', 'Platform']).size().reset_index(name='count')
        
        # Calculate total count for each code
        code_counts = code_platform_counts.groupby('Code Name')['count'].sum().reset_index(name='code_total')
        
        # Calculate total count across all codes
        total_count = code_platform_counts['count'].sum()
        
        # Prepare data for the sunburst chart
        sunburst_data = []
        
        # Add root node
        sunburst_data.append({
            'id': 'All QEC Codes',
            'label': f'All QEC Codes ({total_count})',
            'parent': '',
            'value': total_count,
            'hover': f'<b>All QEC Codes</b><br>{total_count} experiments'
        })
        
        # Add code nodes
        for _, code_row in code_counts.iterrows():
            code_name = code_row['Code Name']
            code_total = code_row['code_total']
            code_percent = (code_total / total_count) * 100
            
            sunburst_data.append({
                'id': code_name,
                'label': f'{code_name} ({code_total})',
                'parent': 'All QEC Codes',
                'value': code_total,
                'hover': f'<b>{code_name}</b><br>{code_total} experiments<br>{code_percent:.1f}% of total'
            })
        
        # Add platform nodes
        for _, platform_row in code_platform_counts.iterrows():
            code_name = platform_row['Code Name']
            platform = platform_row['Platform']
            count = platform_row['count']
            
            # Get the total for this code
            code_total = code_counts[code_counts['Code Name'] == code_name]['code_total'].values[0]
            platform_percent = (count / code_total) * 100
            total_percent = (count / total_count) * 100
            
            # Get experiments for this code and platform
            experiments = self.data[(self.data['Code Name'] == code_name) & 
                                  (self.data['Platform'] == platform)]
            
            # Create hover text with experiment links
            experiment_links = '<br>'.join([f'• {row["Article Title"]} (<a href=\'{row["Link"]}\' target=\'_blank\'>link</a>)' 
                                          for _, row in experiments.iterrows()])
            
            hover_text = f'<b>{platform}</b> - {code_name}<br>{count} experiments<br>{platform_percent:.1f}% of {code_name}<br>{total_percent:.1f}% of total<br>{experiment_links}'
            
            sunburst_data.append({
                'id': f'{code_name}-{platform}',
                'label': f'{platform} ({count})',
                'parent': code_name,
                'value': count,
                'hover': hover_text
            })
        
        # Convert to DataFrame
        return pd.DataFrame(sunburst_data)
        
    def create_plot(self):
        """Create interactive sunburst chart of QEC implementations by platform."""
        # Prepare data
        plot_data = self.prepare_sunburst_data()
        
        # Create traces for the sunburst plot
        traces = []
        trace = {
            'type': 'sunburst',
            'ids': plot_data['id'].tolist(),
            'labels': plot_data['label'].tolist(),
            'parents': plot_data['parent'].tolist(),
            'values': plot_data['value'].tolist(),
            'customdata': plot_data['hover'].tolist(),
            'hovertemplate': '%{customdata}<extra></extra>',
            'branchvalues': 'total',  # This ensures correct proportions
            'insidetextorientation': 'radial',  # Change to radial for better visibility
            'textfont': {'size': 18},  # Increase text size
            'outsidetextfont': {'size': 16, 'color': '#333333'},  # Add outside text font
            'marker': {'line': {'width': 2, 'color': '#ffffff'}},  # Add borders for better visibility
            'leaf': {'opacity': 1},  # Make leaf nodes fully opaque
            'maxdepth': 3  # Increase depth to show all levels
        }
        traces.append(trace)
        
        # Create layout with standardized settings
        layout = {
            'title': {
                'text': 'Distribution of QEC Implementations Across Platforms',
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            'width': self.plot_settings['export']['width'],
            'height': self.plot_settings['export']['height'],
            'font': self.PLOTLY_LAYOUT_DEFAULTS['font'],
            'showlegend': False,  # Hide legend to give more space to the chart
            'plot_bgcolor': self.PLOTLY_LAYOUT_DEFAULTS['plot_bgcolor'],
            'paper_bgcolor': self.PLOTLY_LAYOUT_DEFAULTS['paper_bgcolor'],
            'margin': self.PLOTLY_LAYOUT_DEFAULTS['margin'],
            'hovermode': self.PLOTLY_LAYOUT_DEFAULTS['hovermode']
        }
        
        # Create a Plotly figure for export
        self.fig = go.Figure(data=traces, layout=layout)
        self.export_to_multiple(export_name="qec_platform_sunburst")
        
def main():
    """Main function to create and save the plot."""
    plot = QECPlatformSunburst()
    plot.create_plot()

if __name__ == "__main__":
    main()
