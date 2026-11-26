// The support chat on the shop page: a "Chat with us" button at the bottom
// right that opens a chat window with the shop's virtual assistant. Closing
// the window keeps the conversation, so opening it again carries on.
//
// When a person from the support team takes the customer's ticket, they join
// this same window: their messages arrive through a quiet check every few
// seconds, and the customer's messages go to them instead of the assistant.
import { useEffect, useRef, useState, type FormEvent, type KeyboardEvent } from 'react'
import { api, ApiError, MAX_MESSAGE_LENGTH, type Handoff, type Session, type TranscriptEntry } from '../../api'
import { FormattedText } from '../FormattedText'
import { Tag } from '../shop/Tag'

type Props = {
  session: Session
  open: boolean
  onOpenChange: (open: boolean) => void
  // A question handed over from the page, like "Ask about this order".
  // `id` changes each time, so the same question can be asked twice.
  question: { text: string; id: number } | null
  onTicketCreated: () => void
  onSessionExpired: () => void
  // Called after every reply, for example so the page can show a new refund request.
  onReplied?: () => void
}

type Entry = TranscriptEntry & { isError?: boolean }

// How often the window checks for messages from the support team.
const CHECK_MS = 3000

// Whether the chat fills the whole page (the "Expand" button), remembered for
// this browser tab like the open/closed state.
const EXPANDED_KEY = 'juniper-lane-chat-expanded'

const SUGGESTIONS = ['What is your return policy?', 'How much is express shipping?', 'I want to talk to a person']

