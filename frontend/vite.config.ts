/// <reference types="vitest/config" />
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// The page talks to the Python API through "/api". While developing, Vite
// passes those requests on to the API server on port 8000, so the browser only
// ever talks to one address.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      // 127.0.0.1, not "localhost": the API listens on IPv4 only, and Node may try IPv6 first.
      '/api': 'http://127.0.0.1:8000',
    },
  },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    css: false,
  },
})
