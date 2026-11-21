import { useEffect, useState, type FormEvent } from 'react'
import { ApiError, dashboardApi, type RefundRequest } from '../../api'
import { dateTime } from '../../format'
import { rupees } from '../shop/cart'
import { Tag } from '../shop/Tag'

type Show = 'waiting' | 'decided' | 'all'

const MAX_RESTOCKING_PERCENT = 20 // Refund Policy: "up to 20%"

const money = (value: string | undefined | null) => rupees(Number(value ?? 0))

// Short status words for the panel; customers see longer, friendlier ones.
const SHORT_STATUS: Record<RefundRequest['status'], string> = {
  approved: 'Approved in chat',
  waiting_for_staff: 'Waiting',
  approved_by_staff: 'Approved',
  denied_by_staff: 'Not approved',
}

const what = (r: RefundRequest) =>
  r.items.length ? r.items.map((i) => `${i.name} ×${i.quantity}`).join(', ') : 'The whole order'

// Refund and return requests from the chat. The shop's rules approve the
// simple ones themselves; the rest wait here for a person to decide.
export function RefundRequests() {
  const [requests, setRequests] = useState<RefundRequest[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [show, setShow] = useState<Show>('waiting')
  const [open, setOpen] = useState<string | null>(null)

  function load() {
    dashboardApi.refundRequests().then(setRequests).catch((e: ApiError) => setError(e.message))
  }

  useEffect(load, [])

  const opened = requests?.find((r) => r.request_id === open)
  if (opened) {
    return (
      <RequestView
        request={opened}
        onBack={() => setOpen(null)}
        onDecided={(changed) => setRequests((all) => (all ?? []).map((r) => (r.request_id === changed.request_id ? changed : r)))}
      />
    )
  }

  const waiting = (r: RefundRequest) => r.status === 'waiting_for_staff'
  const counts = {
    waiting: (requests ?? []).filter(waiting).length,
    decided: (requests ?? []).filter((r) => !waiting(r)).length,
    all: (requests ?? []).length,
  }
  const shown = (requests ?? []).filter((r) => show === 'all' || (show === 'waiting' ? waiting(r) : !waiting(r)))

  return (
    <section aria-labelledby="refunds-title">
      <header className="ad-page-head">
        <h2 id="refunds-title">Refund requests</h2>
        <p className="ad-muted">
          Returns and refunds asked for in the chat. The shop's rules approve simple ones; the rest wait here for a person.
        </p>
      </header>

      {error ? (
        <p className="ad-error" role="alert">{error}</p>
      ) : !requests ? (
        <p className="ad-muted">Loading requests…</p>
      ) : requests.length === 0 ? (
        <p className="ad-empty">No requests yet. They appear here when a customer asks for a return or refund in the chat.</p>
      ) : (
        <>
          <div className="ad-choice ad-show" role="radiogroup" aria-label="Show">
            {([['waiting', 'Waiting'], ['decided', 'Decided'], ['all', 'All']] as const).map(([id, label]) => (
              <button key={id} type="button" role="radio" aria-checked={show === id} className={show === id ? 'selected' : ''} onClick={() => setShow(id)}>
                {label} <span className="ad-mono ad-muted">{counts[id]}</span>
              </button>
            ))}
          </div>

          {shown.length === 0 ? (
            <p className="ad-empty">{show === 'waiting' ? 'No requests are waiting for a person.' : 'No requests here yet.'}</p>
          ) : (
            <div className="ad-table-wrap">
              <table className="ad-table" aria-label="Refund requests">
                <thead>
                  <tr>
                    <th>Request</th>
                    <th>Created</th>
                    <th>Customer</th>
                    <th>Order</th>
                    <th>Reason</th>
                    <th className="num">Refund</th>
                    <th>Status</th>
                    <th>
                      <span className="visually-hidden">Open</span>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {shown.map((r) => (
                    <tr key={r.request_id}>
                      <td>
                        <Tag>{r.request_id}</Tag>
                      </td>
                      <td className="nowrap ad-muted">{dateTime(r.created_at)}</td>
                      <td className="nowrap">
                        {r.customer_name ?? '—'}
                        {r.customer_id && <span className="ad-muted ad-mono"> · {r.customer_id}</span>}
                      </td>
                      <td className="nowrap">
                        <Tag>{r.order_id}</Tag>
                      </td>
                      <td className="nowrap">{r.reason_words}</td>
                      <td className="num ad-mono">{r.money ? money(r.money.net_refund) : '—'}</td>
                      <td className={waiting(r) ? 'ad-status open nowrap' : 'ad-status nowrap'}>{SHORT_STATUS[r.status] ?? r.status_words}</td>
                      <td className="nowrap">
                        <button type="button" className="ad-link" onClick={() => setOpen(r.request_id)}>
                          Open
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </section>
  )
}

type ViewProps = {
  request: RefundRequest
  onBack: () => void
  onDecided: (request: RefundRequest) => void
}

function RequestView({ request: r, onBack, onDecided }: ViewProps) {
  const [fee, setFee] = useState('')
  const [note, setNote] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const m = r.money
  const changedMind = r.reason === 'changed_mind'
  const maxFee = m ? Math.floor((Number(m.item_refund) * MAX_RESTOCKING_PERCENT) / 100) : 0

  async function decide(approve: boolean, e?: FormEvent) {
    e?.preventDefault()
    setBusy(true)
    setError(null)
    try {
      const changed = approve
        ? await dashboardApi.approveRequest(r.request_id, { restocking_fee: Number(fee || 0), note })
        : await dashboardApi.denyRequest(r.request_id, note)
      onDecided(changed)
    } catch (err) {
      setError((err as ApiError).message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <section aria-label={`Request ${r.request_id}`}>
      <button type="button" className="ad-link ad-back" onClick={onBack}>
        ← All requests
      </button>
      <header className="ad-page-head">
        <h2>
          Request <span className="ad-mono">{r.request_id}</span>
        </h2>
        <p className="ad-muted">
          {r.reason_words} · {r.status_words}
        </p>
      </header>

      {error && <p className="ad-error" role="alert">{error}</p>}

      <div className="ad-ticket">
        <div className="ad-ticket-main">
          <section className="ad-card" aria-label="What the customer asked for">
            <h3>What the customer asked for</h3>
            <dl className="ad-facts">
              <div>
                <dt>Customer</dt>
                <dd>
                  {r.customer_name ?? '—'}
                  {r.customer_id && <span className="ad-muted ad-mono"> · {r.customer_id}</span>}
                </dd>
              </div>
              <div>
                <dt>Order</dt>
                <dd>
                  <Tag>{r.order_id}</Tag>
                </dd>
              </div>
              <div>
                <dt>Items</dt>
                <dd>{what(r)}</dd>
              </div>
              <div>
                <dt>Ticket</dt>
                <dd>{r.ticket_id ? <Tag>{r.ticket_id}</Tag> : 'None'}</dd>
              </div>
            </dl>
            {r.details && (
              <>
                <h3 className="ad-subhead">In the customer's words</h3>
                <p>{r.details}</p>
              </>
            )}
            {r.why_staff.length > 0 && (
              <>
                <h3 className="ad-subhead">Why a person decides</h3>
                <ul className="ad-reasons">
                  {r.why_staff.map((why) => (
                    <li key={why}>{why}</li>
                  ))}
                </ul>
              </>
            )}
          </section>

          {m && (
            <section className="ad-card" aria-label="Refund worked out by the rules">
              <h3>Refund worked out by the rules</h3>
              <ul className="ad-outline ad-money">
                <li>
                  <span>Items</span>
                  <span className="ad-mono">{money(m.item_refund)}</span>
                </li>
                {Number(m.shipping_refunded) > 0 && (
                  <li>
                    <span>Shipping refunded</span>
                    <span className="ad-mono">{money(m.shipping_refunded)}</span>
                  </li>
                )}
                {Number(m.return_fee) > 0 && (
                  <li>
                    <span>Return fee</span>
                    <span className="ad-mono">−{money(m.return_fee)}</span>
                  </li>
                )}
                {Number(m.restocking_fee ?? 0) > 0 && (
                  <li>
                    <span>Restocking fee</span>
                    <span className="ad-mono">−{money(m.restocking_fee)}</span>
                  </li>
                )}
                <li className="total">
                  <span>Refund</span>
                  <span className="ad-mono">{money(m.net_refund)}</span>
                </li>
              </ul>
              <p className="ad-muted">
                To {m.refunded_to}
                {m.free_return_label ? ' · free return label' : ''}
              </p>
            </section>
          )}
        </div>

        <aside className="ad-ticket-side" aria-label="Decision">
          <section className="ad-card">
            <h3>Decision</h3>
            {r.status === 'waiting_for_staff' ? (
              <form className="ad-decision" onSubmit={(e) => decide(true, e)}>
                {changedMind && m && (
                  <div className="ad-field">
                    <label htmlFor="restocking-fee">Restocking fee, if the item came back used or without its box</label>
                    <input
                      id="restocking-fee"
                      type="number"
                      inputMode="numeric"
                      min={0}
                      max={maxFee}
                      step={1}
                      value={fee}
                      onChange={(e) => setFee(e.target.value)}
                      placeholder="0"
                      aria-describedby="restocking-fee-hint"
                    />
                    <span id="restocking-fee-hint" className="ad-muted">
                      Up to {rupees(maxFee)} ({MAX_RESTOCKING_PERCENT}% of the items)
                    </span>
                  </div>
                )}
                <div className="ad-field">
                  <label htmlFor="decision-note">Note for the customer</label>
                  <textarea
                    id="decision-note"
                    rows={3}
                    maxLength={1000}
                    value={note}
                    onChange={(e) => setNote(e.target.value)}
                    aria-describedby="decision-note-hint"
                  />
                  <span id="decision-note-hint" className="ad-muted">
                    Needed when you do not approve
                  </span>
                </div>
                <div className="ad-actions">
                  <button type="submit" className="ad-button primary" disabled={busy}>
                    Approve
                  </button>
                  <button type="button" className="ad-button" disabled={busy || note.trim().length < 5} onClick={() => decide(false)}>
                    Not approve
                  </button>
                </div>
              </form>
            ) : r.status === 'approved' ? (
              <p>Approved in the chat by the shop's rules. No one needed to decide.</p>
            ) : (
              <dl className="ad-facts one">
                <div>
                  <dt>{r.status === 'approved_by_staff' ? 'Approved by' : 'Not approved by'}</dt>
                  <dd>
                    {r.decided_by?.name}
                    {r.decided_by?.staff_id && <span className="ad-muted ad-mono"> · {r.decided_by.staff_id}</span>}
                  </dd>
                </div>
                {r.decided_at && (
                  <div>
                    <dt>When</dt>
                    <dd>{dateTime(r.decided_at)}</dd>
                  </div>
                )}
                {r.staff_note && (
                  <div>
                    <dt>Note for the customer</dt>
                    <dd>{r.staff_note}</dd>
                  </div>
                )}
              </dl>
            )}
          </section>
        </aside>
      </div>
    </section>
  )
}
