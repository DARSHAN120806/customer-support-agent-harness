// Tests for the support dashboard. The API is a fake, so nothing is paid.
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import type { ConversationSummary, EvaluationRun, HarnessEvent, Stats, Ticket } from './api'
import { detailsOf, groupTurns } from './turns'

const TICKETS: Ticket[] = [
  {
    ticket_id: 'TCK-20261120-AAA111',
    created_at: '2026-11-20T10:05:00+00:00',
    status: 'open',
    conversation_id: 'conv_aaaaaaaaaaaa',
    customer_email: '[EMAIL]',
    reason: 'refund_request',
    order_id: 'JL-10231',
    summary: 'Customer wants a refund for the coffee set.',
  },
  {
    ticket_id: 'TCK-20261120-BBB222',
    created_at: '2026-11-20T09:00:00+00:00',
    status: 'open',
    conversation_id: null,
    customer_email: '[EMAIL]',
    reason: 'upset_customer',
    order_id: null,
    summary: 'Emailed three times without an answer.',
  },
]

const STATS: Stats = {
  conversations: 9,
  customers: 4,
  messages: 11,
  tickets: 3,
  open_tickets: 3,
  tickets_by_harness: 1,
  handover_rate: 0.333,
  cost_usd: 0.08,
  cost_per_message_usd: 0.0073,
  average_reply_ms: 5400,
  outcomes: { completed: 10, reply_blocked: 1 },
  checks: { identity_leak: 2, unverified_policy: 1 },
  tickets_by_reason: { refund_request: 2, upset_customer: 1 },
  days: [
    { date: '2026-11-19', messages: 0, tickets: 0 },
    { date: '2026-11-20', messages: 11, tickets: 3 },
  ],
}

const CONVERSATIONS: ConversationSummary[] = [
  {
    conversation_id: 'conv_aaaaaaaaaaaa',
    started_at: '2026-11-20T10:00:00+00:00',
    last_at: '2026-11-20T10:05:00+00:00',
    customer_ref: 'cust_123456789abc',
    model: 'test-model',
    harness: true,
    turns: 1,
    cost_usd: 0.0123,
    escalated: true,
    blocked_or_rewritten: 1,
    first_message: 'I want a refund, my email is [EMAIL]',
  },
]

const EVENTS: HarnessEvent[] = [
  { event: 'conversation_start', turn: 0, model: 'test-model', date_used: '2026-11-20', harness: true },
  { event: 'turn_start', turn: 1, message: 'I want a refund, my email is [EMAIL]' },
  { event: 'model_call', turn: 1, step: 1, duration_ms: 900, input_tokens: 100, output_tokens: 20, tools_requested: [], is_rewrite: false },
  { event: 'reply_rewrite', turn: 1, step: 1, rules: ['unverified_policy'] },
  { event: 'ticket_created', turn: 1, ticket_id: 'TCK-20261120-AAA111', reason: 'refund_request', created_by: 'model' },
  { event: 'turn_end', turn: 1, outcome: 'completed', steps: 1, input_tokens: 100, output_tokens: 20, cost_usd: 0.0123, duration_ms: 4200, escalated: true, tools_used: [], violations: ['unverified_policy'], reply: 'Your ticket is TCK-20261120-AAA111.' },
  { event: 'turn_start', turn: 2, message: 'Thanks' },
  { event: 'model_call', turn: 2, step: 1, duration_ms: 500, input_tokens: 50, output_tokens: 10, tools_requested: [], is_rewrite: false },
  { event: 'turn_end', turn: 2, outcome: 'completed', steps: 1, input_tokens: 50, output_tokens: 10, cost_usd: 0.001, duration_ms: 600, escalated: false, tools_used: [], violations: [], reply: 'You are welcome.' },
]

function run(name: string, harness: string, passed: number, violations?: Record<string, number>): EvaluationRun {
  return {
    name,
    run_at: '2026-11-20T18:30:00',
    model: 'test-model',
    harness,
    summary: {
      passed,
      total: 41,
      cost_usd: 0.33,
      by_category: { easy: { passed: 9, total: 9 }, attack: { passed: 11, total: 11 } },
      ...(violations ? { violations, violation_total: Object.values(violations).reduce((a, b) => a + b, 0) } : {}),
    },
  }
}

const RUNS = [
  run('haiku45_harness_on', 'on', 39),
  run('haiku45_harness_on_counted', 'on', 39, { missed_ticket: 1 }),
  run('haiku45_harness_off_run1', 'off', 38, { missed_ticket: 2, invented_figure: 1 }),
]

