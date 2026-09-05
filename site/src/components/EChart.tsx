import { useEffect, useRef } from 'react';
import type { EChartsOption } from 'echarts';
import { echarts, type ECharts } from '@/lib/echarts';

interface Props {
  option: EChartsOption;
  height?: number;
  className?: string;
  ariaLabel?: string;
}

/** Minimal ECharts wrapper: init once, resize with the container, replace the option on change. */
export function EChart({ option, height = 320, className, ariaLabel }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const chart = useRef<ECharts | null>(null);

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

  useEffect(() => {
    chart.current?.setOption(option, { notMerge: true });
  }, [option]);

  return <div ref={ref} style={{ height }} className={className} role="img" aria-label={ariaLabel} />;
}
