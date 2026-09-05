import { useEffect, useState } from 'react';
import type { Theme } from '@/lib/figure';

const LIGHT: Theme = { text: '#1c1c1c', muted: '#6b6b6b', grid: '#e6e6e6', background: '#ffffff' };
const DARK: Theme = { text: '#ededed', muted: '#a3a3a3', grid: '#2e2e2e', background: '#171717' };

const isDark = () => typeof document !== 'undefined' && document.documentElement.classList.contains('dark');

/** Chart colors that follow the site's light/dark class on <html>. */
export function useChartTheme(): Theme {
  const [theme, setTheme] = useState<Theme>(() => (isDark() ? DARK : LIGHT));
  useEffect(() => {
    const update = () => setTheme(isDark() ? DARK : LIGHT);
    update();
    const obs = new MutationObserver(update);
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
    return () => obs.disconnect();
  }, []);
  return theme;
}
