import { useEffect, useState } from 'react'
import { api, type Session } from './api'
import { Chat } from './components/Chat'
import { SignIn } from './components/SignIn'

// The chat's ID is kept for this browser tab only, so a page refresh does not
// lose the conversation, and closing the tab forgets it.
const STORAGE_KEY = 'juniper-lane-session'

// Flat pastel shapes behind the glass panels. Purely decorative.
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

export default function App() {
  return (
    <>
      <Backdrop />
      <Screen />
    </>
  )
}

function Screen() {
  const [session, setSession] = useState<Session | null>(null)
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

  function signedIn(newSession: Session) {
    sessionStorage.setItem(STORAGE_KEY, newSession.session_id)
    setNotice(null)
    setSession(newSession)
  }

  function signOut() {
    if (session) api.signOut(session.session_id).catch(() => undefined)
    sessionStorage.removeItem(STORAGE_KEY)
    setSession(null)
  }

  function expired() {
    sessionStorage.removeItem(STORAGE_KEY)
    setSession(null)
    setNotice('Your chat ended because it was idle for a while. Please sign in again.')
  }

  if (restoring) return <p className="loading">Loading…</p>
  if (!session) {
    return (
      <>
        {notice && <p className="notice" role="status">{notice}</p>}
        <SignIn onSignedIn={signedIn} />
      </>
    )
  }
  return <Chat session={session} onSignOut={signOut} onSessionExpired={expired} />
}
