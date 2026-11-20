import type { HarnessEvent, ReplyDetails } from '../api'
import { OUTCOME_LABEL, RULE_LABEL, money, ms } from '../format'

// "Behind the scenes": what the harness did to produce one reply. Every value
// comes from the agent's event log, which has personal data masked already.

const TOOL_LABEL: Record<string, string> = {
  search_knowledge_base: 'Searched the shop documents',
  lookup_order: 'Looked up an order',
  calculate_date: 'Calculated a date',
  escalate_to_human: 'Handed over to a person',
}

function rules(value: unknown): string {
  return Array.isArray(value) ? value.map((r) => RULE_LABEL[String(r)] ?? String(r)).join(', ') : ''
}

// One line of the timeline, chosen by the kind of event.
export function Step({ event }: { event: HarnessEvent }) {
  const e = event
  switch (e.event) {
    case 'model_call': {
      const tools = (e.tools_requested as string[] | undefined) ?? []
      return (
        <li className="step step-model">
          <span className="step-title">
            {e.is_rewrite ? 'Model rewrote its reply' : 'Model thought'}
            <span className="step-meta">{ms(e.duration_ms)}</span>
          </span>
          <span className="step-body">
            {tools.length ? `Asked for: ${tools.map((t) => TOOL_LABEL[t] ?? t).join(', ')}` : 'Wrote a reply'}
            {' · '}
            {Number(e.input_tokens).toLocaleString()} in / {Number(e.output_tokens).toLocaleString()} out
          </span>
        </li>
      )
    }
    case 'tool_call': {
      const input = e.input && typeof e.input === 'object' ? JSON.stringify(e.input) : ''
      return (
        <li className={`step step-tool${e.is_error ? ' step-warn' : ''}`}>
          <span className="step-title">
            {TOOL_LABEL[String(e.tool)] ?? String(e.tool)}
            <span className="step-meta">{ms(e.duration_ms)}</span>
          </span>
          {input && <code className="step-code">{input}</code>}
          {e.is_error ? <span className="step-body">The tool reported a problem.</span> : null}
          {typeof e.result_preview === 'string' && e.result_preview && (
            <details>
              <summary>What the tool returned</summary>
              <pre>{e.result_preview}</pre>
            </details>
          )}
        </li>
      )
    }
    case 'reply_rewrite':
      return (
        <li className="step step-check">
          <span className="step-title">Check caught the draft, asked for a rewrite</span>
          <span className="step-body">{rules(e.rules)}</span>
        </li>
      )
    case 'reply_blocked':
      return (
        <li className="step step-block">
          <span className="step-title">Check withheld the reply</span>
          <span className="step-body">{rules(e.rules)}</span>
        </li>
      )
    case 'ticket_created':
      return (
        <li className="step step-ticket">
          <span className="step-title">Ticket {String(e.ticket_id)}</span>
          <span className="step-body">
            Created by {e.created_by === 'harness' ? 'the harness (automatic)' : 'the assistant'} · {String(e.reason).replace(/_/g, ' ')}
          </span>
        </li>
      )
    case 'retry':
      return (
        <li className="step step-warn">
          <span className="step-title">Retried after a temporary failure</span>
          <span className="step-body">
            {String(e.operation)} · attempt {String(e.attempt)} of {String(e.max_attempts)} · waited {ms(e.wait_ms)}
          </span>
        </li>
      )
    case 'error':
      return (
        <li className="step step-block">
          <span className="step-title">Failed: {String(e.operation)}</span>
          <span className="step-body">{String(e.error_kind)}</span>
        </li>
      )
    default:
      return null
  }
}

type Props = {
  details: ReplyDetails | null | undefined
  // How the reply ended, as reported by the API (for example "completed").
  outcome: string | undefined
  conversationId: string
  replyNumber: number | null
  onClose: () => void
}

export function BehindTheScenes({ details, outcome, conversationId, replyNumber, onClose }: Props) {
  return (
    <aside className="insights glass" aria-label="Behind the scenes">
      <div className="insights-head">
        <h2>Behind the scenes</h2>
        <button className="secondary small-button" onClick={onClose} aria-label="Hide behind the scenes">
          Hide
        </button>
      </div>
      <p className="muted small">
        What the harness did for {replyNumber ? `reply ${replyNumber}` : 'a reply'}. Conversation{' '}
        <code>{conversationId}</code>
      </p>

      {!details ? (
        <p className="insights-empty">
          {replyNumber
            ? 'Details are only kept for replies sent during this visit to the page.'
            : 'Send a message to see each step here: the tools used, the checks run, and the cost.'}
        </p>
      ) : (
        <>
          <dl className="stats">
            <div>
              <dt>Result</dt>
              <dd>{OUTCOME_LABEL[outcome ?? ''] ?? outcome ?? '—'}</dd>
            </div>
            <div>
              <dt>Model calls</dt>
              <dd>{details.steps}</dd>
            </div>
            <div>
              <dt>Tokens</dt>
              <dd>
                {details.input_tokens.toLocaleString()} in · {details.output_tokens.toLocaleString()} out
              </dd>
            </div>
            <div>
              <dt>Cost</dt>
              <dd>{money(details.cost_usd)}</dd>
            </div>
            <div>
              <dt>Time</dt>
              <dd>{ms(details.duration_ms)}</dd>
            </div>
            <div>
              <dt>Handed to a person</dt>
              <dd>{details.escalated ? 'Yes' : 'No'}</dd>
            </div>
          </dl>

          <div className={`checks ${details.violations.length ? 'checks-fired' : 'checks-clear'}`}>
            {details.violations.length ? (
              <>
                <strong>Code checks fired:</strong> {rules(details.violations)}
              </>
            ) : (
              <>All code checks passed.</>
            )}
          </div>

          <h3>Steps</h3>
          <ol className="timeline">
            {details.events.map((event, i) => (
              <Step key={i} event={event} />
            ))}
          </ol>
        </>
      )}
    </aside>
  )
}
