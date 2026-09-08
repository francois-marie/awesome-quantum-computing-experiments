import { useMemo, useState } from 'react';
import type { EChartsOption } from 'echarts';
import { EChart } from './EChart';
import { useChartTheme } from '@/hooks/useChartTheme';
import { PLATFORMS, platformColor, type Platform } from '@/lib/data';
import { METRICS, rankings, points, years, type Metric, type Ranking } from '@/lib/metrics';
import { cn } from 'cn';

type View = 'metric' | 'platform';
const WINDOWS = [
  { label: '5 years', value: 5 },
  { label: '10 years', value: 10 },
  { label: 'All time', value: Infinity },
];

const platformsFor = (m: Metric): Platform[] => {
  const present = new Set(points(m).map((p) => p.platform));
  return PLATFORMS.filter((p) => present.has(p));
};

const rateLabel = (m: Metric, r: Ranking) => {
  if (!r.rate) return 'no trend (needs 2 points in window)';
  if (!Number.isFinite(r.rate.doublingTime)) return 'flat';
  const verb = m.better === 'min' ? '÷2' : '×2';
  return r.rate.slope > 0 ? `${verb} every ${r.rate.doublingTime.toFixed(1)} y` : `getting worse (${r.rate.doublingTime.toFixed(1)} y)`;
};

function radarOption(
  indicators: string[],
  series: { name: string; values: number[]; color: string; dashed?: boolean; tips: string[] }[],
  n: number,
  theme: { text: string; muted: string; grid: string; background: string },
): EChartsOption {
  return {
    backgroundColor: 'transparent',
    animationDuration: 300,
    tooltip: {
      trigger: 'item',
      confine: true,
      backgroundColor: theme.background,
      borderColor: theme.grid,
      textStyle: { color: theme.text, fontSize: 12 },
      formatter: (p: { seriesIndex: number; name: string }) => {
        const s = series[p.seriesIndex];
        return `<b>${p.name}</b><br>${s.tips.join('<br>')}`;
      },
    },
    legend: { bottom: 0, textStyle: { color: theme.muted, fontSize: 11 }, itemWidth: 14, icon: 'roundRect' },
    radar: {
      indicator: indicators.map((name) => ({ name, max: n, min: 0 })),
      radius: '62%',
      center: ['50%', '46%'],
      splitNumber: n,
      axisName: { color: theme.text, fontSize: 11 },
      splitLine: { lineStyle: { color: theme.grid } },
      splitArea: { show: false },
      axisLine: { lineStyle: { color: theme.grid } },
    },
    series: series.map((s) => ({
      type: 'radar',
      name: s.name,
      symbolSize: 6,
      data: [{ value: s.values, name: s.name }],
      lineStyle: { color: s.color, width: 2, type: s.dashed ? 'dashed' : 'solid' },
      itemStyle: { color: s.color },
      areaStyle: { color: s.color, opacity: s.dashed ? 0.06 : 0.18 },
    })),
  };
}

