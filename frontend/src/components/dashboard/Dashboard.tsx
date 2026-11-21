import { useState } from 'react'
import type { PanelPerson } from '../../api'
import { ConversationList, ConversationReplay } from './Conversations'
import { Documents } from './Documents'
import { Evaluations } from './Evaluations'
import { ModelSettings } from './ModelSettings'
import { Orders } from './Orders'
import { Overview } from './Overview'
import { RefundRequests } from './RefundRequests'
import { Tickets } from './Tickets'

type Section = 'overview' | 'tickets' | 'refunds' | 'conversations' | 'evaluations' | 'documents' | 'orders' | 'model'

// Support staff see what they need to answer tickets; the admin sees everything.
const STAFF_SECTIONS: Section[] = ['overview', 'tickets', 'refunds', 'conversations', 'orders']

const SECTIONS: { id: Section; label: string }[] = [
  { id: 'overview', label: 'Overview' },
  { id: 'tickets', label: 'Tickets' },
  { id: 'refunds', label: 'Refund requests' },
  { id: 'conversations', label: 'Conversations' },
  { id: 'evaluations', label: 'Evaluations' },
  { id: 'documents', label: 'Documents' },
  { id: 'orders', label: 'Orders' },
  { id: 'model', label: 'Model' },
]

type Props = {
  person: PanelPerson
  onSignOut: () => void
}

// The admin panel: how the assistant is doing, the tickets it handed over,
// every conversation step by step, and the saved evaluation runs.
export function Dashboard({ person, onSignOut }: Props) {
  const [section, setSection] = useState<Section>('overview')
  const [openConversation, setOpenConversation] = useState<string | null>(null)
  // A ticket to open straight away in the Tickets section, with its reply box.
  const [ticketToOpen, setTicketToOpen] = useState<string | null>(null)

  function go(next: Section) {
    setSection(next)
    setOpenConversation(null)
    setTicketToOpen(null)
  }

  function showConversation(id: string) {
    setSection('conversations')
    setOpenConversation(id)
  }

  function showTicket(id: string) {
    setSection('tickets')
    setOpenConversation(null)
    setTicketToOpen(id)
  }

  return (
    <div className="admin">
      <aside className="ad-sidebar">
        <div className="ad-brand">
          <p className="wordmark">Juniper Lane Goods</p>
          <p className="ad-muted">{person.role === 'admin' ? 'Support admin' : 'Support team'}</p>
        </div>
        <nav aria-label="Admin sections">
          {SECTIONS.filter((s) => person.role === 'admin' || STAFF_SECTIONS.includes(s.id)).map((s) => (
            <button
              key={s.id}
              type="button"
              className={section === s.id ? 'ad-nav active' : 'ad-nav'}
              aria-current={section === s.id ? 'page' : undefined}
              onClick={() => go(s.id)}
            >
              {s.label}
            </button>
          ))}
        </nav>
        <p className="ad-me">
          Signed in as <strong>{person.name}</strong>
          {person.staff_id && <span className="ad-mono"> · {person.staff_id}</span>}
        </p>
        <button type="button" className="ad-signout" onClick={onSignOut}>
          Sign out
        </button>
      </aside>

      <main className="ad-main">
        <h1 className="visually-hidden">Support dashboard</h1>
        {section === 'overview' && <Overview onOpenTickets={() => go('tickets')} onOpenTicket={showTicket} />}
        {section === 'tickets' && (
          <Tickets key={ticketToOpen ?? 'list'} person={person} openFirst={ticketToOpen} onOpenConversation={showConversation} />
        )}
        {section === 'refunds' && <RefundRequests onOpenTicket={showTicket} />}
        {section === 'conversations' &&
          (openConversation ? (
            <ConversationReplay conversationId={openConversation} onBack={() => setOpenConversation(null)} onOpenTicket={showTicket} />
          ) : (
            <ConversationList onOpen={setOpenConversation} />
          ))}
        {section === 'evaluations' && <Evaluations />}
        {section === 'documents' && <Documents />}
        {section === 'orders' && <Orders />}
        {section === 'model' && <ModelSettings />}
      </main>
    </div>
  )
}
