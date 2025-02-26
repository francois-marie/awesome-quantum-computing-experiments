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
        plots_dir = self.config['paths']['output']['plots']
        plots = self.config['plots']
        return f"""# Awesome Quantum Computing Experiments

A curated list of notable quantum computing experiments, focused primarily on the implementation of quantum error correction codes.

![Plot]({plots_dir}/{plots['nkd']})
![Plot]({plots_dir}/{plots['qec_time']})
![Plot]({plots_dir}/{plots['entangled']})
![Plot]({plots_dir}/{plots['qubit_count']})
![Plot]({plots_dir}/{plots['coherence_times']})

## Overview

This repository maintains a comprehensive database of quantum computing experiments, with a focus on:
- Quantum Error Correction (QEC) implementations
- Magic State Distillation (MSD) experiments
- Entangled State Error measurements
- Physical Qubit Count evolution
- Relaxation and Coherence Times (see [Superconducting Qubits: Current State of Play](https://arxiv.org/abs/1905.13641) for more details)

## Quick Start

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

"""
    
    def _generate_toc(self) -> str:
        """Generate table of contents."""
        content = "## Table of Contents\n\n"
        
        # QEC section
        content += "- [Quantum Error Correction](#quantum-error-correction)\n"
        content += self.sections[0].generate_toc()
        
        # MSD section
        content += "- [Magic State Distillation](#magic-state-distillation)\n"
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

## License

This work is licensed under a [CC0 1.0 Universal (Public Domain Dedication)](LICENSE).
To the extent possible under law, the authors have dedicated all copyright and related and neighboring rights to this work to the public domain worldwide.
For more information, see [Creative Commons CC0 1.0 Legal Code](https://creativecommons.org/publicdomain/zero/1.0/).
"""

    def generate_plots_section(self) -> str:
        return "\n".join([
            "![Plot](out/plots/nkd_plot.png)",
            "![Plot](out/plots/qec_time_evolution.png)",
            "![Plot](out/plots/entangled_state_error_vs_year.png)",
            "![Plot](out/plots/qubit_count_vs_year.png)",
            "![Plot](out/plots/coherence_times.png)"
        ])

def main():
    """Main function to generate the README."""
    generator = MarkdownGenerator()
    generator.generate()

if __name__ == "__main__":
    main() 