function fakeApi(overrides: Record<string, unknown> = {}) {
  return vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, init) => {
    const url = String(input)
    if (url === '/api/sessions') {
      return new Response(JSON.stringify({ role: 'admin', admin_token: 'admin-token-1' }), { status: 201 })
    }
    if (url === '/api/admin/session') return new Response(null, { status: 204 })
    // Every dashboard request must carry the admin's key.
    const auth = new Headers(init?.headers).get('Authorization')
    if (auth !== 'Bearer admin-token-1') {
      return new Response(JSON.stringify({ detail: 'Please sign in as an admin.' }), { status: 401 })
    }
    const routes: Record<string, unknown> = {
      '/api/stats': STATS,
      '/api/tickets': TICKETS,
      '/api/conversations?limit=200': CONVERSATIONS,
      '/api/conversations/conv_aaaaaaaaaaaa': EVENTS,
      '/api/evaluations': RUNS,
      ...overrides,
    }
    if (url in routes) return new Response(JSON.stringify(routes[url]), { status: 200 })
    return new Response(JSON.stringify({ detail: 'Not found' }), { status: 404 })
  })
}

async function openDashboard() {
  sessionStorage.setItem('juniper-lane-admin', 'admin-token-1')
  window.location.hash = '#/dashboard'
  const user = userEvent.setup()
  render(<App />)
  await screen.findByRole('heading', { name: 'Support dashboard' })
  return user
}

afterEach(() => {
  window.location.hash = ''
})

describe('getting to the dashboard', () => {
  it('opens when the admin signs in, and signing out closes it', async () => {
    const fetchSpy = fakeApi()
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByLabelText('Email'), 'admin@juniperlane.example')
    await user.type(screen.getByLabelText('Password'), 'admin-pass')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))
    expect(await screen.findByRole('heading', { name: 'Support dashboard' })).toBeInTheDocument()
    expect(window.location.hash).toBe('#/dashboard')
    expect(sessionStorage.getItem('juniper-lane-admin')).toBe('admin-token-1')
    expect(await screen.findByText(TICKETS[0].ticket_id)).toBeInTheDocument() // the key was accepted

    await user.click(screen.getByRole('button', { name: 'Sign out' }))
    expect(await screen.findByRole('button', { name: 'Sign in' })).toBeInTheDocument()
    expect(sessionStorage.getItem('juniper-lane-admin')).toBeNull()
    expect(fetchSpy.mock.calls.some(([url, init]) => url === '/api/admin/session' && init?.method === 'DELETE')).toBe(true)
  })

  it('asks for the admin sign-in when the dashboard is opened without it', async () => {
    fakeApi()
    window.location.hash = '#/dashboard'
    render(<App />)

    expect(screen.getByRole('status')).toHaveTextContent('Sign in with an admin or support staff account to open the dashboard')
    expect(screen.queryByRole('heading', { name: 'Support dashboard' })).not.toBeInTheDocument()
  })
})

