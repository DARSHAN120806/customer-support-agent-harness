import { useEffect, useState, type FormEvent } from 'react'
import { ApiError, dashboardApi, type OrderDetail, type OrderRow } from '../../api'
import { day } from '../../format'
import { Tag } from '../shop/Tag'
import { rupees } from '../shop/cart'

// The kinds of records an order can carry, in plain words.
const RECORDS: Record<string, string> = {
  past_support_tickets: 'Earlier support tickets',
  refunds: 'Refunds',
  returns: 'Returns',
  warranty_claims: 'Warranty claims',
  address_change_requests: 'Address changes',
  carrier_investigations: 'Carrier investigations',
  refund_disputes: 'Refund disputes',
  damage_reports: 'Damage reports',
}
// Order fields shown at the top, in this order.
const FIELDS: [string, string][] = [
  ['status', 'Status'],
  ['placed_on', 'Placed'],
  ['dispatched_on', 'Dispatched'],
  ['delivered_on', 'Delivered'],
  ['shipping_method', 'Shipping'],
  ['carrier', 'Carrier'],
  ['tracking_number', 'Tracking'],
  ['payment_method', 'Payment'],
  ['ship_to', 'Ship to'],
]

const words = (key: string) => key.replace(/_/g, ' ').replace(/^./, (c) => c.toUpperCase())

// Orders, read only: find an order and see everything on it.
export function Orders() {
  const [query, setQuery] = useState('')
  const [rows, setRows] = useState<OrderRow[] | null>(null)
  const [total, setTotal] = useState(0)
  const [open, setOpen] = useState<OrderDetail | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function search(q: string) {
    setError(null)
    try {
      const found = await dashboardApi.orders(q)
      setRows(found.orders)
      setTotal(found.total)
    } catch (e) {
      setError((e as ApiError).message)
    }
  }

  // The newest orders, before any search.
  useEffect(() => {
    dashboardApi
      .orders('')
      .then((found) => {
        setRows(found.orders)
        setTotal(found.total)
      })
      .catch((e: ApiError) => setError(e.message))
  }, [])

  function submit(event: FormEvent) {
    event.preventDefault()
    setOpen(null)
    search(query)
  }

  async function show(id: string) {
    try {
      setOpen(await dashboardApi.order(id))
    } catch (e) {
      setError((e as ApiError).message)
    }
  }

  if (open) return <OrderView detail={open} onBack={() => setOpen(null)} />

  return (
    <section aria-labelledby="orders-title">
      <header className="ad-page-head">
        <h2 id="orders-title">Orders</h2>
        <p className="ad-muted">Every order and its records, read only. Customer emails are masked.</p>
      </header>

      <form className="ad-filters" onSubmit={submit} role="search">
        <label className="grow">
          <span>Find</span>
          <input type="search" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Order ID, customer name or email, or item" />
        </label>
        <button type="submit" className="ad-button">
          Search
        </button>
        {rows && (
          <span className="ad-count">
            {rows.length < total ? `${rows.length} of ${total.toLocaleString()} orders` : `${total.toLocaleString()} order${total === 1 ? '' : 's'}`}
          </span>
        )}
      </form>

      {error && <p className="ad-error" role="alert">{error}</p>}
      {rows && rows.length === 0 && <p className="ad-empty">No orders match</p>}
      {rows && rows.length > 0 && (
        <div className="ad-table-wrap">
          <table className="ad-table" aria-label="Orders">
            <thead>
              <tr>
                <th>Order</th>
                <th>Placed</th>
                <th>Customer</th>
                <th>Items</th>
                <th>Status</th>
                <th className="num">Records</th>
                <th className="num">Total</th>
                <th>
                  <span className="visually-hidden">Open</span>
                </th>
              </tr>
            </thead>
            <tbody>
              {rows.map((o) => (
                <tr key={o.order_id}>
                  <td>
                    <Tag>{o.order_id}</Tag>
                  </td>
                  <td className="nowrap ad-muted">{day(o.placed_on)}</td>
                  <td className="nowrap">{o.customer_name}</td>
                  <td className="ad-summary">{o.items.join(', ')}</td>
                  <td className="nowrap">{words(o.status)}</td>
                  <td className="num ad-mono">{o.records || '—'}</td>
                  <td className="num ad-mono">{rupees(o.total)}</td>
                  <td>
                    <button type="button" className="ad-link" onClick={() => show(o.order_id)}>
                      Open
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

export function OrderView({ detail, onBack, backLabel = '← All orders' }: { detail: OrderDetail; onBack: () => void; backLabel?: string }) {
  const { order, customer } = detail
  return (
    <section aria-label={`Order ${order.order_id}`}>
      <button type="button" className="ad-link ad-back" onClick={onBack}>
        {backLabel}
      </button>
      <header className="ad-page-head">
        <h2>
          Order <span className="ad-mono">{order.order_id}</span>
        </h2>
        <p className="ad-muted">
          {customer.name}
          {customer.city ? ` · ${customer.city}` : ''} · {customer.email}
        </p>
      </header>

      <div className="ad-grid">
        <section className="ad-card" aria-label="Items">
          <h3>Items</h3>
          <ul className="ad-outline">
            {order.items.map((item, i) => (
              <li key={i}>
                <span>
                  {item.name} <span className="ad-muted">× {item.quantity}</span>
                </span>
                <span className="ad-mono">{rupees(item.unit_price * item.quantity)}</span>
              </li>
            ))}
            <li>
              <span className="ad-muted">Shipping</span>
              <span className="ad-mono">{rupees(Number(order.shipping_cost ?? 0))}</span>
            </li>
            <li>
              <strong>Total</strong>
              <span className="ad-mono">{rupees(Number(order.total ?? 0))}</span>
            </li>
          </ul>
        </section>
        <section className="ad-card" aria-label="Details">
          <h3>Details</h3>
          <dl className="ad-facts">
            {FIELDS.filter(([key]) => order[key] != null && order[key] !== '').map(([key, label]) => (
              <div key={key}>
                <dt>{label}</dt>
                <dd>{words(String(order[key]))}</dd>
              </div>
            ))}
          </dl>
        </section>
      </div>

      {Object.entries(RECORDS).map(([key, label]) => {
        const records = order[key]
        if (!Array.isArray(records) || records.length === 0) return null
        return (
          <section key={key} className="ad-card ad-records" aria-label={label}>
            <h3>{label}</h3>
            {records.map((record, i) => (
              <dl key={i} className="ad-record">
                {Object.entries(record as Record<string, unknown>).map(([field, value]) => (
                  <div key={field}>
                    <dt>{words(field)}</dt>
                    <dd>{typeof value === 'object' ? JSON.stringify(value) : String(value)}</dd>
                  </div>
                ))}
              </dl>
            ))}
          </section>
        )
      })}
    </section>
  )
}