export function RadarRankings() {
  const theme = useChartTheme();
  const [view, setView] = useState<View>('metric');
  const [year, setYear] = useState(years.max);
  const [window, setWindow] = useState(10);

  const table = useMemo(
    () => METRICS.map((m) => ({ metric: m, platforms: platformsFor(m), rows: rankings(m, year, window, platformsFor(m)) })),
    [year, window],
  );

  // Rank -> radial value so rank 1 sits on the outer ring.
  const score = (rank: number, n: number) => n + 1 - rank;

  const metricCards = table.map(({ metric, platforms, rows }) => {
    const n = platforms.length;
    const byPlatform = new Map(rows.map((r) => [r.platform, r]));
    const ordered = platforms.map((p) => byPlatform.get(p)!);
    const option = radarOption(
      platforms,
      [
        {
          name: `Best value (as of ${year})`,
          color: '#2563eb',
          values: ordered.map((r) => (r.best ? score(r.bestRank, n) : 0)),
          tips: ordered.map((r) => (r.best ? `#${r.bestRank} best: ${metric.format(r.best.value)} (${r.best.year})` : 'no data yet')),
        },
        {
          name: `Improvement rate (last ${Number.isFinite(window) ? `${window} y` : 'all years'})`,
          color: '#f97316',
          dashed: true,
          values: ordered.map((r) => (r.rate ? score(r.rateRank, n) : 0)),
          tips: ordered.map((r) => `#${r.rateRank} pace: ${rateLabel(metric, r)}`),
        },
      ],
      n,
      theme,
    );
    return { metric, option, rows: [...rows].sort((a, b) => a.bestRank - b.bestRank) };
  });

  const platformCards = PLATFORMS.map((platform) => {
    const rel = table.filter((t) => t.platforms.includes(platform));
    if (rel.length < 3) return null;
    const rows = rel.map((t) => t.rows.find((r) => r.platform === platform)!);
    // Axes have different platform counts, so rescale each to the shared max:
    // rank 1 always lands on the outer ring whatever the field size.
    const axisMax = Math.max(...rel.map((t) => t.platforms.length));
    const scaled = (rank: number, i: number) => (score(rank, rel[i].platforms.length) / rel[i].platforms.length) * axisMax;
    const option = radarOption(
      rel.map((t) => t.metric.short),
      [
        {
          name: 'Rank on best value',
          color: platformColor(platform),
          values: rows.map((r, i) => (r.best ? scaled(r.bestRank, i) : 0)),
          tips: rows.map((r, i) => `${rel[i].metric.label}: #${r.bestRank} of ${rel[i].platforms.length}${r.best ? ` (${rel[i].metric.format(r.best.value)})` : ''}`),
        },
        {
          name: 'Rank on improvement rate',
          color: '#f97316',
          dashed: true,
          values: rows.map((r, i) => (r.rate ? scaled(r.rateRank, i) : 0)),
          tips: rows.map((r, i) => `${rel[i].metric.label}: #${r.rateRank} pace, ${rateLabel(rel[i].metric, r)}`),
        },
      ],
      axisMax,
      theme,
    );
    return { platform, option };
  });

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center gap-x-6 gap-y-3 rounded-xl border bg-card p-4 text-sm">
        <div className="flex items-center gap-1 rounded-lg bg-muted p-0.5" role="tablist">
          {(['metric', 'platform'] as View[]).map((v) => (
            <button
              key={v}
              role="tab"
              aria-selected={view === v}
              onClick={() => setView(v)}
              className={cn('rounded-md px-3 py-1 transition-colors', view === v ? 'bg-background shadow-sm' : 'text-muted-foreground hover:text-foreground')}
            >
              {v === 'metric' ? 'One radar per metric' : 'One radar per platform'}
            </button>
          ))}
        </div>
        <label className="flex items-center gap-3">
          <span className="text-muted-foreground">State of the art as of</span>
          <input
            type="range"
            min={years.min + 5}
            max={years.max}
            value={year}
            onChange={(e) => setYear(Number(e.target.value))}
            className="w-40 accent-foreground"
          />
          <span className="w-10 font-semibold tabular-nums">{year}</span>
        </label>
        <label className="flex items-center gap-2">
          <span className="text-muted-foreground">Rate window</span>
          <select value={window} onChange={(e) => setWindow(Number(e.target.value))} className="h-8 rounded-md border bg-background px-2">
            {WINDOWS.map((w) => (
              <option key={w.label} value={w.value}>
                {w.label}
              </option>
            ))}
          </select>
        </label>
      </div>

      {view === 'metric' ? (
        <div className="grid gap-4 md:grid-cols-2">
          {metricCards.map(({ metric, option, rows }) => (
            <section key={metric.key} className="rounded-xl border bg-card p-4">
              <h3 className="font-semibold">{metric.label}</h3>
              <p className="text-xs text-muted-foreground">
                Outer ring is rank 1. Solid: best value{metric.aggregate === 'count' ? ' (count)' : ''}. Dashed: improvement rate.
              </p>
              <EChart option={option} height={330} ariaLabel={`${metric.label} platform ranking`} />
              <ol className="mt-1 grid grid-cols-1 gap-x-4 gap-y-0.5 text-xs sm:grid-cols-2">
                {rows.map((r) => (
                  <li key={r.platform} className="flex items-baseline gap-1.5 tabular-nums">
                    <span className="w-5 text-muted-foreground">#{r.bestRank}</span>
                    <span className="inline-block size-2 shrink-0 translate-y-[-1px] rounded-full" style={{ background: platformColor(r.platform) }} />
                    <span className="truncate">{r.platform}</span>
                    <span className="ml-auto text-muted-foreground">{r.best ? metric.format(r.best.value) : '—'}</span>
                  </li>
                ))}
              </ol>
            </section>
          ))}
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {platformCards.map((c) =>
            c ? (
              <section key={c.platform} className="rounded-xl border bg-card p-4">
                <h3 className="flex items-center gap-2 font-semibold">
                  <span className="inline-block size-2.5 rounded-full" style={{ background: platformColor(c.platform) }} />
                  {c.platform}
                </h3>
                <p className="text-xs text-muted-foreground">Outer ring is rank 1 among the platforms with data on that metric.</p>
                <EChart option={c.option} height={330} ariaLabel={`${c.platform} ranking across metrics`} />
              </section>
            ) : null,
          )}
        </div>
      )}
    </div>
  );
}
