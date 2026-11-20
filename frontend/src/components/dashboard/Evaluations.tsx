import { useEffect, useMemo, useState } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { ApiError, dashboardApi, type EvaluationRun } from '../../api'
import { RULE_LABEL, money } from '../../format'

const GROUPS = ['easy', 'tricky', 'angry', 'refund', 'attack']
const VIOLATIONS = [
  'refund_claim',
  'other_customer_email',
  'identity_leak',
  'human_claim',
  'invented_figure',
  'forbidden_content',
  'missed_ticket',
]
const VIOLATION_LABEL: Record<string, string> = {
  refund_claim: 'Refund claim',
  other_customer_email: "Other customer's email",
  identity_leak: 'AI name',
  human_claim: 'Claimed human',
  invented_figure: 'Invented figure',
  forbidden_content: 'Forbidden content',
  missed_ticket: 'Missed ticket',
}
// Flat pastel colours, one per run. No gradients.
const COLOURS = ['#b9a9ff', '#9fdcbf', '#ffc4a8', '#a9d2ff', '#ffd98a', '#ffb3c0']

// The runs compared at first: the harness on/off comparison if it exists.
const DEFAULT_RUNS = ['haiku45_harness_on_counted', 'haiku45_harness_off_run1', 'haiku45_harness_off_run2']

// Legend names in dark text: the pastel bar colours are too light to read as text.
function legendText(value: string) {
  return <span style={{ color: '#2b2f3a' }}>{value}</span>
}

// Bars grow in with a short animation, unless the person's device asks for
// reduced motion (an accessibility setting), in which case they appear at once.
function prefersReducedMotion(): boolean {
  return typeof window.matchMedia === 'function' && window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

function label(run: EvaluationRun): string {
  return run.name.replace(/^haiku45_/, '').replace(/_/g, ' ')
}

export function Evaluations() {
  const [runs, setRuns] = useState<EvaluationRun[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [chosen, setChosen] = useState<string[]>([])
  const [animate] = useState(() => !prefersReducedMotion())

  useEffect(() => {
    dashboardApi
      .evaluations()
      .then((all) => {
        setRuns(all)
        const defaults = all.filter((r) => DEFAULT_RUNS.includes(r.name)).map((r) => r.name)
        setChosen(defaults.length ? defaults : all.map((r) => r.name))
      })
      .catch((e: ApiError) => setError(e.message))
  }, [])

  const compared = useMemo(() => (runs ?? []).filter((r) => chosen.includes(r.name)), [runs, chosen])

  // One row per group, one value per run: the share of cases passed, in percent.
  const passRows = GROUPS.map((group) => {
    const row: Record<string, string | number> = { group }
    for (const run of compared) {
      const c = run.summary.by_category[group]
      if (c && c.total) row[label(run)] = Math.round((c.passed / c.total) * 100)
    }
    return row
  })
  const counted = compared.filter((r) => r.summary.violations)
  const violationRows = VIOLATIONS.map((kind) => {
    const row: Record<string, string | number> = { kind: VIOLATION_LABEL[kind] ?? RULE_LABEL[kind] ?? kind }
    for (const run of counted) row[label(run)] = run.summary.violations?.[kind] ?? 0
    return row
  })

  function toggle(name: string) {
    setChosen((current) => (current.includes(name) ? current.filter((n) => n !== name) : [...current, name]))
  }

  if (error) return <p className="error" role="alert">{error}</p>
  if (!runs) return <p className="muted">Loading evaluation results…</p>
  if (runs.length === 0) return <p className="empty">No saved evaluation runs yet.</p>

  return (
    <section aria-label="Evaluations" className="dash-section">
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Compare</th>
              <th>Run</th>
              <th>Harness</th>
              <th>Passed</th>
              <th>Violations seen</th>
              <th>Cost</th>
              <th>Run at</th>
            </tr>
          </thead>
          <tbody>
            {runs.map((run) => (
              <tr key={run.name}>
                <td>
                  <input
                    type="checkbox"
                    aria-label={`Compare ${label(run)}`}
                    checked={chosen.includes(run.name)}
                    onChange={() => toggle(run.name)}
                  />
                </td>
                <td className="strong">{label(run)}</td>
                <td>
                  <span className={`tag ${run.harness === 'off' ? 'tag-warn' : ''}`}>{run.harness.toUpperCase()}</span>
                </td>
                <td className="nowrap">
                  {run.summary.passed} / {run.summary.total}
                </td>
                <td>{run.summary.violation_total ?? 'not counted'}</td>
                <td className="nowrap">{run.summary.cost_usd != null ? money(run.summary.cost_usd) : '—'}</td>
                <td className="nowrap">{(run.run_at ?? '').replace('T', ' ').slice(0, 16)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {compared.length === 0 ? (
        <p className="empty">Tick at least one run to compare.</p>
      ) : (
        <div className="charts">
          <figure className="chart-card">
            <figcaption>Cases passed per group (%)</figcaption>
            <div className="chart-box">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={passRows} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e4e0f0" />
                  <XAxis dataKey="group" tick={{ fill: '#565d6d', fontSize: 12 }} />
                  <YAxis domain={[0, 100]} tick={{ fill: '#565d6d', fontSize: 12 }} />
                  <Tooltip formatter={(value) => `${value}%`} />
                  <Legend formatter={legendText} />
                  {compared.map((run, i) => (
                    <Bar key={run.name} dataKey={label(run)} fill={COLOURS[i % COLOURS.length]} radius={[6, 6, 0, 0]}
                        isAnimationActive={animate} />
                  ))}
                </BarChart>
              </ResponsiveContainer>
            </div>
          </figure>

          <figure className="chart-card">
            <figcaption>Rule violations the customer would have seen</figcaption>
            {counted.length === 0 ? (
              <p className="empty">The chosen runs were saved before violations were counted.</p>
            ) : (
              <div className="chart-box">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={violationRows} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e4e0f0" />
                    <XAxis dataKey="kind" tick={{ fill: '#565d6d', fontSize: 11 }} interval={0} angle={-20} textAnchor="end" height={60} />
                    <YAxis allowDecimals={false} tick={{ fill: '#565d6d', fontSize: 12 }} />
                    <Tooltip />
                    <Legend formatter={legendText} />
                    {counted.map((run) => (
                      <Bar
                        key={run.name}
                        dataKey={label(run)}
                        fill={COLOURS[compared.indexOf(run) % COLOURS.length]}
                        radius={[6, 6, 0, 0]}
                        isAnimationActive={animate}
                      />
                    ))}
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </figure>
        </div>
      )}

      <p className="muted small">
        One run is a snapshot: the model's answers vary between runs, so small differences in cases
        passed are not meaningful on their own. Violation counts are the clearer signal.
      </p>
    </section>
  )
}
