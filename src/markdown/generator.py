"""Generate README.md from the CSV files in ``data/``.

Layout of the generated README (top to bottom):

1. Title, one-line pitch, badges
2. "The data": table of the CSV files that feed every plot and table
3. Plot gallery (markdown table of PNGs)
4. Contents + curated paper lists, one section per dataset
5. Quick Start, Local Development
6. Contributing, Citation, License
"""

import re
from pathlib import Path

import pandas as pd
import yaml

from .sections import (
    QECSection, MSDSection, EntangledSection,
    QubitCountSection, PhysicalQubitsSection
)

REPO_URL = "https://github.com/francois-marie/awesome-quantum-computing-experiments"
SITE_URL = "https://francoismarieleregent.xyz/awesome-quantum-computing-experiments"
ARXIV_ID = "2507.03678"

# (config key, file description, key columns) in display order.
DATASETS = [
    ("qec", "Quantum error correction experiments",
     "Code Name, Code Parameters [[n,k,d]], Platform, Year, Research Group"),
    ("msd", "Magic state preparation, distillation and code switching",
     "Magic State, Fidelity, Acceptance Rate, QEC Code, Experiment Type"),
    ("entangled", "Entangled state and two-qubit gate errors",
     "Entangled State Error, Platform, Year"),
    ("qubit_count", "Physical qubit count records",
     "Number of qubits, Platform, Year"),
    ("physical_qubits", "Coherence times of physical qubits",
     "Physical system, T1, T2, Platform, Year"),
]

# (caption, png file name, site anchor) in gallery order.
PLOTS = [
    ("Entangled state error", "entangled_error_plot", "entangled-state-error"),
    ("Qubit count", "qubit_count_plot", "qubit-count"),
    ("Coherence times (T1, T2)", "coherence_times_plot", "coherence-times"),
    ("Magic state error vs acceptance rate", "msd_plot", "magic-state"),
    ("Magic state error over time", "msd_error_evolution_plot", "magic-state-evolution"),
    ("QEC timeline", "qec_timeline_aggregated", "qec-timeline"),
    ("[[n, k, d]] code parameters", "nkd_plot_aggregated", "nkd"),
    ("QEC experiments per platform (cumulative)", "experiment_counts", "experiment-counts"),
    ("QEC experiments per platform (yearly)", "experiment_counts_yearly", "experiment-counts-yearly"),
    ("QEC experiments per code (cumulative)", "qec_cumulative_growth", "qec-cumulative"),
    ("QEC codes by platform", "qec_platform_sunburst", "qec-sunburst"),
    ("Papers per year, industry vs academia", "papers_by_org_type", "papers-by-org-type"),
    ("Top research groups", "top_research_groups", "top-research-groups"),
    ("Platform rankings per metric (spider charts)", "rankings_radar", "/rankings"),
    ("Q-day estimates: trends vs published requirements", "qday_summary", "/qday"),
    ("Neutral atoms: qubit count vs Shor requirements", "qday_qubits_neutral_atoms", "/qday"),
    ("Superconducting circuits: qubit count vs Shor requirements", "qday_qubits_superconducting_circuits", "/qday"),
    ("Ion traps: qubit count vs Shor requirements", "qday_qubits_ion_traps", "/qday"),
]


