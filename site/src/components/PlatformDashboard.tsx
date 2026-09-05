import { useEffect, useMemo, useState } from 'react';
import { FigureChart } from './FigureChart';
import { FIGURES, figuresByName } from '@/lib/figures';
import { PLATFORMS, platformColor, canonicalPlatform, datasets, DATASET_KEYS, type Platform } from '@/lib/data';
import { METRICS, bestAsOf, rankings } from '@/lib/metrics';
import { cn } from 'cn';

const slug = (p: string) => p.toLowerCase().replace(/[^a-z0-9]+/g, '-');

/** Which platforms actually appear in a figure (by legend/trace names). */
function platformsIn(name: string): Set<Platform> {
  const fig = figuresByName[name];
  const out = new Set<Platform>();
  fig?.data.forEach((t) => {
    const fromGroup = t.legendgroup && !t.legendgroup.startsWith('header_') ? canonicalPlatform(t.legendgroup.replace(/^data_/, '')) : null;
    const p = fromGroup ?? (t.name ? canonicalPlatform(t.name) : null);
    if (p && (t.x ?? []).some((v) => v !== null)) out.add(p);
  });
  return out;
}

const counts = Object.fromEntries(
  PLATFORMS.map((p) => [p, DATASET_KEYS.reduce((s, k) => s + datasets[k].rows.filter((r) => canonicalPlatform(r.Platform ?? '') === p).length, 0)]),
) as Record<Platform, number>;

export function PlatformDashboard() {
  const available = PLATFORMS.filter((p) => counts[p] > 0);
  const [platform, setPlatform] = useState<Platform>(available[0]);

  // Deep link: /platforms#neutral-atoms
  useEffect(() => {
    const fromHash = () => {
      const h = decodeURIComponent(location.hash.replace('#', ''));
      const match = available.find((p) => slug(p) === h);
      if (match) setPlatform(match);
    };
    fromHash();
    window.addEventListener('hashchange', fromHash);
    return () => window.removeEventListener('hashchange', fromHash);
  }, []);

  const select = (p: Platform) => {
    setPlatform(p);
    history.replaceState(null, '', `#${slug(p)}`);
  };

  const figures = useMemo(() => FIGURES.filter((f) => f.perPlatform && platformsIn(f.name).has(platform)), [platform]);
  const color = platformColor(platform);

  const summary = METRICS.map((m) => {
    const best = bestAsOf(m).get(platform);
    const rank = rankings(m).find((r) => r.platform === platform);
    return { metric: m, best, rank };
  }).filter((s) => s.best);

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-wrap gap-2" role="tablist">
        {available.map((p) => (
          <button
            key={p}
            role="tab"
            aria-selected={p === platform}
            onClick={() => select(p)}
            className={cn(
              'inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-sm transition-colors hover:bg-muted',
              p === platform && 'border-foreground bg-foreground text-background hover:bg-foreground',
            )}
          >
            <span className="inline-block size-2 rounded-full" style={{ background: platformColor(p) }} />
            {p}
            <span className={cn('tabular-nums', p === platform ? 'text-background/70' : 'text-muted-foreground')}>{counts[p]}</span>
          </button>
        ))}
      </div>

      <section>
        <h2 className="mb-3 flex items-center gap-2 text-xl font-semibold tracking-tight">
          <span className="inline-block size-3 rounded-full" style={{ background: color }} />
          {platform}
        </h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {summary.map(({ metric, best, rank }) => (
            <a key={metric.key} href={best!.link} target="_blank" rel="noopener" className="rounded-xl border bg-card p-3 hover:border-foreground/30">
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>{metric.label}</span>
                {rank && <span className="rounded-full border px-1.5 py-0.5 tabular-nums">#{rank.bestRank}</span>}
              </div>
              <div className="mt-1 text-lg font-semibold tabular-nums">{metric.format(best!.value)}</div>
              <div className="mt-0.5 line-clamp-1 text-xs text-muted-foreground">
                {best!.year}{best!.author ? ` · ${best!.author} et al.` : ''}
              </div>
            </a>
          ))}
        </div>
      </section>

      <div className="flex flex-col gap-8">
        {figures.map((f) => (
          <article key={f.name} className="rounded-xl border bg-card p-4 sm:p-6">
            <header className="mb-4">
              <h3 className="text-base font-semibold">{f.title}</h3>
              <p className="text-sm text-muted-foreground">{f.description}</p>
            </header>
            <FigureChart figure={figuresByName[f.name]} platforms={[platform]} height={380} />
          </article>
        ))}
      </div>
    </div>
  );
}
