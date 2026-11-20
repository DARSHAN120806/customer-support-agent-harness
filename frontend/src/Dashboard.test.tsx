// Tests for the support dashboard. The API is a fake, so nothing is paid.
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import type { ConversationSummary, EvaluationRun, HarnessEvent, Ticket } from './api'
import { groupTurns } from './turns'

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
  { event: 'turn_end', turn: 1, outcome: 'completed', cost_usd: 0.0123, duration_ms: 4200, violations: ['unverified_policy'], reply: 'Your ticket is TCK-20261120-AAA111.' },
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
  return vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
    const url = String(input)
    const routes: Record<string, unknown> = {
      '/api/tickets': TICKETS,
      '/api/conversations?limit=200': CONVERSATIONS,
      '/api/conversations/conv_aaaaaaaaaaaa': EVENTS,
      '/api/evaluations': RUNS,
      '/api/customers?q=&limit=8': [],
      ...overrides,
    }
    if (url in routes) return new Response(JSON.stringify(routes[url]), { status: 200 })
    return new Response(JSON.stringify({ detail: 'Not found' }), { status: 404 })
  })
}

async function openDashboard() {
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
  it('opens from the sign-in page and goes back to the chat', async () => {
    fakeApi()
    const user = userEvent.setup()
    render(<App />)

    await user.click(screen.getByRole('button', { name: 'Open the support dashboard' }))
    expect(await screen.findByRole('heading', { name: 'Support dashboard' })).toBeInTheDocument()
    expect(window.location.hash).toBe('#/dashboard')
    expect(screen.getByRole('note')).toHaveTextContent(/no password/)

    await user.click(screen.getByRole('button', { name: 'Customer chat' }))
    expect(await screen.findByLabelText(/Find a customer/)).toBeInTheDocument()
  })
})

describe('tickets', () => {
  it('lists tickets with masked emails, and filters them', async () => {
    fakeApi()
    const user = await openDashboard()

    const table = await screen.findByRole('table')
    expect(within(table).getByText('TCK-20261120-AAA111')).toBeInTheDocument()
    expect(within(table).getByText('upset customer')).toBeInTheDocument()
    expect(screen.getByText('2 of 2 tickets')).toBeInTheDocument()

    await user.selectOptions(screen.getByLabelText('Reason'), 'refund_request')
    expect(screen.getByText('1 of 2 tickets')).toBeInTheDocument()
    expect(within(table).queryByText('TCK-20261120-BBB222')).not.toBeInTheDocument()

    await user.selectOptions(screen.getByLabelText('Reason'), 'all')
    await user.type(screen.getByLabelText('Search'), 'emailed three')
    expect(screen.getByText('1 of 2 tickets')).toBeInTheDocument()
  })

  it('opens the conversation behind a ticket', async () => {
    fakeApi()
    const user = await openDashboard()

    await user.click(await screen.findByRole('button', { name: 'View chat' }))

    expect(await screen.findByRole('region', { name: 'Conversation replay' })).toBeInTheDocument()
    // The ticket number is highlighted, so the sentence is split into pieces;
    // look for the paragraph that holds the whole sentence.
    const reply = await screen.findByText(
      (_, element) => element?.tagName === 'P' && element.textContent === 'Your ticket is TCK-20261120-AAA111.',
    )
    expect(reply.querySelector('.ticket-ref')).toHaveTextContent('TCK-20261120-AAA111')
  })

  it('says so when there are no tickets yet', async () => {
    fakeApi({ '/api/tickets': [] })
    await openDashboard()

    expect(await screen.findByText(/No tickets yet/)).toBeInTheDocument()
  })
})

describe('conversations', () => {
  it('lists conversations and replays one step by step', async () => {
    fakeApi()
    const user = await openDashboard()
    await user.click(screen.getByRole('button', { name: 'Conversations' }))

    const table = await screen.findByRole('table')
    expect(within(table).getByText('cust_123456789abc')).toBeInTheDocument()
    expect(within(table).getByText('$0.012')).toBeInTheDocument()

    await user.click(within(table).getByRole('button', { name: 'Replay' }))
    const replay = await screen.findByRole('region', { name: 'Conversation replay' })
    expect(within(replay).getByText('I want a refund, my email is [EMAIL]')).toBeInTheDocument()
    expect(within(replay).getByText(/checks fired: Policy stated without looking it up/)).toBeInTheDocument()
    expect(within(replay).getByText('Check caught the draft, asked for a rewrite')).toBeInTheDocument()

    await user.click(within(replay).getByRole('button', { name: '← All conversations' }))
    expect(await screen.findByRole('region', { name: 'Conversations' })).toBeInTheDocument()
  })

  it('groups log lines into customer messages', () => {
    const { start, turns } = groupTurns(EVENTS)

    expect(start?.model).toBe('test-model')
    expect(turns).toHaveLength(1)
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

    const table = await screen.findByRole('table')
    expect(within(table).getAllByRole('row')).toHaveLength(4)
    expect(within(table).getByText('not counted')).toBeInTheDocument()
    expect(screen.getByRole('checkbox', { name: 'Compare harness on' })).not.toBeChecked()
    expect(screen.getByRole('checkbox', { name: 'Compare harness on counted' })).toBeChecked()
    expect(screen.getByRole('checkbox', { name: 'Compare harness off run1' })).toBeChecked()
    expect(screen.getByText('Cases passed per group (%)')).toBeInTheDocument()
    expect(screen.getByText('Rule violations the customer would have seen')).toBeInTheDocument()
  })

  it('asks for a run to be ticked when none is chosen', async () => {
    fakeApi()
    const user = await openDashboard()
    await user.click(screen.getByRole('button', { name: 'Evaluations' }))
    await screen.findByRole('table')

    await user.click(screen.getByRole('checkbox', { name: 'Compare harness on counted' }))
    await user.click(screen.getByRole('checkbox', { name: 'Compare harness off run1' }))

    expect(screen.getByText('Tick at least one run to compare.')).toBeInTheDocument()
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
    window.location.hash = '#/dashboard'
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new TypeError('Failed to fetch'))
    render(<App />)

    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent(/could not be reached/))
  })
})
