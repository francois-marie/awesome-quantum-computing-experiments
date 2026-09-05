/**
 * Adapter from the Plotly figure JSON written by `src/plotting` (Python) to an
 * Apache ECharts option plus a legend model rendered in HTML.
 *
 * The Python side stays the single source of truth for *what* is plotted
 * (traces, fits, legend entries, hover text). This module only decides *how*
 * it is drawn.
 */
import type { EChartsOption, SeriesOption } from 'echarts';

export interface PlotlyTrace {
  type: string;
  mode?: string;
  name?: string;
  x?: (number | string | null)[];
  y?: (number | null)[];
  text?: string[];
  customdata?: unknown[];
  hovertemplate?: string;
  hoverinfo?: string;
  legendgroup?: string;
  showlegend?: boolean;
  marker?: {
    color?: string | string[];
    size?: number | number[];
    symbol?: string | string[];
    opacity?: number;
    line?: { color?: string; width?: number };
  };
  line?: { color?: string; width?: number; dash?: string };
  error_y?: { array: number[]; arrayminus?: number[]; color?: string; symmetric?: boolean };
  stackgroup?: string;
  fillcolor?: string;
  orientation?: 'v' | 'h';
  xaxis?: string;
  yaxis?: string;
  // sunburst
  ids?: string[];
  labels?: string[];
  parents?: string[];
  values?: number[];
}

export interface PlotlyAxis {
  title?: { text?: string };
  type?: 'linear' | 'log' | 'category';
  range?: [number, number];
  tickvals?: number[];
  ticktext?: string[];
  categoryarray?: string[];
  tickangle?: number;
  dtick?: number | string;
}

export interface PlotlyAnnotation {
  text: string;
  x: number;
  y: number;
  xref?: string;
  yref?: string;
}

export interface Figure {
  name: string;
  data: PlotlyTrace[];
  layout: {
    title?: { text?: string };
    xaxis?: PlotlyAxis;
    yaxis?: PlotlyAxis;
    barmode?: string;
    annotations?: PlotlyAnnotation[];
    legend?: { title?: { text?: string } };
  };
}

export interface LegendEntry {
  id: string;
  label: string;
  color: string;
  symbol: string;
  kind: 'marker' | 'line' | 'bar' | 'area' | 'key';
  dash?: string;
  open?: boolean;
  /** Indexes into figure.data toggled by this entry. Empty for explanatory keys. */
  traces: number[];
}

export interface LegendGroup {
  title?: string;
  entries: LegendEntry[];
}

export interface SizeLegend {
  title: string;
  items: { label: string; size: number }[];
}

export interface FigureModel {
  figure: Figure;
  title: string;
  groups: LegendGroup[];
  sizeLegend: SizeLegend | null;
  /** Trace indexes never drawn as data (legend placeholders, size samples). */
  hiddenTraces: Set<number>;
}

// ------------------------------------------------------------------ helpers

/** Map Unicode "Mathematical Bold" letters (used for legend headers) back to ASCII. */
export function deBold(s: string): string {
  return Array.from(s)
    .map((ch) => {
      const cp = ch.codePointAt(0)!;
      if (cp >= 0x1d400 && cp <= 0x1d419) return String.fromCharCode(65 + cp - 0x1d400);
      if (cp >= 0x1d41a && cp <= 0x1d433) return String.fromCharCode(97 + cp - 0x1d41a);
      return ch;
    })
    .join('');
}

const isHeader = (t: PlotlyTrace) => !!t.legendgroup && t.legendgroup.startsWith('header_');
const isKeyOnly = (t: PlotlyTrace) => t.legendgroup === 'symbol_legend' || t.legendgroup === 'magic_state_legend';
const isSizeSample = (t: PlotlyTrace) => !t.name && t.showlegend === false && t.hoverinfo === 'skip';
const isPlaceholder = (t: PlotlyTrace) =>
  Array.isArray(t.x) && t.x.length === 1 && t.x[0] === null && Array.isArray(t.y) && t.y[0] === null;
const isBareErrorTrace = (t: PlotlyTrace) => !t.name && t.showlegend === false && !!t.error_y;

const traceColor = (t: PlotlyTrace): string => {
  const mc = t.marker?.color;
  if (typeof mc === 'string' && mc !== 'rgba(0,0,0,0)') return mc;
  if (t.line?.color) return t.line.color;
  if (Array.isArray(mc) && mc.length) return mc[0];
  return '#888';
};

