import { useEffect, useMemo, useRef, useState } from 'react';
import { echarts, type ECharts } from '@/lib/echarts';
import { buildModel, toOption, type Figure, type LegendEntry } from '@/lib/figure';
import { canonicalPlatform, config, platformColor, type Platform } from '@/lib/data';
import { useChartTheme } from '@/hooks/useChartTheme';
import { FigureLegend } from './FigureLegend';
import { cn } from 'cn';

interface Props {
  figure: Figure;
  /** Keep only traces belonging to these platforms (dashboard mode). */
  platforms?: Platform[];
  height?: number;
  className?: string;
  /** Hide the HTML legend (e.g. compact cards). */
  legend?: boolean;
}

const codeColor = (label: string) => {
  const name = label.replace(/\s*\(\d+\)\s*$/, '');
  return config.code_colors[name] ?? '#a3a3a3';
};

/**
 * Renders one figure from `out/figures/*.json` with ECharts and an HTML legend.
 * Content (traces, fits, hover text) comes straight from the Python export.
 */
export function FigureChart({ figure, platforms, height = 440, className, legend = true }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const chart = useRef<ECharts | null>(null);
  const theme = useChartTheme();
  const model = useMemo(() => buildModel(figure), [figure]);
  const [toggled, setToggled] = useState<Set<number>>(new Set());

  // Traces filtered out by the platform selector.
  const filtered = useMemo(() => {
    const out = new Set<number>();
    if (!platforms) return out;
    figure.data.forEach((t, i) => {
      const fromGroup = t.legendgroup && !t.legendgroup.startsWith('header_') ? canonicalPlatform(t.legendgroup.replace(/^data_/, '')) : null;
      const p = fromGroup ?? (t.name ? canonicalPlatform(t.name) : null);
      if (p && !platforms.includes(p)) out.add(i);
    });
    return out;
  }, [figure, platforms]);

  const hidden = useMemo(() => new Set([...toggled, ...filtered]), [toggled, filtered]);

  useEffect(() => {
    if (!ref.current) return;
    const instance = echarts.init(ref.current, undefined, { renderer: 'canvas' });
    chart.current = instance;
    const ro = new ResizeObserver(() => instance.resize());
    ro.observe(ref.current);
    return () => {
      ro.disconnect();
      instance.dispose();
      chart.current = null;
    };
  }, []);

  const [size, setSize] = useState<{ width: number; height: number }>({ width: 800, height });

  useEffect(() => {
    if (!ref.current) return;
    const el = ref.current;
    const ro = new ResizeObserver(() => setSize({ width: el.clientWidth, height: el.clientHeight }));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  useEffect(() => {
    const colorFor = (label: string, depth: number) => (depth === 1 ? codeColor(label) : depth === 2 ? platformColor(label.replace(/\s*\(\d+\)\s*$/, '')) : theme.grid);
    chart.current?.setOption(toOption({ model, hidden, theme, colorFor, size }), { notMerge: true });
  }, [model, hidden, theme, size]);

  const onToggle = (entry: LegendEntry) => {
    setToggled((prev) => {
      const next = new Set(prev);
      const allOff = entry.traces.every((t) => next.has(t));
      for (const t of entry.traces) allOff ? next.delete(t) : next.add(t);
      return next;
    });
  };

  // Legend groups restricted to visible platforms.
  const groups = useMemo(() => {
    if (!platforms) return model.groups;
    return model.groups
      .map((g) => ({ ...g, entries: g.entries.filter((e) => e.traces.length === 0 || e.traces.some((t) => !filtered.has(t))) }))
      .filter((g) => g.entries.length);
  }, [model, platforms, filtered]);

  return (
    <div className={cn('flex flex-col gap-4 md:flex-row', className)}>
      <div ref={ref} style={{ height }} className="min-w-0 flex-1" role="img" aria-label={model.title} />
      {legend && (groups.length > 0 || model.sizeLegend) && (
        <FigureLegend groups={groups} sizeLegend={model.sizeLegend} hidden={hidden} onToggle={onToggle} className="md:w-60 md:shrink-0 md:pt-2" />
      )}
    </div>
  );
}
