// Tests for refund and return requests: support staff deciding them in the
// admin panel, and customers seeing them under their orders. Fake API only.
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import App from './App'
import type { MyRefundRequest, RefundRequest, Session } from './api'

type Route = { status?: number; body?: unknown }
type Routes = Record<string, (body: unknown) => Route>

function fakeApi(routes: Routes) {
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

const WAITING: RefundRequest = {
  request_id: 'RQ-20261121-AAA111',
  created_at: '2026-11-21T09:00:00+00:00',
  status: 'waiting_for_staff',
  status_words: 'Waiting for the support team',
  order_id: 'JL-10231',
  reason: 'changed_mind',
  reason_words: 'Changed their mind',
  items: [
    { name: 'Linen Napkins (Set of 4)', quantity: 1 },
    { name: 'Ceramic Pour-Over Coffee Set', quantity: 1 },
  ],
  money: {
    item_refund: '6050.00', shipping_refunded: '0.00', return_fee: '699.00', net_refund: '5351.00',
    refunded_to: 'Original payment (Visa)', free_return_label: false,
  },
  why_staff: ['Refunds over ₹5,000 are checked by the support team.'],
  notes: [],
  ticket_id: 'TCK-20261121-BBB222',
  details: 'The colours are not what I expected.',
  customer_name: 'Priya Nair',
  customer_id: 'C001',
}
const APPROVED_IN_CHAT: RefundRequest = {
  ...WAITING, request_id: 'RQ-20261121-CCC333', status: 'approved', status_words: 'Approved', why_staff: [], ticket_id: null,
}

const STATS = {
  conversations: 0, customers: 0, messages: 0, tickets: 0, open_tickets: 0, tickets_in_progress: 0, tickets_by_harness: 0,
  handover_rate: 0, cost_usd: 0, cost_per_message_usd: 0, average_reply_ms: 0, outcomes: {}, checks: {}, tickets_by_reason: {}, days: [], team: [],
}

async function openRequestsAsAsha(routes: Routes) {
  const calls = fakeApi({ 'GET /api/stats': () => ({ body: STATS }), 'GET /api/tickets': () => ({ body: [] }), ...routes })
  sessionStorage.setItem('juniper-lane-admin', 'staff-token')
  sessionStorage.setItem('juniper-lane-admin-person', JSON.stringify({ role: 'staff', name: 'Asha Rao', staff_id: 'JLS-101' }))
  window.location.hash = '#/dashboard'
  const user = userEvent.setup()
  render(<App />)
  await screen.findByRole('heading', { name: 'Overview' })
  await user.click(screen.getByRole('button', { name: 'Refund requests' }))
  return { user, calls }
}

describe('refund requests in the admin panel', () => {
  it('lists waiting requests first, with the customer and the refund', async () => {
    await openRequestsAsAsha({ 'GET /api/admin/refund-requests': () => ({ body: [APPROVED_IN_CHAT, WAITING] }) })

    const table = await screen.findByRole('table', { name: 'Refund requests' })
    const rows = within(table).getAllByRole('row').slice(1)
    expect(rows).toHaveLength(1) // only the waiting one
    expect(rows[0]).toHaveTextContent('RQ-20261121-AAA111')
    expect(rows[0]).toHaveTextContent('Priya Nair · C001')
    expect(rows[0]).toHaveTextContent('₹5,351')
    expect(screen.getByRole('radio', { name: /Decided/ })).toHaveTextContent('1')
  })

  it('opens a request, takes off a restocking fee and approves it', async () => {
    const { user, calls } = await openRequestsAsAsha({
      'GET /api/admin/refund-requests': () => ({ body: [WAITING] }),
      'POST /api/admin/refund-requests/RQ-20261121-AAA111/approve': () => ({
        body: {
          ...WAITING,
          status: 'approved_by_staff',
          status_words: 'Approved by the support team',
          money: { ...WAITING.money!, restocking_fee: '420.00', net_refund: '4931.00' },
          decided_by: { name: 'Asha Rao', staff_id: 'JLS-101' },
          decided_at: '2026-11-21T10:00:00+00:00',
          staff_note: 'Box was missing.',
        },
      }),
    })
    await user.click(await screen.findByRole('button', { name: 'Open' }))
    const view = await screen.findByRole('region', { name: 'Request RQ-20261121-AAA111' })

    expect(within(view).getByRole('region', { name: 'Refund worked out by the rules' })).toHaveTextContent('Refund₹5,351')
    expect(within(view).getByText('Refunds over ₹5,000 are checked by the support team.')).toBeInTheDocument()
    expect(within(view).getByText('The colours are not what I expected.')).toBeInTheDocument()
    expect(within(view).getByText('Up to ₹1,210 (20% of the items)')).toBeInTheDocument()
    expect(within(view).getByRole('button', { name: 'Not approve' })).toBeDisabled() // needs a note first

    await user.type(within(view).getByLabelText(/Restocking fee/), '420')
    await user.type(within(view).getByLabelText('Note for the customer'), 'Box was missing.')
    await user.click(within(view).getByRole('button', { name: 'Approve' }))

    const after = await screen.findByRole('region', { name: 'Request RQ-20261121-AAA111' })
    expect(await within(after).findByText('Asha Rao')).toBeInTheDocument()
    expect(within(after).getByRole('region', { name: 'Refund worked out by the rules' })).toHaveTextContent('Restocking fee−₹420')
    expect(calls.find((c) => c.url.endsWith('/approve'))?.body).toEqual({ restocking_fee: 420, note: 'Box was missing.' })
  })

  it('shows why a decision failed', async () => {
    const { user } = await openRequestsAsAsha({
      'GET /api/admin/refund-requests': () => ({ body: [WAITING] }),
      'POST /api/admin/refund-requests/RQ-20261121-AAA111/deny': () => ({ status: 409, body: { detail: 'This request has already been decided.' } }),
    })
    await user.click(await screen.findByRole('button', { name: 'Open' }))
    await user.type(await screen.findByLabelText('Note for the customer'), 'The items were used.')
    await user.click(screen.getByRole('button', { name: 'Not approve' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('This request has already been decided.')
  })
})

describe('the customer under Your orders', () => {
  it('sees each request under its order with where it stands', async () => {
    const session: Session = {
      role: 'customer', session_id: 'session-abc', conversation_id: 'conv_aaaaaaaaaaaa',
      customer: { name: 'Priya Nair', email: 'priya.nair@example.com', order_count: 1 },
      orders: [{ order_id: 'JL-10231', placed_on: '2026-11-03', status: 'delivered', total: 6050, items: ['Linen Napkins (Set of 4)'] }],
      transcript: [], assistant_name: 'Juniper Lane Goods virtual assistant', handoff: null,
    }
    const mine: MyRefundRequest[] = [
      {
        request_id: 'RQ-20261121-DDD444', created_at: '2026-11-21T09:00:00+00:00', order_id: 'JL-10231',
        items: [{ name: 'Linen Napkins (Set of 4)', quantity: 1 }], reason: 'Changed their mind',
        status: 'approved', status_words: 'Approved', net_refund: '1151.00', refunded_to: 'Original payment (Visa)',
        ticket_id: null, decided_by: null, staff_note: null,
      },
    ]
    fakeApi({
      'GET /api/sessions/session-abc': () => ({ body: session }),
      'GET /api/products': () => ({ body: [] }),
      'GET /api/sessions/session-abc/tickets': () => ({ body: [] }),
      'GET /api/sessions/session-abc/refund-requests': () => ({ body: mine }),
    })
    sessionStorage.setItem('juniper-lane-session', 'session-abc')
    window.location.hash = '#/'
    render(<App />)

    const line = await screen.findByLabelText('Request RQ-20261121-DDD444')
    expect(line).toHaveTextContent('Return of Linen Napkins (Set of 4) · Approved · ₹1,151 to Original payment (Visa)')
  })
})