const traceKind = (t: PlotlyTrace): LegendEntry['kind'] => {
  if (t.type === 'bar') return 'bar';
  if (t.stackgroup) return 'area';
  if (isKeyOnly(t)) return 'key';
  if (t.mode && t.mode.includes('lines') && !t.mode.includes('markers')) return 'line';
  return 'marker';
};

// ------------------------------------------------------------ legend model

export function buildModel(figure: Figure): FigureModel {
  const groups: LegendGroup[] = [];
  const hiddenTraces = new Set<number>();
  let current: LegendGroup = { entries: [] };
  groups.push(current);

  const traces = figure.data;
  traces.forEach((t, i) => {
    if (isHeader(t)) {
      hiddenTraces.add(i);
      current = { title: deBold(t.name ?? ''), entries: [] };
      groups.push(current);
      return;
    }
    if (isSizeSample(t) || isBareErrorTrace(t)) {
      hiddenTraces.add(i);
      return;
    }
    if (isPlaceholder(t)) hiddenTraces.add(i);
    if (t.showlegend === false || !t.name) return;

    const kind = traceKind(t);
    const symbol = typeof t.marker?.symbol === 'string' ? t.marker.symbol : 'circle';
    const entry: LegendEntry = {
      id: `${i}`,
      label: t.name,
      color: traceColor(t),
      symbol: symbol.replace('-open', ''),
      open: symbol.endsWith('-open'),
      kind,
      dash: t.line?.dash,
      traces: [],
    };
    if (kind !== 'key') {
      traces.forEach((u, j) => {
        if (hiddenTraces.has(j) && !isBareErrorTrace(u)) return;
        const sameGroup = !!t.legendgroup && u.legendgroup === t.legendgroup;
        const sameName = u.name === t.name;
        const prefixed = !!u.name && u.name.startsWith(`${t.name} (`);
        if (sameGroup || sameName || prefixed) entry.traces.push(j);
      });
      // Bare error-bar traces belong to the data trace right before them.
      traces.forEach((u, j) => {
        if (isBareErrorTrace(u) && entry.traces.includes(j - 1)) entry.traces.push(j);
      });
    }
    current.entries.push(entry);
  });

  // Size legend: unnamed grey samples paired with annotations at the same y.
  let sizeLegend: SizeLegend | null = null;
  const samples = traces.map((t, i) => ({ t, i })).filter(({ t }) => isSizeSample(t));
  const annotations = figure.layout.annotations ?? [];
  if (samples.length && annotations.length) {
    const titleAnn = annotations.find((a) => /marker size/i.test(a.text));
    const items = samples
      .map(({ t }) => {
        const y = t.y?.[0] as number;
        const ann = annotations.find((a) => a !== titleAnn && Math.abs(a.y - y) < 1e-6);
        const size = typeof t.marker?.size === 'number' ? t.marker.size : (t.marker?.size as number[])?.[0] ?? 10;
        return ann ? { label: ann.text.replace(/<[^>]+>/g, ''), size } : null;
      })
      .filter((x): x is { label: string; size: number } => x !== null)
      .sort((a, b) => a.size - b.size);
    sizeLegend = { title: titleAnn ? titleAnn.text.replace(/<[^>]+>/g, '') : 'Marker size', items };
  }

  const rawTitle = figure.layout.title?.text ?? figure.name;
  return {
    figure,
    title: rawTitle.replace(/<[^>]+>/g, ''),
    groups: groups.filter((g) => g.entries.length),
    sizeLegend,
    hiddenTraces,
  };
}

// --------------------------------------------------------- hover templates

const fmtNumber = (v: unknown, spec?: string): string => {
  if (typeof v !== 'number') return String(v ?? '');
  if (spec) {
    const m = spec.match(/^\.(\d+)f$/);
    if (m) return v.toFixed(Number(m[1]));
  }
  if (v !== 0 && (Math.abs(v) < 1e-3 || Math.abs(v) >= 1e6)) return v.toExponential(2).replace('e-', 'e-').replace('.00e', 'e');
  return Number.isInteger(v) ? String(v) : String(Number(v.toPrecision(6)));
};

