import { useEffect, useState } from 'react'
import { ApiError, dashboardApi, type ConversationSummary, type HarnessEvent } from '../../api'
import { OUTCOME_LABEL, RULE_LABEL, money, ms } from '../../format'
import { groupTurns } from '../../turns'
import { Step } from '../BehindTheScenes'
import { FormattedText } from '../FormattedText'

// --- The list ---------------------------------------------------------------------

type ListProps = {
  onOpen: (conversationId: string) => void
}

export function ConversationList({ onOpen }: ListProps) {
  const [rows, setRows] = useState<ConversationSummary[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    dashboardApi.conversations().then(setRows).catch((e: ApiError) => setError(e.message))
  }, [])

  if (error) return <p className="error" role="alert">{error}</p>
  if (!rows) return <p className="muted">Loading conversations…</p>
  if (rows.length === 0) return <p className="empty">No conversations logged yet.</p>

  return (
    <section aria-label="Conversations" className="dash-section">
      <p className="muted small">
        Newest first. Customers appear as codes, and emails, phone numbers, and addresses are masked.
      </p>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Last activity</th>
              <th>Customer</th>
              <th>First message</th>
              <th>Messages</th>
              <th>Checks fired</th>
              <th>Ticket</th>
              <th>Cost</th>
              <th aria-label="Open" />
            </tr>
          </thead>
          <tbody>
            {rows.map((c) => (
              <tr key={c.conversation_id}>
                <td className="nowrap">{c.last_at.replace('T', ' ').slice(0, 16)}</td>
                <td className="nowrap">
                  <code>{c.customer_ref}</code>
                  {c.harness === false && <span className="tag tag-warn">harness off</span>}
                </td>
                <td className="summary-cell">{c.first_message ?? '—'}</td>
                <td>{c.turns}</td>
                <td>{c.blocked_or_rewritten || '—'}</td>
                <td>{c.escalated ? 'Yes' : 'No'}</td>
                <td className="nowrap">{money(c.cost_usd)}</td>
                <td>
                  <button className="link-button" onClick={() => onOpen(c.conversation_id)}>
                    Replay
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

// --- The replay ---------------------------------------------------------------------

type ReplayProps = {
  conversationId: string
  onBack: () => void
}

export function ConversationReplay({ conversationId, onBack }: ReplayProps) {
  const [events, setEvents] = useState<HarnessEvent[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    dashboardApi.conversation(conversationId).then(setEvents).catch((e: ApiError) => setError(e.message))
  }, [conversationId])

  const { start, turns } = groupTurns(events ?? [])

  return (
    <section aria-label="Conversation replay" className="dash-section">
      <button className="secondary small-button back-button" onClick={onBack}>
        ← All conversations
      </button>
      <h2 className="replay-title">
        Conversation <code>{conversationId}</code>
      </h2>
      {start && (
        <p className="muted small">
          Model {String(start.model)} · date used {String(start.date_used)}
          {start.harness === false ? ' · harness OFF' : ''}
        </p>
      )}
      {error && <p className="error" role="alert">{error}</p>}
      {!events && !error && <p className="muted">Loading…</p>}

      {turns.map((turn) => {
        const end = turn.end
        const violations = (end?.violations as string[] | undefined) ?? []
        return (
          <article key={turn.number} className="replay-turn">
            <div className="bubble-row customer">
              <div className="bubble customer">
                <p>{turn.message}</p>
              </div>
            </div>

            <details className="replay-steps">
              <summary>
                {turn.steps.length} steps
                {end && ` · ${OUTCOME_LABEL[String(end.outcome)] ?? String(end.outcome)}`}
                {end && ` · ${money(end.cost_usd as number)} · ${ms(end.duration_ms)}`}
                {violations.length > 0 && ` · checks fired: ${violations.map((v) => RULE_LABEL[v] ?? v).join(', ')}`}
              </summary>
              <ol className="timeline">
                {turn.steps.map((event, i) => (
                  <Step key={i} event={event} />
                ))}
              </ol>
            </details>

            {end && (
              <div className="bubble-row assistant">
                <div className="bubble assistant">
                  <FormattedText text={String(end.reply ?? '')} />
                </div>
              </div>
            )}
          </article>
        )
      })}
    </section>
  )
}
