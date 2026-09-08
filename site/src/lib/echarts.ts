/** Tree-shaken ECharts bundle: only the chart types and components the site uses. */
import * as echarts from 'echarts/core';
import { ScatterChart, LineChart, BarChart, SunburstChart, CustomChart, RadarChart } from 'echarts/charts';
import { GridComponent, TooltipComponent, RadarComponent, LegendComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
  ScatterChart,
  LineChart,
  BarChart,
  SunburstChart,
  CustomChart,
  RadarChart,
  GridComponent,
  TooltipComponent,
  RadarComponent,
  LegendComponent,
  CanvasRenderer,
]);

export { echarts };
export type ECharts = echarts.ECharts;
