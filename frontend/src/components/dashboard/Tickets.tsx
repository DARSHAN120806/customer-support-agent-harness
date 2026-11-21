import { useEffect, useMemo, useState } from 'react'
import { ApiError, dashboardApi, type PanelPerson, type Ticket } from '../../api'
import { REASON_LABEL, dateTime, statusLabel } from '../../format'
import { Tag } from '../shop/Tag'
import { TicketView } from './TicketView'

type Props = {
  person: PanelPerson
  onOpenConversation: (conversationId: string) => void
}

type Show = 'waiting' | 'mine' | 'all'

// Every ticket the assistant or the harness created, newest first. Support
// staff take a waiting ticket and answer the customer from here.
export function Tickets({ person, onOpenConversation }: Props) {
  const [tickets, setTickets] = useState<Ticket[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [show, setShow] = useState<Show>('waiting')
  const [reason, setReason] = useState('all')
  const [search, setSearch] = useState('')
  const [open, setOpen] = useState<string | null>(null)

  function load() {
    dashboardApi.tickets().then(setTickets).catch((e: ApiError) => setError(e.message))
  }

  useEffect(load, [])

  const mine = (t: Ticket) => t.assigned_to?.staff_id === person.staff_id && t.assigned_to?.name === person.name
  const counts = useMemo(
    () => ({
      waiting: (tickets ?? []).filter((t) => t.status === 'open').length,
      mine: (tickets ?? []).filter((t) => t.status === 'in_progress' && mine(t)).length,
      all: (tickets ?? []).length,
    }),
    // `mine` only reads the signed-in person, which does not change here.
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [tickets],
  )

  if (open) {
    return (
      <TicketView
        ticketId={open}
        person={person}
        onBack={() => {
          setOpen(null)
          load()
        }}
        onOpenConversation={onOpenConversation}
      />
    )
  }

  const reasons = [...new Set((tickets ?? []).map((t) => t.reason))].sort()
  const needle = search.trim().toLowerCase()
  const shown = (tickets ?? []).filter(
    (t) =>
      (show === 'all' || (show === 'waiting' ? t.status === 'open' : t.status === 'in_progress' && mine(t))) &&
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
        <p className="ad-muted">
          Chats the assistant handed to a person. Take a waiting ticket to answer the customer. Customer emails are masked.
        </p>
      </header>

      {error ? (
        <p className="ad-error" role="alert">{error}</p>
      ) : !tickets ? (
        <p className="ad-muted">Loading tickets…</p>
      ) : tickets.length === 0 ? (
        <p className="ad-empty">No tickets yet. They appear here when the assistant hands a chat to a person.</p>
      ) : (
        <>
          <div className="ad-choice ad-show" role="radiogroup" aria-label="Show">
            {([['waiting', 'Waiting'], ['mine', 'Mine'], ['all', 'All']] as const).map(([id, label]) => (
              <button key={id} type="button" role="radio" aria-checked={show === id} className={show === id ? 'selected' : ''} onClick={() => setShow(id)}>
                {label} <span className="ad-mono ad-muted">{counts[id]}</span>
              </button>
            ))}
          </div>

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

          {shown.length === 0 ? (
            <p className="ad-empty">
              {show === 'waiting' ? 'No tickets are waiting.' : show === 'mine' ? 'You are not answering any tickets.' : 'No tickets match.'}
            </p>
          ) : (
            <div className="ad-table-wrap">
              <table className="ad-table" aria-label="Tickets">
                <thead>
                  <tr>
                    <th>Ticket</th>
                    <th>Created</th>
                    <th>Reason</th>
                    <th>Order</th>
                    <th>Summary</th>
                    <th>Status</th>
                    <th>
                      <span className="visually-hidden">Open</span>
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
                      <td className={t.status === 'open' ? 'ad-status open' : 'ad-status'}>
                        {statusLabel(t)}
                        {t.live && t.status !== 'closed' && <span className="ad-live">in the chat</span>}
                      </td>
                      <td className="nowrap">
                        <button type="button" className="ad-link" onClick={() => setOpen(t.ticket_id)}>
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
