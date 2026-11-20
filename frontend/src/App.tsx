import { useEffect, useState } from 'react'
import { ADMIN_TOKEN_KEY, api, dashboardApi, type Session, type SignInResult } from './api'
import { Dashboard } from './components/dashboard/Dashboard'
import { Shop } from './components/shop/Shop'
import { SignIn } from './components/SignIn'

// The chat's ID is kept for this browser tab only, so a page refresh does not
// lose the conversation, and closing the tab forgets it.
const STORAGE_KEY = 'juniper-lane-session'

type Page = 'shop' | 'dashboard'

const ADDRESS: Record<Page, string> = { shop: '#/', dashboard: '#/dashboard' }

// The page shown depends on the address: "#/dashboard" is the admin's
// dashboard, anything else the shop (with its chat window). Back and forward work.
function usePage(): [Page, (page: Page) => void] {
  const read = (): Page => (window.location.hash === '#/dashboard' ? 'dashboard' : 'shop')
  const [page, setPage] = useState<Page>(read)
  useEffect(() => {
    const onChange = () => setPage(read())
    window.addEventListener('hashchange', onChange)
    return () => window.removeEventListener('hashchange', onChange)
  }, [])
  const go = (next: Page) => {
    window.location.hash = ADDRESS[next]
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
    go('shop')
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
    go('shop')
  }

  function expired() {
    sessionStorage.removeItem(STORAGE_KEY)
    setSession(null)
    setNotice('Your chat ended because it was idle for a while. Please sign in again')
  }

  if (restoring) return <p className="loading">Loading…</p>

  if (page === 'dashboard' && isAdmin) {
    return <Dashboard onSignOut={adminSignOut} />
  }
  if (page === 'shop' && session) {
    return <Shop session={session} onSignOut={signOut} onSessionExpired={expired} />
  }
  return (
    <SignIn
      onSignedIn={signedIn}
      notice={notice ?? (page === 'dashboard' ? 'Sign in with the admin account to open the dashboard' : null)}
    />
  )
}
