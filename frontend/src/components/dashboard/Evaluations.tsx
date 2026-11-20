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
import { RULE_LABEL, dateTime, money } from '../../format'
import { CHART, prefersReducedMotion } from './chart'

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
// The first run compared gets the accent; the others neutral steps, so one leads.
const COLOURS = [CHART.accent, ...CHART.steps]

// The runs compared at first: the harness on/off comparison if it exists.
const DEFAULT_RUNS = ['haiku45_harness_on_counted', 'haiku45_harness_off_run1', 'haiku45_harness_off_run2']

// Legend names in the secondary text colour.
function legendText(value: string) {
  return <span style={{ color: '#5e554a', fontSize: 13 }}>{value}</span>
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

  // Runs with the harness on come first, so the one that matters gets the accent.
  const compared = useMemo(
    () =>
      (runs ?? [])
        .filter((r) => chosen.includes(r.name))
        .sort((a, b) => Number(a.harness === 'off') - Number(b.harness === 'off')),
    [runs, chosen],
  )

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

  function toggle(name: string) {
    setChosen((current) => (current.includes(name) ? current.filter((n) => n !== name) : [...current, name]))
  }

  const head = (
    <header className="ad-page-head">
      <h2>Evaluations</h2>
      <p className="ad-muted">Saved test runs of the assistant, with and without the harness</p>
    </header>
  )
  if (error) return <section aria-label="Evaluations">{head}<p className="ad-error" role="alert">{error}</p></section>
  if (!runs) return <section aria-label="Evaluations">{head}<p className="ad-muted">Loading evaluation results…</p></section>
  if (runs.length === 0) return <section aria-label="Evaluations">{head}<p className="ad-empty">No saved evaluation runs yet</p></section>

  return (
    <section aria-label="Evaluations">
      {head}
      <div className="ad-table-wrap">
        <table className="ad-table" aria-label="Saved runs">
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
                <td>{label(run)}</td>
                <td>{run.harness === 'off' ? <span className="ad-flag">Off</span> : 'On'}</td>
                <td className="nowrap ad-mono">
                  {run.summary.passed} / {run.summary.total}
                </td>
                <td>{run.summary.violation_total ?? 'not counted'}</td>
                <td className="nowrap ad-mono">{run.summary.cost_usd != null ? money(run.summary.cost_usd) : '—'}</td>
                <td className="nowrap ad-muted">{run.run_at ? dateTime(run.run_at) : '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {compared.length === 0 ? (
        <p className="ad-empty">Tick at least one run to compare</p>
      ) : (
        <div className="ad-stack">
          <figure className="ad-card">
            <figcaption>Cases passed per group (%)</figcaption>
            <div className="ad-chart-box">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={passRows} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
                  <CartesianGrid vertical={false} stroke={CHART.grid} />
                  <XAxis dataKey="group" tick={CHART.tick} tickLine={false} axisLine={{ stroke: CHART.grid }} />
                  <YAxis domain={[0, 100]} tick={CHART.tick} tickLine={false} axisLine={false} />
                  <Tooltip formatter={(value) => `${value}%`} cursor={{ fill: CHART.cursor }} contentStyle={CHART.tooltip} />
                  <Legend formatter={legendText} />
                  {compared.map((run, i) => (
                    <Bar key={run.name} dataKey={label(run)} fill={COLOURS[i % COLOURS.length]} radius={[4, 4, 0, 0]}
                        isAnimationActive={animate} />
                  ))}
                </BarChart>
              </ResponsiveContainer>
            </div>
          </figure>

          {/* A short table, not a second chart: one main chart per screen. */}
          <figure className="ad-card">
            <figcaption>Rule violations the customer would have seen</figcaption>
            {counted.length === 0 ? (
              <p className="ad-empty">The chosen runs were saved before violations were counted</p>
            ) : (
              <table className="ad-table ad-compact" aria-label="Violations per run">
                <thead>
                  <tr>
                    <th>Kind</th>
                    {counted.map((run) => (
                      <th key={run.name} className="num">
                        {label(run)}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {VIOLATIONS.map((kind) => (
                    <tr key={kind}>
                      <td>{VIOLATION_LABEL[kind] ?? RULE_LABEL[kind] ?? kind}</td>
                      {counted.map((run) => {
                        const n = run.summary.violations?.[kind] ?? 0
                        return (
                          <td key={run.name} className={n ? 'num ad-mono' : 'num ad-mono ad-muted'}>
                            {n}
                          </td>
                        )
                      })}
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr>
                    <td>Total</td>
                    {counted.map((run) => (
                      <td key={run.name} className="num ad-mono">
                        {run.summary.violation_total ?? 0}
                      </td>
                    ))}
                  </tr>
                </tfoot>
              </table>
            )}
          </figure>
        </div>
      )}

      <p className="ad-muted ad-note">
        One run is a snapshot: the model's answers vary between runs, so small differences in cases
        passed are not meaningful on their own. Violation counts are the clearer signal.
      </p>
    </section>
  )
}
