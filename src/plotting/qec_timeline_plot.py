from .base import BasePlot
import plotly.express as px
import plotly.utils
import json
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import numpy as np

class QECTimelineScatterPlot(BasePlot):
    """Creates a scatter plot showing aggregated QEC implementations over time."""
    
    def __init__(self, double_column=False):
        super().__init__(double_column)
        self.data = self.load_data(self.config['paths']['data']['qec'])
        
    def create_plot(self):
        """Create an interactive scatter plot of aggregated QEC implementations."""
        self.data = self.data.copy()
        self.data['Year'] = pd.to_numeric(self.data['Year'], errors='coerce')
        self.data['Year_str'] = self.data['Year'].astype(str)

        # Aggregate data. The erroneous indexer has been removed here.
        agg_data = self.data.groupby(['Platform', 'Year_str', 'Code Name']).size().reset_index(name='Count')

        # Create custom hover text for the aggregated data points
        agg_data['hover_text'] = agg_data.apply(
            lambda row: f"<b>Platform: {row['Platform']}</b><br>" +
                      f"Year: {row['Year_str']}<br>" +
                      f"Experiments: {row['Count']}",
            axis=1
        )

        # Convert categorical Code Name to numeric for jitter
        unique_codes = sorted(agg_data['Code Name'].unique())
        code_to_numeric = {code: i for i, code in enumerate(unique_codes)}
        agg_data['Code_Numeric'] = agg_data['Code Name'].map(code_to_numeric)
        
        # Get unique platforms and create platform-specific jitter
        platforms = sorted(agg_data['Platform'].unique())
        n_platforms = len(platforms)
        # Create evenly spaced jitter values between -0.3 and 0.3
        platform_jitter = {platform: -0.3 + i * (0.6 / (n_platforms - 1)) if n_platforms > 1 else 0 
                         for i, platform in enumerate(platforms)}
        
        # Apply platform-specific jitter
        agg_data['Code_Numeric_Jittered'] = agg_data.apply(
            lambda row: row['Code_Numeric'] + platform_jitter[row['Platform']], 
            axis=1
        )

        # Create scatter plot using graph_objects for better control
        fig = go.Figure()
        
        # Get unique platforms for traces
        platforms = agg_data['Platform'].unique()
        
        for platform in platforms:
            platform_data = agg_data[agg_data['Platform'] == platform]
            
            fig.add_trace(go.Scatter(
                x=platform_data['Year_str'],
                y=platform_data['Code_Numeric_Jittered'],
                mode='markers',
                name=platform,
                marker=dict(
                    size=np.sqrt(platform_data['Count']) * 20,  # Scale sqrt of count for area proportionality
                    color=self.PLATFORM_COLORS.get(platform, '#636EFA'),
                    line=dict(width=1.5, color='white'),
                    opacity=0.8
                ),
                customdata=platform_data['hover_text'],
                hovertemplate="%{customdata}<extra></extra>"
            ))

        # Apply standardized layout settings
        fig.update_layout(
            title={
                'text': "Aggregated Timeline of Quantum Error Correction Implementations",
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            showlegend=True,
            legend={
                'title': {'text': 'Quantum Platform'},
                'itemsizing': 'constant',
                **{k: v for k, v in self.PLOTLY_LAYOUT_DEFAULTS['legend'].items() if k not in ['title']}
            },
            hovermode=self.PLOTLY_LAYOUT_DEFAULTS['hovermode'],
            font=self.PLOTLY_LAYOUT_DEFAULTS['font'],
            plot_bgcolor=self.PLOTLY_LAYOUT_DEFAULTS['plot_bgcolor'],
            paper_bgcolor=self.PLOTLY_LAYOUT_DEFAULTS['paper_bgcolor'],
            margin=self.PLOTLY_LAYOUT_DEFAULTS['margin'],
            xaxis=dict(
                title={"text": "Publication Year"},
                type='category',
                categoryorder='array',
                categoryarray=sorted(agg_data['Year_str'].unique()),
                **{k: v for k, v in self.PLOTLY_LAYOUT_DEFAULTS['xaxis'].items() if k not in ['title', 'type']}
            ),
            yaxis=dict(
                title={"text": "QEC Code Type"},
                tickmode='array',
                tickvals=list(range(len(unique_codes))),
                ticktext=unique_codes,
                **{k: v for k, v in self.PLOTLY_LAYOUT_DEFAULTS['yaxis'].items() if k not in ['title', 'type']}
            ),
            height=self.plot_settings['export']['height'],
            width=self.plot_settings['export']['width']
        )
        
        self.fig = fig
        self.agg_data = agg_data  # Store for size reference
        
        # Add size reference legend
        self.add_size_reference()
        
        self.export_to_multiple(export_name="qec_timeline_aggregated", element_id="qec-timeline-aggregated-scatter")

    def add_size_reference(self):
        """Add a size reference to show marker size vs experiment count."""
        # Get the range of counts to create meaningful reference sizes
        if self.agg_data.empty:
            return
            
        min_count = self.agg_data['Count'].min()
        max_count = self.agg_data['Count'].max()
        
        # Create reference points (1, 5, 10, or based on data range)
        if max_count <= 5:
            ref_counts = [1, max_count] if max_count > 1 else [1]
        elif max_count <= 10:
            ref_counts = [1, 5, max_count] if max_count > 5 else [1, max_count]
        else:
            ref_counts = [1, 5, 10, max_count]
        
        # Remove duplicates and sort
        ref_counts = sorted(list(set(ref_counts)))
        
        # Calculate positions for the size reference (bottom-left corner)
        unique_codes = sorted(self.agg_data['Code Name'].unique())
        y_range = len(unique_codes) - 1
        
        # Position reference in bottom-left area
        ref_x_pos = 0.15  # Position as fraction of plot width
        ref_y_start = 0.5  # Start from bottom
        
        # Add reference markers and labels
        for i, count in enumerate(ref_counts):
            y_pos = ref_y_start + i * 0.15  # Reduced from 0.4 to 0.25 for tighter spacing
            marker_size = np.sqrt(count) * 20  # Match the main plot's sqrt scaling
            
            # Add invisible scatter point for the reference marker
            self.fig.add_trace(go.Scatter(
                x=[ref_x_pos],
                y=[y_pos],
                mode='markers',
                marker=dict(
                    size=marker_size,
                    color='gray',
                    opacity=0.7,
                    line=dict(width=1.5, color='white')
                ),
                showlegend=False,
                hoverinfo='skip',
                xaxis='x2',
                yaxis='y2'
            ))
            
            # Add text label
            self.fig.add_annotation(
                x=ref_x_pos + 0.08,
                y=y_pos,
                text=f"{count} exp{'s' if count > 1 else ''}",
                showarrow=False,
                font=dict(size=10, color='black'),
                xanchor='left',
                yanchor='middle',
                xref='x2',
                yref='y2'
            )
        
        # Add title for the size reference
        self.fig.add_annotation(
            x=ref_x_pos,
            y=ref_y_start - 0.15,  # Reduced from -0.3 to -0.15 for tighter spacing
            text="<b>Marker Size</b>",
            showarrow=False,
            font=dict(size=11, color='black'),
            xanchor='center',
            yanchor='top',
            xref='x2',
            yref='y2'
        )
        
        # Add secondary axes for the size reference (invisible)
        self.fig.update_layout(
            xaxis2=dict(
                overlaying='x',
                side='top',
                range=[0, 1],
                showgrid=False,
                showticklabels=False,
                showline=False,
                zeroline=False
            ),
            yaxis2=dict(
                overlaying='y',
                side='right',
                range=[0, max(3, len(ref_counts))],  # Ensure enough space for all markers
                showgrid=False,
                showticklabels=False,
                showline=False,
                zeroline=False
            )
        )

def main():
    """Main function to create and save the plot."""
    plot = QECTimelineScatterPlot()
    plot.create_plot()

if __name__ == "__main__":
    main()
