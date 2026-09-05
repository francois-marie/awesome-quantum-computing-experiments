/**
 * Figure JSON produced by `make plots` (see `BasePlot.export_to_figure_json`).
 * The files are committed in `out/figures/` so the site builds without Python.
 */
import type { Figure } from './figure';
import type { DatasetKey } from './data';

const modules = import.meta.glob<{ default: Figure }>('../../../out/figures/*.json', { eager: true });

export const figuresByName: Record<string, Figure> = Object.fromEntries(
  Object.values(modules).map((m) => [m.default.name, m.default]),
);

export interface FigureMeta {
  name: string;
  anchor: string;
  title: string;
  description: string;
  /** Dataset the figure is built from; undefined for figures built from research_groups.csv. */
  dataset?: DatasetKey;
  /** Per-platform dashboard: can this figure be filtered to one platform? */
  perPlatform: boolean;
  /** Section on the home page. */
  section: 'metrics' | 'qec' | 'groups';
}

export const FIGURES: FigureMeta[] = [
  {
    name: 'entangled_error_plot',
    anchor: 'entangled-state-error',
    title: 'Entangled state error',
    description: 'Bell-state and two-qubit gate error versus year, with an exponential fit per platform.',
    dataset: 'entangled',
    perPlatform: true,
    section: 'metrics',
  },
  {
    name: 'qubit_count_plot',
    anchor: 'qubit-count',
    title: 'Qubit count',
    description: 'Largest number of physical qubits controlled in one experiment, per platform.',
    dataset: 'qubit_count',
    perPlatform: true,
    section: 'metrics',
  },
  {
    name: 'coherence_times_plot',
    anchor: 'coherence-times',
    title: 'Coherence times',
    description: 'T1 (filled) and T2 (hollow) of physical qubits over time.',
    dataset: 'physical_qubits',
    perPlatform: true,
    section: 'metrics',
  },
  {
    name: 'msd_plot',
    anchor: 'magic-state',
    title: 'Magic state error vs acceptance rate',
    description: 'Logical magic state infidelity against the acceptance rate of the preparation or distillation protocol.',
    dataset: 'msd',
    perPlatform: true,
    section: 'metrics',
  },
  {
    name: 'msd_error_evolution_plot',
    anchor: 'magic-state-evolution',
    title: 'Magic state error over time',
    description: 'Logical magic state infidelity versus year, with error bars from the reported confidence intervals.',
    dataset: 'msd',
    perPlatform: true,
    section: 'metrics',
  },
  {
    name: 'qec_timeline_aggregated',
    anchor: 'qec-timeline',
    title: 'QEC timeline',
    description: 'Every quantum error correction experiment by year and code family. Marker size is the number of experiments.',
    dataset: 'qec',
    perPlatform: true,
    section: 'qec',
  },
  {
    name: 'nkd_plot_aggregated',
    anchor: 'nkd',
    title: '[[n, k, d]] code parameters',
    description: 'Code distance against number of physical qubits for every implemented code.',
    dataset: 'qec',
    perPlatform: false,
    section: 'qec',
  },
  {
    name: 'qec_data_qubit_count_plot',
    anchor: 'qec-data-qubits',
    title: 'Data qubits in QEC experiments',
    description: 'Number of data qubits used in QEC experiments per platform over time.',
    dataset: 'qec',
    perPlatform: true,
    section: 'qec',
  },
  {
    name: 'experiment_counts',
    anchor: 'experiment-counts',
    title: 'QEC experiments per platform, cumulative',
    description: 'Running total of QEC experiments by platform.',
    dataset: 'qec',
    perPlatform: true,
    section: 'qec',
  },
  {
    name: 'experiment_counts_yearly',
    anchor: 'experiment-counts-yearly',
    title: 'QEC experiments per platform, yearly',
    description: 'QEC experiments published each year, stacked by platform.',
    dataset: 'qec',
    perPlatform: true,
    section: 'qec',
  },
  {
    name: 'qec_cumulative_growth',
    anchor: 'qec-cumulative',
    title: 'QEC experiments per code, cumulative',
    description: 'Running total of experiments by code family.',
    dataset: 'qec',
    perPlatform: false,
    section: 'qec',
  },
  {
    name: 'qec_platform_sunburst',
    anchor: 'qec-sunburst',
    title: 'QEC codes by platform',
    description: 'Share of each code family and, within it, of each platform.',
    dataset: 'qec',
    perPlatform: false,
    section: 'qec',
  },
  {
    name: 'papers_by_org_type',
    anchor: 'papers-by-org-type',
    title: 'Papers per year, industry vs academia',
    description: "Unique papers in the database by publication year and by the first author's organisation type.",
    perPlatform: false,
    section: 'groups',
  },
  {
    name: 'top_research_groups',
    anchor: 'top-research-groups',
    title: 'Top research groups',
    description: 'Groups with the most papers in the database, coloured by organisation type. Hover for the per-dataset breakdown.',
    perPlatform: false,
    section: 'groups',
  },
];

export const SECTIONS: { key: FigureMeta['section']; title: string; blurb: string }[] = [
  { key: 'metrics', title: 'Hardware metrics', blurb: 'Two-qubit error, qubit count, coherence and magic states over time.' },
  { key: 'qec', title: 'Quantum error correction', blurb: 'Which codes were implemented, where, and how large.' },
  { key: 'groups', title: 'Who does the work', blurb: 'Research groups and the industry versus academia split.' },
];

export const figureMeta = (name: string) => FIGURES.find((f) => f.name === name);
