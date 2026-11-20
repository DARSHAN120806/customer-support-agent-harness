import { useState, type FormEvent } from 'react'
import { api, ApiError, type SignInResult } from '../api'
import { PackingSlip } from './PackingSlip'

type Props = {
  onSignedIn: (result: SignInResult) => void
  // A short message above the form, like "your chat ended".
  notice?: string | null
}

// Sign-in for customers and for the shop's admin. The server decides which one
// an account is: customers go to their chat, the admin to the dashboard.
export function SignIn({ onSignedIn, notice }: Props) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  async function submit(event: FormEvent) {
    event.preventDefault()
    setBusy(true)
    setError(null)
    try {
      onSignedIn(await api.signIn(email.trim(), password))
    } catch (e) {
      setError((e as ApiError).message)
      setBusy(false)
    }
  }

  return (
    <main className="auth">
      <section className="auth-form-side">
        <p className="wordmark">Juniper Lane Goods</p>

        <div className="auth-form-block">
          <h1>Sign in to see your orders and get help</h1>
          <p className="auth-lede">Use the email address from your orders</p>

          {notice && (
            <p className="auth-notice" role="status">
              {notice}
            </p>
          )}

          <form className="auth-form" onSubmit={submit} noValidate>
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoFocus
            />

            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            {error && (
              <p className="auth-error" role="alert">
                {error}
              </p>
            )}

            <button type="submit" className="auth-submit" disabled={busy || !email.trim() || !password}>
              {busy ? 'Signing in…' : 'Sign in'}
            </button>
          </form>
        </div>
      </section>

      <section className="auth-visual-side" aria-hidden="true">
        <PackingSlip />
      </section>
    </main>
  )
}
