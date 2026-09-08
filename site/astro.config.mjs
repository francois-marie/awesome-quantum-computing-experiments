// @ts-check
import { defineConfig } from 'astro/config';

import react from '@astrojs/react';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://francoismarieleregent.xyz',
  base: '/awesome-quantum-computing-experiments',
  trailingSlash: 'ignore',
  output: 'static',
  integrations: [react()],

  vite: {
    plugins: [tailwindcss()],
    server: {
      // The CSV files and figure JSON live in the repository root, one level up.
      fs: { allow: ['..'] },
    },
  },
});
