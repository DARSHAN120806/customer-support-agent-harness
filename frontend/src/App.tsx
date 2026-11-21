import { useEffect, useState } from 'react'
import { ADMIN_TOKEN_KEY, api, dashboardApi, type PanelPerson, type Session, type SignInResult } from './api'
import { Dashboard } from './components/dashboard/Dashboard'
import { Shop } from './components/shop/Shop'
import { SignIn } from './components/SignIn'

// The chat's ID is kept for this browser tab only, so a page refresh does not
// lose the conversation, and closing the tab forgets it.
const STORAGE_KEY = 'juniper-lane-session'
// Who is signed in to the admin panel (role, name, staff ID), for this tab only.
const PANEL_PERSON_KEY = 'juniper-lane-admin-person'

function savedPerson(): PanelPerson | null {
  if (sessionStorage.getItem(ADMIN_TOKEN_KEY) === null) return null
  try {
    const saved = JSON.parse(sessionStorage.getItem(PANEL_PERSON_KEY) ?? 'null')
    return saved && typeof saved === 'object' ? saved : { role: 'admin', name: 'Admin', staff_id: '' }
  } catch {
    return { role: 'admin', name: 'Admin', staff_id: '' }
  }
}

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
  const [person, setPerson] = useState<PanelPerson | null>(savedPerson)
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
    if (result.role !== 'customer') {
      // The admin or a support person: the admin panel.
      const who: PanelPerson = { role: result.role, name: result.name ?? 'Admin', staff_id: result.staff_id ?? '' }
      sessionStorage.setItem(ADMIN_TOKEN_KEY, result.admin_token)
      sessionStorage.setItem(PANEL_PERSON_KEY, JSON.stringify(who))
      setPerson(who)
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
    sessionStorage.removeItem(PANEL_PERSON_KEY)
    setPerson(null)
    go('shop')
  }

  function expired() {
    sessionStorage.removeItem(STORAGE_KEY)
    setSession(null)
    setNotice('Your chat ended because it was idle for a while. Please sign in again.')
  }

  if (restoring) return <p className="loading">Loading…</p>

  if (page === 'dashboard' && person) {
    return <Dashboard person={person} onSignOut={adminSignOut} />
  }
  if (page === 'shop' && session) {
    return <Shop session={session} onSignOut={signOut} onSessionExpired={expired} />
  }
  return (
    <SignIn
      onSignedIn={signedIn}
      notice={notice ?? (page === 'dashboard' ? 'Sign in with an admin or support staff account to open the dashboard' : null)}
    />
  )
}
