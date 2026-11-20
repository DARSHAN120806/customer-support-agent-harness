// Tests for the customer chat page. The API is replaced by a fake, so no
// server and no paid model calls are needed.
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import App from './App'
import type { Reply, Session } from './api'
import { FormattedText } from './components/FormattedText'

const PRIYA = { name: 'Priya Nair', email: 'priya.nair@example.com', order_count: 2 }

const SESSION: Session = {
  session_id: 'session-abc',
  conversation_id: 'conv_000000000001',
  customer: PRIYA,
  orders: [
    { order_id: 'JL-10198', placed_on: '2026-09-14', status: 'delivered', total: 44.98, items: ['Bluetooth Speaker Mini'] },
    { order_id: 'JL-10231', placed_on: '2026-11-03', status: 'delivered', total: 60.5, items: ['Ceramic Pour-Over Coffee Set', 'Linen Napkins (Set of 4)'] },
  ],
  transcript: [],
  assistant_name: 'Juniper Lane Goods virtual assistant',
}

function reply(text: string, tickets: string[] = []): Reply {
  return { reply: text, outcome: 'completed', new_ticket_ids: tickets, details: null }
}

type Handler = (url: string, init?: RequestInit) => { status?: number; body?: unknown }

// Replaces the browser's fetch with a fake API and records every request.
function fakeApi(handler: Handler) {
  const calls: { url: string; method: string; body: unknown }[] = []
  vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, init) => {
    const url = String(input)
    calls.push({ url, method: init?.method ?? 'GET', body: init?.body ? JSON.parse(String(init.body)) : undefined })
    const { status = 200, body } = handler(url, init)
    return new Response(status === 204 ? null : JSON.stringify(body), { status })
  })
  return calls
}

function defaultApi(overrides: Partial<Record<string, () => { status?: number; body?: unknown }>> = {}) {
  return fakeApi((url, init) => {
    const method = init?.method ?? 'GET'
    for (const [key, make] of Object.entries(overrides)) {
      if (url.includes(key) && make) return make()
    }
    if (url.startsWith('/api/customers')) return { body: [PRIYA] }
    if (url === '/api/sessions' && method === 'POST') return { status: 201, body: SESSION }
    if (url.endsWith('/messages')) return { body: reply('Your order was delivered on 2026-11-07.') }
    if (method === 'DELETE') return { status: 204 }
    if (url.startsWith('/api/sessions/')) return { body: SESSION }
    return { status: 404, body: { detail: 'Not found' } }
  })
}

async function signInAsPriya() {
  const user = userEvent.setup()
  render(<App />)
  await user.click(await screen.findByRole('button', { name: /Priya Nair/ }))
  await screen.findByRole('heading', { name: 'Juniper Lane Goods virtual assistant' })
  return user
}

describe('sign-in', () => {
  it('shows the demo warning and finds customers as you type', async () => {
    const calls = defaultApi()
    const user = userEvent.setup()
    render(<App />)

    expect(screen.getByRole('note')).toHaveTextContent(/Demo sign-in/)
    await user.type(screen.getByLabelText(/Find a customer/), 'priya')

    await waitFor(() => expect(calls.some((c) => c.url === '/api/customers?q=priya&limit=8')).toBe(true))
    expect(await screen.findByRole('button', { name: /Priya Nair/ })).toHaveTextContent('2 orders')
  })

  it('signs in and opens the chat with your own orders', async () => {
    const calls = defaultApi()
    await signInAsPriya()

    expect(calls.find((c) => c.url === '/api/sessions')?.body).toEqual({ email: PRIYA.email })
    const orders = screen.getByRole('complementary', { name: 'Your orders' })
    expect(within(orders).getByText('JL-10231')).toBeInTheDocument()
    expect(within(orders).getByText('JL-10198')).toBeInTheDocument()
    expect(screen.getByText(/Hi Priya!/)).toBeInTheDocument()
    expect(sessionStorage.getItem('juniper-lane-session')).toBe('session-abc')
  })

  it('says so when the server cannot be reached', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new TypeError('Failed to fetch'))
    render(<App />)

    expect(await screen.findByRole('alert')).toHaveTextContent(/could not be reached/)
  })
})

