import { useState } from 'react'
import { ConversationList, ConversationReplay } from './Conversations'
import { Evaluations } from './Evaluations'
import { Tickets } from './Tickets'

type Tab = 'tickets' | 'conversations' | 'evaluations'

const TABS: { id: Tab; label: string }[] = [
  { id: 'tickets', label: 'Tickets' },
  { id: 'conversations', label: 'Conversations' },
  { id: 'evaluations', label: 'Evaluations' },
]

type Props = {
  onBackToChat: () => void
}

// The support team's view: tickets to answer, chats to review, and how well
// the assistant scored in testing.
export function Dashboard({ onBackToChat }: Props) {
  const [tab, setTab] = useState<Tab>('tickets')
  const [openConversation, setOpenConversation] = useState<string | null>(null)

  function showConversation(id: string) {
    setTab('conversations')
    setOpenConversation(id)
  }

  return (
    <div className="dashboard">
      <header className="topbar glass">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">JL</span>
          <div>
            <h1>Support dashboard</h1>
            <p className="muted small">Juniper Lane Goods</p>
          </div>
        </div>
        <button className="secondary" onClick={onBackToChat}>
          Customer chat
        </button>
      </header>

      <p className="demo-note dash-note" role="note">
        <strong>Demo dashboard.</strong> It has no password, so it is for your own computer only.
        Customer emails are masked.
      </p>

      <nav className="tabs glass" aria-label="Dashboard sections">
        {TABS.map((t) => (
          <button
            key={t.id}
            className={tab === t.id ? 'tab active' : 'tab'}
            aria-current={tab === t.id ? 'page' : undefined}
            onClick={() => {
              setTab(t.id)
              setOpenConversation(null)
            }}
          >
            {t.label}
          </button>
        ))}
      </nav>

      <main className="dash-body glass">
        {tab === 'tickets' && <Tickets onOpenConversation={showConversation} />}
        {tab === 'conversations' &&
          (openConversation ? (
            <ConversationReplay conversationId={openConversation} onBack={() => setOpenConversation(null)} />
          ) : (
            <ConversationList onOpen={setOpenConversation} />
          ))}
        {tab === 'evaluations' && <Evaluations />}
      </main>
    </div>
  )
}
