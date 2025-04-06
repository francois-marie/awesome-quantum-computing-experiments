from .base import BasePlot
import plotly.express as px
import plotly.utils
import json
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

class QECTimelineScatterPlot(BasePlot):
    """Creates a scatter plot showing QEC code evolution over time."""
    
    def __init__(self, double_column=False):
        super().__init__(double_column)
        self.data = self.load_data(self.config['paths']['data']['qec'])
        
    def create_plot(self):
        """Create interactive scatter plot of QEC implementations over time."""
        self.data = self.data.copy()  # Create a copy to avoid modifying original
        self.data['Year'] = pd.to_numeric(self.data['Year'], errors='coerce')
        
        # Convert Year to string to treat it as a categorical variable
        self.data['Year_str'] = self.data['Year'].astype(str)
        
        # Create custom hover text
        self.data['hover_text'] = self.data.apply(
            lambda row: f"<b>{row['Article Title']}</b><br>{row['Link']}<br>" + 
                      f"Platform: {row['Platform']}<br>" +
                      f"Code: {row['Code Name']}<br>" +
                      f"Year: {row['Year']}", 
            axis=1
        )

        SYMBOLS = ['circle']
        
        # Create strip plot
        fig = px.strip(
            self.data, 
            y='Code Name',
            x='Year_str',  # Use the string version of Year
            color='Platform',
            title="Timeline of Quantum Error Correction Implementations",
            labels={
                "Code Name": "QEC Code Type",
                "Year_str": "Publication Year",  # Update label
                "Platform": "Quantum Platform"
            },
            custom_data=['hover_text'],  # Include our custom hover text
            color_discrete_map=self.PLATFORM_COLORS
        )

        # Customize the jitter and point appearance
        fig.update_traces(
            jitter=0.8,  # Reduce jitter slightly for better organization
            marker=dict(
                size=12,  # Increase marker size
                opacity=0.9,  # Slight transparency for overlapping points
                line=dict(width=1.5, color='black'),  # Thicker border for better visibility
                symbol=SYMBOLS[0]
            ),
            orientation='h',  # Ensure horizontal orientation
            hovertemplate="%{customdata}<extra></extra>"  # Use our custom hover text
        )

        # Apply standardized layout settings
        fig.update_layout(
            title={
                'text': "Timeline of Quantum Error Correction Implementations",
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            showlegend=True,
            legend={
                'title': {'text': 'Quantum Platform'},
                **{k: v for k, v in self.PLOTLY_LAYOUT_DEFAULTS['legend'].items() if k not in ['title']}
            },
            hovermode=self.PLOTLY_LAYOUT_DEFAULTS['hovermode'],
            font=self.PLOTLY_LAYOUT_DEFAULTS['font'],
            plot_bgcolor=self.PLOTLY_LAYOUT_DEFAULTS['plot_bgcolor'],
            paper_bgcolor=self.PLOTLY_LAYOUT_DEFAULTS['paper_bgcolor'],
            margin=self.PLOTLY_LAYOUT_DEFAULTS['margin'],
            xaxis=dict(
                title={"text": "Publication Year"},
                type='category',  # Treat x-axis as categorical
                categoryorder='array',
                categoryarray=sorted(self.data['Year_str'].unique()),  # Sort years
                **{k: v for k, v in self.PLOTLY_LAYOUT_DEFAULTS['xaxis'].items() if k not in ['title', 'type']}
            ),
            yaxis=dict(
                title={"text": "QEC Code Type"},
                type='category',
                categoryorder='category ascending',
                **{k: v for k, v in self.PLOTLY_LAYOUT_DEFAULTS['yaxis'].items() if k not in ['title', 'type']}
            ),
            height=self.plot_settings['export']['height'],
            width=self.plot_settings['export']['width']
        )
        
        # Store the figure as an instance attribute for export
        self.fig = fig
        
        # Export to multiple formats
        self.export_to_multiple(export_name="qec_timeline", element_id="qec-timeline-scatter")

def main():
    """Main function to create and save the plot."""
    plot = QECTimelineScatterPlot()
    plot.create_plot()

if __name__ == "__main__":
    main()