export function renderHover(trace: PlotlyTrace, i: number): string {
  const tpl = trace.hovertemplate;
  const x = trace.x?.[i];
  const y = trace.y?.[i];
  if (!tpl) {
    if (trace.hoverinfo === 'skip' || trace.hoverinfo === 'none') return '';
    const parts = [trace.name && `<b>${trace.name}</b>`, x !== undefined && `x: ${fmtNumber(x)}`, y !== undefined && `y: ${fmtNumber(y)}`];
    return parts.filter(Boolean).join('<br>');
  }
  const cd = trace.customdata?.[i];
  return tpl
    .replace(/<extra>.*?<\/extra>/g, '')
    .replace(/%\{text\}/g, String(trace.text?.[i] ?? ''))
    .replace(/%\{fullData\.name\}/g, trace.name ?? '')
    .replace(/%\{customdata\[(\d+)\]\}/g, (_, k) => String((cd as unknown[])?.[Number(k)] ?? ''))
    .replace(/%\{customdata\}/g, String(cd ?? ''))
    .replace(/%\{x(?::([^}]+))?\}/g, (_, spec) => fmtNumber(x, spec))
    .replace(/%\{y(?::([^}]+))?\}/g, (_, spec) => fmtNumber(y, spec));
}

// ------------------------------------------------------------ echarts option

export interface Theme {
  text: string;
  muted: string;
  grid: string;
  background: string;
}

const SYMBOLS: Record<string, string> = {
  circle: 'circle',
  square: 'rect',
  diamond: 'diamond',
  'triangle-up': 'triangle',
  cross: 'path://M-1,-3h2v2h2v2h-2v2h-2v-2h-2v-2h2z',
  x: 'path://M-3,-2l1,-1l2,2l2,-2l1,1l-2,2l2,2l-1,1l-2,-2l-2,2l-1,-1l2,-2z',
};

const DASH: Record<string, 'solid' | 'dashed' | 'dotted' | number[]> = {
  solid: 'solid',
  dash: 'dashed',
  dot: 'dotted',
  dashdot: [10, 4, 2, 4],
};

const at = <T,>(v: T | T[] | undefined, i: number, fallback: T): T =>
  Array.isArray(v) ? (v[i] ?? fallback) : v === undefined ? fallback : v;

function axisOption(axis: PlotlyAxis | undefined, theme: Theme, categories: string[] | null, isX: boolean, values: number[] = []) {
  const name = axis?.title?.text ?? '';
  const base = {
    name,
    nameLocation: 'middle' as const,
    nameGap: isX ? 30 : 55,
    nameTextStyle: { color: theme.text, fontSize: 12, fontWeight: 500 },
    axisLine: { lineStyle: { color: theme.grid } },
    axisTick: { lineStyle: { color: theme.grid } },
    axisLabel: { color: theme.muted, fontSize: 11, rotate: axis?.tickangle ? -axis.tickangle : 0 },
    splitLine: { lineStyle: { color: theme.grid } },
  };
  if (categories) return { ...base, type: 'category' as const, data: categories, axisLabel: { ...base.axisLabel, interval: 0 } };
  if (axis?.type === 'log') {
    const positive = values.filter((v) => v > 0);
    const lo = positive.length ? 10 ** Math.floor(Math.log10(Math.min(...positive))) : undefined;
    const hi = positive.length ? 10 ** Math.ceil(Math.log10(Math.max(...positive))) : undefined;
    return {
      ...base,
      type: 'log' as const,
      logBase: 10,
      min: lo,
      max: hi,
      interval: lo && hi && Math.log10(hi / lo) > 12 ? 2 : 1,
      axisLabel: { ...base.axisLabel, formatter: (v: number) => fmtNumber(v) },
    };
  }
  if (axis?.ticktext && axis.tickvals) {
    const labels = new Map(axis.tickvals.map((v, i) => [v, axis.ticktext![i]]));
    return {
      ...base,
      type: 'value' as const,
      min: Math.min(...axis.tickvals) - 1,
      max: Math.max(...axis.tickvals) + 1,
      interval: 1,
      splitLine: { lineStyle: { color: theme.grid, type: 'dashed' as const } },
      axisLabel: { ...base.axisLabel, formatter: (v: number) => labels.get(v) ?? '' },
    };
  }
  const opt: Record<string, unknown> = { ...base, type: 'value' as const };
  if (axis?.range) {
    opt.min = axis.range[0];
    opt.max = axis.range[1];
  } else {
    opt.scale = true;
  }
  if (isX && name.toLowerCase().includes('year')) {
    opt.axisLabel = { ...base.axisLabel, formatter: (v: number) => String(v) };
    opt.minInterval = 1;
    if (values.length) {
      opt.min = Math.floor(Math.min(...values)) - 1;
      opt.max = Math.ceil(Math.max(...values)) + 1;
      delete opt.scale;
    }
  }
  if (typeof axis?.dtick === 'number') opt.interval = axis.dtick;
  return opt;
}

