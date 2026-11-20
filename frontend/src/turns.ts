import type { HarnessEvent, ReplyDetails } from './api'

export type Turn = {
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

// The "behind the scenes" details of one reply, rebuilt from its log lines.
// Null while the reply has no end line yet (it is still being written, or the
// server stopped before it finished).
export function detailsOf(turn: Turn): ReplyDetails | null {
  const end = turn.end
  if (!end) return null
  const list = (value: unknown) => (Array.isArray(value) ? value.map(String) : [])
  return {
    turn: turn.number,
    steps: Number(end.steps ?? 0),
    tools_used: list(end.tools_used),
    escalated: Boolean(end.escalated),
    violations: list(end.violations),
    gave_up_because: end.gave_up_because == null ? null : String(end.gave_up_because),
    input_tokens: Number(end.input_tokens ?? 0),
    output_tokens: Number(end.output_tokens ?? 0),
    cost_usd: end.cost_usd == null ? null : Number(end.cost_usd),
    duration_ms: Number(end.duration_ms ?? 0),
    events: turn.steps,
  }
}
