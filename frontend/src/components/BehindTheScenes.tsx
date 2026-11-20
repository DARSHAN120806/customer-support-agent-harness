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
        <li className="ad-step">
          <span className="ad-step-title">
            {e.is_rewrite ? 'Model rewrote its reply' : 'Model thought'}
            <span className="ad-step-meta">{ms(e.duration_ms)}</span>
          </span>
          <span className="ad-step-body">
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
        <li className={e.is_error ? 'ad-step warn' : 'ad-step'}>
          <span className="ad-step-title">
            {TOOL_LABEL[String(e.tool)] ?? String(e.tool)}
            <span className="ad-step-meta">{ms(e.duration_ms)}</span>
          </span>
          {input && <code className="ad-code">{input}</code>}
          {e.is_error ? <span className="ad-step-body">The tool reported a problem</span> : null}
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
        <li className="ad-step check">
          <span className="ad-step-title">Check caught the draft, asked for a rewrite</span>
          <span className="ad-step-body">{rules(e.rules)}</span>
        </li>
      )
    case 'reply_blocked':
      return (
        <li className="ad-step block">
          <span className="ad-step-title">Check withheld the reply</span>
          <span className="ad-step-body">{rules(e.rules)}</span>
        </li>
      )
    case 'ticket_created':
      return (
        <li className="ad-step ticket">
          <span className="ad-step-title">Ticket {String(e.ticket_id)}</span>
          <span className="ad-step-body">
            Created by {e.created_by === 'harness' ? 'the harness (automatic)' : 'the assistant'} · {String(e.reason).replace(/_/g, ' ')}
          </span>
        </li>
      )
    case 'retry':
      return (
        <li className="ad-step warn">
          <span className="ad-step-title">Retried after a temporary failure</span>
          <span className="ad-step-body">
            {String(e.operation)} · attempt {String(e.attempt)} of {String(e.max_attempts)} · waited {ms(e.wait_ms)}
          </span>
        </li>
      )
    case 'error':
      return (
        <li className="ad-step block">
          <span className="ad-step-title">Failed: {String(e.operation)}</span>
          <span className="ad-step-body">{String(e.error_kind)}</span>
        </li>
      )
    default:
      return null
  }
}

type Props = {
  // Rebuilt from the log; null while the reply has no end line yet.
  details: ReplyDetails | null
  // How the reply ended, for example "completed".
  outcome: string | undefined
  replyNumber: number
}

// "Behind the scenes" for the admin: what the harness did to produce one reply.
// Customers never see this; it is shown in the conversation replay.
export function BehindTheScenes({ details, outcome, replyNumber }: Props) {
  return (
    <aside className="ad-insights" aria-label="Behind the scenes">
      <h2>Behind the scenes</h2>
      <p className="ad-muted">What the harness did for reply {replyNumber}</p>

      {!details ? (
        <p className="ad-empty">This reply has no end line in the log yet, so its details are not complete</p>
      ) : (
        <>
          <dl className="ad-facts">
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

          <p className={details.violations.length ? 'ad-checks fired' : 'ad-checks'}>
            {details.violations.length ? (
              <>
                <strong>Code checks fired:</strong> {rules(details.violations)}
              </>
            ) : (
              'All code checks passed'
            )}
          </p>

          <h3>Steps</h3>
          <ol className="ad-timeline">
            {details.events.map((event, i) => (
              <Step key={i} event={event} />
            ))}
          </ol>
        </>
      )}
    </aside>
  )
}
