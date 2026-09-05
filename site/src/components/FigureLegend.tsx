import type { LegendEntry, LegendGroup, SizeLegend } from '@/lib/figure';
import { cn } from 'cn';

function Swatch({ entry }: { entry: LegendEntry }) {
  const c = entry.color;
  if (entry.kind === 'line') {
    const dash = entry.dash === 'dot' ? '2 3' : entry.dash === 'dashdot' ? '8 3 2 3' : entry.dash === 'dash' ? '6 3' : undefined;
    return (
      <svg width="22" height="12" className="shrink-0">
        <line x1="1" y1="6" x2="21" y2="6" stroke={c} strokeWidth="2" strokeDasharray={dash} />
      </svg>
    );
  }
  if (entry.kind === 'bar' || entry.kind === 'area') {
    return <span className="inline-block size-3 shrink-0 rounded-[3px]" style={{ background: c }} />;
  }
  const fill = entry.open ? 'transparent' : c;
  const stroke = entry.open ? c : 'rgba(0,0,0,.15)';
  const common = { fill, stroke, strokeWidth: entry.open ? 2 : 1 };
  return (
    <svg width="14" height="14" viewBox="0 0 14 14" className="shrink-0">
      {entry.symbol === 'square' && <rect x="2" y="2" width="10" height="10" {...common} />}
      {entry.symbol === 'diamond' && <polygon points="7,1 13,7 7,13 1,7" {...common} />}
      {entry.symbol === 'triangle-up' && <polygon points="7,1.5 13,12.5 1,12.5" {...common} />}
      {entry.symbol === 'star' && <polygon points="7,0.5 8.6,5 13.5,5 9.5,8 11,13 7,10 3,13 4.5,8 0.5,5 5.4,5" {...common} />}
      {entry.symbol === 'x' && <path d="M2,2 L12,12 M12,2 L2,12" stroke={c} strokeWidth="2.5" fill="none" />}
      {!['square', 'diamond', 'triangle-up', 'star', 'x'].includes(entry.symbol) && <circle cx="7" cy="7" r="5" {...common} />}
    </svg>
  );
}

interface Props {
  groups: LegendGroup[];
  sizeLegend: SizeLegend | null;
  hidden: Set<number>;
  onToggle: (entry: LegendEntry) => void;
  className?: string;
}

/**
 * HTML legend reproducing Plotly's legend groups (headers, per-platform
 * entries, fit lines, marker-shape keys, marker-size samples).
 */
export function FigureLegend({ groups, sizeLegend, hidden, onToggle, className }: Props) {
  return (
    <div className={cn('flex flex-col gap-3 text-[12.5px] leading-tight', className)}>
      {groups.map((g, gi) => (
        <div key={gi} className="flex flex-col gap-1">
          {g.title && <div className="mb-0.5 text-[11px] font-semibold uppercase tracking-wide text-muted-foreground">{g.title}</div>}
          {g.entries.map((e) => {
            const off = e.traces.length > 0 && e.traces.every((t) => hidden.has(t));
            const clickable = e.kind !== 'key' && e.traces.length > 0;
            return (
              <button
                key={e.id}
                type="button"
                disabled={!clickable}
                onClick={() => clickable && onToggle(e)}
                aria-pressed={!off}
                className={cn(
                  'flex items-start gap-2 rounded-md px-1.5 py-0.5 text-left transition-colors [&>svg]:mt-0.5',
                  clickable && 'hover:bg-muted cursor-pointer',
                  off && 'opacity-40',
                )}
              >
                <Swatch entry={e} />
                <span className={cn('break-words', off && 'line-through')}>{e.label}</span>
              </button>
            );
          })}
        </div>
      ))}
      {sizeLegend && (
        <div className="flex flex-col gap-1">
          <div className="mb-0.5 text-[11px] font-semibold uppercase tracking-wide text-muted-foreground">{sizeLegend.title}</div>
          {sizeLegend.items.map((it) => (
            <div key={it.label} className="flex items-center gap-2 px-1.5 py-0.5">
              <span className="flex w-8 shrink-0 items-center justify-center">
                <span
                  className="inline-block rounded-full bg-muted-foreground/60"
                  style={{ width: Math.min(it.size, 28), height: Math.min(it.size, 28) }}
                />
              </span>
              <span>{it.label}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
