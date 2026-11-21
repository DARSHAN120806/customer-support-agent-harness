// Tests for the admin panel's Documents and Orders pages. The API is a fake.
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import App from './App'
import type { DocumentDetail, DocumentSummary, OrderDetail, OrderRow } from './api'

const LIST: DocumentSummary[] = [
  { name: 'faq.md', title: 'Frequently Asked Questions', sections: 2, chars: 300, updated_at: '2026-11-20T10:00:00+00:00' },
  { name: 'warranty.md', title: 'Warranty Policy', sections: 2, chars: 500, updated_at: '2026-11-20T10:00:00+00:00' },
]

const FAQ: DocumentDetail = {
  ...LIST[0],
  text: '# Frequently Asked Questions\n\n## Do you price match?\n\nNo.\n',
  version: 'v1',
  sections: [{ heading: 'Do you price match?', chars: 3 }, { heading: 'Very long section', chars: 5000 }],
  protected: [],
  history: [{ id: '20261120T100000000000Z', saved_at: '2026-11-20T10:00:00+00:00', chars: 40 }],
}

const WARRANTY: DocumentDetail = {
  ...LIST[1],
  text: '# Warranty Policy\n\n## Warranty claim statuses\n\nApproved means...\n',
  version: 'w1',
  sections: [{ heading: 'Warranty claim statuses', chars: 18 }],
  protected: ['Warranty claim statuses'],
  history: [],
}

const ROWS: OrderRow[] = [
  { order_id: 'JL-10231', placed_on: '2026-11-03', status: 'delivered', total: 6050, items: ['Ceramic Pour-Over Coffee Set'], customer_name: 'Priya Nair', records: 0 },
  { order_id: 'JL-10198', placed_on: '2026-09-14', status: 'delivered', total: 4498, items: ['Bluetooth Speaker Mini'], customer_name: 'Priya Nair', records: 1 },
]

const ORDER: OrderDetail = {
  order: {
    order_id: 'JL-10198', status: 'delivered', placed_on: '2026-09-14', tracking_number: 'TRK1', total: 4498, shipping_cost: 499,
    items: [{ name: 'Bluetooth Speaker Mini', quantity: 1, unit_price: 3999 }],
    warranty_claims: [{ claim_id: 'WC-40001', status: 'Approved — awaiting product' }],
  },
  customer: { name: 'Priya Nair', email: '[EMAIL]', city: 'Austin, TX' },
}

type Route = { status?: number; body?: unknown }

function fakeApi(routes: Record<string, (body: unknown) => Route>) {
  const calls: { method: string; url: string; body: unknown }[] = []
  vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, init) => {
    const url = String(input)
    const method = init?.method ?? 'GET'
    const body = init?.body ? JSON.parse(String(init.body)) : undefined
    calls.push({ method, url, body })
    const handler = routes[`${method} ${url}`]
    const { status = 200, body: out } = handler ? handler(body) : { status: 200, body: {} }
    return new Response(JSON.stringify(out), { status })
  })
  return calls
}

const STATS = {
  conversations: 0, customers: 0, messages: 0, tickets: 0, open_tickets: 0, tickets_by_harness: 0, handover_rate: 0,
  cost_usd: 0, cost_per_message_usd: 0, average_reply_ms: 0, outcomes: {}, checks: {}, tickets_by_reason: {}, days: [],
}

async function openSection(name: string, routes: Record<string, (body: unknown) => Route>) {
  const calls = fakeApi({
    'GET /api/stats': () => ({ body: STATS }),
    'GET /api/tickets': () => ({ body: [] }),
    'GET /api/admin/documents': () => ({ body: LIST }),
    'GET /api/admin/documents/faq.md': () => ({ body: FAQ }),
    'GET /api/admin/documents/warranty.md': () => ({ body: WARRANTY }),
    'GET /api/admin/orders?q=': () => ({ body: { total: 1016, orders: ROWS } }),
    ...routes,
  })
  sessionStorage.setItem('juniper-lane-admin', 'admin-token-1')
  window.location.hash = '#/dashboard'
  const user = userEvent.setup()
  render(<App />)
  await user.click(await screen.findByRole('button', { name }))
  return { user, calls }
}

