// Tests for the "behind the scenes" panel. The API is a fake, so nothing is paid.
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import App from './App'
import type { ReplyDetails, Session } from './api'
import { BehindTheScenes } from './components/BehindTheScenes'

const SESSION: Session = {
  role: 'customer',
  session_id: 'session-abc',
  conversation_id: 'conv_000000000001',
  customer: { name: 'Priya Nair', email: 'priya.nair@example.com', order_count: 0 },
  orders: [],
  transcript: [],
  assistant_name: 'Juniper Lane Goods virtual assistant',
}

const LOOKUP: ReplyDetails = {
  turn: 1,
  steps: 2,
  tools_used: ['lookup_order'],
  escalated: false,
  violations: [],
  gave_up_because: null,
  input_tokens: 6417,
  output_tokens: 165,
  cost_usd: 0.007242,
  duration_ms: 3724,
  events: [
    { event: 'model_call', step: 1, duration_ms: 1766, input_tokens: 2503, output_tokens: 69, tools_requested: ['lookup_order'], is_rewrite: false },
    { event: 'tool_call', step: 1, tool: 'lookup_order', input: { order_id: 'JL-10231' }, is_error: false, duration_ms: 2, result_preview: '{"status": "delivered"}' },
    { event: 'model_call', step: 2, duration_ms: 1553, input_tokens: 3914, output_tokens: 96, tools_requested: [], is_rewrite: false },
  ],
}

const BLOCKED: ReplyDetails = {
  ...LOOKUP,
  tools_used: [],
  escalated: true,
  violations: ['refund_claim'],
  gave_up_because: 'reply blocked by safety check: refund claim',
  events: [
    { event: 'model_call', step: 1, duration_ms: 900, input_tokens: 2000, output_tokens: 40, tools_requested: [], is_rewrite: false },
    { event: 'reply_blocked', step: 1, rules: ['refund_claim'], details: 'claimed a refund' },
    { event: 'ticket_created', ticket_id: 'TCK-20261120-ABC123', reason: 'other', created_by: 'harness' },
  ],
}

function fakeApi() {
  vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, init) => {
    const url = String(input)
    const method = init?.method ?? 'GET'
    let body: unknown = SESSION
    let status = 200
    if (url === '/api/sessions' && method === 'POST') status = 201
    else if (url === '/api/products' || url.endsWith('/tickets')) body = []
    else if (url.endsWith('/messages')) body = { reply: 'Reply one', outcome: 'completed', new_ticket_ids: [] }
    return new Response(JSON.stringify(body), { status })
  })
}

describe('customers', () => {
  it('never see the panel: it is for the admin only', async () => {
    fakeApi()
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByLabelText('Email'), 'priya.nair@example.com')
    await user.type(screen.getByLabelText('Password'), 'test-pass')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))
    await user.click(await screen.findByRole('button', { name: 'Chat with us' }))
    await user.type(screen.getByLabelText('Your message'), 'Hi{Enter}')
    await screen.findByText('Reply one')

    expect(screen.queryByRole('button', { name: 'Behind the scenes' })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'How was this answered?' })).not.toBeInTheDocument()
    expect(screen.queryByRole('complementary', { name: 'Behind the scenes' })).not.toBeInTheDocument()
  })
})

describe('the panel on its own', () => {
  it('shows checks that fired and a ticket the harness created', () => {
    render(
      <BehindTheScenes details={BLOCKED} outcome="reply_blocked" conversationId="conv_x" replyNumber={2} onClose={() => {}} />,
    )

    expect(screen.getByText('Reply replaced by a safe one')).toBeInTheDocument()
    expect(screen.getByText(/Code checks fired:/).parentElement).toHaveTextContent('Claimed to give a refund')
    expect(screen.getByText('Check withheld the reply')).toBeInTheDocument()
    expect(screen.getByText('Ticket TCK-20261120-ABC123')).toBeInTheDocument()
    expect(screen.getByText(/the harness \(automatic\)/)).toBeInTheDocument()
    expect(screen.getByText('Yes')).toBeInTheDocument()
  })

  it('explains why a reply restored after a refresh has no details', () => {
    render(<BehindTheScenes details={null} outcome={undefined} conversationId="conv_x" replyNumber={1} onClose={() => {}} />)

    expect(screen.getByText(/only kept for replies sent during this visit/)).toBeInTheDocument()
  })

  it('invites a first message when nothing has been sent yet', () => {
    render(<BehindTheScenes details={undefined} outcome={undefined} conversationId="conv_x" replyNumber={null} onClose={() => {}} />)

    expect(screen.getByText(/Send a message to see each step here/)).toBeInTheDocument()
  })

  it('shows retries and rewrites in plain words', () => {
    const details: ReplyDetails = {
      ...LOOKUP,
      violations: ['ungrounded_figure'],
      events: [
        { event: 'retry', operation: 'model_call', attempt: 1, max_attempts: 3, wait_ms: 1200 },
        { event: 'reply_rewrite', step: 1, rules: ['ungrounded_figure'] },
        { event: 'model_call', step: 2, duration_ms: 800, input_tokens: 10, output_tokens: 5, tools_requested: [], is_rewrite: true },
      ],
    }
    render(<BehindTheScenes details={details} outcome="completed" conversationId="conv_x" replyNumber={1} onClose={() => {}} />)

    expect(screen.getByText('Retried after a temporary failure')).toBeInTheDocument()
    expect(screen.getByText(/attempt 1 of 3 · waited 1.2 s/)).toBeInTheDocument()
    expect(screen.getByText('Check caught the draft, asked for a rewrite')).toBeInTheDocument()
    expect(screen.getByText('Model rewrote its reply')).toBeInTheDocument()
  })
})