describe('overview', () => {
  it('opens first, with the numbers, the checks that fired and recent tickets', async () => {
    fakeApi()
    await openDashboard()

    expect(await screen.findByRole('heading', { name: 'Overview' })).toBeInTheDocument()
    expect(screen.getByText('Messages answered').parentElement).toHaveTextContent('11')
    expect(screen.getByText('Handed to a person').parentElement).toHaveTextContent('33%')
    expect(screen.getByText('5.4 s average reply time')).toBeInTheDocument()
    const checks = screen.getByRole('region', { name: 'Checks that fired' })
    expect(within(checks).getByText('Named the AI behind the assistant')).toBeInTheDocument()
    expect(screen.getByText('TCK-20261120-AAA111')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Overview' })).toHaveAttribute('aria-current', 'page')
  })

  it('goes to all tickets from the recent list', async () => {
    fakeApi()
    const user = await openDashboard()

    await user.click(await screen.findByRole('button', { name: 'All tickets' }))

    expect(await screen.findByRole('heading', { name: 'Tickets' })).toBeInTheDocument()
  })
})

describe('tickets', () => {
  it('lists tickets with masked emails, and filters them', async () => {
    fakeApi()
    const user = await openDashboard()
    await user.click(screen.getByRole('button', { name: 'Tickets' }))

    const table = await screen.findByRole('table')
    expect(within(table).getByText('TCK-20261120-AAA111')).toBeInTheDocument()
    expect(within(table).getByText('Upset customer')).toBeInTheDocument()
    expect(screen.getByText('2 of 2 tickets')).toBeInTheDocument()

    await user.selectOptions(screen.getByLabelText('Reason'), 'refund_request')
    expect(screen.getByText('1 of 2 tickets')).toBeInTheDocument()
    expect(within(table).queryByText('TCK-20261120-BBB222')).not.toBeInTheDocument()

    await user.selectOptions(screen.getByLabelText('Reason'), 'all')
    await user.type(screen.getByLabelText('Search'), 'emailed three')
    expect(screen.getByText('1 of 2 tickets')).toBeInTheDocument()
  })

  it('opens a ticket from the overview, where it can be answered', async () => {
    // Found 21 Nov 2026: "View chat" here led to the read-only replay, with no
    // way to answer the customer. "Open" now opens the ticket itself.
    const detail = { ticket: { ...TICKETS[0], assigned_to: null, messages: [] }, chat: [], customer: null }
    fakeApi({ '/api/tickets/TCK-20261120-AAA111': detail })
    const user = await openDashboard()

    const recent = await screen.findByRole('heading', { name: 'Recent tickets' })
    const row = within(recent.closest('section')!).getByText('TCK-20261120-AAA111').closest('li')!
    await user.click(within(row).getByRole('button', { name: 'Open' }))

    const view = await screen.findByRole('region', { name: 'Ticket TCK-20261120-AAA111' })
    expect(within(view).getByRole('button', { name: 'Take ticket' })).toBeInTheDocument()
  })

  it('opens the conversation behind a ticket, and leads back to the ticket', async () => {
    const detail = { ticket: { ...TICKETS[0], assigned_to: null, messages: [] }, chat: [], customer: null }
    fakeApi({ '/api/tickets/TCK-20261120-AAA111': detail })
    const user = await openDashboard()
    await user.click(screen.getByRole('button', { name: 'Conversations' }))
    await user.click((await screen.findAllByRole('button', { name: 'Replay' }))[0])

    expect(await screen.findByRole('region', { name: 'Conversation replay' })).toBeInTheDocument()
    // The ticket number is highlighted, so the sentence is split into pieces;
    // look for the paragraph that holds the whole sentence.
    const reply = await screen.findByText(
      (_, element) => element?.tagName === 'P' && element.textContent === 'Your ticket is TCK-20261120-AAA111.',
    )
    expect(reply.querySelector('.ticket-ref')).toHaveTextContent('TCK-20261120-AAA111')

    // The replay is read only, and says where to answer.
    expect(screen.getByText(/This replay is read only/)).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'TCK-20261120-AAA111' }))
    expect(await screen.findByRole('region', { name: 'Ticket TCK-20261120-AAA111' })).toBeInTheDocument()
  })

  it('says so when there are no tickets yet', async () => {
    fakeApi({ '/api/tickets': [] })
    const user = await openDashboard()
    await user.click(screen.getByRole('button', { name: 'Tickets' }))

    expect(await screen.findByText(/No tickets yet. They appear here/)).toBeInTheDocument()
  })
})

