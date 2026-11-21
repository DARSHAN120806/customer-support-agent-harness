import { useEffect, useRef, useState, type FormEvent } from 'react'
import { ApiError, dashboardApi, MAX_MESSAGE_LENGTH, type PanelPerson, type TicketDetail } from '../../api'
import { REASON_LABEL, dateTime, statusLabel } from '../../format'
import { FormattedText } from '../FormattedText'
import { Tag } from '../shop/Tag'

// How often the open ticket checks for new customer messages.
const REFRESH_MS = 3000

type Props = {
  ticketId: string
  person: PanelPerson
  onBack: () => void
  onOpenConversation: (conversationId: string) => void
}

// One ticket: the customer's chat with the assistant, then the chat with the
// support team. The person who takes the ticket answers it and ends the chat.
export function TicketView({ ticketId, person, onBack, onOpenConversation }: Props) {
  const [detail, setDetail] = useState<TicketDetail | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [draft, setDraft] = useState('')
  const [busy, setBusy] = useState(false)
  const threadRef = useRef<HTMLDivElement>(null)

  // Load the ticket, then check for new messages every few seconds.
  useEffect(() => {
    let stopped = false
    const load = () =>
      dashboardApi
        .ticket(ticketId)
        .then((d) => !stopped && setDetail(d))
        .catch((e: ApiError) => !stopped && setError(e.message))
    load()
    const timer = setInterval(load, REFRESH_MS)
    return () => {
      stopped = true
      clearInterval(timer)
    }
  }, [ticketId])

  const messageCount = detail?.ticket.messages?.length ?? 0
  useEffect(() => {
    const thread = threadRef.current
    thread?.scrollTo?.({ top: thread.scrollHeight, behavior: 'smooth' })
  }, [messageCount])

  async function act(work: Promise<TicketDetail>, clear = false) {
    setBusy(true)
    setError(null)
    try {
      setDetail(await work)
      if (clear) setDraft('')
    } catch (e) {
      setError((e as ApiError).message)
    } finally {
      setBusy(false)
    }
  }

  function send(event: FormEvent) {
    event.preventDefault()
    if (draft.trim()) act(dashboardApi.replyToTicket(ticketId, draft.trim()), true)
  }

  if (!detail) {
    return (
      <section aria-label="Ticket">
        <button type="button" className="ad-link ad-back" onClick={onBack}>
          ← All tickets
        </button>
        {error ? <p className="ad-error" role="alert">{error}</p> : <p className="ad-muted">Loading…</p>}
      </section>
    )
  }

  const { ticket, chat } = detail
  const mine = ticket.status === 'in_progress' && ticket.assigned_to?.name === person.name && ticket.assigned_to?.staff_id === person.staff_id
  const messages = ticket.messages ?? []

  return (
    <section aria-label={`Ticket ${ticket.ticket_id}`}>
      <button type="button" className="ad-link ad-back" onClick={onBack}>
        ← All tickets
      </button>
      <header className="ad-page-head">
        <h2>
          Ticket <span className="ad-mono">{ticket.ticket_id}</span>
        </h2>
        <p className="ad-muted">
          {REASON_LABEL[ticket.reason] ?? ticket.reason} · {statusLabel(ticket)}
        </p>
      </header>

      {error && <p className="ad-error" role="alert">{error}</p>}

      <div className="ad-ticket">
        <div className="ad-ticket-main">
          <section className="ad-card" aria-label="Chat with the assistant">
            <div className="ad-card-head">
              <h3>Chat with the assistant</h3>
              {ticket.conversation_id && (
                <button type="button" className="ad-link" onClick={() => onOpenConversation(ticket.conversation_id!)}>
                  Replay with details
                </button>
              )}
            </div>
            {chat.length === 0 ? (
              <p className="ad-empty">No earlier chat was logged for this ticket</p>
            ) : (
              <div className="ad-thread compact">
                {chat.map((line, i) => (
                  <div key={i} className={`ad-line ${line.role}`}>
                    <span className="ad-line-who">{line.role === 'customer' ? 'Customer' : 'Assistant'}</span>
                    <div className="ad-line-text">
                      <FormattedText text={line.text} />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>

          <section className="ad-card" aria-label="Chat with the team">
            <h3>Chat with the team</h3>
            <div className="ad-thread" ref={threadRef} role="log" aria-live="polite">
              {messages.length === 0 ? (
                <p className="ad-empty">
                  {ticket.status === 'open' ? 'Take the ticket to start answering the customer' : 'No messages yet'}
                </p>
              ) : (
                messages.map((m, i) => (
                  <div key={i} className={`ad-line ${m.from}`}>
                    <span className="ad-line-who">
                      {m.from === 'customer' ? 'Customer' : `${m.name}${m.staff_id ? ` · ${m.staff_id}` : ''}`}
                      <span className="ad-muted"> · {dateTime(m.at)}</span>
                    </span>
                    <div className="ad-line-text">
                      <p>{m.text}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
            {mine && (
              <form className="ad-reply-form" onSubmit={send}>
                <label htmlFor="ticket-reply" className="visually-hidden">
                  Your reply
                </label>
                <textarea
                  id="ticket-reply"
                  rows={3}
                  maxLength={MAX_MESSAGE_LENGTH}
                  value={draft}
                  onChange={(e) => setDraft(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) send(e)
                  }}
                  placeholder="Write to the customer"
                />
                <button type="submit" className="ad-button primary" disabled={busy || !draft.trim()}>
                  Send
                </button>
              </form>
            )}
          </section>
        </div>

        <aside className="ad-ticket-side" aria-label="About this ticket">
          <section className="ad-card">
            <h3>About this ticket</h3>
            <dl className="ad-facts one">
              <div>
                <dt>Created</dt>
                <dd>{dateTime(ticket.created_at)}</dd>
              </div>
              {ticket.order_id && (
                <div>
                  <dt>Order</dt>
                  <dd>
                    <Tag>{ticket.order_id}</Tag>
                  </dd>
                </div>
              )}
              <div>
                <dt>Summary from the assistant</dt>
                <dd>{ticket.summary}</dd>
              </div>
              <div>
                <dt>Customer</dt>
                <dd>
                  {ticket.status === 'closed'
                    ? 'The chat has ended'
                    : ticket.live
                      ? 'In the chat now: your replies appear straight away'
                      : 'Not in the chat: they will see your replies under Your tickets when they next sign in'}
                </dd>
              </div>
            </dl>
          </section>

          <section className="ad-card" aria-label="Answering">
            <h3>Answering</h3>
            {ticket.status === 'open' && (
              <>
                <p className="ad-muted ad-help">Nobody has taken this ticket yet</p>
                <button type="button" className="ad-button primary" disabled={busy} onClick={() => act(dashboardApi.takeTicket(ticketId))}>
                  Take ticket
                </button>
              </>
            )}
            {ticket.status === 'in_progress' && mine && (
              <>
                <p className="ad-help">
                  Answering as <strong>{person.name}</strong>
                  {person.staff_id && <span className="ad-mono"> · {person.staff_id}</span>}
                </p>
                <button type="button" className="ad-button" disabled={busy} onClick={() => act(dashboardApi.endTicket(ticketId))}>
                  End chat
                </button>
                <p className="ad-muted ad-help">Ending closes the ticket; the assistant then answers the customer again</p>
              </>
            )}
            {ticket.status === 'in_progress' && !mine && (
              <p className="ad-help">
                {ticket.assigned_to?.name} <span className="ad-mono">· {ticket.assigned_to?.staff_id}</span> is answering this ticket
              </p>
            )}
            {ticket.status === 'closed' && (
              <p className="ad-help">
                Closed by {ticket.assigned_to?.name ?? 'the team'}
                {ticket.closed_at && <span className="ad-muted"> · {dateTime(ticket.closed_at)}</span>}
              </p>
            )}
          </section>
        </aside>
      </div>
    </section>
  )
}