function sunburstOption(trace: PlotlyTrace, theme: Theme, colorFor: (label: string, depth: number) => string, radiusPx = 300): EChartsOption {
  const ids = trace.ids ?? [];
  const nodes = new Map<string, { name: string; value: number; children: unknown[]; hover: string; id: string; depth: number }>();
  ids.forEach((id, i) => {
    nodes.set(id, {
      id,
      name: trace.labels?.[i] ?? id,
      value: trace.values?.[i] ?? 0,
      children: [],
      hover: String(trace.customdata?.[i] ?? ''),
      depth: 0,
    });
  });
  const roots: unknown[] = [];
  ids.forEach((id, i) => {
    const parent = trace.parents?.[i];
    const node = nodes.get(id)!;
    if (parent && nodes.has(parent)) {
      const p = nodes.get(parent)!;
      node.depth = p.depth + 1;
      p.children.push(node);
    } else roots.push(node);
  });
  // ECharts computes parent values from children; keep leaf values only.
  const finalize = (n: { children: unknown[]; name: string; depth: number; value: number; id: string }): unknown => ({
    name: n.name,
    value: n.children.length ? undefined : n.value,
    hover: (n as { hover: string }).hover,
    itemStyle: { color: colorFor(n.name, n.depth) },
    children: (n.children as typeof n[]).map(finalize),
  });
  const data = (roots as (typeof nodes extends Map<string, infer V> ? V : never)[]).map(finalize);
  // Ring radii as fractions of the chart radius; label widths follow the ring thickness.
  const rings = { center: 0.17, mid: 0.55, outer: 0.97 };
  const px = (f: number) => Math.round(f * radiusPx);
  return {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      enterable: true,
      confine: true,
      formatter: (p: { data?: { hover?: string } }) => p.data?.hover ?? '',
      backgroundColor: theme.background,
      borderColor: theme.grid,
      textStyle: { color: theme.text, fontSize: 12 },
      extraCssText: 'max-width: 360px; white-space: normal; border-radius: 8px;',
    },
    series: [
      {
        type: 'sunburst',
        radius: ['0%', `${rings.outer * 100}%`],
        center: ['50%', '50%'],
        data: data as never,
        sort: undefined,
        emphasis: { focus: 'ancestor' },
        itemStyle: { borderColor: theme.background, borderWidth: 2 },
        label: { color: theme.text, rotate: 'radial', overflow: 'truncate', ellipsis: '…', minAngle: 4 },
        levels: [
          {},
          {
            r0: '0%',
            r: `${rings.center * 100}%`,
            label: { rotate: 0, fontSize: 12, fontWeight: 'bold', overflow: 'break', width: px(rings.center) * 2 - 16, lineHeight: 15 },
            itemStyle: { color: theme.grid },
          },
          {
            r0: `${rings.center * 100}%`,
            r: `${rings.mid * 100}%`,
            label: { fontSize: 11, width: px(rings.mid - rings.center) - 12, minAngle: 6 },
          },
          {
            r0: `${rings.mid * 100}%`,
            r: `${rings.outer * 100}%`,
            label: { fontSize: 10, width: px(rings.outer - rings.mid) - 12, minAngle: 5 },
          },
        ],
      },
    ],
  };
}

const numbersOf = (traces: { t: PlotlyTrace }[], key: 'x' | 'y'): number[] =>
  traces.flatMap(({ t }) => {
    const vals = (t[key] ?? []).filter((v): v is number => typeof v === 'number' && Number.isFinite(v));
    if (key !== 'y' || !t.error_y) return vals;
    return vals.concat(vals.map((v, k) => v + (t.error_y!.array?.[k] ?? 0)), vals.map((v, k) => v - (t.error_y!.arrayminus?.[k] ?? t.error_y!.array?.[k] ?? 0)));
  });

