// Dates and words for the shop page.

const DATE = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })

// "2026-11-03" or "2026-06-21T10:39" becomes "3 Nov 2026".
export function shortDate(value: string): string {
  const date = new Date(value.length === 10 ? `${value}T12:00:00` : value)
  return Number.isNaN(date.getTime()) ? value : DATE.format(date)
}

export function sentence(value: string): string {
  return value ? value[0].toUpperCase() + value.slice(1).replace(/_/g, ' ') : value
}
