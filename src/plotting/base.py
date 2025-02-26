from abc import ABC, abstractmethod
import yaml
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

class BasePlot(ABC):
    """Base class for all plotting classes."""
    
    def __init__(self, double_column=False):
        """Initialize plot settings and load config."""
        self.config = self.load_config()
        self.plot_settings = self.config['plot_settings']
        self.double_column = double_column
        
        # Set publication-ready style
        plt.style.use('default')
        
        # Use LaTeX for text rendering if available
        plt.rcParams.update({
            'text.usetex': False,
            'font.family': 'sans-serif',
            'figure.figsize': self.plot_settings['figsize_double'] if double_column 
                            else self.plot_settings['figsize'],
            'figure.dpi': self.plot_settings['style']['figure']['dpi'],
            'axes.linewidth': 0.5,
            'grid.linewidth': 0.5,
            'lines.linewidth': self.plot_settings['style']['linewidth'],
            'xtick.major.width': 0.5,
            'ytick.major.width': 0.5,
            'xtick.minor.width': 0.5,
            'ytick.minor.width': 0.5,
            'xtick.major.size': 3,
            'ytick.major.size': 3,
            'xtick.minor.size': 1.5,
            'ytick.minor.size': 1.5,
            'axes.labelpad': 4,
            'legend.frameon': False,
            'legend.borderpad': 0.4,
            'legend.handlelength': 1.5,
            'legend.handletextpad': 0.5,
            'legend.columnspacing': 1.0,
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
        # save also as pdf
        plt.savefig(output_path.with_suffix('.pdf'), bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close()

    def setup_plot(self, title: str, xlabel: str, ylabel: str):
        """Set up the basic plot parameters."""
        plt.figure()
        plt.title(title, fontsize=self.plot_settings['fontsize']['title'])
        plt.xlabel(xlabel, fontsize=self.plot_settings['fontsize']['label'])
        plt.ylabel(ylabel, fontsize=self.plot_settings['fontsize']['label'])
        
        # Configure ticks
        plt.tick_params(
            axis='both',
            which='major',
            labelsize=self.plot_settings['fontsize']['tick']
        )
        plt.tick_params(
            axis='both',
            which='minor',
            labelsize=self.plot_settings['fontsize']['tick']
        )

    def load_config(self):
        """Load configuration from YAML file."""
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f) 