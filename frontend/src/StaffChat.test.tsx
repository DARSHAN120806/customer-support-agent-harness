// Tests for support staff answering tickets, and for the customer's side of
// that chat. The API is a fake, so nothing is paid.
import { act, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import type { ChatUpdates, CustomerTicket, Session, Ticket, TicketDetail } from './api'

type Route = { status?: number; body?: unknown }
type Routes = Record<string, (body: unknown) => Route>

function fakeApi(routes: Routes) {
  const calls: { method: string; url: string; body: unknown }[] = []
  vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, init) => {
    const url = String(input)
    const method = init?.method ?? 'GET'
    const body = init?.body ? JSON.parse(String(init.body)) : undefined
    calls.push({ method, url, body })
    const handler = routes[`${method} ${url}`] ?? routes[`${method} ${url.split('?')[0]}`]
    const { status = 200, body: out } = handler ? handler(body) : { status: 200, body: {} }
    return new Response(status === 204 ? null : JSON.stringify(out), { status })
  })
  return calls
}

afterEach(() => {
  vi.useRealTimers()
})

// --- The admin panel, signed in as a support person -----------------------------------

const ASHA = { role: 'staff', name: 'Asha Rao', staff_id: 'JLS-101' }

const WAITING: Ticket = {
  ticket_id: 'TCK-20261121-AAA111', created_at: '2026-11-21T09:00:00+00:00', status: 'open', conversation_id: 'conv_aaaaaaaaaaaa',
  customer_email: '[EMAIL]', reason: 'human_requested', order_id: 'JL-10231', summary: 'Wants a person about a leaking kettle.',
  assigned_to: null, messages: [], live: true,
}
const TAKEN: Ticket = { ...WAITING, status: 'in_progress', assigned_to: { name: 'Asha Rao', staff_id: 'JLS-101' } }
const CHAT = [
  { role: 'customer' as const, text: 'Can I speak to a person?' },
  { role: 'assistant' as const, text: 'I have created ticket TCK-20261121-AAA111.' },
]

const STATS = {
  conversations: 1, customers: 1, messages: 1, tickets: 1, open_tickets: 1, tickets_in_progress: 0, tickets_by_harness: 0,
  handover_rate: 1, cost_usd: 0, cost_per_message_usd: 0, average_reply_ms: 0, outcomes: {}, checks: {}, tickets_by_reason: {}, days: [],
  team: [{ name: 'Asha Rao', staff_id: 'JLS-101', taken: 4, closed: 3, answering_now: 1, messages: 12, average_minutes_to_close: 6.5 }],
}

async function openPanelAsAsha(routes: Routes) {
  const calls = fakeApi({
    'GET /api/stats': () => ({ body: STATS }),
    'GET /api/tickets': () => ({ body: [WAITING] }),
    ...routes,
  })
  sessionStorage.setItem('juniper-lane-admin', 'staff-token')
  sessionStorage.setItem('juniper-lane-admin-person', JSON.stringify(ASHA))
  window.location.hash = '#/dashboard'
  const user = userEvent.setup()
  render(<App />)
  await screen.findByRole('heading', { name: 'Overview' })
  return { user, calls }
}