function horizontalBarOption(model: FigureModel, visible: { t: PlotlyTrace; i: number }[], theme: Theme): EChartsOption {
  const { figure } = model;
  const spec = figure.layout.yaxis;
  const categories =
    spec?.categoryarray ?? [...new Set(visible.flatMap(({ t }) => (t.y ?? []).map((v) => String(v))))];
  const series: SeriesOption[] = visible.map(({ t, i }) => ({
    type: 'bar',
    name: t.name,
    id: `t${i}`,
    stack: 'total',
    barCategoryGap: '30%',
    data: (t.y ?? []).map((cat, k) => [t.x?.[k] ?? 0, String(cat)]) as never,
    itemStyle: { color: traceColor(t) },
    emphasis: { focus: 'series' },
    tooltip: { formatter: (p: { dataIndex: number }) => renderHover(t, p.dataIndex) },
  }));
  const longest = Math.max(...categories.map((c) => c.length));
  return {
    backgroundColor: 'transparent',
    animation: false,
    grid: { left: Math.min(260, 24 + longest * 6.5), right: 24, top: 12, bottom: 44 },
    tooltip: {
      trigger: 'item',
      confine: true,
      backgroundColor: theme.background,
      borderColor: theme.grid,
      textStyle: { color: theme.text, fontSize: 12 },
      extraCssText: 'max-width: 320px; white-space: normal; border-radius: 8px;',
    },
    xAxis: {
      type: 'value',
      minInterval: 1,
      name: figure.layout.xaxis?.title?.text ?? '',
      nameLocation: 'middle',
      nameGap: 28,
      nameTextStyle: { color: theme.text, fontSize: 12, fontWeight: 500 },
      axisLabel: { color: theme.muted, fontSize: 11 },
      splitLine: { lineStyle: { color: theme.grid } },
      axisLine: { lineStyle: { color: theme.grid } },
    },
    yAxis: {
      type: 'category',
      data: categories,
      axisLabel: { color: theme.text, fontSize: 11, width: Math.min(240, longest * 6.5), overflow: 'truncate' },
      axisLine: { lineStyle: { color: theme.grid } },
      axisTick: { show: false },
    },
    series,
  };
}

export interface ToOptionArgs {
  model: FigureModel;
  hidden: Set<number>;
  theme: Theme;
  colorFor?: (label: string, depth: number) => string;
  /** Chart size in px, used to size sunburst rings and labels. */
  size?: { width: number; height: number };
}

