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
  // "staff" is a person from the support team; "system" a short note such as
  // "Asha from the support team has joined the chat".
  role: 'customer' | 'assistant' | 'staff' | 'system'
  text: string
  ticket_ids?: string[]
  name?: string
}

// Who from the support team is in the chat, if anyone.
export type Handoff = { name: string } | null

export type Session = {
  role: 'customer'
  session_id: string
  conversation_id: string
  customer: Customer
  orders: OrderSummary[]
  transcript: TranscriptEntry[]
  assistant_name: string
  handoff?: Handoff
}

// A product from the shop's own document (company_overview.md).
export type Product = {
  slug: string
  name: string
  category: string
  price: number | null // null for the gift card, which has amounts to pick from
  price_options: number[]
  warranty: string
  stock_status: 'In stock' | 'Low stock' | 'Out of stock' | string
  units_in_stock: number | null
}

// One of the signed-in customer's support tickets.
export type TicketMessage = { from: 'staff' | 'customer'; text: string; at: string; name?: string }

export type CustomerTicket = {
  ticket_id: string
  created_at: string
  status: string // "open" (waiting), "in_progress" (someone is on it) or "closed"
  topic: string
  summary: string
  order_id: string | null
  source: 'records' | 'chat'
  // Chat tickets only: who from the team is answering, and the messages.
  assigned_name?: string | null
  messages?: TicketMessage[]
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
  // null when a person from the support team is in the chat: the message went to them.
  reply: string | null
  outcome: string
  new_ticket_ids: string[]
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

// A customer gets their chat; the admin and support staff get a key for the
// admin panel, with their name and staff ID.
export type PanelPerson = { role: 'admin' | 'staff'; name: string; staff_id: string }
export type AdminSignIn = PanelPerson & { admin_token: string }
export type SignInResult = Session | AdminSignIn

export type ChatUpdates = { entries: TranscriptEntry[]; next: number; handoff: Handoff }

export const api = {
  signIn: (email: string, password: string) =>
    request<SignInResult>('/sessions', { method: 'POST', body: JSON.stringify({ email, password }) }),
  getSession: (sessionId: string) => request<Session>(`/sessions/${encodeURIComponent(sessionId)}`),
  products: () => request<Product[]>('/products'),
  myTickets: (sessionId: string) =>
    request<CustomerTicket[]>(`/sessions/${encodeURIComponent(sessionId)}/tickets`),
  signOut: (sessionId: string) =>
    request<void>(`/sessions/${encodeURIComponent(sessionId)}`, { method: 'DELETE' }),
  sendMessage: (sessionId: string, text: string) =>
    request<Reply>(`/sessions/${encodeURIComponent(sessionId)}/messages`, {
      method: 'POST',
      body: JSON.stringify({ text }),
    }),
  updates: (sessionId: string, after: number) =>
    request<ChatUpdates>(`/sessions/${encodeURIComponent(sessionId)}/updates?after=${after}`),
  replyToTicket: (sessionId: string, ticketId: string, text: string) =>
    request<CustomerTicket>(
      `/sessions/${encodeURIComponent(sessionId)}/tickets/${encodeURIComponent(ticketId)}/messages`,
      { method: 'POST', body: JSON.stringify({ text }) },
    ),
}

// The longest message the API accepts.
export const MAX_MESSAGE_LENGTH = 2000

// --- Support dashboard ---------------------------------------------------------

export type Ticket = {
  ticket_id: string
  created_at: string
  status: string // "open" (waiting), "in_progress" or "closed"
  conversation_id: string | null
  customer_email: string // always masked by the API
  reason: string
  order_id: string | null
  summary: string
  assigned_to?: { name: string; staff_id: string } | null
  assigned_at?: string
  closed_at?: string
  messages?: (TicketMessage & { staff_id?: string })[]
  // Whether the customer still has this chat open, so replies reach them live.
  live?: boolean
}

export type TicketDetail = {
  ticket: Ticket
  // The customer's chat with the assistant before the hand-over.
  chat: { role: 'customer' | 'assistant'; text: string }[]
}

export type TeamRow = {
  name: string
  staff_id: string
  taken: number
  closed: number
  answering_now: number
  messages: number
  average_minutes_to_close: number | null
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

// The admin's key is kept for this browser tab only, like the customer's chat.
export const ADMIN_TOKEN_KEY = 'juniper-lane-admin'

function asAdmin<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = sessionStorage.getItem(ADMIN_TOKEN_KEY) ?? ''
  return request<T>(path, { ...options, headers: { Authorization: `Bearer ${token}` } })
}

// Numbers for the admin overview (see web/stats.py).
export type Stats = {
  conversations: number
  customers: number
  messages: number
  tickets: number
  open_tickets: number
  tickets_by_harness: number
  handover_rate: number
  cost_usd: number
  cost_per_message_usd: number
  average_reply_ms: number
  outcomes: Record<string, number>
  checks: Record<string, number>
  tickets_by_reason: Record<string, number>
  days: { date: string; messages: number; tickets: number }[]
  tickets_in_progress?: number
  team?: TeamRow[]
}

// The model settings, as the admin panel sees them. Keys never come back:
// only a hint such as "…abcd" when one is saved.
export type ChatModel = {
  provider: 'bedrock' | 'anthropic' | 'openai_compatible'
  model: string
  base_url: string | null
  aws_region: string | null
  input_price: number
  output_price: number
  key_hint: string | null
}

export type SearchModel = {
  provider: 'titan' | 'openai_compatible'
  model: string
  base_url: string | null
  key_hint: string | null
}

export type ModelView = {
  chat: ChatModel
  search: SearchModel
  source: 'admin panel' | '.env'
  saved_at: string | null
  providers: { chat: Record<string, string>; search: Record<string, string> }
}

// What the form sends. An empty key keeps the key saved before.
export type ModelForm = {
  chat: Omit<ChatModel, 'key_hint'> & { api_key: string }
  search: Omit<SearchModel, 'key_hint'> & { api_key: string }
}

export type ConnectionCheck = {
  ok: boolean
  ms: number
  error?: string
  reply?: string
  tools_ok?: boolean
  dimensions?: number
}

export type ConnectionResult = { chat: ConnectionCheck; search: ConnectionCheck }

// A shop document, as the admin panel edits it.
export type DocumentSummary = { name: string; title: string; sections: number; chars: number; updated_at: string }

export type DocumentDetail = Omit<DocumentSummary, 'sections'> & {
  text: string
  // A fingerprint of the text, sent back on save to notice someone else's save.
  version: string
  sections: { heading: string; chars: number }[]
  protected: string[]
  history: { id: string; saved_at: string; chars: number }[]
}

export type DocumentSaved = { document: DocumentDetail; warnings: string[] }

export type OrderRow = OrderSummary & { customer_name: string; records: number }

export type OrderDetail = {
  order: Record<string, unknown> & { order_id: string; items: { name: string; quantity: number; unit_price: number }[] }
  customer: { name: string; email: string; city?: string }
}

const docPath = (name: string) => `/admin/documents/${encodeURIComponent(name)}`

const ticketPath = (id: string) => `/tickets/${encodeURIComponent(id)}`

export const dashboardApi = {
  me: () => asAdmin<PanelPerson>('/admin/me'),
  ticket: (id: string) => asAdmin<TicketDetail>(ticketPath(id)),
  takeTicket: (id: string) => asAdmin<TicketDetail>(`${ticketPath(id)}/take`, { method: 'POST' }),
  replyToTicket: (id: string, text: string) =>
    asAdmin<TicketDetail>(`${ticketPath(id)}/messages`, { method: 'POST', body: JSON.stringify({ text }) }),
  endTicket: (id: string) => asAdmin<TicketDetail>(`${ticketPath(id)}/end`, { method: 'POST' }),
  stats: () => asAdmin<Stats>('/stats'),
  documents: () => asAdmin<DocumentSummary[]>('/admin/documents'),
  document: (name: string) => asAdmin<DocumentDetail>(docPath(name)),
  saveDocument: (name: string, text: string, version: string) =>
    asAdmin<DocumentSaved>(docPath(name), { method: 'PUT', body: JSON.stringify({ text, version }) }),
  documentVersion: (name: string, id: string) =>
    asAdmin<{ text: string }>(`${docPath(name)}/history/${encodeURIComponent(id)}`),
  restoreDocument: (name: string, versionId: string, version: string) =>
    asAdmin<DocumentSaved>(`${docPath(name)}/restore`, {
      method: 'POST',
      body: JSON.stringify({ version_id: versionId, version }),
    }),
  orders: (q: string) => asAdmin<{ total: number; orders: OrderRow[] }>(`/admin/orders?q=${encodeURIComponent(q)}`),
  order: (id: string) => asAdmin<OrderDetail>(`/admin/orders/${encodeURIComponent(id)}`),
  model: () => asAdmin<ModelView>('/admin/model'),
  testModel: (form: ModelForm) =>
    asAdmin<ConnectionResult>('/admin/model/test', { method: 'POST', body: JSON.stringify(form) }),
  saveModel: (form: ModelForm) =>
    asAdmin<ModelView>('/admin/model', { method: 'PUT', body: JSON.stringify(form) }),
  resetModel: () => asAdmin<ModelView>('/admin/model', { method: 'DELETE' }),
  tickets: () => asAdmin<Ticket[]>('/tickets'),
  conversations: () => asAdmin<ConversationSummary[]>('/conversations?limit=200'),
  conversation: (id: string) => asAdmin<HarnessEvent[]>(`/conversations/${encodeURIComponent(id)}`),
  evaluations: () => asAdmin<EvaluationRun[]>('/evaluations'),
  signOut: () => asAdmin<void>('/admin/session', { method: 'DELETE' }),
}
