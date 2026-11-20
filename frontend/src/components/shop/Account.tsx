// "Your orders" and "Your tickets" on the shop page: the signed-in customer's
// own orders, and their support tickets from the shop's records and from chat.
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
}

export function YourTickets({ tickets, error }: TicketsProps) {
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
              </div>
              <span className={ticket.status === 'open' ? 'ticket-status open' : 'ticket-status'}>{sentence(ticket.status)}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
