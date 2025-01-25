from .base import BasePlot
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

class QubitCountPlot(BasePlot):
    """Creates the qubit count evolution plot."""
    
    def __init__(self):
        super().__init__()
        self.data = self.load_data(self.config['paths']['data']['qubit_count'])
        
    def load_data(self, csv_path: str):
        """Load and preprocess qubit count data."""
        data = super().load_data(csv_path)
        data["Number of qubits"] = pd.to_numeric(
            data["Number of qubits"], errors="coerce"
        )
        return data
        
    def create_plot(self):
        """Create the qubit count evolution plot."""
        self.setup_plot(
            title="Number of Qubits vs. Year by Platform",
            xlabel="Year",
            ylabel="Number of Qubits"
        )
        
        # Create the plot
        sns.lineplot(
            data=self.data,
            x="Year",
            y="Number of qubits",
            hue="Platform",
            marker="o",
            palette=self.plot_settings['style']['palette'],
            linewidth=self.plot_settings['style']['linewidth'],
            alpha=self.plot_settings['style']['alpha'],
        )
        
        # Additional customization
        plt.yscale("log")
        plt.legend(title="Platform", fontsize=self.plot_settings['fontsize']['tick'], 
                  loc="upper left")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()

def main():
    """Main function to create and save the plot."""
    plot = QubitCountPlot()
    plot.create_plot()
    plot.save_plot("qubit_count_vs_year.png")

if __name__ == "__main__":
    main() 