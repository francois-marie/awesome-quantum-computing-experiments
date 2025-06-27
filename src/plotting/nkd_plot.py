from .base import BasePlot
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import re
from typing import Tuple, List

class NKDPlot(BasePlot):
    """Creates the [n,k,d] parameter space plot, aggregated across all code types."""

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

        # Find all occurrences of [n,k,d] patterns
        param_groups = re.findall(r'(\[+\d+,\s*\d+,\s*\d+\]+)', params)

        for param in param_groups:
            # Extract n, k, d values
            match = re.search(r'\[+(\d+),\s*(\d+),\s*(\d+)\]+', param)
            if match:
                n = int(match.group(1))
                k = int(match.group(2))
                d = int(match.group(3))

                # For single brackets [n,k,d], distance is treated as 1
                if param.count('[') == 1:
                    d = 1

                n_values.append(n)
                k_values.append(k)
                d_values.append(d)

        return n_values, k_values, d_values

    def load_data(self, csv_path: str):
        """Load and preprocess QEC data, aggregating across all code types."""
        data = super().load_data(csv_path)

        # Filter out rows without code parameters
        data = data.dropna(subset=['Code Parameters'])

        # Parse code parameters for each row
        parsed_params = data['Code Parameters'].apply(self.parse_code_parameters)

        # Create an expanded list of all individual experiments
        expanded_data = []
        for idx, row in data.iterrows():
            n_values, k_values, d_values = parsed_params[idx]
            if not n_values:
                continue

            for n, k, d in zip(n_values, k_values, d_values):
                new_row = row.copy()
                new_row['n'] = n
                new_row['k'] = k
                new_row['d'] = d
                # Create detailed hover text for each individual experiment
                new_row['hover_text'] = (
                    f"<b>{row['Article Title']} ({row['Year']})</b><br>"
                    f"Code: {row['Code Name']} {row['Code Parameters']}<br>"
                    f"Platform: {row['Platform']}"
                )
                expanded_data.append(new_row)

        if expanded_data:
            df = pd.DataFrame(expanded_data)

            # Group by [n, k, d] only, aggregating across all code types
            aggregated_data = (
                df.groupby(['n', 'k', 'd'])
                .agg(
                    count=('n', 'size'),  # Count total experiments for (n,k,d)
                    hover_text=('hover_text', lambda x: '<br>---<br>'.join(x))
                )
                .reset_index()
            )

            # Create a new, comprehensive hover text for the aggregated points
            aggregated_data['custom_data'] = aggregated_data.apply(
                lambda row: (
                    f"<b>{row['count']} experiment(s) with [[{row['n']},{row['k']},{row['d']}]]</b><br>"
                    f"Aggregated across all code types.<br>"
                    f"<br><b>Sources:</b><br>{row['hover_text']}"
                ),
                axis=1
            )
            return aggregated_data
        else:
            return pd.DataFrame(columns=data.columns.tolist() + ['n', 'k', 'd', 'count', 'custom_data'])

    def create_plot(self):
        """Create the aggregated NKD parameter space plot using Plotly."""
        if self.data.empty:
            # print("No data available to plot.")
            return

        # Get unique k values for color mapping
        unique_k = sorted(self.data['k'].unique())
        k_to_color = {k: list(self.CODE_COLORS.values())[i % len(self.CODE_COLORS)] for i, k in enumerate(unique_k)}

        # Create one trace for each value of k
        traces = []
        yjitter = 0.
        base_marker_size = 15  # Scale factor for marker size

        for k_val in unique_k[::-1]:
            k_data = self.data[self.data['k'] == k_val]

            if not k_data.empty:
                # Add jitter to 'd' for visualization to reduce exact overlaps
                d_jittered = k_data['d'] + np.random.uniform(-yjitter, yjitter, size=len(k_data))

                trace = go.Scatter(
                    x=k_data['n'],
                    y=d_jittered,
                    mode='markers',
                    name=f"k = {k_val}",  # Legend shows k-value
                    marker=dict(
                        symbol='circle',  # All markers are circles
                        color=k_to_color[k_val],
                        # Marker area is proportional to count, so radius is proportional to sqrt(count)
                        size=np.sqrt(k_data['count']) * base_marker_size,
                        # line=dict(width=2, color='grey'),
                        opacity=1
                    ),
                    hovertemplate='%{customdata}<extra></extra>',
                    customdata=k_data['custom_data']
                )
                traces.append(trace)

        # Create layout with standardized settings
        layout = go.Layout(
            title={
                'text': 'Aggregated Quantum Error Correction Parameters',
                'font': self.PLOTLY_LAYOUT_DEFAULTS['title']['font']
            },
            xaxis={
                'title': {'text': 'Number of Physical Qubits (n)'},
                'type': 'linear',
                **self.PLOTLY_LAYOUT_DEFAULTS['xaxis']
            },
            yaxis={
                'title': {'text': 'Distance (d)'},
                'type': 'linear',
                'dtick': 1,
                'minor': {'ticks': ''},
                **self.PLOTLY_LAYOUT_DEFAULTS['yaxis']
            },
            showlegend=True,
            legend={
                'title': {'text': 'Logical Qubits (k)'},
                **self.PLOTLY_LAYOUT_DEFAULTS['legend']
            },
            font=self.PLOTLY_LAYOUT_DEFAULTS['font'],
            plot_bgcolor=self.PLOTLY_LAYOUT_DEFAULTS['plot_bgcolor'],
            paper_bgcolor=self.PLOTLY_LAYOUT_DEFAULTS['paper_bgcolor'],
            margin=self.PLOTLY_LAYOUT_DEFAULTS['margin'],
            hovermode=self.PLOTLY_LAYOUT_DEFAULTS['hovermode'],
            width=self.plot_settings['export']['width'],
            height=self.plot_settings['export']['height']
        )

        # Create a Plotly figure for export
        self.fig = go.Figure(data=traces, layout=layout)
        self.fig.update_yaxes(minor_ticks="")

        # Add size reference annotation
        self.add_size_reference()

        # Export to multiple formats
        self.export_to_multiple(export_name="nkd_plot_aggregated")

    def add_size_reference(self):
        """Add a size reference to show marker size vs experiment count."""
        # Get the range of counts to create meaningful reference sizes
        if self.data.empty:
            return
            
        min_count = self.data['count'].min()
        max_count = self.data['count'].max()
        
        # Create reference points (1, 5, 10, or based on data range)
        if max_count <= 5:
            ref_counts = [1, max_count] if max_count > 1 else [1]
        elif max_count <= 10:
            ref_counts = [1, 5, max_count] if max_count > 5 else [1, max_count]
        else:
            ref_counts = [1, 5, 10, max_count]
        
        # Remove duplicates and sort
        ref_counts = sorted(list(set(ref_counts)))
        
        # Calculate positions for the size reference (top-right corner)
        x_range = self.data['n'].max() - self.data['n'].min()
        y_range = self.data['d'].max() - self.data['d'].min()
        
        ref_x = self.data['n'].max() - 0.15 * x_range
        ref_y_start = self.data['d'].min() + 0.1 * y_range
        
        base_marker_size = 15
        
        # Add reference markers and labels
        for i, count in enumerate(ref_counts):
            y_pos = ref_y_start - i * 0.08 * y_range
            marker_size = np.sqrt(count) * base_marker_size
            
            # Add invisible scatter point for the reference marker
            self.fig.add_trace(go.Scatter(
                x=[ref_x],
                y=[y_pos],
                mode='markers',
                marker=dict(
                    size=marker_size,
                    color='gray',
                    opacity=0.7,
                    line=dict(width=1, color='black')
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Add text label
            self.fig.add_annotation(
                x=ref_x + 0.05 * x_range,
                y=y_pos,
                text=f"{count} exp{'s' if count > 1 else ''}",
                showarrow=False,
                font=dict(size=10, color='black'),
                xanchor='left',
                yanchor='middle'
            )
        
        # Add title for the size reference
        self.fig.add_annotation(
            x=ref_x,
            y=ref_y_start + 0.05 * y_range,
            text="<b>Marker Size</b>",
            showarrow=False,
            font=dict(size=11, color='black'),
            xanchor='center',
            yanchor='bottom'
        )

def main():
    """Main function to create and save the plot."""
    plot = NKDPlot()
    plot.create_plot()

if __name__ == "__main__":
    main()