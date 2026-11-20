import type { OrderSummary } from '../api'

type Props = {
  orders: OrderSummary[]
  onAsk: (question: string) => void
}

const STATUS_LABEL: Record<string, string> = {
  processing: 'Processing',
  dispatched: 'On its way',
  shipped: 'On its way',
  delivered: 'Delivered',
  cancelled: 'Cancelled',
  lost: 'Lost in transit',
  refunded: 'Refunded',
  return_requested: 'Return requested',
}

// The signed-in customer's own orders, so they don't have to remember order IDs.
export function OrdersSidebar({ orders, onAsk }: Props) {
  const newestFirst = [...orders].sort((a, b) => b.placed_on.localeCompare(a.placed_on))
  return (
    <aside className="orders glass" aria-label="Your orders">
      <h2>Your orders</h2>
      {newestFirst.length === 0 && <p className="muted">No orders yet.</p>}
      <ul>
        {newestFirst.map((order) => (
          <li key={order.order_id} className="order">
            <div className="order-head">
              <span className="order-id">{order.order_id}</span>
              <span className={`status status-${order.status}`}>
                {STATUS_LABEL[order.status] ?? order.status}
              </span>
            </div>
            <p className="order-items">{order.items.join(', ')}</p>
            <p className="muted small">
              Placed {order.placed_on} · ${order.total.toFixed(2)}
            </p>
            <button className="link-button" onClick={() => onAsk(`What's the status of my order ${order.order_id}?`)}>
              Ask about this order
            </button>
          </li>
        ))}
      </ul>
    </aside>
  )
}