export function SupportChat({ session, open, onOpenChange, question, onTicketCreated, onSessionExpired, onReplied }: Props) {
  const [entries, setEntries] = useState<Entry[]>(session.transcript)
  const [draft, setDraft] = useState('')
  const [waiting, setWaiting] = useState(false)
  const listRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const launcherRef = useRef<HTMLButtonElement>(null)
  const wasOpen = useRef(open)
  const firstName = session.customer.name.split(' ')[0]
  // Who from the team is in the chat, and how many of their messages arrived
  // while the window was closed.
  const [handoff, setHandoff] = useState<Handoff>(session.handoff ?? null)
  const [unread, setUnread] = useState(0)
  const [expanded, setExpanded] = useState(() => sessionStorage.getItem(EXPANDED_KEY) === 'yes')

  function toggleExpanded() {
    const next = !expanded
    setExpanded(next)
    sessionStorage.setItem(EXPANDED_KEY, next ? 'yes' : 'no')
    inputRef.current?.focus()
  }

  // While the chat fills the page, the shop behind it does not scroll.
  useEffect(() => {
    if (!(open && expanded)) return
    const before = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      document.body.style.overflow = before
    }
  }, [open, expanded])
  // How many chat lines the server has; the check asks only for newer ones.
  const known = useRef(session.transcript.length)
  const openRef = useRef(open)
  const callbacks = useRef({ onTicketCreated, onSessionExpired })
  useEffect(() => {
    openRef.current = open
    callbacks.current = { onTicketCreated, onSessionExpired }
  })
  // Opening the window counts the new messages as read.
  if (open && unread !== 0) setUnread(0)

  // Check for news from the support team every few seconds. The customer's own
  // messages and the assistant's replies are already on screen, so only the
  // team's messages and notes ("Asha has joined the chat") are added.
  useEffect(() => {
    let stopped = false
    const check = () =>
      api
        .updates(session.session_id, known.current)
        .then((news) => {
          if (stopped) return
          known.current = news.next
          setHandoff(news.handoff)
          const fromTeam = news.entries.filter((e) => e.role === 'staff' || e.role === 'system')
          if (fromTeam.length === 0) return
          setEntries((current) => [...current, ...fromTeam])
          if (!openRef.current) setUnread((n) => n + fromTeam.filter((e) => e.role === 'staff').length)
          callbacks.current.onTicketCreated() // "Your tickets" shows the change too
        })
        .catch((e: ApiError) => {
          if (!stopped && e.status === 404) callbacks.current.onSessionExpired()
        })
    const timer = setInterval(check, CHECK_MS)
    return () => {
      stopped = true
      clearInterval(timer)
    }
  }, [session.session_id])

  // A question from the page goes into the message box, ready to send. This is
  // React's way of adjusting state when a prop changes: during the render.
  const [seenQuestion, setSeenQuestion] = useState<number | null>(null)
  if (question && question.id !== seenQuestion) {
    setSeenQuestion(question.id)
    setDraft(question.text)
  }

  // Opening moves the keyboard to the message box; closing gives it back to
  // the button that opened the chat.
  useEffect(() => {
    if (open) inputRef.current?.focus()
    else if (wasOpen.current) launcherRef.current?.focus()
    wasOpen.current = open
  }, [open, question])

  // Scroll only the message list, never the page. When a reply arrives, show
  // it from its start, with the question above it, so a long answer is read
  // from the top. Otherwise (sending, typing) go to the bottom.
  useEffect(() => {
    const list = listRef.current
    if (!list) return
    const last = entries.at(-1)
    const questions = list.querySelectorAll<HTMLElement>('.sc-row.customer')
    const question = questions[questions.length - 1]
    if (!waiting && last?.role === 'assistant' && question) {
      const offset = question.getBoundingClientRect().top - list.getBoundingClientRect().top
      list.scrollTo?.({ top: list.scrollTop + offset - 16, behavior: 'smooth' })
    } else {
      list.scrollTo?.({ top: list.scrollHeight, behavior: 'smooth' })
    }
  }, [entries, waiting, open])

  async function send(text: string) {
    const message = text.trim()
    if (!message || waiting) return
    setDraft('')
    setEntries((current) => [...current, { role: 'customer', text: message }])
    setWaiting(true)
    try {
      const reply = await api.sendMessage(session.session_id, message)
      // No reply means a person from the team has the message; theirs arrives
      // through the check above.
      if (reply.reply !== null) {
        const text = reply.reply
        setEntries((current) => [...current, { role: 'assistant', text, ticket_ids: reply.new_ticket_ids }])
      }
      if (reply.new_ticket_ids.length > 0) onTicketCreated()
      onReplied?.()
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

  // Enter sends; Shift+Enter starts a new line; Escape closes the window.
  function onKeyDown(e: KeyboardEvent<HTMLElement>) {
    if (e.key === 'Escape') {
      onOpenChange(false)
      return
    }
    if (e.target === inputRef.current && e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send(draft)
    }
  }

  return (
    <>
      {!open && (
        <button ref={launcherRef} type="button" className="sc-launcher" onClick={() => onOpenChange(true)}>
          <ChatIcon />
          <span>Chat with us</span>
          {unread > 0 && <span className="sc-unread">{unread} new</span>}
        </button>
      )}

      <section
        className={expanded ? 'sc-panel expanded' : 'sc-panel'}
        role="dialog"
        aria-modal={expanded}
        aria-label={session.assistant_name}
        hidden={!open}
        onKeyDown={onKeyDown}
      >
        <header className="sc-head">
          <div>
            <h2>{handoff ? `${handoff.name} from the support team` : session.assistant_name}</h2>
            {handoff ? (
              <p className="sc-sub">
                <span className="sc-ai person">Person</span> You're talking to a member of our team
              </p>
            ) : (
              <p className="sc-sub">
                <span className="sc-ai">AI</span> An automated assistant. Ask for a person at any time
              </p>
            )}
          </div>
          <div className="sc-head-actions">
            <button type="button" className="sc-close sc-size" onClick={toggleExpanded}>
              {expanded ? 'Shrink' : 'Expand'}
            </button>
            <button type="button" className="sc-close" onClick={() => onOpenChange(false)}>
              Close
            </button>
          </div>
        </header>

        <div className="sc-messages" role="log" aria-live="polite" ref={listRef}>
          {entries.length === 0 && (
            <div className="sc-welcome">
              <p>
                Hi {firstName}. I can help with your orders, shipping, returns, refunds and warranties
              </p>
              <div className="sc-suggestions">
                {SUGGESTIONS.map((s) => (
                  <button key={s} type="button" className="sc-chip" onClick={() => send(s)}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {entries.map((entry, i) =>
            entry.role === 'system' ? (
              // A short note, such as "Asha from the support team has joined the chat".
              <p key={i} className="sc-note">
                {entry.text}
              </p>
            ) : (
              <div key={i} className={`sc-row ${entry.role}`}>
                <div className={`sc-bubble ${entry.role}${entry.isError ? ' error' : ''}`}>
                  {entry.role === 'staff' && <span className="sc-who">{entry.name} · Support team</span>}
                  {entry.role === 'assistant' ? <FormattedText text={entry.text} /> : <p>{entry.text}</p>}
                  {entry.ticket_ids?.map((id) => (
                    <p key={id} className="sc-ticket">
                      Ticket <Tag>{id}</Tag> created. Someone from our team will answer here or under Your tickets
                    </p>
                  ))}
                </div>
              </div>
            ),
          )}

          {waiting && !handoff && (
            <div className="sc-row assistant">
              <div className="sc-bubble assistant sc-typing" aria-label="The assistant is typing">
                <span /> <span /> <span />
              </div>
            </div>
          )}
        </div>

        <form className="sc-composer" onSubmit={onSubmit}>
          <label htmlFor="sc-message" className="visually-hidden">
            Your message
          </label>
          <textarea
            id="sc-message"
            ref={inputRef}
            rows={2}
            maxLength={MAX_MESSAGE_LENGTH}
            placeholder="Write a message"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
          />
          <button type="submit" className="sc-send" disabled={waiting || !draft.trim()}>
            {waiting ? 'Sending…' : 'Send'}
          </button>
        </form>
      </section>
    </>
  )
}

// A speech bubble, drawn as a line icon (same style as the lucide icon set).
function ChatIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z" />
    </svg>
  )
}
