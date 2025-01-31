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
        
        # Get unique code names for color mapping
        unique_codes = df_plot['Code Name'].unique()
        markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', 'h', '8']
        
        # Use color palette from config
        colors = sns.color_palette(
            self.config['plot_settings']['style']['palette'], 
            n_colors=len(unique_codes)
        )
        
        # Create scatter plot with different colors and markers for each code
        for i, (code, color) in enumerate(zip(unique_codes, colors)):
            mask = df_plot['Code Name'] == code
            data = df_plot[mask]
            
            sizes = 100 * data['k'] + 50
            
            plt.scatter(data['n'], data['d'], 
                       s=sizes,
                       marker=markers[i % len(markers)],
                       label=code,
                       alpha=self.config['plot_settings']['style']['alpha'],
                       color=color,
                       edgecolor='black',
                       linewidth=0.5)
        
        # Improve legend appearance
        plt.legend(
            loc='upper left',
            framealpha=1.0,      # Solid background
            edgecolor='black',   # Black edge
            fancybox=True,       # Rounded corners
            fontsize=self.plot_settings['fontsize']['legend']
        )
        
        plt.xscale('log')
        plt.yscale('log')
        
        # Add grid with improved visibility
        plt.grid(True, which="both", ls="-", alpha=0.2)
        
        plt.tight_layout()
        
        # Add text annotations with improved visibility
        for _, row in df_plot.iterrows():
            plt.annotate(
                f'k={row["k"]}', 
                (row['n'], row['d']),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=self.plot_settings['fontsize']['annotation'],
                alpha=0.9,
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)
            )

def main():
    """Main function to create and save the plot."""
    plot = NKDPlot()
    plot.create_plot()
    plot.save_plot(plot.config['plots']['nkd'])

if __name__ == "__main__":
    main() 