describe('a support person in the admin panel', () => {
  it('sees only their pages, with their name and ID', async () => {
    await openPanelAsAsha({})

    const nav = screen.getByRole('navigation', { name: 'Admin sections' })
    expect(within(nav).getAllByRole('button').map((b) => b.textContent)).toEqual(['Overview', 'Tickets', 'Conversations', 'Orders'])
    expect(screen.getByText(/Signed in as/)).toHaveTextContent('Signed in as Asha Rao · JLS-101')
  })

  it('sees who handled how many tickets on the overview', async () => {
    await openPanelAsAsha({})

    const team = screen.getByRole('table', { name: 'Support team' })
    expect(within(team).getByText('Asha Rao').closest('tr')).toHaveTextContent('Asha RaoJLS-101431126.5 min')
    expect(screen.getByText('1 waiting · 0 being answered')).toBeInTheDocument()
  })

  it('takes a waiting ticket, answers the customer, and ends the chat', async () => {
    let state: TicketDetail = { ticket: WAITING, chat: CHAT }
    const { user, calls } = await openPanelAsAsha({
      'GET /api/tickets/TCK-20261121-AAA111': () => ({ body: state }),
      'POST /api/tickets/TCK-20261121-AAA111/take': () => {
        state = { ticket: TAKEN, chat: CHAT }
        return { body: state }
      },
      'POST /api/tickets/TCK-20261121-AAA111/messages': (body) => {
        const text = (body as { text: string }).text
        state = { ticket: { ...TAKEN, messages: [{ from: 'staff', name: 'Asha Rao', staff_id: 'JLS-101', text, at: '2026-11-21T09:05:00+00:00' }] }, chat: CHAT }
        return { body: state }
      },
      'POST /api/tickets/TCK-20261121-AAA111/end': () => {
        state = { ticket: { ...state.ticket, status: 'closed', closed_at: '2026-11-21T09:10:00+00:00' }, chat: CHAT }
        return { body: state }
      },
    })
    await user.click(screen.getByRole('button', { name: 'Tickets' }))
    const table = await screen.findByRole('table', { name: 'Tickets' })
    expect(within(table).getByText('Waiting')).toBeInTheDocument()
    expect(within(table).getByText('in the chat')).toBeInTheDocument()

    await user.click(within(table).getByRole('button', { name: 'Open' }))
    const view = await screen.findByRole('region', { name: 'Ticket TCK-20261121-AAA111' })
    expect(within(view).getByText('Can I speak to a person?')).toBeInTheDocument()
    expect(within(view).getByText(/In the chat now/)).toBeInTheDocument()
    expect(within(view).queryByLabelText('Your reply')).not.toBeInTheDocument() // take it first

    await user.click(within(view).getByRole('button', { name: 'Take ticket' }))
    expect(await within(view).findByText(/Answering as/)).toHaveTextContent('Answering as Asha Rao · JLS-101')

    await user.type(within(view).getByLabelText('Your reply'), 'Hi Priya, I am here.{Enter}')
    expect(await within(view).findByText('Hi Priya, I am here.')).toBeInTheDocument()
    expect(calls.find((c) => c.url.endsWith('/messages'))?.body).toEqual({ text: 'Hi Priya, I am here.' })
    expect(within(view).getByLabelText('Your reply')).toHaveValue('')

    await user.click(within(view).getByRole('button', { name: 'End chat' }))
    expect(await within(view).findByText(/Closed by Asha Rao/)).toBeInTheDocument()
    expect(within(view).queryByLabelText('Your reply')).not.toBeInTheDocument()
  })

  it('shows who is answering a ticket someone else took, and why taking failed', async () => {
    const tom: Ticket = { ...WAITING, status: 'in_progress', assigned_to: { name: 'Tom Becker', staff_id: 'JLS-102' } }
    const { user } = await openPanelAsAsha({
      'GET /api/tickets': () => ({ body: [tom] }),
      'GET /api/tickets/TCK-20261121-AAA111': () => ({ body: { ticket: tom, chat: CHAT } }),
    })
    await user.click(screen.getByRole('button', { name: 'Tickets' }))
    await user.click(await screen.findByRole('radio', { name: /All/ }))
    await user.click(await screen.findByRole('button', { name: 'Open' }))

    const view = await screen.findByRole('region', { name: 'Ticket TCK-20261121-AAA111' })
    expect(within(view).getByText(/is answering this ticket/)).toHaveTextContent('Tom Becker · JLS-102 is answering this ticket')
    expect(within(view).queryByRole('button', { name: 'Take ticket' })).not.toBeInTheDocument()
  })

  it('filters tickets into waiting, mine and all', async () => {
    const mine: Ticket = { ...TAKEN, ticket_id: 'TCK-20261121-BBB222' }
    const closed: Ticket = { ...WAITING, ticket_id: 'TCK-20261121-CCC333', status: 'closed' }
    const { user } = await openPanelAsAsha({ 'GET /api/tickets': () => ({ body: [WAITING, mine, closed] }) })
    await user.click(screen.getByRole('button', { name: 'Tickets' }))

    const rows = () => within(screen.getByRole('table', { name: 'Tickets' })).getAllByRole('row').length - 1
    await screen.findByRole('table', { name: 'Tickets' })
    expect(rows()).toBe(1)
    await user.click(screen.getByRole('radio', { name: /Mine/ }))
    expect(rows()).toBe(1)
    expect(screen.getByText('With Asha Rao')).toBeInTheDocument()
    await user.click(screen.getByRole('radio', { name: /All/ }))
    expect(rows()).toBe(3)
  })
})

// --- The customer's side ----------------------------------------------------------------

const SESSION: Session = {
  role: 'customer', session_id: 'session-abc', conversation_id: 'conv_aaaaaaaaaaaa',
  customer: { name: 'Priya Nair', email: 'priya.nair@example.com', order_count: 0 }, orders: [],
  transcript: [{ role: 'customer', text: 'Can I speak to a person?' }, { role: 'assistant', text: 'A ticket was created.' }],
  assistant_name: 'Juniper Lane Goods virtual assistant', handoff: null,
}

async function openShopAsPriya(routes: Routes, chatOpen: boolean) {
  vi.useFakeTimers({ shouldAdvanceTime: true })
  const calls = fakeApi({
    'GET /api/sessions/session-abc': () => ({ body: SESSION }),
    'GET /api/products': () => ({ body: [] }),
    'GET /api/sessions/session-abc/tickets': () => ({ body: [] }),
    ...routes,
  })
  sessionStorage.setItem('juniper-lane-session', 'session-abc')
  sessionStorage.setItem('juniper-lane-chat-open', chatOpen ? 'open' : 'closed')
  const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime })
  render(<App />)
  await screen.findByRole('heading', { name: 'Homeware, furniture and electronics' })
  return { user, calls }
}

