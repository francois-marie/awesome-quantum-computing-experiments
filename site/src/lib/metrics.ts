/**
 * Metric definitions shared by the records board, the rankings radar and the
 * milestone estimates. A metric maps CSV rows to one number per row (or counts
 * rows) and says which direction is better.
 */
import { datasets, canonicalPlatform, num, leadingNumber, maxDistance, type Row, type Platform, PLATFORMS } from './data';

export interface Metric {
  key: string;
  label: string;
  short: string;
  unit?: string;
  dataset: keyof typeof datasets;
  /** Value for one row, or null if the row has no such measurement. */
  value: (row: Row) => number | null;
  /** 'count' metrics sum one per row instead of taking the best row. */
  aggregate: 'best' | 'count';
  better: 'min' | 'max';
  /** Fit trends in log space (all physical metrics span decades). */
  log: boolean;
  format: (v: number) => string;
}

const sci = (v: number) => (v >= 1e-2 && v < 1e4 ? v.toPrecision(3).replace(/\.?0+$/, '') : v.toExponential(2));
const seconds = (v: number) => {
  if (v >= 1) return `${sci(v)} s`;
  if (v >= 1e-3) return `${sci(v * 1e3)} ms`;
  if (v >= 1e-6) return `${sci(v * 1e6)} µs`;
  return `${sci(v * 1e9)} ns`;
};

export const METRICS: Metric[] = [
  {
    key: 'entangled_error',
    label: 'Entangled state error',
    short: '2Q error',
    dataset: 'entangled',
    value: (r) => num(r['Entangled State Error']),
    aggregate: 'best',
    better: 'min',
    log: true,
    format: sci,
  },
  {
    key: 'qubit_count',
    label: 'Qubit count',
    short: 'Qubits',
    dataset: 'qubit_count',
    value: (r) => num(r['Number of qubits']),
    aggregate: 'best',
    better: 'max',
    log: true,
    format: (v) => v.toLocaleString('en-US'),
  },
  {
    key: 't1',
    label: 'Relaxation time T1',
    short: 'T1',
    dataset: 'physical_qubits',
    value: (r) => num(r.T1),
    aggregate: 'best',
    better: 'max',
    log: true,
    format: seconds,
  },
  {
    key: 't2',
    label: 'Coherence time T2',
    short: 'T2',
    dataset: 'physical_qubits',
    value: (r) => num(r.T2),
    aggregate: 'best',
    better: 'max',
    log: true,
    format: seconds,
  },
  {
    key: 'qec_distance',
    label: 'Largest QEC code distance',
    short: 'Distance',
    dataset: 'qec',
    value: (r) => maxDistance(r['Code Parameters']),
    aggregate: 'best',
    better: 'max',
    log: false,
    format: (v) => `d = ${v}`,
  },
  {
    key: 'qec_count',
    label: 'QEC experiments',
    short: 'QEC exps',
    dataset: 'qec',
    value: () => 1,
    aggregate: 'count',
    better: 'max',
    log: false,
    format: (v) => `${v}`,
  },
  {
    key: 'magic_error',
    label: 'Magic state error',
    short: 'Magic error',
    dataset: 'msd',
    value: (r) => {
      const f = leadingNumber(r.Fidelity);
      return f === null || f >= 1 ? null : 1 - f;
    },
    aggregate: 'best',
    better: 'min',
    log: true,
    format: sci,
  },
];

export const metricByKey = (key: string) => METRICS.find((m) => m.key === key)!;

export interface Point {
  year: number;
  value: number;
  platform: Platform;
  title: string;
  link: string;
  author: string;
  row: Row;
}

/** All rows of a metric with a usable value, oldest first. */
export function points(metric: Metric): Point[] {
  return datasets[metric.dataset].rows
    .map((row) => {
      const value = metric.value(row);
      const year = num(row.Year);
      const platform = canonicalPlatform(row.Platform ?? '');
      if (value === null || year === null || !platform) return null;
      return { year, value, platform, title: row['Article Title'], link: row.Link, author: row['First Author'], row };
    })
    .filter((p): p is Point => p !== null)
    .sort((a, b) => a.year - b.year || a.title.localeCompare(b.title));
}

const isBetter = (m: Metric, a: number, b: number) => (m.better === 'min' ? a < b : a > b);

/** Best value per platform using rows up to and including `year`. */
export function bestAsOf(metric: Metric, year = Infinity): Map<Platform, Point & { value: number }> {
  const out = new Map<Platform, Point>();
  for (const p of points(metric)) {
    if (p.year > year) continue;
    const cur = out.get(p.platform);
    if (metric.aggregate === 'count') {
      out.set(p.platform, cur ? { ...p, value: cur.value + 1 } : { ...p, value: 1 });
    } else if (!cur || isBetter(metric, p.value, cur.value)) {
      out.set(p.platform, p);
    }
  }
  return out;
}

