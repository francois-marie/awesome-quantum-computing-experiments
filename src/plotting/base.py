from abc import ABC, abstractmethod
import yaml
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

class BasePlot(ABC):
    """Base class for all plotting classes."""
    
    def __init__(self):
        with open("config.yaml") as f:
            self.config = yaml.safe_load(f)
        
        # Use seaborn's default style directly instead of matplotlib's deprecated seaborn style
        sns.set_theme()  # This replaces plt.style.use('seaborn')
        self.plot_settings = self.config['plot_settings']
        
    def load_data(self, csv_path: str) -> pd.DataFrame:
        """Load data from CSV file and ensure numeric types."""
        data = pd.read_csv(csv_path)
        # Convert year to numeric, handling errors
        data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
        return data
        
    @abstractmethod
    def create_plot(self):
        """Create the plot. Must be implemented by child classes."""
        pass
        
    def save_plot(self, filename: str):
        """Save the plot to the configured output directory."""
        output_path = Path(self.config['paths']['output']['plots']) / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path)
        plt.close()

    def setup_plot(self, title: str, xlabel: str, ylabel: str):
        """Set up common plot elements."""
        plt.figure(figsize=tuple(self.plot_settings['figsize']))
        plt.title(title, fontsize=self.plot_settings['fontsize']['title'])
        plt.xlabel(xlabel, fontsize=self.plot_settings['fontsize']['label'])
        plt.ylabel(ylabel, fontsize=self.plot_settings['fontsize']['label'])
        plt.xticks(fontsize=self.plot_settings['fontsize']['tick'])
        plt.yticks(fontsize=self.plot_settings['fontsize']['tick']) 