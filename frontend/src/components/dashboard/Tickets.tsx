import { useEffect, useMemo, useState } from 'react'
import { ApiError, dashboardApi, type Ticket } from '../../api'

type Props = {
  onOpenConversation: (conversationId: string) => void
}

function words(text: string): string {
  return text.replace(/_/g, ' ')
}

// Every ticket the assistant or the harness created, newest first.
export function Tickets({ onOpenConversation }: Props) {
  const [tickets, setTickets] = useState<Ticket[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [reason, setReason] = useState('all')
  const [search, setSearch] = useState('')

  useEffect(() => {
    dashboardApi.tickets().then(setTickets).catch((e: ApiError) => setError(e.message))
  }, [])

  const reasons = useMemo(() => [...new Set((tickets ?? []).map((t) => t.reason))].sort(), [tickets])
  const shown = (tickets ?? []).filter((t) => {
    const needle = search.trim().toLowerCase()
    return (
      (reason === 'all' || t.reason === reason) &&
      (!needle ||
        t.ticket_id.toLowerCase().includes(needle) ||
        (t.order_id ?? '').toLowerCase().includes(needle) ||
        t.summary.toLowerCase().includes(needle))
    )
  })

  if (error) return <p className="error" role="alert">{error}</p>
  if (!tickets) return <p className="muted">Loading tickets…</p>

  return (
    <section aria-label="Tickets" className="dash-section">
      <div className="filters">
        <label>
          Reason
          <select value={reason} onChange={(e) => setReason(e.target.value)}>
            <option value="all">All reasons</option>
            {reasons.map((r) => (
              <option key={r} value={r}>
                {words(r)}
              </option>
            ))}
          </select>
        </label>
        <label className="grow">
          Search
          <input
            type="search"
            placeholder="Ticket, order, or summary"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </label>
        <span className="muted small">
          {shown.length} of {tickets.length} tickets
        </span>
      </div>

      {tickets.length === 0 ? (
        <p className="empty">No tickets yet. They appear here when the assistant hands a chat to a person.</p>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Ticket</th>
                <th>Created</th>
                <th>Reason</th>
                <th>Order</th>
                <th>Summary</th>
                <th>Status</th>
                <th aria-label="Conversation" />
              </tr>
            </thead>
            <tbody>
              {shown.map((t) => (
                <tr key={t.ticket_id}>
                  <td className="nowrap strong">{t.ticket_id}</td>
                  <td className="nowrap">{t.created_at.replace('T', ' ').slice(0, 16)}</td>
                  <td>
                    <span className="tag">{words(t.reason)}</span>
                  </td>
                  <td className="nowrap">{t.order_id ?? '—'}</td>
                  <td className="summary-cell">{t.summary}</td>
                  <td>
                    <span className={`status status-${t.status}`}>{t.status}</span>
                  </td>
                  <td>
                    {t.conversation_id && (
                      <button className="link-button" onClick={() => onOpenConversation(t.conversation_id!)}>
                        View chat
                      </button>
                    )}
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
