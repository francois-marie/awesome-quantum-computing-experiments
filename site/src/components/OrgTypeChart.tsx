import { useMemo } from 'react';
import type { EChartsOption } from 'echarts';
import { EChart } from './EChart';
import { useChartTheme } from '@/hooks/useChartTheme';

interface Props {
  years: number[];
  series: { key: string; label: string; color: string; values: number[] }[];
  height?: number;
}

/** Stacked bars of papers per year, split by industry / academic / mixed. */
export function OrgTypeChart({ years, series, height = 300 }: Props) {
  const theme = useChartTheme();
  const option = useMemo<EChartsOption>(
    () => ({
      backgroundColor: 'transparent',
      animation: false,
      grid: { left: 40, right: 12, top: 30, bottom: 40 },
      legend: { top: 0, textStyle: { color: theme.muted, fontSize: 11 }, icon: 'roundRect', itemWidth: 12 },
      tooltip: {
        trigger: 'axis',
        backgroundColor: theme.background,
        borderColor: theme.grid,
        textStyle: { color: theme.text, fontSize: 12 },
      },
      xAxis: {
        type: 'category',
        data: years.map(String),
        axisLabel: { color: theme.muted, fontSize: 11 },
        axisLine: { lineStyle: { color: theme.grid } },
        axisTick: { show: false },
      },
      yAxis: {
        type: 'value',
        minInterval: 1,
        axisLabel: { color: theme.muted, fontSize: 11 },
        splitLine: { lineStyle: { color: theme.grid } },
      },
      series: series.map((s) => ({
        type: 'bar',
        name: s.label,
        stack: 'total',
        data: s.values,
        itemStyle: { color: s.color },
        barMaxWidth: 26,
      })),
    }),
    [years, series, theme],
  );
  return <EChart option={option} height={height} ariaLabel="Papers per year by organisation type" />;
}
