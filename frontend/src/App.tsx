import { useEffect, useState } from 'react'
import { ADMIN_TOKEN_KEY, api, dashboardApi, type Session, type SignInResult } from './api'
import { Chat } from './components/Chat'
import { Dashboard } from './components/dashboard/Dashboard'
import { SignIn } from './components/SignIn'

// The chat's ID is kept for this browser tab only, so a page refresh does not
// lose the conversation, and closing the tab forgets it.
const STORAGE_KEY = 'juniper-lane-session'

// Flat pastel shapes behind the glass panels of the chat and the dashboard.
// The sign-in page already has the new design; the other pages follow later.
function Backdrop() {
  return (
    <div className="backdrop" aria-hidden="true">
      <span className="shape-1" />
      <span className="shape-2" />
      <span className="shape-3" />
      <span className="shape-4" />
    </div>
  )
}

type Page = 'chat' | 'dashboard'

// The page shown depends on the address: "#/dashboard" is the admin's
// dashboard, anything else is the customer side. Back and forward work.
function usePage(): [Page, (page: Page) => void] {
  const read = (): Page => (window.location.hash === '#/dashboard' ? 'dashboard' : 'chat')
  const [page, setPage] = useState<Page>(read)
  useEffect(() => {
    const onChange = () => setPage(read())
    window.addEventListener('hashchange', onChange)
    return () => window.removeEventListener('hashchange', onChange)
  }, [])
  const go = (next: Page) => {
    window.location.hash = next === 'dashboard' ? '#/dashboard' : '#/'
    setPage(next)
  }
  return [page, go]
}

export default function App() {
  const [page, go] = usePage()
  const [session, setSession] = useState<Session | null>(null)
  const [isAdmin, setIsAdmin] = useState(() => sessionStorage.getItem(ADMIN_TOKEN_KEY) !== null)
  const [restoring, setRestoring] = useState(() => sessionStorage.getItem(STORAGE_KEY) !== null)
  const [notice, setNotice] = useState<string | null>(null)

  // After a refresh, pick the chat up where it was.
  useEffect(() => {
    const saved = sessionStorage.getItem(STORAGE_KEY)
    if (!saved) return
    api
      .getSession(saved)
      .then(setSession)
      .catch(() => sessionStorage.removeItem(STORAGE_KEY))
      .finally(() => setRestoring(false))
  }, [])

  function signedIn(result: SignInResult) {
    setNotice(null)
    if (result.role === 'admin') {
      sessionStorage.setItem(ADMIN_TOKEN_KEY, result.admin_token)
      setIsAdmin(true)
      go('dashboard')
      return
    }
    sessionStorage.setItem(STORAGE_KEY, result.session_id)
    setSession(result)
    go('chat')
  }

  function signOut() {
    if (session) api.signOut(session.session_id).catch(() => undefined)
    sessionStorage.removeItem(STORAGE_KEY)
    setSession(null)
  }

  function adminSignOut() {
    dashboardApi.signOut().catch(() => undefined)
    sessionStorage.removeItem(ADMIN_TOKEN_KEY)
    setIsAdmin(false)
    go('chat')
  }

  function expired() {
    sessionStorage.removeItem(STORAGE_KEY)
    setSession(null)
    setNotice('Your chat ended because it was idle for a while. Please sign in again')
  }

  if (restoring) return <p className="loading">Loading…</p>

  if (page === 'dashboard' && isAdmin) {
    return (
      <>
        <Backdrop />
        <Dashboard onSignOut={adminSignOut} />
      </>
    )
  }
  if (page === 'chat' && session) {
    return (
      <>
        <Backdrop />
        <Chat session={session} onSignOut={signOut} onSessionExpired={expired} />
      </>
    )
  }
  return (
    <SignIn
      onSignedIn={signedIn}
      notice={notice ?? (page === 'dashboard' ? 'Sign in with the admin account to open the dashboard' : null)}
    />
  )
}