class MarkdownGenerator:
    """Generates the complete README.md file."""

    def __init__(self):
        with open("config.yaml") as f:
            self.config = yaml.safe_load(f)

        paths = self.config['paths']['data']
        self.datasets = {key: pd.read_csv(paths[key]) for key, _, _ in DATASETS}
        self.qec_data = self.datasets['qec']
        self.msd_data = self.datasets['msd']
        self.entangled_data = self.datasets['entangled']
        self.qubit_count_data = self.datasets['qubit_count']
        self.physical_qubits_data = self.datasets['physical_qubits']

        self.sections = [
            QECSection(self.qec_data),
            MSDSection(self.msd_data),
            EntangledSection(self.entangled_data),
            QubitCountSection(self.qubit_count_data),
            PhysicalQubitsSection(self.physical_qubits_data),
        ]

    # ------------------------------------------------------------------ public

    def generate(self):
        """Generate the complete README.md content and write it to disk."""
        content = self._generate_header()
        content += self._generate_data_section()
        content += self._generate_plots_section()
        content += self._generate_toc()
        content += self._generate_sections()
        content += self._generate_usage()
        content += self._generate_footer()

        readme_path = Path(self.config['paths']['output']['readme'])
        readme_path.write_text(content)

    # ----------------------------------------------------------------- helpers

    @property
    def total_entries(self) -> int:
        return sum(len(df) for df in self.datasets.values())

    @property
    def total_papers(self) -> int:
        links = pd.concat(df['Link'] for df in self.datasets.values() if 'Link' in df)
        return links.dropna().nunique()

    def _generate_header(self) -> str:
        return f"""# Awesome Quantum Computing Experiments

> A curated, machine-readable database of quantum computing experiments, with an emphasis on quantum error correction. {self.total_entries} entries from {self.total_papers} papers, every one of them a row in a CSV file.

[![CI]({REPO_URL}/actions/workflows/ci.yml/badge.svg)]({REPO_URL}/actions/workflows/ci.yml)
[![arXiv](https://img.shields.io/badge/arXiv-{ARXIV_ID}-b31b1b.svg)](https://arxiv.org/abs/{ARXIV_ID})
[![Entries](https://img.shields.io/badge/entries-{self.total_entries}-blue.svg)](#the-data)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Interactive plots, filterable tables, [platform rankings]({SITE_URL}/rankings) (spider charts, replayable by year) and [research groups]({SITE_URL}/groups) live on the **[website]({SITE_URL})**. This README is generated from the same data by `make readme`.

"""

    def _generate_data_section(self) -> str:
        paths = self.config['paths']['data']
        rows = []
        for key, description, columns in DATASETS:
            path = paths[key]
            name = Path(path).name
            rows.append(f"| [`{name}`]({path}) | {description} | {len(self.datasets[key])} | {columns} |")
        table = "\n".join(rows)
        return f"""## The data

**Everything in this repository comes from five CSV files in [`data/`](data/).** The plots below, the interactive website, and the paper lists further down are all generated from them. To add or fix an experiment, edit a CSV row and open a pull request; CI regenerates the README and the plots.

| File | What it tracks | Entries | Key columns |
|---|---|---:|---|
{table}

Every file also carries `Article Title`, `First Author`, `Link`, `Year`, `Platform` and free-text `Notes`. A sixth file, [`research_groups.csv`](data/research_groups.csv), maps each paper to its research group and organisation type (industry / academic / mixed); it is generated from [OpenAlex](https://openalex.org) by `make groups` and hand-corrected rows are kept. A seventh, [`qday_targets.csv`](data/qday_targets.csv), lists the physical qubit counts and error rates that published resource estimates require to break RSA-2048 or ECC-256, per platform; the [Q-day page]({SITE_URL}/qday) extrapolates each platform's trend to those requirements. The full column reference is in [docs/DOCUMENTATION.md](docs/DOCUMENTATION.md) and the submission rules in [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

"""

    def _generate_plots_section(self) -> str:
        cells = []
        for caption, png, anchor in PLOTS:
            # Anchors starting with "/" are site pages, the rest are home-page sections.
            url = f"{SITE_URL}{anchor}" if anchor.startswith("/") else f"{SITE_URL}/#{anchor}"
            cells.append(
                f"[![{caption}](out/png/{png}.png)]({url})<br>"
                f"**{caption}** ([interactive]({url}))"
            )
        # Two plots per row.
        rows = []
        for i in range(0, len(cells), 2):
            pair = cells[i:i + 2]
            if len(pair) == 1:
                pair.append("")
            rows.append("| " + " | ".join(pair) + " |")
        table = "\n".join(rows)
        return f"""## Plots

Static exports of the interactive website plots. Regenerate them with `make plots` (PNG in `out/png`, PDF in `out/pdf`, figure JSON for the website in `out/figures`).

| | |
|---|---|
{table}

"""

    def _generate_toc(self) -> str:
        """Generate table of contents for the paper lists."""
        content = "## Contents\n\n"
        headings = [
            ("Quantum Error Correction", "quantum-error-correction"),
            ("Magic State", "magic-state"),
            ("Entangled State Error", "entangled-state-error"),
            ("Qubit Count", "qubit-count"),
            ("Physical Qubits", "physical-qubits"),
        ]
        for section, (title, anchor) in zip(self.sections, headings):
            content += f"- [{title}](#{anchor})\n"
            content += section.generate_toc()
        content += "\n"
        return self._deduplicate_anchors(content)

    @staticmethod
    def _deduplicate_anchors(toc: str) -> str:
        """Suffix repeated anchors with -1, -2, ... the way GitHub does.

        The same sub-heading (e.g. "Ion traps") appears under several
        sections; the TOC is in document order so a running count per
        anchor reproduces GitHub's generated ids.
        """
        seen: dict = {}

        def replace(match):
            anchor = match.group(1)
            count = seen.get(anchor, 0)
            seen[anchor] = count + 1
            return f"](#{anchor}-{count})" if count else f"](#{anchor})"

        return re.sub(r"\]\(#([^)]+)\)", replace, toc)

    def _generate_sections(self) -> str:
        return "".join(section.generate_content() for section in self.sections)

    def _generate_usage(self) -> str:
        return f"""
## Quick Start

```bash
git clone {REPO_URL}.git
cd awesome-quantum-computing-experiments
pip install -e ".[test]"
make all        # regenerate plots (out/) and this README
make test       # run the test suite
```

Individual targets: `make plots`, `make readme`, `make export_pdf`. Each plot can also be produced on its own, for example `python -m src.plotting.entangled_error_plot`.

## Local Development

The website is an [Astro](https://astro.build) site in [`site/`](site/). It reads the CSV files in `data/` and the figure JSON in `out/figures/` at build time, so run `make plots` first if the figures are missing.

```bash
cd site
npm install
npm run dev     # http://localhost:4321/awesome-quantum-computing-experiments/
npm run build   # static output in site/dist
```
"""

    def _generate_footer(self) -> str:
        return f"""
## Contributing

Contributions are welcome. Add a row to the relevant CSV in `data/` and open a pull request, or open an issue with the paper link. See the [Contributing Guide](docs/CONTRIBUTING.md).

## Citation

If you use this dataset in your research, please cite:

```bibtex
@unpublished{{leregentAwesomeQuantumComputing2025,
  title = {{Awesome Quantum Computing Experiments: Benchmarking Experimental Progress Towards Fault-Tolerant Quantum Computation}},
  author = {{Le Régent, François-Marie}},
  date = {{2025-07-04}},
  doi = {{10.48550/arXiv.{ARXIV_ID}}},
  url = {{http://arxiv.org/abs/{ARXIV_ID}}},
}}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
"""


def main():
    """Main function to generate the README."""
    generator = MarkdownGenerator()
    generator.generate()


if __name__ == "__main__":
    main()