describe('conversations', () => {
  it('lists conversations and replays one step by step', async () => {
    fakeApi()
    const user = await openDashboard()
    await user.click(screen.getByRole('button', { name: 'Conversations' }))

    const table = await screen.findByRole('table')
    expect(within(table).getByText('cust_123456789abc')).toBeInTheDocument()
    expect(within(table).getByText('$0.0123')).toBeInTheDocument()

    await user.click(within(table).getByRole('button', { name: 'Replay' }))
    const replay = await screen.findByRole('region', { name: 'Conversation replay' })
    expect(within(replay).getByText('I want a refund, my email is [EMAIL]')).toBeInTheDocument()
    expect(within(replay).getByText(/checks fired: Policy stated without looking it up/)).toBeInTheDocument()
    await user.click(within(replay).getByRole('button', { name: 'Show how reply 1 was made' }))
    expect(within(replay).getByText('Check caught the draft, asked for a rewrite')).toBeInTheDocument()

    await user.click(within(replay).getByRole('button', { name: '← All conversations' }))
    expect(await screen.findByRole('region', { name: 'Conversations' })).toBeInTheDocument()
  })

  it('shows behind the scenes for the newest reply, and for any reply clicked', async () => {
    fakeApi()
    const user = await openDashboard()
    await user.click(screen.getByRole('button', { name: 'Conversations' }))
    await user.click(await screen.findByRole('button', { name: 'Replay' }))

    const panel = await screen.findByRole('complementary', { name: 'Behind the scenes' })
    expect(within(panel).getByText('What the harness did for reply 2')).toBeInTheDocument()
    expect(within(panel).getByText('All code checks passed')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Show how reply 1 was made' }))
    expect(within(panel).getByText('What the harness did for reply 1')).toBeInTheDocument()
    expect(within(panel).getByText(/Code checks fired:/).parentElement).toHaveTextContent('Policy stated without looking it up')
    expect(within(panel).getByText('100 in · 20 out')).toBeInTheDocument()
    expect(within(panel).getByText('Ticket TCK-20261120-AAA111')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Show how reply 1 was made' })).toHaveAttribute('aria-pressed', 'true')
  })

  it('says so when a conversation has no messages', async () => {
    fakeApi({ '/api/conversations/conv_aaaaaaaaaaaa': [EVENTS[0]] })
    const user = await openDashboard()
    await user.click(screen.getByRole('button', { name: 'Conversations' }))
    await user.click(await screen.findByRole('button', { name: 'Replay' }))

    expect(await screen.findByText('No messages in this conversation')).toBeInTheDocument()
    expect(screen.queryByRole('complementary', { name: 'Behind the scenes' })).not.toBeInTheDocument()
  })

  it('rebuilds the details of a reply from its log lines', () => {
    const { turns } = groupTurns(EVENTS)
    const details = detailsOf(turns[0])

    expect(details).toMatchObject({ steps: 1, input_tokens: 100, cost_usd: 0.0123, escalated: true, violations: ['unverified_policy'] })
    expect(details?.events.map((e) => e.event)).toEqual(['model_call', 'reply_rewrite', 'ticket_created'])
    expect(detailsOf({ number: 3, message: 'Still writing', steps: [] })).toBeNull()
  })

  it('groups log lines into customer messages', () => {
    const { start, turns } = groupTurns(EVENTS)

    expect(start?.model).toBe('test-model')
    expect(turns).toHaveLength(2)
    expect(turns[0].message).toBe('I want a refund, my email is [EMAIL]')
    expect(turns[0].steps.map((e) => e.event)).toEqual(['model_call', 'reply_rewrite', 'ticket_created'])
    expect(turns[0].end?.reply).toBe('Your ticket is TCK-20261120-AAA111.')
  })
})

describe('evaluations', () => {
  it('lists every saved run and compares the harness on/off runs by default', async () => {
    fakeApi()
    const user = await openDashboard()
    await user.click(screen.getByRole('button', { name: 'Evaluations' }))

    const table = await screen.findByRole('table', { name: 'Saved runs' })
    expect(within(table).getAllByRole('row')).toHaveLength(4)
    expect(within(table).getByText('not counted')).toBeInTheDocument()
    expect(screen.getByRole('checkbox', { name: 'Compare harness on' })).not.toBeChecked()
    expect(screen.getByRole('checkbox', { name: 'Compare harness on counted' })).toBeChecked()
    expect(screen.getByRole('checkbox', { name: 'Compare harness off run1' })).toBeChecked()
    expect(screen.getByText('Cases passed per group (%)')).toBeInTheDocument()
    expect(screen.getByText('Rule violations the customer would have seen')).toBeInTheDocument()

    // Violations are a short table, not a second chart.
    const violations = screen.getByRole('table', { name: 'Violations per run' })
    const missed = within(violations).getByText('Missed ticket').closest('tr')!
    expect(missed).toHaveTextContent('Missed ticket12')
    expect(within(violations).getByText('Total').closest('tr')).toHaveTextContent('Total13')
  })

  it('asks for a run to be ticked when none is chosen', async () => {
    fakeApi()
    const user = await openDashboard()
    await user.click(screen.getByRole('button', { name: 'Evaluations' }))
    await screen.findByRole('table', { name: 'Saved runs' })

    await user.click(screen.getByRole('checkbox', { name: 'Compare harness on counted' }))
    await user.click(screen.getByRole('checkbox', { name: 'Compare harness off run1' }))

    expect(screen.getByText('Tick at least one run to compare')).toBeInTheDocument()
  })

  it('explains when the chosen runs have no violation counts', async () => {
    fakeApi({ '/api/evaluations': [run('old_run', 'on', 39)] })
    const user = await openDashboard()
    await user.click(screen.getByRole('button', { name: 'Evaluations' }))

    expect(await screen.findByText(/saved before violations were counted/)).toBeInTheDocument()
  })
})

describe('errors', () => {
  it('shows a message when the API cannot be reached', async () => {
    sessionStorage.setItem('juniper-lane-admin', 'admin-token-1')
    window.location.hash = '#/dashboard'
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new TypeError('Failed to fetch'))
    render(<App />)

    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent(/could not be reached/))
  })
})
