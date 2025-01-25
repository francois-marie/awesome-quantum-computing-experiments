import yaml
import pandas as pd
from pathlib import Path
from .sections import QECSection, MSDSection, EntangledSection, QubitCountSection

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
        
        # Initialize section generators
        self.sections = {
            'qec': QECSection(self.qec_data),
            'msd': MSDSection(self.msd_data),
            'entangled': EntangledSection(self.entangled_data),
            'qubit_count': QubitCountSection(self.qubit_count_data)
        }
    
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

## Overview

This repository maintains a comprehensive database of quantum computing experiments, with a focus on:
- Quantum Error Correction (QEC) implementations
- Magic State Distillation (MSD) experiments
- Entangled State Error measurements
- Physical Qubit Count evolution

## Quick Start

1. Clone the repository and install dependencies:
```bash
git clone https://github.com/yourusername/awesome-quantum-computing-experiments.git
cd awesome-quantum-computing-experiments
pip install -r requirements.txt
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
        content += self.sections['qec'].generate_toc()
        
        # MSD section
        content += "- [Magic State Distillation](#magic-state-distillation)\n"
        content += self.sections['msd'].generate_toc()
        
        # Entangled section
        content += "- [Entangled State Error](#entangled-state-error)\n"
        content += self.sections['entangled'].generate_toc()
        
        # Qubit count section
        content += "- [Qubit Count](#qubit-count)\n"
        content += self.sections['qubit_count'].generate_toc()
        
        content += "\n"
        return content
    
    def _generate_sections(self) -> str:
        return "".join(section.generate_content() for section in self.sections.values())
    
    def _generate_footer(self) -> str:
        return """
## Contributing

Contributions are welcome! If you have suggestions for new entries, please submit a pull request or open an issue.

## License

This work is licensed under a [CC0 1.0 Universal (Public Domain Dedication)](LICENSE).
To the extent possible under law, the authors have dedicated all copyright and related and neighboring rights to this work to the public domain worldwide.
For more information, see [Creative Commons CC0 1.0 Legal Code](https://creativecommons.org/publicdomain/zero/1.0/).
"""

def main():
    """Main function to generate the README."""
    generator = MarkdownGenerator()
    generator.generate()

if __name__ == "__main__":
    main() 