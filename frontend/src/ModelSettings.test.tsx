// Tests for the admin panel's Model page. The API is a fake, so nothing is paid.
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import App from './App'
import type { ConnectionResult, ModelView } from './api'

const PROVIDERS = {
  chat: { bedrock: 'Amazon Bedrock', anthropic: 'Anthropic API', openai_compatible: 'OpenAI-compatible' },
  search: { titan: 'Amazon Titan', openai_compatible: 'OpenAI-compatible' },
}

const FROM_ENV: ModelView = {
  chat: {
    provider: 'bedrock',
    model: 'global.anthropic.claude-haiku-4-5-20251001-v1:0',
    base_url: null,
    aws_region: 'ap-southeast-2',
    input_price: 1,
    output_price: 5,
    key_hint: null,
  },
  search: { provider: 'titan', model: 'amazon.titan-embed-text-v2:0', base_url: null, key_hint: null },
  source: '.env',
  saved_at: null,
  providers: PROVIDERS,
}

const SAVED_LOCAL: ModelView = {
  ...FROM_ENV,
  chat: { provider: 'openai_compatible', model: 'llama3.1', base_url: 'http://localhost:11434/v1', aws_region: 'ap-southeast-2', input_price: 0, output_price: 0, key_hint: null },
  source: 'admin panel',
  saved_at: '2026-11-21T10:00:00+00:00',
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

async function openModelPage(routes: Record<string, (body: unknown) => Route>) {
  const calls = fakeApi({
    'GET /api/stats': () => ({
      body: {
        conversations: 0, customers: 0, messages: 0, tickets: 0, open_tickets: 0, tickets_by_harness: 0,
        handover_rate: 0, cost_usd: 0, cost_per_message_usd: 0, average_reply_ms: 0,
        outcomes: {}, checks: {}, tickets_by_reason: {}, days: [],
      },
    }),
    'GET /api/tickets': () => ({ body: [] }),
    'GET /api/admin/model': () => ({ body: FROM_ENV }),
    ...routes,
  })
  sessionStorage.setItem('juniper-lane-admin', 'admin-token-1')
  window.location.hash = '#/dashboard'
  const user = userEvent.setup()
  render(<App />)
  await user.click(await screen.findByRole('button', { name: 'Model' }))
  await screen.findByRole('heading', { name: 'Model' })
  return { user, calls }
}

describe('the model page', () => {
  it('shows the model in use and where it comes from', async () => {
    await openModelPage({})

    expect(screen.getByText(/In use:/)).toHaveTextContent('Amazon Bedrock · global.anthropic.claude-haiku-4-5-20251001-v1:0')
    expect(screen.getByText(/In use:/)).toHaveTextContent('from the .env file')
    expect(screen.getByLabelText(/AWS region/)).toHaveValue('ap-southeast-2')
    expect(screen.queryByRole('button', { name: 'Go back to the .env settings' })).not.toBeInTheDocument()
  })

  it('asks for an address and a key for an OpenAI-compatible model, and fills the address for Ollama', async () => {
    const { user } = await openModelPage({})
    const chat = screen.getByRole('group', { name: 'Chat model' })

    await user.click(within(chat).getByRole('radio', { name: 'OpenAI-compatible' }))
    expect(within(chat).queryByLabelText(/AWS region/)).not.toBeInTheDocument()
    expect(within(chat).getByLabelText(/^Key/)).toHaveAttribute('type', 'password')

    await user.click(within(chat).getByRole('button', { name: 'Ollama' }))
    expect(within(chat).getByLabelText(/Web address/)).toHaveValue('http://localhost:11434/v1')
    expect(within(chat).getByLabelText(/Price in/)).toHaveValue(0) // a local model costs nothing
  })

  it('starts the model name empty when the service changes, and brings it back when switching back', async () => {
    const { user } = await openModelPage({})
    const chat = screen.getByRole('group', { name: 'Chat model' })

    await user.click(within(chat).getByRole('radio', { name: 'OpenAI-compatible' }))
    expect(within(chat).getByLabelText(/Model name/)).toHaveValue('')

    await user.click(within(chat).getByRole('radio', { name: 'Amazon Bedrock' }))
    expect(within(chat).getByLabelText(/Model name/)).toHaveValue(FROM_ENV.chat.model)
  })

  it('never shows a saved key, only its last characters', async () => {
    const withKey: ModelView = { ...SAVED_LOCAL, chat: { ...SAVED_LOCAL.chat, key_hint: '…abcd' } }
    await openModelPage({ 'GET /api/admin/model': () => ({ body: withKey }) })
    const chat = screen.getByRole('group', { name: 'Chat model' })

    expect(within(chat).getByLabelText(/^Key/)).toHaveValue('')
    expect(within(chat).getByText(/A key ending abcd is saved/)).toBeInTheDocument()
  })

  it('tests the connection and explains a model that cannot use tools', async () => {
    const result: ConnectionResult = {
      chat: { ok: true, ms: 1200, reply: 'OK', tools_ok: false },
      search: { ok: false, ms: 30, error: 'Could not reach the embedding service.' },
    }
    const { user, calls } = await openModelPage({ 'POST /api/admin/model/test': () => ({ body: result }) })

    await user.click(screen.getByRole('button', { name: 'Test connection' }))

    const box = await screen.findByRole('status', { name: 'Connection test' })
    expect(within(box).getByText(/Replied in 1.2 s/)).toBeInTheDocument()
    expect(within(box).getByText(/It did not ask for a tool/)).toBeInTheDocument()
    expect(within(box).getByText('Could not reach the embedding service.')).toBeInTheDocument()
    expect(calls.find((c) => c.method === 'POST')?.body).toMatchObject({ chat: { provider: 'bedrock', api_key: '' } })
  })

  it('saves the choice, says what changes, and can go back to .env', async () => {
    const { user, calls } = await openModelPage({
      'PUT /api/admin/model': () => ({ body: SAVED_LOCAL }),
      'DELETE /api/admin/model': () => ({ body: FROM_ENV }),
    })
    const chat = screen.getByRole('group', { name: 'Chat model' })
    await user.click(within(chat).getByRole('radio', { name: 'OpenAI-compatible' }))
    await user.click(within(chat).getByRole('button', { name: 'Ollama' }))
    const model = within(chat).getByLabelText(/Model name/)
    await user.clear(model)
    await user.type(model, 'llama3.1')

    await user.click(screen.getByRole('button', { name: 'Save and use for new chats' }))

    expect(await screen.findByText(/New chats now use llama3.1/)).toBeInTheDocument()
    expect(calls.find((c) => c.method === 'PUT')?.body).toMatchObject({
      chat: { provider: 'openai_compatible', model: 'llama3.1', base_url: 'http://localhost:11434/v1', input_price: 0 },
    })
    expect(screen.getByText(/In use:/)).toHaveTextContent('saved here')

    await user.click(screen.getByRole('button', { name: 'Go back to the .env settings' }))
    expect(await screen.findByText(/Back to the settings in .env/)).toBeInTheDocument()
  })

  it('shows why a save was refused', async () => {
    const { user } = await openModelPage({
      'PUT /api/admin/model': () => ({ status: 400, body: { detail: 'Nothing was changed: Amazon Bedrock needs an AWS region.' } }),
    })

    await user.click(screen.getByRole('button', { name: 'Save and use for new chats' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Nothing was changed')
  })

  it('offers the search model choice with its own address', async () => {
    const { user } = await openModelPage({})

    const search = screen.getByRole('group', { name: 'Search model' })
    await user.click(within(search).getByRole('radio', { name: 'OpenAI-compatible' }))
    await user.click(within(search).getByRole('button', { name: 'Ollama' }))

    expect(within(search).getByLabelText(/Web address/)).toHaveValue('http://localhost:11434/v1')
  })
})
