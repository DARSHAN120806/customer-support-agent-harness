import { useEffect, useState } from 'react'
import { Bar, CartesianGrid, ComposedChart, Line, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { ApiError, dashboardApi, type Stats, type Ticket } from '../../api'
import { REASON_LABEL, RULE_LABEL, dateTime, day, money, ms, percent } from '../../format'
import { Tag } from '../shop/Tag'
import { CHART, prefersReducedMotion } from './chart'

type Props = {
  onOpenTickets: () => void
  onOpenConversation: (conversationId: string) => void
}

export function Overview({ onOpenTickets, onOpenConversation }: Props) {
  const [stats, setStats] = useState<Stats | null>(null)
  const [tickets, setTickets] = useState<Ticket[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [animate] = useState(() => !prefersReducedMotion())

  useEffect(() => {
    Promise.all([dashboardApi.stats(), dashboardApi.tickets()])
      .then(([s, t]) => {
        setStats(s)
        setTickets(t)
      })
      .catch((e: ApiError) => setError(e.message))
  }, [])

  if (error) return <p className="ad-error" role="alert">{error}</p>
  if (!stats || !tickets) return <p className="ad-muted">Loading the overview…</p>

  const chartDays = stats.days.map((d) => ({ ...d, label: day(d.date) }))

  return (
    <section aria-labelledby="overview-title">
      <header className="ad-page-head">
        <h2 id="overview-title">Overview</h2>
        <p className="ad-muted">Every conversation logged on this server</p>
      </header>

      <div className="ad-stats">
        <Figure label="Conversations" value={stats.conversations.toLocaleString()} note={`${stats.customers} customers`} />
        <Figure
          label="Messages answered"
          value={stats.messages.toLocaleString()}
          note={`${ms(stats.average_reply_ms)} average reply time`}
        />
        <Figure
          label="Handed to a person"
          value={percent(stats.handover_rate)}
          note={`${stats.tickets} tickets, ${stats.tickets_by_harness} made by the harness`}
        />
        <Figure label="Model cost so far" value={money(stats.cost_usd)} note={`${money(stats.cost_per_message_usd)} per message`} />
      </div>

      <div className="ad-grid">
        <figure className="ad-card ad-main-chart">
          <figcaption>
            <span>Messages and tickets, last 14 days</span>
            <span className="ad-legend">
              <span className="ad-key bars" /> Messages <span className="ad-key line" /> Tickets
            </span>
          </figcaption>
          <div className="ad-chart-box">
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={chartDays} margin={{ top: 8, right: 8, bottom: 0, left: -24 }}>
                <CartesianGrid vertical={false} stroke={CHART.grid} />
                <XAxis dataKey="label" tick={CHART.tick} tickLine={false} axisLine={{ stroke: CHART.grid }} interval="preserveStartEnd" minTickGap={20} />
                <YAxis allowDecimals={false} tick={CHART.tick} tickLine={false} axisLine={false} />
                <Tooltip cursor={{ fill: CHART.cursor }} contentStyle={CHART.tooltip} />
                <Bar dataKey="messages" name="Messages" fill={CHART.neutral} radius={[4, 4, 0, 0]} isAnimationActive={animate} />
                <Line dataKey="tickets" name="Tickets" stroke={CHART.accent} strokeWidth={2} dot={false} isAnimationActive={animate} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </figure>

        <div className="ad-side">
          <RankedList title="Checks that fired" counts={stats.checks} labels={RULE_LABEL} empty="No check has fired yet" />
          <RankedList title="Ticket reasons" counts={stats.tickets_by_reason} labels={REASON_LABEL} empty="No tickets yet" />
        </div>
      </div>

      <section className="ad-card" aria-labelledby="recent-title">
        <div className="ad-card-head">
          <h3 id="recent-title">Recent tickets</h3>
          <button type="button" className="ad-link" onClick={onOpenTickets}>
            All tickets
          </button>
        </div>
        {tickets.length === 0 ? (
          <p className="ad-empty">No tickets yet</p>
        ) : (
          <ul className="ad-rows">
            {tickets.slice(0, 5).map((t) => (
              <li key={t.ticket_id} className="ad-row">
                <Tag>{t.ticket_id}</Tag>
                <span className="ad-row-main">
                  {REASON_LABEL[t.reason] ?? t.reason}
                  <span className="ad-muted"> · {dateTime(t.created_at)}</span>
                </span>
                {t.conversation_id && (
                  <button type="button" className="ad-link" onClick={() => onOpenConversation(t.conversation_id!)}>
                    View chat
                  </button>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>
    </section>
  )
}

function Figure({ label, value, note }: { label: string; value: string; note: string }) {
  return (
    <div className="ad-card ad-figure">
      <p className="ad-figure-label">{label}</p>
      <p className="ad-figure-value">{value}</p>
      <p className="ad-muted">{note}</p>
    </div>
  )
}

type RankedProps = {
  title: string
  counts: Record<string, number>
  labels: Record<string, string>
  empty: string
}

// A short ranked list with thin bars: the biggest one gets the accent.
function RankedList({ title, counts, labels, empty }: RankedProps) {
  const rows = Object.entries(counts)
  const top = Math.max(1, ...rows.map(([, n]) => n))
  return (
    <section className="ad-card" aria-label={title}>
      <h3>{title}</h3>
      {rows.length === 0 ? (
        <p className="ad-empty">{empty}</p>
      ) : (
        <ul className="ad-ranked">
          {rows.map(([key, n], i) => (
            <li key={key}>
              <span className="ad-ranked-label">{labels[key] ?? key.replace(/_/g, ' ')}</span>
              <span className="ad-ranked-count">{n}</span>
              <span className="ad-bar" aria-hidden="true">
                <span className={i === 0 ? 'lead' : ''} style={{ width: `${(n / top) * 100}%` }} />
              </span>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
