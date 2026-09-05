/**
 * Research groups behind each paper, from `data/research_groups.csv`
 * (built by `scripts/fetch_research_groups.py` from OpenAlex, with manual
 * overrides). Joined to every dataset row on the paper link.
 */
import Papa from 'papaparse';
import groupsRaw from '../../../data/research_groups.csv?raw';
import { datasets, DATASET_KEYS, canonicalPlatform, num, config, type DatasetKey, type Platform } from './data';
import { METRICS, recordHistory } from './metrics';

export type OrgType = 'industry' | 'academic' | 'mixed' | 'unknown';

export interface GroupInfo {
  link: string;
  group: string;
  institutions: string[];
  orgType: OrgType;
  country: string;
  source: string;
}

const parsed = Papa.parse<Record<string, string>>(groupsRaw, { header: true, skipEmptyLines: true }).data;

export const groupByLink = new Map<string, GroupInfo>(
  parsed.map((r) => [
    r.Link.trim(),
    {
      link: r.Link.trim(),
      group: (r['Research Group'] || '').trim() || 'Unknown',
      institutions: (r.Institutions || '').split(';').map((s) => s.trim()).filter(Boolean),
      orgType: ((r['Org Type'] || '').trim() || 'unknown') as OrgType,
      country: (r.Country || '').trim(),
      source: (r.Source || '').trim(),
    },
  ]),
);

const orgColors = (config as unknown as { org_type_colors?: Record<string, string> }).org_type_colors ?? {};
export const ORG_TYPES: { key: OrgType; label: string; color: string }[] = [
  { key: 'industry', label: 'Industry', color: orgColors.industry ?? '#2563eb' },
  { key: 'academic', label: 'Academic', color: orgColors.academic ?? '#16a34a' },
  { key: 'mixed', label: 'Mixed', color: orgColors.mixed ?? '#f59e0b' },
  { key: 'unknown', label: 'Unknown', color: orgColors.unknown ?? '#a3a3a3' },
];

export interface GroupSummary {
  group: string;
  orgType: OrgType;
  country: string;
  papers: number;
  entries: number;
  byDataset: Record<DatasetKey, number>;
  platforms: Platform[];
  records: { metric: string; value: string; year: number }[];
  firstYear: number;
  lastYear: number;
}

const currentRecords = METRICS.filter((m) => m.aggregate === 'best').map((m) => {
  const chain = recordHistory(m);
  const r = chain[chain.length - 1];
  return { metric: m, point: r };
});

export function groupSummaries(): GroupSummary[] {
  const acc = new Map<string, GroupSummary & { links: Set<string>; platformSet: Set<Platform> }>();
  for (const key of DATASET_KEYS) {
    for (const row of datasets[key].rows) {
      const info = groupByLink.get((row.Link || '').trim());
      const name = info?.group || 'Unknown';
      let g = acc.get(name);
      if (!g) {
        g = {
          group: name,
          orgType: info?.orgType ?? 'unknown',
          country: info?.country ?? '',
          papers: 0,
          entries: 0,
          byDataset: { qec: 0, msd: 0, entangled: 0, qubit_count: 0, physical_qubits: 0 },
          platforms: [],
          records: [],
          firstYear: Infinity,
          lastYear: -Infinity,
          links: new Set(),
          platformSet: new Set(),
        };
        acc.set(name, g);
      }
      g.entries += 1;
      g.byDataset[key] += 1;
      if (row.Link) g.links.add(row.Link.trim());
      const p = canonicalPlatform(row.Platform || '');
      if (p) g.platformSet.add(p);
      const y = num(row.Year);
      if (y !== null) {
        g.firstYear = Math.min(g.firstYear, y);
        g.lastYear = Math.max(g.lastYear, y);
      }
    }
  }
  return [...acc.values()]
    .map((g) => ({
      ...g,
      papers: g.links.size,
      platforms: [...g.platformSet],
      records: currentRecords
        .filter(({ point }) => point && g.links.has(point.link.trim()))
        .map(({ metric, point }) => ({ metric: metric.label, value: metric.format(point.value), year: point.year })),
    }))
    .sort((a, b) => b.papers - a.papers || b.entries - a.entries || a.group.localeCompare(b.group));
}

/** Unique papers per year split by organisation type. */
export function papersPerYearByOrgType(): { years: number[]; series: Record<OrgType, number[]> } {
  const seen = new Map<string, { year: number; orgType: OrgType }>();
  for (const key of DATASET_KEYS) {
    for (const row of datasets[key].rows) {
      const link = (row.Link || '').trim();
      const year = num(row.Year);
      if (!link || year === null || seen.has(link)) continue;
      seen.set(link, { year, orgType: groupByLink.get(link)?.orgType ?? 'unknown' });
    }
  }
  const ys = [...seen.values()].map((v) => v.year);
  const years = Array.from({ length: Math.max(...ys) - Math.min(...ys) + 1 }, (_, i) => Math.min(...ys) + i);
  const series = { industry: [], academic: [], mixed: [], unknown: [] } as Record<OrgType, number[]>;
  for (const t of Object.keys(series) as OrgType[]) series[t] = years.map((y) => [...seen.values()].filter((v) => v.year === y && v.orgType === t).length);
  return { years, series };
}

export function recordsByOrgType(): Record<OrgType, number> {
  const out: Record<OrgType, number> = { industry: 0, academic: 0, mixed: 0, unknown: 0 };
  for (const { point } of currentRecords) if (point) out[groupByLink.get(point.link.trim())?.orgType ?? 'unknown'] += 1;
  return out;
}
