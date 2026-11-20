import type { HarnessEvent } from './api'

type Turn = {
  number: number
  message: string
  steps: HarnessEvent[]
  end?: HarnessEvent
}

// Group the log lines into customer messages, each with its steps and reply.
export function groupTurns(events: HarnessEvent[]): { start?: HarnessEvent; turns: Turn[] } {
  const start = events.find((e) => e.event === 'conversation_start')
  const turns: Turn[] = []
  for (const event of events) {
    const number = Number(event.turn)
    if (event.event === 'turn_start') {
      turns.push({ number, message: String(event.message ?? ''), steps: [] })
      continue
    }
    const turn = turns.find((t) => t.number === number)
    if (!turn) continue
    if (event.event === 'turn_end') turn.end = event
    else turn.steps.push(event)
  }
  return { start, turns }
}