export function toOption({ model, hidden, theme, colorFor, size }: ToOptionArgs): EChartsOption {
  const { figure } = model;
  const traces = figure.data;

  if (traces[0]?.type === 'sunburst') {
    const radius = size ? Math.min(size.width, size.height) / 2 : 300;
    return sunburstOption(traces[0], theme, colorFor ?? (() => '#888'), radius);
  }

  const visible = traces
    .map((t, i) => ({ t, i }))
    .filter(({ i }) => !hidden.has(i) && !model.hiddenTraces.has(i));

  const horizontal = traces.some((t) => t.type === 'bar' && t.orientation === 'h');
  if (horizontal) return horizontalBarOption(model, visible, theme);

  // Category x axis when Plotly says so or x values are strings.
  const xAxisSpec = figure.layout.xaxis;
  let categories: string[] | null = null;
  if (xAxisSpec?.type === 'category' && xAxisSpec.categoryarray) categories = xAxisSpec.categoryarray;
  else if (traces.some((t) => t.type === 'bar' || (t.x ?? []).some((v) => typeof v === 'string'))) {
    const seen = new Set<string>();
    for (const t of traces) for (const v of t.x ?? []) if (v !== null) seen.add(String(v));
    categories = [...seen].sort();
  }

  const series: SeriesOption[] = [];
  const stacked = figure.layout.barmode === 'stack' || figure.layout.barmode === 'relative';

  for (const { t, i } of visible) {
    const color = traceColor(t);
    const xs = t.x ?? [];
    const ys = t.y ?? [];
    const pairs = xs.map((x, k) => [categories ? String(x) : x, ys[k]] as [string | number, number | null]);

    if (t.type === 'bar') {
      series.push({
        type: 'bar',
        name: t.name,
        id: `t${i}`,
        stack: stacked ? 'total' : undefined,
        data: pairs as never,
        itemStyle: { color },
        emphasis: { focus: 'series' },
        tooltip: { formatter: (p: { dataIndex: number }) => renderHover(t, p.dataIndex) },
      });
      continue;
    }

    const mode = t.mode ?? 'markers';
    const hasLines = mode.includes('lines');
    const hasMarkers = mode.includes('markers');

    if (t.stackgroup) {
      series.push({
        type: 'line',
        name: t.name,
        id: `t${i}`,
        stack: t.stackgroup,
        data: pairs as never,
        showSymbol: false,
        lineStyle: { color: t.line?.color ?? color, width: 1.5 },
        areaStyle: { color: t.fillcolor ?? color },
        emphasis: { focus: 'series' },
        tooltip: { formatter: (p: { dataIndex: number }) => renderHover(t, p.dataIndex) },
      });
      continue;
    }

    if (hasLines) {
      series.push({
        type: 'line',
        name: t.name,
        id: `t${i}`,
        data: pairs as never,
        showSymbol: hasMarkers,
        symbol: 'circle',
        symbolSize: at(t.marker?.size, 0, 8),
        itemStyle: { color, borderColor: t.marker?.line?.color, borderWidth: t.marker?.line?.width ?? 0 },
        lineStyle: { color: t.line?.color ?? color, width: t.line?.width ?? 2, type: DASH[t.line?.dash ?? 'solid'] ?? 'solid' },
        z: hasMarkers ? 3 : 1,
        silent: !hasMarkers,
        tooltip: { formatter: (p: { dataIndex: number }) => renderHover(t, p.dataIndex) },
      });
      continue;
    }

    // Markers.
    const data = pairs.map(([x, y], k) => {
      const symbol = at(t.marker?.symbol, k, 'circle');
      const open = symbol.endsWith('-open');
      const size = at(t.marker?.size, k, 10);
      const c = at(t.marker?.color as string | string[] | undefined, k, color);
      return {
        value: [x, y],
        symbol: SYMBOLS[symbol.replace('-open', '')] ?? 'circle',
        symbolSize: size,
        itemStyle: open
          ? { color: 'transparent', borderColor: c, borderWidth: 2 }
          : { color: c, borderColor: t.marker?.line?.color ?? theme.background, borderWidth: t.marker?.line?.width ?? 1, opacity: t.marker?.opacity ?? 1 },
      };
    });
    series.push({
      type: 'scatter',
      name: t.name,
      id: `t${i}`,
      data: data as never,
      z: 4,
      emphasis: { scale: 1.3 },
      tooltip: { formatter: (p: { dataIndex: number }) => renderHover(t, p.dataIndex) },
    });

    // Error bars: Plotly puts them on the trace or on a bare follow-up trace.
    const err = t.error_y ?? (isBareErrorTrace(traces[i + 1] ?? { type: '' }) ? traces[i + 1].error_y : undefined);
    if (err) {
      const errData = pairs.map(([x, y], k) => {
        const plus = err.array?.[k] ?? 0;
        const minus = err.symmetric === false ? err.arrayminus?.[k] ?? plus : plus;
        return [x, y, (y ?? 0) + plus, (y ?? 0) - minus];
      });
      series.push({
        type: 'custom',
        name: `${t.name} error`,
        id: `e${i}`,
        silent: true,
        z: 3,
        data: errData as never,
        renderItem: (params, api) => {
          const x = api.value(0);
          const hi = api.coord([x, api.value(2)]);
          const lo = api.coord([x, api.value(3)]);
          if (!Number.isFinite(hi[1]) || !Number.isFinite(lo[1])) return undefined as never;
          const style = { stroke: err.color ?? color, fill: 'none', lineWidth: 1.5 };
          const cap = 4;
          return {
            type: 'group',
            children: [
              { type: 'line', shape: { x1: hi[0], y1: hi[1], x2: lo[0], y2: lo[1] }, style },
              { type: 'line', shape: { x1: hi[0] - cap, y1: hi[1], x2: hi[0] + cap, y2: hi[1] }, style },
              { type: 'line', shape: { x1: lo[0] - cap, y1: lo[1], x2: lo[0] + cap, y2: lo[1] }, style },
            ],
          } as never;
        },
      });
    }
  }

  return {
    backgroundColor: 'transparent',
    animation: false,
    grid: { left: figure.layout.yaxis?.ticktext ? 150 : 64, right: 20, top: 20, bottom: 52, containLabel: false },
    tooltip: {
      trigger: 'item',
      enterable: true,
      confine: true,
      backgroundColor: theme.background,
      borderColor: theme.grid,
      textStyle: { color: theme.text, fontSize: 12 },
      extraCssText: 'max-width: 320px; white-space: normal; box-shadow: 0 4px 24px rgba(0,0,0,.12); border-radius: 8px;',
    },
    xAxis: axisOption(figure.layout.xaxis, theme, categories, true, numbersOf(visible, 'x')) as never,
    yAxis: axisOption(figure.layout.yaxis, theme, null, false, numbersOf(visible, 'y')) as never,
    series,
  };
}
