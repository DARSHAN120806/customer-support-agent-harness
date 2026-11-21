import { useEffect, useState } from 'react'
import { ApiError, dashboardApi, type ConversationSummary, type HarnessEvent } from '../../api'
import { OUTCOME_LABEL, RULE_LABEL, dateTime, money, ms } from '../../format'
import { detailsOf, groupTurns } from '../../turns'
import { BehindTheScenes } from '../BehindTheScenes'
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

  return (
    <section aria-label="Conversations">
      <header className="ad-page-head">
        <h2>Conversations</h2>
        <p className="ad-muted">
          Newest first. Customers appear as codes, and emails, phone numbers and addresses are masked.
        </p>
      </header>

      {error ? (
        <p className="ad-error" role="alert">{error}</p>
      ) : !rows ? (
        <p className="ad-muted">Loading conversations…</p>
      ) : rows.length === 0 ? (
        <p className="ad-empty">No conversations logged yet</p>
      ) : (
        <div className="ad-table-wrap">
          <table className="ad-table">
            <thead>
              <tr>
                <th>Last activity</th>
                <th>Customer</th>
                <th>First message</th>
                <th className="num">Messages</th>
                <th className="num">Checks fired</th>
                <th>Ticket</th>
                <th className="num">Cost</th>
                <th>
                  <span className="visually-hidden">Open</span>
                </th>
              </tr>
            </thead>
            <tbody>
              {rows.map((c) => (
                <tr key={c.conversation_id}>
                  <td className="nowrap ad-muted">{dateTime(c.last_at)}</td>
                  <td className="nowrap ad-mono">
                    {c.customer_ref}
                    {c.harness === false && <span className="ad-flag">harness off</span>}
                  </td>
                  <td className="ad-summary">{c.first_message ?? '—'}</td>
                  <td className="num">{c.turns}</td>
                  <td className="num">{c.blocked_or_rewritten || '—'}</td>
                  <td>{c.escalated ? 'Yes' : 'No'}</td>
                  <td className="num ad-mono">{money(c.cost_usd)}</td>
                  <td className="nowrap">
                    <button type="button" className="ad-link" onClick={() => onOpen(c.conversation_id)}>
                      Replay
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}

// --- The replay ---------------------------------------------------------------------

type ReplayProps = {
  conversationId: string
  onBack: () => void
  // Opens a ticket from this conversation, where staff can answer the customer.
  onOpenTicket?: (ticketId: string) => void
}

export function ConversationReplay({ conversationId, onBack, onOpenTicket }: ReplayProps) {
  const [events, setEvents] = useState<HarnessEvent[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  // Which reply the panel describes; null means "the newest one".
  const [selected, setSelected] = useState<number | null>(null)

  useEffect(() => {
    dashboardApi.conversation(conversationId).then(setEvents).catch((e: ApiError) => setError(e.message))
  }, [conversationId])

  const { start, turns } = groupTurns(events ?? [])
  const shownTurn = turns.find((t) => t.number === selected) ?? turns.at(-1)
  // Tickets created in this conversation, oldest first, each once.
  const ticketIds = [
    ...new Set((events ?? []).filter((e) => e.event === 'ticket_created' && e.ticket_id).map((e) => String(e.ticket_id))),
  ]

  return (
    <section aria-label="Conversation replay">
      <button type="button" className="ad-link ad-back" onClick={onBack}>
        ← All conversations
      </button>
      <header className="ad-page-head">
        <h2>
          Conversation <span className="ad-mono">{conversationId}</span>
        </h2>
        {start && (
          <p className="ad-muted">
            Model {String(start.model)} · date used {String(start.date_used)}
            {start.harness === false ? ' · harness off' : ''}
          </p>
        )}
      </header>
      {error && <p className="ad-error" role="alert">{error}</p>}
      {onOpenTicket && ticketIds.length > 0 && (
        <p className="ad-note">
          This replay is read only. To answer the customer, open the ticket:{' '}
          {ticketIds.map((id, n) => (
            <span key={id}>
              {n > 0 && ', '}
              <button type="button" className="ad-link" onClick={() => onOpenTicket(id)}>
                {id}
              </button>
            </span>
          ))}
        </p>
      )}
      {!events && !error && <p className="ad-muted">Loading…</p>}
      {events && turns.length === 0 && <p className="ad-empty">No messages in this conversation</p>}

      {turns.length > 0 && (
        <div className="ad-replay">
          <div className="ad-transcript">
            {turns.map((turn) => {
              const end = turn.end
              const violations = (end?.violations as string[] | undefined) ?? []
              const current = shownTurn?.number === turn.number
              return (
                <article key={turn.number} className="ad-turn">
                  <div className="ad-bubble customer">
                    <p>{turn.message}</p>
                  </div>
                  <button
                    type="button"
                    className={current ? 'ad-reply current' : 'ad-reply'}
                    aria-pressed={current}
                    aria-label={`Show how reply ${turn.number} was made`}
                    onClick={() => setSelected(turn.number)}
                  >
                    <span className="ad-reply-meta">
                      Reply {turn.number}
                      {end && ` · ${OUTCOME_LABEL[String(end.outcome)] ?? String(end.outcome)}`}
                      {end && ` · ${money(end.cost_usd as number)} · ${ms(end.duration_ms)}`}
                      {violations.length > 0 &&
                        ` · checks fired: ${violations.map((v) => RULE_LABEL[v] ?? v).join(', ')}`}
                    </span>
                    {end ? <FormattedText text={String(end.reply ?? '')} /> : <p className="ad-muted">No reply logged</p>}
                  </button>
                </article>
              )
            })}
          </div>

          {shownTurn && (
            <BehindTheScenes
              details={detailsOf(shownTurn)}
              outcome={shownTurn.end ? String(shownTurn.end.outcome) : undefined}
              replyNumber={shownTurn.number}
            />
          )}
        </div>
      )}
    </section>
  )
}
