import { useEffect, useMemo, useState } from 'react'
import { ApiError, dashboardApi, type Ticket } from '../../api'
import { REASON_LABEL, dateTime } from '../../format'
import { Tag } from '../shop/Tag'

type Props = {
  onOpenConversation: (conversationId: string) => void
}

// Every ticket the assistant or the harness created, newest first. Emails are
// masked by the API.
export function Tickets({ onOpenConversation }: Props) {
  const [tickets, setTickets] = useState<Ticket[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [reason, setReason] = useState('all')
  const [search, setSearch] = useState('')

  useEffect(() => {
    dashboardApi.tickets().then(setTickets).catch((e: ApiError) => setError(e.message))
  }, [])

  const reasons = useMemo(() => [...new Set((tickets ?? []).map((t) => t.reason))].sort(), [tickets])
  const needle = search.trim().toLowerCase()
  const shown = (tickets ?? []).filter(
    (t) =>
      (reason === 'all' || t.reason === reason) &&
      (!needle ||
        t.ticket_id.toLowerCase().includes(needle) ||
        (t.order_id ?? '').toLowerCase().includes(needle) ||
        t.summary.toLowerCase().includes(needle)),
  )

  return (
    <section aria-labelledby="tickets-title">
      <header className="ad-page-head">
        <h2 id="tickets-title">Tickets</h2>
        <p className="ad-muted">Chats the assistant handed to a person, newest first. Customer emails are masked.</p>
      </header>

      {error ? (
        <p className="ad-error" role="alert">{error}</p>
      ) : !tickets ? (
        <p className="ad-muted">Loading tickets…</p>
      ) : tickets.length === 0 ? (
        <p className="ad-empty">No tickets yet. They appear here when the assistant hands a chat to a person.</p>
      ) : (
        <>
          <div className="ad-filters">
            <label>
              <span>Reason</span>
              <select value={reason} onChange={(e) => setReason(e.target.value)}>
                <option value="all">All reasons</option>
                {reasons.map((r) => (
                  <option key={r} value={r}>
                    {REASON_LABEL[r] ?? r}
                  </option>
                ))}
              </select>
            </label>
            <label className="grow">
              <span>Search</span>
              <input type="search" placeholder="Ticket, order or summary" value={search} onChange={(e) => setSearch(e.target.value)} />
            </label>
            <span className="ad-count">
              {shown.length} of {tickets.length} tickets
            </span>
          </div>

          <div className="ad-table-wrap">
            <table className="ad-table">
              <thead>
                <tr>
                  <th>Ticket</th>
                  <th>Created</th>
                  <th>Reason</th>
                  <th>Order</th>
                  <th>Summary</th>
                  <th>Status</th>
                  <th>
                    <span className="visually-hidden">Conversation</span>
                  </th>
                </tr>
              </thead>
              <tbody>
                {shown.map((t) => (
                  <tr key={t.ticket_id}>
                    <td>
                      <Tag>{t.ticket_id}</Tag>
                    </td>
                    <td className="nowrap ad-muted">{dateTime(t.created_at)}</td>
                    <td className="nowrap">{REASON_LABEL[t.reason] ?? t.reason}</td>
                    <td className="nowrap">{t.order_id ? <Tag>{t.order_id}</Tag> : '—'}</td>
                    <td className="ad-summary">{t.summary}</td>
                    <td className={t.status === 'open' ? 'ad-status open' : 'ad-status'}>{t.status === 'open' ? 'Open' : 'Closed'}</td>
                    <td className="nowrap">
                      {t.conversation_id && (
                        <button type="button" className="ad-link" onClick={() => onOpenConversation(t.conversation_id!)}>
                          View chat
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </section>
  )
}
