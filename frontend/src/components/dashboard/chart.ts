// Chart colours and styles for the admin panel, from the warm neutral ramp in
// theme.css. One accent per chart, for the thing that matters; the rest neutral.

export const CHART = {
  accent: '#2f5d4e',
  neutral: '#d9cfc0',
  // Neutral steps for comparing several runs, after the accent.
  steps: ['#b9ae9c', '#8f8576', '#d9cfc0', '#6f665a'],
  grid: '#ebe5da',
  cursor: 'rgba(31, 27, 22, 0.04)',
  tick: { fill: '#6f665a', fontSize: 11, fontFamily: 'IBM Plex Mono, monospace' },
  tooltip: {
    border: '1px solid rgba(31, 27, 22, 0.08)',
    borderRadius: 8,
    boxShadow: '0 8px 24px rgba(0, 0, 0, 0.06)',
    fontSize: 13,
  },
}

// Charts draw in with a short animation, unless the device asks for reduced
// motion (an accessibility setting), in which case they appear at once.
export function prefersReducedMotion(): boolean {
  return typeof window.matchMedia === 'function' && window.matchMedia('(prefers-reduced-motion: reduce)').matches
}
