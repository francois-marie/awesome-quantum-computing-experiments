from .base import BasePlot
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class QECTimePlot(BasePlot):
    """Creates the QEC time evolution plot."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['qec'])
        
    def load_data(self, csv_path: str):
        """Load and preprocess QEC data."""
        return super().load_data(csv_path)
        
    def create_plot(self):
        """Create the QEC time evolution plot."""
        self.setup_plot(
            title="Time Evolution of Quantum Error Correction Experiments",
            xlabel="Year",
            ylabel="Platform"
        )
        
        # Create the stripplot
        sns.stripplot(
            data=self.data,
            x="Year",
            y="Platform",
            hue="Code Name",
            jitter=True,
            dodge=True,
            palette=self.plot_settings['style']['palette'],
            size=8,
            alpha=self.plot_settings['style']['alpha'],
        )
        
        # Add shaded intervals for each platform
        platforms = self.data["Platform"].unique()
        palette = sns.color_palette(self.plot_settings['style']['palette'], 
                                  len(platforms))
        platform_colors = dict(zip(platforms, palette))
        
        for i, platform in enumerate(platforms):
            plt.fill_betweenx(
                y=[i - 0.5, i + 0.5],
                x1=self.data["Year"].min() - 1,
                x2=self.data["Year"].max() + 1,
                color=platform_colors[platform],
                alpha=0.1,
            )
            
        plt.tight_layout()

def main():
    """Main function to create and save the plot."""
    plot = QECTimePlot()
    plot.create_plot()
    plot.save_plot("qec_time_evolution.png")

if __name__ == "__main__":
    main() 