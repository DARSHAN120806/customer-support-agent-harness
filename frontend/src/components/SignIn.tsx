import { useEffect, useState } from 'react'
import { api, ApiError, type Customer, type Session } from '../api'

type Props = {
  onSignedIn: (session: Session) => void
}

// Demo sign-in: pick any customer from the shop's data. In a real shop the
// customer would log in with a password, and the login would decide who they
// are. This is why the page must only ever run on your own computer.
export function SignIn({ onSignedIn }: Props) {
  const [query, setQuery] = useState('')
  const [customers, setCustomers] = useState<Customer[]>([])
  const [error, setError] = useState<string | null>(null)
  const [busyEmail, setBusyEmail] = useState<string | null>(null)

  // Search again shortly after the person stops typing.
  useEffect(() => {
    let cancelled = false
    const timer = setTimeout(() => {
      api
        .findCustomers(query)
        .then((found) => {
          if (!cancelled) {
            setCustomers(found)
            setError(null)
          }
        })
        .catch((e: ApiError) => !cancelled && setError(e.message))
    }, 250)
    return () => {
      cancelled = true
      clearTimeout(timer)
    }
  }, [query])

  async function choose(email: string) {
    setBusyEmail(email)
    setError(null)
    try {
      onSignedIn(await api.signIn(email))
    } catch (e) {
      setError((e as ApiError).message)
      setBusyEmail(null)
    }
  }

  return (
    <main className="signin">
      <div className="signin-card glass">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">JL</span>
          <div>
            <h1>Juniper Lane Goods</h1>
            <p className="muted">Customer support</p>
          </div>
        </div>

        <p className="demo-note" role="note">
          <strong>Demo sign-in.</strong> Choose a customer to chat as. A real shop would ask
          for a password; this page is for your own computer only.
        </p>

        <label htmlFor="customer-search">Find a customer by name or email</label>
        <input
          id="customer-search"
          type="search"
          placeholder="e.g. Priya"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          autoFocus
        />

        {error && <p className="error" role="alert">{error}</p>}

        <ul className="customer-list" aria-label="Customers">
          {customers.map((c) => (
            <li key={c.email}>
              <button onClick={() => choose(c.email)} disabled={busyEmail !== null}>
                <span className="customer-name">{c.name}</span>
                <span className="muted">{c.email}</span>
                <span className="pill">
                  {busyEmail === c.email ? 'Signing in…' : `${c.order_count} order${c.order_count === 1 ? '' : 's'}`}
                </span>
              </button>
            </li>
          ))}
          {!error && customers.length === 0 && query && <li className="muted">No customers match.</li>}
        </ul>
      </div>
    </main>
  )
}