async function waitForCheck() {
  await act(() => vi.advanceTimersByTimeAsync(3100))
}

describe('the customer when a person joins the chat', () => {
  it('sees the person join, their messages, and their messages go to the person', async () => {
    let news: ChatUpdates = {
      entries: [
        { role: 'system', text: "Asha from the support team has joined the chat. You're now talking to a person." },
        { role: 'staff', text: 'Hi Priya, how can I help?', name: 'Asha' },
      ],
      next: 4,
      handoff: { name: 'Asha' },
    }
    const { user, calls } = await openShopAsPriya(
      {
        'GET /api/sessions/session-abc/updates': () => ({ body: news }),
        'POST /api/sessions/session-abc/messages': () => ({ body: { reply: null, outcome: 'sent_to_team', new_ticket_ids: [] } }),
      },
      true,
    )

    await waitForCheck()
    const chat = screen.getByRole('dialog', { name: /virtual assistant/ })
    expect(within(chat).getByText(/has joined the chat/)).toHaveClass('sc-note')
    expect(within(chat).getByText('Asha · Support team')).toBeInTheDocument()
    expect(within(chat).getByText('Hi Priya, how can I help?')).toBeInTheDocument()
    expect(within(chat).getByRole('heading', { name: 'Asha from the support team' })).toBeInTheDocument()
    expect(within(chat).getByText('Person')).toBeInTheDocument()
    expect(calls.some((c) => c.url === '/api/sessions/session-abc/updates?after=2')).toBe(true)

    news = { entries: [], next: 4, handoff: { name: 'Asha' } }
    await user.type(within(chat).getByLabelText('Your message'), 'My kettle leaks.{Enter}')
    expect(await within(chat).findByText('My kettle leaks.')).toBeInTheDocument()
    expect(within(chat).queryByLabelText('The assistant is typing')).not.toBeInTheDocument()
    // No empty assistant bubble: the person answers through the check.
    expect(chat.querySelectorAll('.sc-bubble.assistant')).toHaveLength(1)
  })

  it('shows a count on the button when the person writes while the chat is closed', async () => {
    const { user } = await openShopAsPriya(
      {
        'GET /api/sessions/session-abc/updates': () => ({
          body: { entries: [{ role: 'staff', text: 'Are you still there?', name: 'Asha' }], next: 3, handoff: { name: 'Asha' } },
        }),
      },
      false,
    )

    await waitForCheck()
    const launcher = screen.getByRole('button', { name: /Chat with us/ })
    expect(launcher).toHaveTextContent('1 new')

    await user.click(launcher)
    expect(screen.getByText('Are you still there?')).toBeVisible()
  })
})

describe('the customer under Your tickets', () => {
  it('reads the messages from the team and answers', async () => {
    const ticket: CustomerTicket = {
      ticket_id: 'TCK-20261121-AAA111', created_at: '2026-11-21T09:00:00+00:00', status: 'in_progress', topic: 'Asked for a person',
      summary: 'Wants a person.', order_id: null, source: 'chat', assigned_name: 'Asha',
      messages: [{ from: 'staff', name: 'Asha', text: 'We can send a new kettle.', at: '2026-11-21T09:05:00+00:00' }],
    }
    const { user, calls } = await openShopAsPriya(
      {
        'GET /api/sessions/session-abc/tickets': () => ({ body: [ticket] }),
        'GET /api/sessions/session-abc/updates': () => ({ body: { entries: [], next: 2, handoff: null } }),
        'POST /api/sessions/session-abc/tickets/TCK-20261121-AAA111/messages': (body) => ({
          body: { ...ticket, messages: [...ticket.messages!, { from: 'customer', text: (body as { text: string }).text, at: '2026-11-21T10:00:00+00:00' }] },
        }),
      },
      false,
    )
    const tickets = screen.getByRole('region', { name: 'Your tickets' })
    expect(await within(tickets).findByText('With Asha')).toBeInTheDocument()

    await user.click(within(tickets).getByRole('button', { name: /Messages \(1\)/ }))
    expect(within(tickets).getByText('We can send a new kettle.')).toBeInTheDocument()
    await user.type(within(tickets).getByLabelText('Reply on TCK-20261121-AAA111'), 'Yes please')
    await user.click(within(tickets).getByRole('button', { name: 'Send' }))

    expect(await within(tickets).findByText('Yes please')).toBeInTheDocument()
    expect(calls.find((c) => c.method === 'POST')?.body).toEqual({ text: 'Yes please' })
  })
})
