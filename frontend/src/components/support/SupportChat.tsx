// The support chat on the shop page: a "Chat with us" button at the bottom
// right that opens a chat window with the shop's virtual assistant. Closing
// the window keeps the conversation, so opening it again carries on.
import { useEffect, useRef, useState, type FormEvent, type KeyboardEvent } from 'react'
import { api, ApiError, MAX_MESSAGE_LENGTH, type Session, type TranscriptEntry } from '../../api'
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
}

type Entry = TranscriptEntry & { isError?: boolean }

const SUGGESTIONS = ['What is your return policy?', 'How much is express shipping?', 'I want to talk to a person']

export function SupportChat({ session, open, onOpenChange, question, onTicketCreated, onSessionExpired }: Props) {
  const [entries, setEntries] = useState<Entry[]>(session.transcript)
  const [draft, setDraft] = useState('')
  const [waiting, setWaiting] = useState(false)
  const listRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const launcherRef = useRef<HTMLButtonElement>(null)
  const wasOpen = useRef(open)
  const firstName = session.customer.name.split(' ')[0]

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
      setEntries((current) => [...current, { role: 'assistant', text: reply.reply, ticket_ids: reply.new_ticket_ids }])
      if (reply.new_ticket_ids.length > 0) onTicketCreated()
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
        </button>
      )}

      <section className="sc-panel" role="dialog" aria-modal="false" aria-label={session.assistant_name} hidden={!open} onKeyDown={onKeyDown}>
        <header className="sc-head">
          <div>
            <h2>{session.assistant_name}</h2>
            <p className="sc-sub">
              <span className="sc-ai">AI</span> An automated assistant. Ask for a person at any time
            </p>
          </div>
          <button type="button" className="sc-close" onClick={() => onOpenChange(false)}>
            Close
          </button>
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

          {entries.map((entry, i) => (
            <div key={i} className={`sc-row ${entry.role}`}>
              <div className={`sc-bubble ${entry.role}${entry.isError ? ' error' : ''}`}>
                {entry.role === 'assistant' ? <FormattedText text={entry.text} /> : <p>{entry.text}</p>}
                {entry.ticket_ids?.map((id) => (
                  <p key={id} className="sc-ticket">
                    Ticket <Tag>{id}</Tag> created. Our team will reply by email
                  </p>
                ))}
              </div>
            </div>
          ))}

          {waiting && (
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
