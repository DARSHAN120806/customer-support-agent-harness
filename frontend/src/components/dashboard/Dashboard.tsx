import { useState } from 'react'
import { ConversationList, ConversationReplay } from './Conversations'
import { Evaluations } from './Evaluations'
import { Overview } from './Overview'
import { Tickets } from './Tickets'

type Section = 'overview' | 'tickets' | 'conversations' | 'evaluations'

const SECTIONS: { id: Section; label: string }[] = [
  { id: 'overview', label: 'Overview' },
  { id: 'tickets', label: 'Tickets' },
  { id: 'conversations', label: 'Conversations' },
  { id: 'evaluations', label: 'Evaluations' },
]

type Props = {
  onSignOut: () => void
}

// The admin panel: how the assistant is doing, the tickets it handed over,
// every conversation step by step, and the saved evaluation runs.
export function Dashboard({ onSignOut }: Props) {
  const [section, setSection] = useState<Section>('overview')
  const [openConversation, setOpenConversation] = useState<string | null>(null)

  function go(next: Section) {
    setSection(next)
    setOpenConversation(null)
  }

  function showConversation(id: string) {
    setSection('conversations')
    setOpenConversation(id)
  }

  return (
    <div className="admin">
      <aside className="ad-sidebar">
        <div className="ad-brand">
          <p className="wordmark">Juniper Lane Goods</p>
          <p className="ad-muted">Support admin</p>
        </div>
        <nav aria-label="Admin sections">
          {SECTIONS.map((s) => (
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
        <button type="button" className="ad-signout" onClick={onSignOut}>
          Sign out
        </button>
      </aside>

      <main className="ad-main">
        <h1 className="visually-hidden">Support dashboard</h1>
        {section === 'overview' && <Overview onOpenTickets={() => go('tickets')} onOpenConversation={showConversation} />}
        {section === 'tickets' && <Tickets onOpenConversation={showConversation} />}
        {section === 'conversations' &&
          (openConversation ? (
            <ConversationReplay conversationId={openConversation} onBack={() => setOpenConversation(null)} />
          ) : (
            <ConversationList onOpen={setOpenConversation} />
          ))}
        {section === 'evaluations' && <Evaluations />}
      </main>
    </div>
  )
}
