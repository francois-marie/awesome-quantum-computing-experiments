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
        markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', 'h', '8']  # Different marker shapes
        
        # Create scatter plot with different colors and markers for each code
        for i, code in enumerate(unique_codes):
            mask = df_plot['Code Name'] == code
            data = df_plot[mask]
            
            # Size proportional to k, but with a minimum size for visibility
            sizes = 100 * data['k'] + 50
            
            plt.scatter(data['n'], data['d'], 
                       s=sizes,
                       marker=markers[i % len(markers)],
                       label=code,
                       alpha=0.7)
        
        # Add legend
        plt.legend(title="Code Types", 
                  bbox_to_anchor=(1.05, 1),
                  loc='upper left',
                  fontsize=self.plot_settings['fontsize']['tick'])
        
        # Set log scale for both axes
        plt.xscale('log')
        plt.yscale('log')
        
        # Add grid
        plt.grid(True, which="both", ls="-", alpha=0.2)
        
        # Adjust layout to prevent legend cutoff
        plt.tight_layout()
        
        # Add text annotations for k values
        for _, row in df_plot.iterrows():
            plt.annotate(f'k={row["k"]}', 
                        (row['n'], row['d']),
                        xytext=(5, 5),
                        textcoords='offset points',
                        fontsize=self.plot_settings['fontsize']['annotation'],
                        alpha=0.7)

def main():
    """Main function to create and save the plot."""
    plot = NKDPlot()
    plot.create_plot()
    plot.save_plot(plot.config['plots']['nkd'])

if __name__ == "__main__":
    main() 