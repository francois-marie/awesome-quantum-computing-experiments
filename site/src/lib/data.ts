/**
 * Build-time access to the CSV files in `data/`.
 *
 * Every table, record card and ranking on the site derives from these five
 * files. Nothing here is fetched at runtime: Vite inlines the CSV text and the
 * parsing happens once at build time (or in the dev server).
 */
import Papa from 'papaparse';
import { load as loadYaml } from 'js-yaml';

import qecRaw from '../../../data/qec_exp.csv?raw';
import msdRaw from '../../../data/msd_exp.csv?raw';
import entangledRaw from '../../../data/entangled_state_error_exp.csv?raw';
import qubitCountRaw from '../../../data/qubit_count.csv?raw';
import physicalQubitsRaw from '../../../data/physical_qubits.csv?raw';
import configRaw from '../../../config.yaml?raw';

export type Row = Record<string, string>;

export interface Dataset {
  key: DatasetKey;
  file: string;
  title: string;
  description: string;
  rows: Row[];
  columns: string[];
}

export type DatasetKey = 'qec' | 'msd' | 'entangled' | 'qubit_count' | 'physical_qubits';

function parse(raw: string): Row[] {
  const { data } = Papa.parse<Row>(raw, { header: true, skipEmptyLines: true });
  return data.map((row) => {
    const clean: Row = {};
    for (const [k, v] of Object.entries(row)) clean[k.trim().replace(/^"|"$/g, '')] = (v ?? '').trim();
    return clean;
  });
}

const DATASET_META: Record<DatasetKey, Omit<Dataset, 'rows' | 'columns' | 'key'>> = {
  qec: {
    file: 'qec_exp.csv',
    title: 'Quantum error correction',
    description: 'Implementations of QEC codes: code, [[n,k,d]] parameters, platform, rounds and more.',
  },
  msd: {
    file: 'msd_exp.csv',
    title: 'Magic states',
    description: 'Magic state preparation, distillation and code switching, with fidelity and acceptance rate.',
  },
  entangled: {
    file: 'entangled_state_error_exp.csv',
    title: 'Entangled state error',
    description: 'Bell-state and two-qubit gate errors over time.',
  },
  qubit_count: {
    file: 'qubit_count.csv',
    title: 'Qubit count',
    description: 'Physical qubit count records per platform.',
  },
  physical_qubits: {
    file: 'physical_qubits.csv',
    title: 'Coherence times',
    description: 'T1 and T2 of physical qubits.',
  },
};

const RAW: Record<DatasetKey, string> = {
  qec: qecRaw,
  msd: msdRaw,
  entangled: entangledRaw,
  qubit_count: qubitCountRaw,
  physical_qubits: physicalQubitsRaw,
};

export const DATASET_KEYS: DatasetKey[] = ['qec', 'msd', 'entangled', 'qubit_count', 'physical_qubits'];

export const datasets: Record<DatasetKey, Dataset> = Object.fromEntries(
  DATASET_KEYS.map((key) => {
    const rows = parse(RAW[key]);
    const columns = rows.length ? Object.keys(rows[0]) : [];
    return [key, { key, ...DATASET_META[key], rows, columns }];
  }),
) as Record<DatasetKey, Dataset>;

export const config = loadYaml(configRaw) as {
  platform_colors: Record<string, string>;
  code_colors: Record<string, string>;
};

// ---------------------------------------------------------------- platforms

/** Canonical platform names. The CSVs use several spellings for the same thing. */
export const PLATFORMS = [
  'Superconducting circuits',
  'Ion traps',
  'Neutral atoms',
  'Semiconductor spins',
  'Photons',
  'NV centers',
  'NMR',
  'Graphene',
] as const;
export type Platform = (typeof PLATFORMS)[number];

export function canonicalPlatform(name: string): Platform | null {
  const n = name.toLowerCase();
  if (n.includes('supercond')) return 'Superconducting circuits';
  if (n.includes('ion')) return 'Ion traps';
  if (n.includes('neutral') || n.includes('atom')) return 'Neutral atoms';
  if (n.includes('semicond') || n.includes('spin') || n.includes('silicon')) return 'Semiconductor spins';
  if (n.includes('photon')) return 'Photons';
  if (n.includes('nv')) return 'NV centers';
  if (n.includes('nmr')) return 'NMR';
  if (n.includes('graphene')) return 'Graphene';
  return null;
}

export function platformColor(name: string): string {
  const colors = config.platform_colors;
  if (colors[name]) return colors[name];
  const canonical = canonicalPlatform(name);
  if (!canonical) return '#888888';
  for (const [k, v] of Object.entries(colors)) if (canonicalPlatform(k) === canonical) return v;
  return '#888888';
}

// ------------------------------------------------------------------ helpers

export const num = (v: string | undefined): number | null => {
  if (v === undefined || v === '') return null;
  const x = Number(v);
  return Number.isFinite(x) ? x : null;
};

/** "0.994-4+3" -> 0.994; "<25%" -> 25 */
export const leadingNumber = (v: string | undefined): number | null => {
  if (!v) return null;
  const m = v.match(/-?\d+(?:\.\d+)?(?:e-?\d+)?/i);
  return m ? Number(m[0]) : null;
};

/** "[[25, 1, 5]]" or "[3,1,3]-[29,1,29]" -> largest distance found. */
export function maxDistance(params: string | undefined): number | null {
  if (!params) return null;
  const matches = [...params.matchAll(/\[\[?\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]?\]/g)];
  if (!matches.length) return null;
  const single = !params.startsWith('[[');
  // Repetition codes written [n,1,n] with single brackets detect only one error type.
  return Math.max(...matches.map((m) => (single ? Number(m[3]) : Number(m[3]))));
}

export const totals = {
  entries: DATASET_KEYS.reduce((s, k) => s + datasets[k].rows.length, 0),
  papers: new Set(DATASET_KEYS.flatMap((k) => datasets[k].rows.map((r) => r.Link).filter(Boolean))).size,
  platforms: new Set(
    DATASET_KEYS.flatMap((k) => datasets[k].rows.map((r) => canonicalPlatform(r.Platform ?? '')).filter(Boolean)),
  ).size,
  latestYear: Math.max(...DATASET_KEYS.flatMap((k) => datasets[k].rows.map((r) => num(r.Year) ?? 0))),
};
