// Words and number formats shared by the chat panel and the dashboard.

// The code checks, in plain words.
export const RULE_LABEL: Record<string, string> = {
  ungrounded_figure: 'Figure not found in any source',
  unverified_policy: 'Policy stated without looking it up',
  handover_missing: 'Unanswered question with no ticket',
  upset_customer_not_escalated: 'Upset customer with no ticket',
  promised_ticket_missing: 'Promised a ticket but made none',
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

export function ms(value: unknown): string {
  const n = Number(value)
  if (!Number.isFinite(n)) return ''
  return n >= 1000 ? `${(n / 1000).toFixed(1)} s` : `${n} ms`
}
