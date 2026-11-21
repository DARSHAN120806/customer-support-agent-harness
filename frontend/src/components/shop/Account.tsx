// "Your orders" and "Your tickets" on the shop page: the signed-in customer's
// own orders, and their support tickets from the shop's records and from chat.
import { useState, type FormEvent } from 'react'
import type { CustomerTicket, OrderSummary } from '../../api'
import { dollars } from './cart'
import { sentence, shortDate } from './dates'
import { Tag } from './Tag'

type OrdersProps = {
  orders: OrderSummary[]
  // Opens the chat with a question about this order.
  onAsk: (orderId: string) => void
}

export function YourOrders({ orders, onAsk }: OrdersProps) {
  const newestFirst = [...orders].sort((a, b) => b.placed_on.localeCompare(a.placed_on))
  return (
    <section className="account-block" id="orders" aria-labelledby="orders-title">
      <h2 id="orders-title">Your orders</h2>
      {newestFirst.length === 0 ? (
        <p className="empty">No orders yet</p>
      ) : (
        <ul className="rows">
          {newestFirst.map((order) => (
            <li key={order.order_id} className="row order-row">
              <Tag>{order.order_id}</Tag>
              <div className="row-main">
                <p className="row-title">{order.items.join(', ')}</p>
                <p className="row-meta">
                  Placed {shortDate(order.placed_on)} · {sentence(order.status)}
                </p>
                <button type="button" className="row-link" onClick={() => onAsk(order.order_id)}>
                  Ask about this order
                </button>
              </div>
              <span className="row-figure">{dollars(order.total)}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}

type TicketsProps = {
  tickets: CustomerTicket[] | null // null while loading
  error: string | null
  // Sends the customer's reply on a ticket and returns the updated ticket.
  onReply: (ticketId: string, text: string) => Promise<void>
}

// A ticket's state in the customer's words.
function ticketStatus(ticket: CustomerTicket): string {
  if (ticket.status === 'in_progress') return `With ${ticket.assigned_name ?? 'our team'}`
  if (ticket.status === 'open' && ticket.source === 'chat') return 'Waiting for the team'
  return sentence(ticket.status)
}

export function YourTickets({ tickets, error, onReply }: TicketsProps) {
  return (
    <section className="account-block" id="tickets" aria-labelledby="tickets-title">
      <h2 id="tickets-title">Your tickets</h2>
      {error ? (
        <p className="empty" role="alert">{error}</p>
      ) : tickets == null ? (
        <p className="empty">Loading…</p>
      ) : tickets.length === 0 ? (
        <p className="empty">No support tickets yet</p>
      ) : (
        <ul className="rows">
          {tickets.map((ticket) => (
            <li key={ticket.ticket_id} className="row ticket-row">
              <Tag>{ticket.ticket_id}</Tag>
              <div className="row-main">
                <p className="row-title">{ticket.topic}</p>
                <p className="row-meta">
                  {shortDate(ticket.created_at)}
                  {ticket.order_id ? ` · ${ticket.order_id}` : ''}
                </p>
                {ticket.summary && <p className="row-summary">{ticket.summary}</p>}
                {ticket.source === 'chat' && <TicketThread ticket={ticket} onReply={onReply} />}
              </div>
              <span className={ticket.status === 'closed' ? 'ticket-status' : 'ticket-status open'}>{ticketStatus(ticket)}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}

type ThreadProps = { ticket: CustomerTicket; onReply: TicketsProps['onReply'] }

// The messages between the customer and the team on one ticket, and a box to
// answer while the ticket is open. Hidden until the customer opens it.
function TicketThread({ ticket, onReply }: ThreadProps) {
  const messages = ticket.messages ?? []
  const fromTeam = messages.filter((m) => m.from === 'staff').length
  const [open, setOpen] = useState(false)
  const [draft, setDraft] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const canReply = ticket.status !== 'closed'

  if (messages.length === 0 && !canReply) return null

  async function send(event: FormEvent) {
    event.preventDefault()
    if (!draft.trim()) return
    setBusy(true)
    setError(null)
    try {
      await onReply(ticket.ticket_id, draft.trim())
      setDraft('')
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="thread">
      <button type="button" className="row-link" aria-expanded={open} onClick={() => setOpen(!open)}>
        {open ? 'Hide messages' : messages.length ? `Messages (${messages.length})` : 'Add a message'}
        {!open && fromTeam > 0 && <span className="thread-new"> · {fromTeam} from the team</span>}
      </button>
      {open && (
        <>
          {messages.length > 0 && (
            <ul className="thread-messages" aria-label={`Messages on ${ticket.ticket_id}`}>
              {messages.map((m, i) => (
                <li key={i} className={`thread-message ${m.from}`}>
                  <span className="thread-who">{m.from === 'staff' ? `${m.name} · Support team` : 'You'}</span>
                  <p>{m.text}</p>
                </li>
              ))}
            </ul>
          )}
          {canReply && (
            <form className="thread-form" onSubmit={send}>
              <label htmlFor={`reply-${ticket.ticket_id}`} className="visually-hidden">
                Reply on {ticket.ticket_id}
              </label>
              <textarea id={`reply-${ticket.ticket_id}`} rows={2} maxLength={2000} value={draft} onChange={(e) => setDraft(e.target.value)} />
              <button type="submit" className="add-button" disabled={busy || !draft.trim()}>
                {busy ? 'Sending…' : 'Send'}
              </button>
            </form>
          )}
          {error && <p className="thread-error" role="alert">{error}</p>}
        </>
      )}
    </div>
  )
}
