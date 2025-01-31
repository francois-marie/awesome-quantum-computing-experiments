from abc import ABC, abstractmethod
import yaml
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

class BasePlot(ABC):
    """Base class for all plotting classes."""
    
    def __init__(self):
        """Initialize plot settings and load config."""
        self.config = self.load_config()
        self.plot_settings = self.config['plot_settings']
        
        # Apply style settings
        plt.style.use('default')  # Reset to default style
        
        # Update rcParams with config settings
        plt.rcParams.update({
            'figure.figsize': self.plot_settings['figsize'],
            'figure.facecolor': self.plot_settings['style']['figure']['facecolor'],
            'figure.dpi': self.plot_settings['style']['figure']['dpi'],
            'axes.facecolor': self.plot_settings['style']['axes']['facecolor'],
            'axes.edgecolor': self.plot_settings['style']['axes']['edgecolor'],
            'axes.grid': self.plot_settings['style']['axes']['grid'],
            'axes.spines.top': self.plot_settings['style']['axes']['spines']['top'],
            'axes.spines.right': self.plot_settings['style']['axes']['spines']['right'],
            'axes.spines.bottom': self.plot_settings['style']['axes']['spines']['bottom'],
            'axes.spines.left': self.plot_settings['style']['axes']['spines']['left'],
            'grid.color': self.plot_settings['style']['grid']['color'],
            'grid.linestyle': self.plot_settings['style']['grid']['linestyle'],
            'grid.alpha': self.plot_settings['style']['grid']['alpha'],
            'text.color': self.plot_settings['style']['text']['color'],
            'xtick.color': self.plot_settings['style']['ticks']['color'],
            'ytick.color': self.plot_settings['style']['ticks']['color']
        })
        
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
        plt.savefig(
            output_path,
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none',
            dpi=300
        )
        plt.close()

    def setup_plot(self, title: str, xlabel: str, ylabel: str):
        """Set up the basic plot parameters."""
        plt.figure(figsize=(10, 6))
        plt.title(title, fontsize=self.config['plot_settings']['fontsize']['title'])
        plt.xlabel(xlabel, fontsize=self.config['plot_settings']['fontsize']['label'])
        plt.ylabel(ylabel, fontsize=self.config['plot_settings']['fontsize']['label'])
        
        # Configure ticks
        plt.tick_params(
            axis='both',
            which='major',
            labelsize=self.config['plot_settings']['fontsize']['tick'],
            length=6,
            width=1,
            colors='black'
        )
        plt.tick_params(
            axis='both',
            which='minor',
            labelsize=self.config['plot_settings']['fontsize']['tick'],
            length=3,
            width=1,
            colors='black'
        )

    def load_config(self):
        """Load configuration from YAML file."""
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f) 