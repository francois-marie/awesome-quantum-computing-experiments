from .base import BasePlot
import plotly.express as px
import plotly.utils
import json
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

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

        # Corrected line: removed the erroneous [2] at the end
        fig = px.scatter(
            agg_data,
            x='Year_str',
            y='Code Name',
            size='Count',
            color='Platform',
            title="Aggregated Timeline of Quantum Error Correction Implementations",
            labels={
                "Platform": "Quantum Platform",
                "Code Name": "QEC Code Type",
                "Year_str": "Publication Year",
                "Count": "Number of Experiments"
            },
            custom_data=['hover_text'],
            color_discrete_map=self.PLATFORM_COLORS
        )

        # Corrected line: removed the erroneous [1] at the end
        fig.update_traces(
            marker=dict(
                sizemode='area',
                sizemin=4,
                line=dict(width=1.5, color='black'),
                opacity=0.8
            ),
            hovertemplate="%{customdata}<extra></extra>"
        )

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
                type='category',
                categoryorder='total ascending',
                **{k: v for k, v in self.PLOTLY_LAYOUT_DEFAULTS['yaxis'].items() if k not in ['title', 'type']}
            ),
            height=self.plot_settings['export']['height'],
            width=self.plot_settings['export']['width']
        )
        
        self.fig = fig
        self.export_to_multiple(export_name="qec_timeline_aggregated", element_id="qec-timeline-aggregated-scatter")

def main():
    """Main function to create and save the plot."""
    plot = QECTimelineScatterPlot()
    plot.create_plot()

if __name__ == "__main__":
    main()
