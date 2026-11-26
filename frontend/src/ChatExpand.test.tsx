// The chat's "Expand" button: the chat can fill the whole page, and "Shrink"
// takes it back to the side panel. The choice is remembered for the tab.
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it } from 'vitest'
import type { Session } from './api'
import { SupportChat } from './components/support/SupportChat'

const SESSION: Session = {
  role: 'customer',
  session_id: 'session-abc',
  conversation_id: 'conv_aaaaaaaaaaaa',
  customer: { name: 'Priya Nair', email: 'priya.nair@example.com', order_count: 0 },
  orders: [],
  transcript: [],
  assistant_name: 'Juniper Lane Goods virtual assistant',
  handoff: null,
}

function openChat() {
  render(
    <SupportChat session={SESSION} open onOpenChange={() => {}} question={null} onTicketCreated={() => {}} onSessionExpired={() => {}} />,
  )
  return screen.getByRole('dialog', { name: 'Juniper Lane Goods virtual assistant' })
}

afterEach(() => {
  sessionStorage.clear()
  document.body.style.overflow = ''
})

describe('the chat window size', () => {
  it('opens as a side panel and expands to the whole page', async () => {
    const user = userEvent.setup()
    const chat = openChat()
    expect(chat).not.toHaveClass('expanded')

    await user.click(screen.getByRole('button', { name: 'Expand' }))

    expect(chat).toHaveClass('expanded')
    expect(chat).toHaveAttribute('aria-modal', 'true')
    expect(document.body.style.overflow).toBe('hidden') // the shop behind does not scroll
    expect(sessionStorage.getItem('juniper-lane-chat-expanded')).toBe('yes')

    await user.click(screen.getByRole('button', { name: 'Shrink' }))

    expect(chat).not.toHaveClass('expanded')
    expect(document.body.style.overflow).toBe('')
    expect(sessionStorage.getItem('juniper-lane-chat-expanded')).toBe('no')
  })

  it('remembers the full-page choice for the tab', () => {
    sessionStorage.setItem('juniper-lane-chat-expanded', 'yes')
    const chat = openChat()

    expect(chat).toHaveClass('expanded')
    expect(screen.getByRole('button', { name: 'Shrink' })).toBeInTheDocument()
  })
})