describe('chatting', () => {
  it('sends a message and shows the reply', async () => {
    const calls = defaultApi()
    const user = await signInAsPriya()

    await user.type(screen.getByLabelText('Your message'), 'Where is JL-10231?{Enter}')

    expect(await screen.findByText('Your order was delivered on 2026-11-07.')).toBeInTheDocument()
    expect(screen.getByText('Where is JL-10231?')).toBeInTheDocument()
    expect(calls.find((c) => c.url.endsWith('/messages'))?.body).toEqual({ text: 'Where is JL-10231?' })
    expect(screen.getByLabelText('Your message')).toHaveValue('')
  })

  it('shows a typing indicator and blocks a second send while waiting', async () => {
    let finish: (value: Response) => void = () => undefined
    defaultApi()
    const user = await signInAsPriya()
    vi.mocked(fetch).mockImplementationOnce(() => new Promise((resolve) => (finish = resolve)))

    await user.type(screen.getByLabelText('Your message'), 'Hello{Enter}')

    expect(screen.getByLabelText('The assistant is typing')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Sending…' })).toBeDisabled()
    finish(new Response(JSON.stringify(reply('Hi there!')), { status: 200 }))
    expect(await screen.findByText('Hi there!')).toBeInTheDocument()
    expect(screen.queryByLabelText('The assistant is typing')).not.toBeInTheDocument()
  })

  it('highlights a new ticket number', async () => {
    defaultApi({ '/messages': () => ({ body: reply('Your ticket is TCK-20261120-ABC123.', ['TCK-20261120-ABC123']) }) })
    const user = await signInAsPriya()

    await user.type(screen.getByLabelText('Your message'), 'I want a human{Enter}')

    expect(await screen.findByText(/Our team will reply by email/)).toHaveTextContent('TCK-20261120-ABC123')
  })

  it('puts a question about an order into the message box', async () => {
    defaultApi()
    const user = await signInAsPriya()

    await user.click(screen.getAllByRole('button', { name: 'Ask about this order' })[0])

    expect(screen.getByLabelText('Your message')).toHaveValue("What's the status of my order JL-10231?")
  })

  it('a suggestion button sends straight away', async () => {
    const calls = defaultApi()
    const user = await signInAsPriya()

    await user.click(screen.getByRole('button', { name: 'What is your return policy?' }))

    await waitFor(() =>
      expect(calls.find((c) => c.url.endsWith('/messages'))?.body).toEqual({ text: 'What is your return policy?' }),
    )
  })

  it('shows an error from the server inside the chat', async () => {
    defaultApi({ '/messages': () => ({ status: 409, body: { detail: 'Please wait for the reply to your last message.' } }) })
    const user = await signInAsPriya()

    await user.type(screen.getByLabelText('Your message'), 'Hello{Enter}')

    expect(await screen.findByText('Please wait for the reply to your last message.')).toBeInTheDocument()
  })

  it('goes back to sign-in when the chat has expired', async () => {
    defaultApi({ '/messages': () => ({ status: 404, body: { detail: 'This chat has ended.' } }) })
    const user = await signInAsPriya()

    await user.type(screen.getByLabelText('Your message'), 'Hello{Enter}')

    expect(await screen.findByRole('status')).toHaveTextContent(/idle for a while/)
    expect(screen.getByLabelText(/Find a customer/)).toBeInTheDocument()
  })

  it('signs out and forgets the chat', async () => {
    const calls = defaultApi()
    const user = await signInAsPriya()

    await user.click(screen.getByRole('button', { name: 'Sign out' }))

    expect(await screen.findByLabelText(/Find a customer/)).toBeInTheDocument()
    expect(calls.some((c) => c.method === 'DELETE' && c.url === '/api/sessions/session-abc')).toBe(true)
    expect(sessionStorage.getItem('juniper-lane-session')).toBeNull()
  })

  it('picks the chat up again after a page refresh', async () => {
    sessionStorage.setItem('juniper-lane-session', 'session-abc')
    defaultApi({
      '/api/sessions/session-abc': () => ({
        body: { ...SESSION, transcript: [{ role: 'customer', text: 'Earlier question' }, { role: 'assistant', text: 'Earlier answer' }] },
      }),
    })
    render(<App />)

    expect(await screen.findByText('Earlier answer')).toBeInTheDocument()
  })

  it('labels the assistant as an AI', async () => {
    defaultApi()
    await signInAsPriya()

    expect(screen.getByText('AI')).toBeInTheDocument()
    expect(screen.getByText(/Ask for a person at any time/)).toBeInTheDocument()
  })
})

describe('formatting replies', () => {
  it('shows paragraphs, bullet lists, bold text, and ticket numbers', () => {
    const { container } = render(
      <FormattedText text={'First line.\n\n- one\n- **two**\n\nTicket TCK-20261120-ABC123 is open.'} />,
    )

    expect(container.querySelectorAll('p')).toHaveLength(2)
    expect(container.querySelectorAll('li')).toHaveLength(2)
    expect(container.querySelector('strong')).toHaveTextContent('two')
    expect(container.querySelector('.ticket-ref')).toHaveTextContent('TCK-20261120-ABC123')
  })

  it('never runs HTML from a reply', () => {
    const { container } = render(<FormattedText text={'<img src=x onerror="alert(1)"> hello'} />)

    expect(container.querySelector('img')).toBeNull()
    expect(container).toHaveTextContent('<img src=x onerror="alert(1)"> hello')
  })
})
