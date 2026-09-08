# Documentation

## Data Files

The project uses several CSV files to store experiment data:

### 1. QEC Experiments (`data/qec_exp.csv`)
- Article Title
- Link
- Year
- Platform
- Code Parameters
- Code Name
- Notes

### 2. Magic State Distillation (`data/msd_exp.csv`)
- Article Title
- Link
- Year
- Platform
- Notes

### 3. Entangled State Error (`data/entangled_state_error_exp.csv`)
- Article Title
- Link
- Year
- Platform
- Entangled State Error
- Notes

### 4. Qubit Count (`data/qubit_count.csv`)
- Article Title
- Link
- Year
- Platform
- Number of qubits
- Notes

### 5. Coherence Times (`data/physical_qubits.csv`)
- Article Title
- Link
- Year
- Platform
- Code Name (qubit type, e.g. Transmon, Fluxonium)
- Physical system
- T1, T2 (seconds)
- Notes

### 6. Research Groups (`data/research_groups.csv`, generated)
One row per unique paper link, produced by `make groups` (`scripts/fetch_research_groups.py`)
from OpenAlex: `Research Group`, `Institutions`, `Org Type` (industry / academic / mixed),
`Country`, `Source`. Rows with `Source = manual` are never overwritten, so fix a wrong
affiliation by editing the row and setting `Source` to `manual`.

## Website

The site in `site/` is an [Astro](https://astro.build) app (React islands, Tailwind, shadcn/ui,
Apache ECharts). It reads the CSV files and the figure JSON in `out/figures/` at build time:

```bash
make plots        # writes out/figures/*.json (plus PNG and PDF)
cd site && npm install && npm run dev
```

Plot *content* (traces, fits, legend groups, hover text) is defined once in `src/plotting`
and exported by `BasePlot.export_to_figure_json`; the site only restyles it
(`site/src/lib/figure.ts`). Rankings, records and milestone estimates are computed in
`site/src/lib/metrics.ts` from the CSVs.

## Generating Plots

### Individual Plots

Each plot can be generated separately:

```bash
# Generate qubit count evolution plot
python -m src.plotting.qubit_count_plot

# Generate entangled error plot
python -m src.plotting.entangled_error_plot

# Generate QEC time evolution plot
python -m src.plotting.qec_time_plot

# Generate NKD plot
python -m src.plotting.nkd_plot
```

### All Plots

Use the Makefile to generate all plots:

```bash
make plots
```

## Generating README

The README.md file is automatically generated from the data:

```bash
make readme
```

## Configuration

The `config.yaml` file contains all configuration settings:

- File paths
- Plot settings
- Visual style parameters

## Development

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_plotting.py

# Run with coverage
pytest --cov=src tests/
```

### Code Structure

#### Plotting Classes
- `BasePlot`: Abstract base class for all plots
- `QubitCountPlot`: Qubit count evolution plot
- `EntangledErrorPlot`: Entangled state error plot
- `QECTimePlot`: QEC implementation timeline
- `NKDPlot`: [n,k,d] parameter space plot

#### Markdown Generation
- `BaseSection`: Base class for markdown sections
- `ExperimentSection`: Base class for experiment sections
- `MarkdownGenerator`: Main class for README generation 