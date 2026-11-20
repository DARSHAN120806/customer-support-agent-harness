import { useEffect, useRef, useState, type FormEvent, type KeyboardEvent } from 'react'
import { api, ApiError, MAX_MESSAGE_LENGTH, type ReplyDetails, type Session, type TranscriptEntry } from '../api'
import { BehindTheScenes } from './BehindTheScenes'
import { FormattedText } from './FormattedText'
import { OrdersSidebar } from './OrdersSidebar'

type Props = {
  session: Session
  onSignOut: () => void
  onSessionExpired: () => void
  onOpenDashboard: () => void
}

// A message in the chat. Replies sent during this visit also keep the
// "behind the scenes" details the API returned with them.
type ChatEntry = TranscriptEntry & { isError?: boolean; details?: ReplyDetails | null; outcome?: string }

// Whether the panel is open is remembered in this browser.
const PANEL_KEY = 'juniper-lane-behind-the-scenes'

const SUGGESTIONS = [
  'What is your return policy?',
  'How much is express shipping?',
  'I want to talk to a human.',
]

export function Chat({ session, onSignOut, onSessionExpired, onOpenDashboard }: Props) {
  const [entries, setEntries] = useState<ChatEntry[]>(session.transcript)
  const [draft, setDraft] = useState('')
  const [waiting, setWaiting] = useState(false)
  const endRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const firstName = session.customer.name.split(' ')[0]
  const [panelOpen, setPanelOpen] = useState(() => localStorage.getItem(PANEL_KEY) === 'open')
  // Which reply the panel describes; null means "the latest one".
  const [selected, setSelected] = useState<number | null>(null)

  function setPanel(open: boolean) {
    localStorage.setItem(PANEL_KEY, open ? 'open' : 'closed')
    setPanelOpen(open)
  }

  const replyIndexes = entries.flatMap((entry, i) => (entry.role === 'assistant' && !entry.isError ? [i] : []))
  const shownIndex = selected ?? replyIndexes.at(-1) ?? null
  const shown = shownIndex === null ? undefined : entries[shownIndex]
  const shownNumber = shownIndex === null ? null : replyIndexes.indexOf(shownIndex) + 1

  // Keep the newest message in view.
  useEffect(() => {
    endRef.current?.scrollIntoView?.({ behavior: 'smooth' })
  }, [entries, waiting])

  async function send(text: string) {
    const message = text.trim()
    if (!message || waiting) return
    setDraft('')
    setEntries((current) => [...current, { role: 'customer', text: message }])
    setWaiting(true)
    try {
      const reply = await api.sendMessage(session.session_id, message)
      setEntries((current) => [
        ...current,
        {
          role: 'assistant',
          text: reply.reply,
          ticket_ids: reply.new_ticket_ids,
          details: reply.details,
          outcome: reply.outcome,
        },
      ])
      setSelected(null) // follow the newest reply
    } catch (e) {
      const error = e as ApiError
      if (error.status === 404) {
        onSessionExpired()
        return
      }
      setEntries((current) => [...current, { role: 'assistant', text: error.message, isError: true }])
    } finally {
      setWaiting(false)
      inputRef.current?.focus()
    }
  }

  function onSubmit(e: FormEvent) {
    e.preventDefault()
    send(draft)
  }

  // Enter sends; Shift+Enter starts a new line.
  function onKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send(draft)
    }
  }

  function askAbout(question: string) {
    setDraft(question)
    inputRef.current?.focus()
  }

  return (
    <div className={`chat-layout${panelOpen ? ' with-insights' : ''}`}>
      <header className="topbar glass">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">JL</span>
          <div>
            <h1>{session.assistant_name}</h1>
            <p className="muted small">
              <span className="ai-badge">AI</span> An automated assistant. Ask for a person at any time.
            </p>
          </div>
        </div>
        <div className="topbar-right">
          <span className="muted small">Signed in as {session.customer.name}</span>
          <button
            className={`secondary${panelOpen ? ' toggled' : ''}`}
            aria-pressed={panelOpen}
            onClick={() => setPanel(!panelOpen)}
          >
            Behind the scenes
          </button>
          <button className="secondary" onClick={onOpenDashboard}>Dashboard</button>
          <button className="secondary" onClick={onSignOut}>Sign out</button>
        </div>
      </header>

      <OrdersSidebar orders={session.orders} onAsk={askAbout} />

      <section className="chat glass" aria-label="Chat">
        <div className="messages" role="log" aria-live="polite">
          {entries.length === 0 && (
            <div className="welcome">
              <p>
                Hi {firstName}! I can help with your orders, shipping, returns, refunds, and warranties.
              </p>
              <div className="suggestions">
                {SUGGESTIONS.map((s) => (
                  <button key={s} className="chip" onClick={() => send(s)}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {entries.map((entry, i) => (
            <div key={i} className={`bubble-row ${entry.role}`}>
              <div className={`bubble ${entry.role}${entry.isError ? ' error-bubble' : ''}`}>
                {entry.role === 'assistant' ? <FormattedText text={entry.text} /> : <p>{entry.text}</p>}
                {entry.ticket_ids?.map((id) => (
                  <p key={id} className="ticket-note">
                    Ticket <strong>{id}</strong> created. Our team will reply by email.
                  </p>
                ))}
                {entry.role === 'assistant' && entry.details && (
                  <button
                    className={`link-button how-link${panelOpen && shownIndex === i ? ' current' : ''}`}
                    onClick={() => {
                      setSelected(i)
                      setPanel(true)
                    }}
                  >
                    How was this answered?
                  </button>
                )}
              </div>
            </div>
          ))}

          {waiting && (
            <div className="bubble-row assistant">
              <div className="bubble assistant typing" aria-label="The assistant is typing">
                <span /> <span /> <span />
              </div>
            </div>
          )}
          <div ref={endRef} />
        </div>

        <form className="composer" onSubmit={onSubmit}>
          <label htmlFor="message" className="visually-hidden">Your message</label>
          <textarea
            id="message"
            ref={inputRef}
            rows={2}
            maxLength={MAX_MESSAGE_LENGTH}
            placeholder="Type your message…"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={onKeyDown}
          />
          <button type="submit" disabled={waiting || !draft.trim()}>
            {waiting ? 'Sending…' : 'Send'}
          </button>
        </form>
      </section>

      {panelOpen && (
        <BehindTheScenes
          details={shown?.details}
          outcome={shown?.outcome}
          conversationId={session.conversation_id}
          replyNumber={shownNumber}
          onClose={() => setPanel(false)}
        />
      )}
    </div>
  )
}
