from .base import BasePlot
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class EntangledErrorPlot(BasePlot):
    """Creates the entangled state error evolution plot."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['entangled'])
        
    def load_data(self, csv_path: str):
        """Load and preprocess entangled error data."""
        data = super().load_data(csv_path)
        data["Entangled State Error"] = pd.to_numeric(
            data["Entangled State Error"], errors="coerce"
        )
        return data
        
    def create_plot(self):
        """Create the entangled state error evolution plot."""
        self.setup_plot(
            title="Entangled State Error vs. Year",
            xlabel="Year",
            ylabel="Entangled State Error"
        )
        
        # Create the plot
        sns.lineplot(
            data=self.data,
            x="Year",
            y="Entangled State Error",
            hue="Platform",
            marker="o",
            palette=self.plot_settings['style']['palette'],
            linewidth=self.plot_settings['style']['linewidth'],
            alpha=self.plot_settings['style']['alpha'],
        )
        
        # Additional customization
        plt.yscale("log")
        plt.legend(title="Platform", fontsize=self.plot_settings['fontsize']['tick'], 
                  loc="lower left")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()

def main():
    """Main function to create and save the plot."""
    plot = EntangledErrorPlot()
    plot.create_plot()
    plot.save_plot("entangled_state_error_vs_year.png")

if __name__ == "__main__":
    main() 