from .base import BasePlot
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import re
from typing import Tuple, List
import numpy as np

class NKDPlot(BasePlot):
    """Creates the [n,k,d] parameter space plot."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['qec'])
        
    def parse_code_parameters(self, params: str) -> Tuple[List[int], List[int], List[int]]:
        """Parse code parameters string into n, k, d lists."""
        if pd.isna(params):
            return [], [], []
            
        # Remove all spaces
        params = params.replace(" ", "")
        # Split on commas separating different code parameters
        code_params_list = re.split(r",(?=\[)", params)
        n_list, k_list, d_list = [], [], []
        
        for code_param in code_params_list:
            if code_param == "1Dwith12qubits":
                continue
            # Store original parameter string before stripping brackets
            original_param = code_param
            # Remove leading/trailing brackets and text
            code_param = code_param.strip("[]")
            code_param = code_param.replace("surfacecode", "").replace("toriccode", "")
            
            # Split on hyphens for multiple codes
            codes = code_param.split("-")
            for code in codes:
                code = code.strip("[]")
                try:
                    n, k, d = map(int, code.split(","))
                    n_list.append(n)
                    k_list.append(k)
                    # Check if this parameter set had single brackets
                    if not original_param.startswith("[["):
                        d = 1
                    d_list.append(d)
                except Exception as e:
                    print(f"Error parsing code parameters '{code}': {e}")
                    
        return n_list, k_list, d_list
        
    def load_data(self, csv_path: str):
        """Load and preprocess QEC data for NKD analysis."""
        data = super().load_data(csv_path)
        # Additional processing could be added here
        return data
        
    def create_plot(self):
        """Create the NKD parameter space plot."""
        self.setup_plot(
            title="Quantum Error Correction Code Parameters",
            xlabel="Number of Physical Qubits (n)",
            ylabel="Distance (d)"
        )
        
        # Process data and create DataFrame for plotting
        plot_data = []
        for _, row in self.data.iterrows():
            n_list, k_list, d_list = self.parse_code_parameters(row['Code Parameters'])
            for n, k, d in zip(n_list, k_list, d_list):
                plot_data.append({
                    'n': n,
                    'k': k,
                    'd': d,
                    'Code Name': row['Code Name'],
                    'Year': row['Year']
                })
        
        df_plot = pd.DataFrame(plot_data)
        
        # Get unique code names for marker mapping
        unique_codes = df_plot['Code Name'].unique()
        markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', 'h', '8']
        
        # Get unique k values for color mapping
        unique_k = sorted(df_plot['k'].unique())
        colors = sns.color_palette(
            self.config['plot_settings']['style']['palette'], 
            n_colors=len(unique_k)
        )
        k_to_color = dict(zip(unique_k, colors))
        
        # Plot the actual data points
        for i, code in enumerate(unique_codes):
            mask = df_plot['Code Name'] == code
            data = df_plot[mask]
            
            for k_val in unique_k:
                k_mask = data['k'] == k_val
                if k_mask.any():
                    plt.scatter(
                        data[k_mask]['n'], 
                        data[k_mask]['d'],
                        s=20, 
                        marker=markers[i % len(markers)],
                        color='black',
                        facecolors=k_to_color[k_val],
                        alpha=self.plot_settings['style']['alpha'],
                        linewidth=0.5,
                        zorder=3  # Ensure points are above grid
                    )
        
        # Create handles and labels for both legends
        code_handles = []
        code_labels = []
        k_handles = []
        k_labels = []
        
        # Collect handles and labels for code names
        for i, code in enumerate(unique_codes):
            handle = plt.Line2D([], [], 
                              color='gray',
                              marker=markers[i % len(markers)],
                              linestyle='None',
                              markersize=3)
            code_handles.append(handle)
            # Simplify code names more aggressively
            simplified_code = (code.replace(" code", "")
                              .replace("Code", "")
                              .replace("[[", "")
                              .replace("]]", "")
                              .replace("Perfect", "Perf.")
                              .strip())
            code_labels.append(simplified_code)
        
        # Collect handles and labels for k values
        for k_val in unique_k:
            handle = plt.Line2D([], [],
                              color=k_to_color[k_val],
                              marker='o',
                              linestyle='None',
                              markersize=3)
            k_handles.append(handle)
            k_labels.append(f'k={k_val}')
        
        # Create first legend for code names
        legend1 = plt.legend(code_handles, code_labels,
            title="Code Name",
            loc='center right',
            fontsize=self.plot_settings['fontsize']['legend'],
            title_fontsize=self.plot_settings['fontsize']['legend'],
            ncol=2,  # Use two columns to make it more compact
            frameon=True,  # Enable frame
            framealpha=0.8,  # Make background more opaque
            edgecolor='none'
        )

        # Add the first legend manually
        plt.gca().add_artist(legend1)
        
        # Create second legend for k values
        legend2 = plt.legend(k_handles, k_labels,
            title="Logical Qubits",
            loc='upper left',
            fontsize=self.plot_settings['fontsize']['legend'],
            title_fontsize=self.plot_settings['fontsize']['legend'],
            ncol=2,  # Use two columns to make it more compact
            frameon=True,  # Enable frame
            framealpha=0.8,  # Make background more opaque
            edgecolor='none'
        )
        
        # Add grid with improved visibility
        plt.grid(True, which="both", ls="-", alpha=0.2, zorder=1)
        
        # Adjust layout to accommodate legends
        plt.tight_layout()
        plt.subplots_adjust(right=0.8)  # Less margin on the right

def main():
    """Main function to create and save the plot."""
    plot = NKDPlot()
    plot.create_plot()
    plot.save_plot(plot.config['plots']['nkd'])

if __name__ == "__main__":
    main() 