describe('the documents page', () => {
  it('opens the first document with its sections and earlier versions', async () => {
    await openSection('Documents', {})

    expect(await screen.findByLabelText('Text of Frequently Asked Questions')).toHaveValue(FAQ.text)
    const outline = screen.getByRole('region', { name: 'Sections' })
    expect(within(outline).getByText('Do you price match?')).toBeInTheDocument()
    expect(within(outline).getByText('5,000')).toHaveClass('ad-long')
    expect(within(screen.getByRole('region', { name: 'Earlier versions' })).getByRole('button', { name: 'View' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Save' })).toBeDisabled()
  })

  it('marks sections that are kept in step with the order data', async () => {
    const { user } = await openSection('Documents', {})
    await screen.findByLabelText('Text of Frequently Asked Questions')

    await user.click(within(screen.getByRole('navigation', { name: 'Documents' })).getByRole('button', { name: /Warranty Policy/ }))

    expect(await screen.findByText('kept in step with order data')).toBeInTheDocument()
  })

  it('saves the edited text with the version it started from, and shows warnings', async () => {
    const saved: DocumentDetail = { ...FAQ, text: FAQ.text + 'More.\n', version: 'v2' }
    const { user, calls } = await openSection('Documents', {
      'PUT /api/admin/documents/faq.md': () => ({ body: { document: saved, warnings: ['The section "Very long section" is long.'] } }),
    })
    const box = await screen.findByLabelText('Text of Frequently Asked Questions')

    await user.type(box, 'More.{Enter}')
    expect(screen.getByText('Unsaved changes')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Save' }))

    expect(await screen.findByText(/The search now uses the new text/)).toBeInTheDocument()
    expect(screen.getByRole('list', { name: 'Warnings' })).toHaveTextContent('"Very long section" is long')
    expect(calls.find((c) => c.method === 'PUT')?.body).toEqual({ text: FAQ.text + 'More.\n', version: 'v1' })
    expect(screen.queryByText('Unsaved changes')).not.toBeInTheDocument()
  })

  it('shows why a save was refused, keeping the edit', async () => {
    const { user } = await openSection('Documents', {
      'PUT /api/admin/documents/faq.md': () => ({
        status: 400,
        body: { detail: 'Customer details cannot be added to a shop document, because every customer can search it: JL-10231' },
      }),
    })
    const box = await screen.findByLabelText('Text of Frequently Asked Questions')
    await user.type(box, 'JL-10231')

    await user.click(screen.getByRole('button', { name: 'Save' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Customer details cannot be added')
    expect(box).toHaveValue(FAQ.text + 'JL-10231')
  })

  it('shows an earlier version and restores it', async () => {
    const restored: DocumentDetail = { ...FAQ, text: '# Old FAQ\n', version: 'v3' }
    const { user, calls } = await openSection('Documents', {
      'GET /api/admin/documents/faq.md/history/20261120T100000000000Z': () => ({ body: { text: '# Old FAQ\n' } }),
      'POST /api/admin/documents/faq.md/restore': () => ({ body: { document: restored, warnings: [] } }),
    })
    await screen.findByLabelText('Text of Frequently Asked Questions')

    await user.click(within(screen.getByRole('region', { name: 'Earlier versions' })).getByRole('button', { name: 'View' }))
    expect(within(screen.getByRole('region', { name: 'Earlier version' })).getByText('# Old FAQ')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Restore this version' }))

    expect(await screen.findByText(/Restored/)).toBeInTheDocument()
    expect(screen.getByLabelText('Text of Frequently Asked Questions')).toHaveValue('# Old FAQ\n')
    expect(calls.find((c) => c.method === 'POST')?.body).toEqual({ version_id: '20261120T100000000000Z', version: 'v1' })
  })
})

describe('the orders page', () => {
  it('lists the newest orders, searches, and opens one with its records', async () => {
    const { user, calls } = await openSection('Orders', {
      'GET /api/admin/orders?q=speaker': () => ({ body: { total: 1, orders: [ROWS[1]] } }),
      'GET /api/admin/orders/JL-10198': () => ({ body: ORDER }),
    })

    const table = await screen.findByRole('table', { name: 'Orders' })
    expect(within(table).getAllByRole('row')).toHaveLength(3)
    expect(screen.getByText('2 of 1,016 orders')).toBeInTheDocument()

    await user.type(screen.getByRole('searchbox'), 'speaker')
    await user.click(screen.getByRole('button', { name: 'Search' }))
    expect(calls.some((c) => c.url === '/api/admin/orders?q=speaker')).toBe(true)
    expect(await screen.findByText('1 order')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Open' }))
    const view = await screen.findByRole('region', { name: 'Order JL-10198' })
    expect(within(view).getByText(/Priya Nair · Austin, TX · \[EMAIL\]/)).toBeInTheDocument()
    expect(within(within(view).getByRole('region', { name: 'Warranty claims' })).getByText('WC-40001')).toBeInTheDocument()
    expect(within(within(view).getByRole('region', { name: 'Items' })).getByText('₹4,498')).toBeInTheDocument()

    await user.click(within(view).getByRole('button', { name: '← All orders' }))
    expect(await screen.findByRole('table', { name: 'Orders' })).toBeInTheDocument()
  })
})
