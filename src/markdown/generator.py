import yaml
import pandas as pd
from pathlib import Path
from .sections import (
    QECSection, MSDSection, EntangledSection,
    QubitCountSection, PhysicalQubitsSection
)

class MarkdownGenerator:
    """Generates the complete README.md file."""
    
    def __init__(self):
        with open("config.yaml") as f:
            self.config = yaml.safe_load(f)
            
        # Load all data
        self.qec_data = pd.read_csv(self.config['paths']['data']['qec'])
        self.msd_data = pd.read_csv(self.config['paths']['data']['msd'])
        self.entangled_data = pd.read_csv(self.config['paths']['data']['entangled'])
        self.qubit_count_data = pd.read_csv(self.config['paths']['data']['qubit_count'])
        self.physical_qubits_data = pd.read_csv(self.config['paths']['data']['physical_qubits'])  # Load physical qubits data
        
        # Initialize section generators
        self.sections = [
            QECSection(self.qec_data),
            MSDSection(self.msd_data),
            EntangledSection(self.entangled_data),
            QubitCountSection(self.qubit_count_data),
            PhysicalQubitsSection(self.physical_qubits_data)  # Pass the data here
        ]
    
    def generate(self):
        """Generate the complete README.md content."""
        content = self._generate_header()
        content += self._generate_toc()
        content += self._generate_sections()
        content += self._generate_footer()
        
        # Write to file
        readme_path = Path(self.config['paths']['output']['readme'])
        readme_path.write_text(content)
    
    def _generate_header(self) -> str:
        """Generate the header section of the README."""
        return f"""# Awesome Quantum Computing Experiments

<div style="text-align: center; font-style: italic; margin: 20px 0;">
A comprehensive database of notable quantum computing experiments, with emphasis on quantum error correction implementations
</div>

<hr style="border: 0; height: 1px; background: #333; background-image: linear-gradient(to right, #ccc, #333, #ccc);">

## Overview

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 3px solid #007bff;">
This repository maintains a comprehensive database of quantum computing experiments, with a focus on:

- Quantum Error Correction (QEC) implementations
- Magic State Distillation (MSD) experiments
- Entangled State Error measurements
- Physical Qubit Count evolution
- Relaxation and Coherence Times (see [Superconducting Qubits: Current State of Play](https://arxiv.org/abs/1905.13641))
</div>

<hr style="margin: 30px 0;">

## Quick Start

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">

1. Clone the repository and install dependencies:
```bash
git clone https://github.com/francois-marie/awesome-quantum-computing-experiments.git
cd awesome-quantum-computing-experiments
pip install -e ".[test]" # Install package and test dependencies
```

2. Generate all plots and README:
```bash
make all
```

For more detailed information:
- See [Documentation](docs/DOCUMENTATION.md) for usage and data format details
- See [Contributing Guide](docs/CONTRIBUTING.md) for how to add new experiments
</div>

<hr style="margin: 30px 0;">

## Local Development

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">

1. Set up Ruby environment using rbenv:
```bash
eval "$(rbenv init -)"
rbenv shell 3.1.0
```

2. Install Ruby dependencies:
```bash
bundle install
```

3. Run Jekyll server:
```bash
bundle exec jekyll clean
bundle exec jekyll serve --baseurl="/awesome-quantum-computing-experiments" --livereload
```

The site will be available at `http://localhost:4000/awesome-quantum-computing-experiments/`.
</div>

<hr style="margin: 30px 0;">

## Visualizations

<div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">

<h4>Generating Visualizations</h4>
All visualizations can be regenerated at any time using:

```bash
# Generate all plots
make plots

# Or use the consolidated generation script
make generate_all
```

<h4>Available Visualizations</h4>
After generation, plots will be available in multiple formats:

- PNG format in the `out/png` directory (for web display)
- PDF format in the `out/pdf` directory (for publication)
- JavaScript in the `out/js` directory (for interactive web display)

<h4>Plot Gallery</h4>

The following PNG files are included in the repository to display in this README:

![Cumulative Experiment Counts by Platform](out/png/experiment_counts.png)

![Yearly Experiment Counts](out/png/experiment_counts_yearly.png)

![QEC Platform Distribution](out/png/qec_platform_sunburst.png)

![Timeline of QEC Implementations](out/png/qec_timeline_aggregated.png)

![[[n, k, d]] Distribution](out/png/nkd_plot_aggregated.png)

![Entangled State Error Progress](out/png/entangled_error_plot.png)

![Qubit Count Evolution](out/png/qubit_count_plot.png)

![Physical Qubit Coherence Times](out/png/coherence_times_plot.png)

![Cumulative Experiment Counts by QEC code](out/png/qec_cumulative_growth.png)

</div>

"""
    
    def _generate_toc(self) -> str:
        """Generate table of contents."""
        content = "## Table of Contents\n\n"
        
        # QEC section
        content += "- [Quantum Error Correction](#quantum-error-correction)\n"
        content += self.sections[0].generate_toc()
        
        # MSD section
        content += "- [Magic State](#magic-state)\n"
        content += self.sections[1].generate_toc()
        
        # Entangled section
        content += "- [Entangled State Error](#entangled-state-error)\n"
        content += self.sections[2].generate_toc()
        
        # Qubit count section
        content += "- [Qubit Count](#qubit-count)\n"
        content += self.sections[3].generate_toc()
        
        # Physical qubits section
        content += "- [Physical Qubits](#physical-qubits)\n"
        content += self.sections[4].generate_toc()
        
        content += "\n"
        return content
    
    def _generate_sections(self) -> str:
        return "".join(section.generate_content() for section in self.sections)
    
    def _generate_footer(self) -> str:
        return """
## Contributing

Contributions are welcome! If you have suggestions for new entries, please submit a pull request or open an issue.

## Citation

If you use this dataset in your research, please cite:

```bibtex
@unpublished{leregentAwesomeQuantumComputing2025,
  title = {Awesome Quantum Computing Experiments: Benchmarking Experimental Progress Towards Fault-Tolerant Quantum Computation},
  author = {Le Régent, François-Marie},
  date = {2025-07-04},
  doi = {10.48550/arXiv.2507.03678},
  url = {http://arxiv.org/abs/2507.03678},
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
"""

    def generate_plots_section(self) -> str:
        return "\n".join([
            "![Cumulative Experiment Counts](out/png/experiment_counts.png)",
            "![Yearly Experiment Counts](out/png/experiment_counts_yearly.png)",
            "![QEC Platform Distribution](out/png/qec_platform_sunburst.png)",
            "![Timeline of QEC Implementations](out/png/qec_timeline_aggregated.png)",
            "![[[n, k, d]] Distribution](out/png/nkd_plot_aggregated.png)",
            "![Entangled State Error Progress](out/png/entangled_error_plot.png)",
            "![Qubit Count Evolution](out/png/qubit_count_plot.png)",
            "![Physical Qubit Coherence Times](out/png/coherence_times_plot.png)",
            "![QEC Code Parameters](out/png/qec_code_params_bubble.png)"
        ])

def main():
    """Main function to generate the README."""
    generator = MarkdownGenerator()
    generator.generate()

if __name__ == "__main__":
    main()
