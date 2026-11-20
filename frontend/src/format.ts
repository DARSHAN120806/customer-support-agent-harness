// Words and number formats shared by the chat panel and the dashboard.

// The code checks, in plain words.
export const RULE_LABEL: Record<string, string> = {
  ungrounded_figure: 'Figure not found in any source',
  unverified_policy: 'Policy stated without looking it up',
  handover_missing: 'Unanswered question with no ticket',
  upset_customer_not_escalated: 'Upset customer with no ticket',
  promised_ticket_missing: 'Promised a ticket but made none',
  human_request_not_escalated: 'Asked for a person, no ticket',
  identity_leak: 'Named the AI behind the assistant',
  human_claim: 'Claimed to be a person',
  personal_data: "Another person's email address",
  refund_claim: 'Claimed to give a refund',
}

export const OUTCOME_LABEL: Record<string, string> = {
  completed: 'Answered',
  reply_blocked: 'Reply replaced by a safe one',
  step_limit: 'Stopped: step limit',
  budget_limit: 'Stopped: token or cost limit',
  model_stopped: 'Stopped: model gave no usable reply',
  model_error: 'Stopped: model unreachable',
  error: 'Stopped: unexpected error',
}

export function money(value: number | null | undefined): string {
  if (value == null) return '—'
  return value < 0.01 ? `$${value.toFixed(4)}` : `$${value.toFixed(3)}`
}

// Ticket reasons in plain words.
export const REASON_LABEL: Record<string, string> = {
  refund_request: 'Refund request',
  return_request: 'Return request',
  warranty_claim: 'Warranty claim',
  order_problem: 'Problem with an order',
  upset_customer: 'Upset customer',
  unsure_of_answer: 'Assistant unsure',
  outside_shop_documents: 'Not in the shop documents',
  human_requested: 'Asked for a person',
  other: 'Other',
}

const DATE_TIME = new Intl.DateTimeFormat('en-GB', {
  day: 'numeric',
  month: 'short',
  hour: '2-digit',
  minute: '2-digit',
})
const DAY = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short' })

// "2026-11-20T15:57:48+00:00" becomes "20 Nov, 15:57" in the viewer's time.
export function dateTime(value: string): string {
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? value : DATE_TIME.format(date)
}

// "2026-11-20" becomes "20 Nov".
export function day(value: string): string {
  const date = new Date(`${value}T12:00:00`)
  return Number.isNaN(date.getTime()) ? value : DAY.format(date)
}

export function percent(share: number): string {
  return `${Math.round(share * 100)}%`
}

export function ms(value: unknown): string {
  const n = Number(value)
  if (!Number.isFinite(n)) return ''
  return n >= 1000 ? `${(n / 1000).toFixed(1)} s` : `${n} ms`
}