/** Chronological chain of record holders across all platforms. */
export function recordHistory(metric: Metric): Point[] {
  const chain: Point[] = [];
  if (metric.aggregate === 'count') return chain;
  for (const p of points(metric)) {
    const last = chain[chain.length - 1];
    if (!last || isBetter(metric, p.value, last.value)) chain.push(p);
  }
  return chain;
}

// -------------------------------------------------------------------- trends

export interface Fit {
  slope: number; // per year, in log10 units when metric.log
  intercept: number;
  n: number;
  /** Years for the metric to halve (min metrics) or double (max metrics). Infinity if flat. */
  doublingTime: number;
}

/** Ordinary least squares, identical to the scipy.stats.linregress fits used for the PNG plots. */
export function fit(metric: Metric, pts: { year: number; value: number }[]): Fit | null {
  const xs = pts.map((p) => p.year);
  const ys = pts.map((p) => (metric.log ? Math.log10(p.value) : p.value));
  const n = xs.length;
  if (n < 2 || new Set(xs).size < 2) return null;
  const mx = xs.reduce((a, b) => a + b, 0) / n;
  const my = ys.reduce((a, b) => a + b, 0) / n;
  let sxx = 0;
  let sxy = 0;
  for (let i = 0; i < n; i++) {
    sxx += (xs[i] - mx) ** 2;
    sxy += (xs[i] - mx) * (ys[i] - my);
  }
  const slope = sxy / sxx;
  const intercept = my - slope * mx;
  const doublingTime = slope === 0 ? Infinity : Math.abs(Math.log10(2) / slope);
  return { slope, intercept, n, doublingTime };
}

/**
 * Improvement rate of a platform as of `year`, fitted on rows from the last
 * `window` years. Positive means moving in the "better" direction; units are
 * decades per year for log metrics.
 */
export function improvementRate(metric: Metric, platform: Platform, year = Infinity, window = Infinity): Fit | null {
  let pts = points(metric).filter((p) => p.platform === platform && p.year <= year && p.year > year - window);
  if (metric.aggregate === 'count') {
    // Cumulative count over time is the trend for count metrics.
    let acc = 0;
    pts = pts.map((p) => ({ ...p, value: ++acc }));
  }
  const f = fit(metric, pts);
  if (!f) return null;
  return metric.better === 'min' ? { ...f, slope: -f.slope } : f;
}

export interface Ranking {
  platform: Platform;
  best: Point | null;
  bestRank: number;
  rate: Fit | null;
  rateRank: number;
}

/** Rank platforms on current best value and on improvement rate. Rank 1 is best; missing data ranks last. */
export function rankings(metric: Metric, year = Infinity, window = Infinity, platforms: readonly Platform[] = PLATFORMS): Ranking[] {
  const best = bestAsOf(metric, year);
  const rows = platforms.map((platform) => ({
    platform,
    best: best.get(platform) ?? null,
    rate: improvementRate(metric, platform, year, window),
  }));
  const byBest = [...rows].sort((a, b) => {
    if (!a.best && !b.best) return 0;
    if (!a.best) return 1;
    if (!b.best) return -1;
    return isBetter(metric, a.best.value, b.best.value) ? -1 : a.best.value === b.best.value ? 0 : 1;
  });
  const byRate = [...rows].sort((a, b) => {
    if (!a.rate && !b.rate) return 0;
    if (!a.rate) return 1;
    if (!b.rate) return -1;
    return b.rate.slope - a.rate.slope;
  });
  return rows.map((r) => ({
    ...r,
    bestRank: byBest.findIndex((x) => x.platform === r.platform) + 1,
    rateRank: byRate.findIndex((x) => x.platform === r.platform) + 1,
  }));
}

/** Year at which the all-time trend of `platform` reaches `target`, or null if it never does. */
export function milestoneYear(metric: Metric, platform: Platform, target: number): number | null {
  const pts = points(metric).filter((p) => p.platform === platform);
  const f = fit(metric, pts);
  if (!f || f.slope === 0) return null;
  const y = metric.log ? Math.log10(target) : target;
  const year = (y - f.intercept) / f.slope;
  const last = Math.max(...pts.map((p) => p.year));
  return Number.isFinite(year) && year >= last - 1 ? year : null;
}

export const years = (() => {
  const all = METRICS.flatMap((m) => points(m).map((p) => p.year));
  return { min: Math.min(...all), max: Math.max(...all) };
})();
