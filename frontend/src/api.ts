// Talking to the Python web API. Every request goes to "/api/...", which the
// development server passes on to the API (see vite.config.ts).

export type Customer = {
  name: string
  email: string
  order_count: number
}

export type OrderSummary = {
  order_id: string
  placed_on: string
  status: string
  total: number
  items: string[]
}

export type TranscriptEntry = {
  role: 'customer' | 'assistant'
  text: string
  ticket_ids?: string[]
}

export type Session = {
  session_id: string
  conversation_id: string
  customer: Customer
  orders: OrderSummary[]
  transcript: TranscriptEntry[]
  assistant_name: string
}

// One step the harness took while answering, as written to the event log.
export type HarnessEvent = {
  event: string
  [field: string]: unknown
}

export type ReplyDetails = {
  turn: number
  steps: number
  tools_used: string[]
  escalated: boolean
  violations: string[]
  gave_up_because: string | null
  input_tokens: number
  output_tokens: number
  cost_usd: number | null
  duration_ms: number
  events: HarnessEvent[]
}

export type Reply = {
  reply: string
  outcome: string
  new_ticket_ids: string[]
  details: ReplyDetails | null
}

// An error the page can show to the person using it.
export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  let response: Response
  try {
    response = await fetch(`/api${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...options.headers },
    })
  } catch {
    throw new ApiError(0, 'The support service could not be reached. Is the API server running?')
  }
  if (!response.ok) {
    let message = `Something went wrong (error ${response.status}).`
    try {
      const body = await response.json()
      // FastAPI puts the reason in "detail": a sentence, or a list for bad input.
      if (typeof body.detail === 'string') message = body.detail
      else if (response.status === 422) message = 'That message could not be sent. Please check it and try again.'
    } catch {
      // keep the general message
    }
    throw new ApiError(response.status, message)
  }
  return response.status === 204 ? (undefined as T) : ((await response.json()) as T)
}

export const api = {
  findCustomers: (query: string) =>
    request<Customer[]>(`/customers?q=${encodeURIComponent(query)}&limit=8`),
  signIn: (email: string) =>
    request<Session>('/sessions', { method: 'POST', body: JSON.stringify({ email }) }),
  getSession: (sessionId: string) => request<Session>(`/sessions/${encodeURIComponent(sessionId)}`),
  signOut: (sessionId: string) =>
    request<void>(`/sessions/${encodeURIComponent(sessionId)}`, { method: 'DELETE' }),
  sendMessage: (sessionId: string, text: string) =>
    request<Reply>(`/sessions/${encodeURIComponent(sessionId)}/messages`, {
      method: 'POST',
      body: JSON.stringify({ text }),
    }),
}

// The longest message the API accepts.
export const MAX_MESSAGE_LENGTH = 2000

// --- Support dashboard ---------------------------------------------------------

export type Ticket = {
  ticket_id: string
  created_at: string
  status: string
  conversation_id: string | null
  customer_email: string // always masked by the API
  reason: string
  order_id: string | null
  summary: string
}

export type ConversationSummary = {
  conversation_id: string
  started_at: string
  last_at: string
  customer_ref: string
  model?: string
  harness?: boolean
  turns: number
  cost_usd: number
  escalated: boolean
  blocked_or_rewritten: number
  first_message?: string
}

export type CategoryResult = { passed: number; total: number; violations?: Record<string, number> }

export type EvaluationSummary = {
  passed: number
  total: number
  pass_rate?: number
  by_category: Record<string, CategoryResult>
  violations?: Record<string, number>
  violation_total?: number
  cost_usd?: number
  duration_s?: number
}

export type EvaluationRun = {
  name: string
  run_at: string | null
  model: string | null
  harness: string
  summary: EvaluationSummary
}

export const dashboardApi = {
  tickets: () => request<Ticket[]>('/tickets'),
  conversations: () => request<ConversationSummary[]>('/conversations?limit=200'),
  conversation: (id: string) => request<HarnessEvent[]>(`/conversations/${encodeURIComponent(id)}`),
  evaluations: () => request<EvaluationRun[]>('/evaluations'),
}
