from .base import BasePlot
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class CoherenceTimesPlot(BasePlot):
    """Creates the coherence times evolution plot."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['physical_qubits'])
        
    def load_data(self, csv_path: str):
        """Load and preprocess coherence times data."""
        data = super().load_data(csv_path)
        # Convert T1 and T2 to numeric, handling any non-numeric values
        data["T1"] = pd.to_numeric(data["T1"], errors="coerce")
        data["T2"] = pd.to_numeric(data["T2"], errors="coerce")
        return data
        
    def create_plot(self):
        """Create the coherence times evolution plot."""
        self.setup_plot(
            title="Evolution of Qubit Coherence Times",
            xlabel="Year",
            ylabel="Coherence Time (s)"
        )
        
        # Plot T1 and T2 for each platform
        platforms = self.data['Platform'].unique()
        markers = ['o', 's', '^', 'D', 'v']  # Different markers for different platforms
        colors = sns.color_palette(self.plot_settings['style']['palette'], len(platforms))
        
        for idx, platform in enumerate(platforms):
            platform_data = self.data[self.data['Platform'] == platform]
            
            # Plot T1
            mask_t1 = platform_data['T1'].notna()
            if mask_t1.any():
                plt.scatter(
                    platform_data[mask_t1]['Year'], 
                    platform_data[mask_t1]['T1'],
                    marker=markers[idx % len(markers)],
                    color=colors[idx],
                    label=f'{platform} (T1)',
                    s=100,
                    alpha=self.plot_settings['style']['alpha']
                )
                # Connect T1 points with a line
                plt.plot(
                    platform_data[mask_t1]['Year'], 
                    platform_data[mask_t1]['T1'],
                    color=colors[idx],
                    alpha=0.5
                )
            
            # Plot T2
            mask_t2 = platform_data['T2'].notna()
            if mask_t2.any():
                plt.scatter(
                    platform_data[mask_t2]['Year'], 
                    platform_data[mask_t2]['T2'],
                    marker=markers[idx % len(markers)],
                    color=colors[idx],
                    label=f'{platform} (T2)',
                    facecolors='none',
                    s=100,
                    alpha=self.plot_settings['style']['alpha']
                )
                # Connect T2 points with a line
                plt.plot(
                    platform_data[mask_t2]['Year'], 
                    platform_data[mask_t2]['T2'],
                    color=colors[idx],
                    alpha=0.5
                )
        
        # Set integer ticks for x-axis
        year_min = int(self.data['Year'].min())
        year_max = int(self.data['Year'].max())
        plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))  # Force integer ticks
        plt.xlim(year_min - 0.5, year_max + 0.5)  # Add padding but keep integer ticks
        
        # Additional customization
        plt.yscale('log')
        plt.legend(title="Platform", fontsize=self.plot_settings['fontsize']['tick'],
                   loc='upper left', bbox_to_anchor=(0.1, 0.9))
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()

def main():
    """Main function to create and save the plot."""
    plot = CoherenceTimesPlot()
    plot.create_plot()
    plot.save_plot("coherence_times.png")

if __name__ == "__main__":
    main() 