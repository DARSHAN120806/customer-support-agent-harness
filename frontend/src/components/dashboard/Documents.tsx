import { useEffect, useState } from 'react'
import { ApiError, dashboardApi, type DocumentDetail, type DocumentSummary } from '../../api'
import { dateTime } from '../../format'

// Sections longer than this are pointed out (see documents.py on the server).
const SECTION_WARN_CHARS = 4000

// The shop documents: what the assistant answers from, and the products and
// stock on the shop page. Every save is checked, kept for undo, and the
// search is rebuilt from the new text.
export function Documents() {
  const [list, setList] = useState<DocumentSummary[] | null>(null)
  const [doc, setDoc] = useState<DocumentDetail | null>(null)
  const [draft, setDraft] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [warnings, setWarnings] = useState<string[]>([])
  const [notice, setNotice] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [earlier, setEarlier] = useState<{ id: string; saved_at: string; text: string } | null>(null)

  const changed = doc !== null && draft !== doc.text

  useEffect(() => {
    dashboardApi
      .documents()
      .then((docs) => {
        setList(docs)
        if (docs[0]) open(docs[0].name)
      })
      .catch((e: ApiError) => setError(e.message))
    // `open` only uses state setters, so it is safe to leave out here.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  function reset() {
    setError(null)
    setWarnings([])
    setNotice(null)
    setEarlier(null)
  }

  async function open(name: string) {
    if (changed && !window.confirm('You have changes that are not saved. Leave them?')) return
    reset()
    try {
      const loaded = await dashboardApi.document(name)
      setDoc(loaded)
      setDraft(loaded.text)
    } catch (e) {
      setError((e as ApiError).message)
    }
  }

  async function finish(work: Promise<{ document: DocumentDetail; warnings: string[] }>, done: string) {
    setBusy(true)
    reset()
    try {
      const { document, warnings: found } = await work
      setDoc(document)
      setDraft(document.text)
      setWarnings(found)
      setNotice(done)
      setList((current) =>
        current?.map((d) => (d.name === document.name ? { ...d, updated_at: document.updated_at, sections: document.sections.length } : d)) ?? null,
      )
    } catch (e) {
      setError((e as ApiError).message)
    } finally {
      setBusy(false)
    }
  }

  async function view(id: string, savedAt: string) {
    if (!doc) return
    try {
      const { text } = await dashboardApi.documentVersion(doc.name, id)
      setEarlier({ id, saved_at: savedAt, text })
    } catch (e) {
      setError((e as ApiError).message)
    }
  }

  return (
    <section aria-labelledby="documents-title">
      <header className="ad-page-head">
        <h2 id="documents-title">Documents</h2>
        <p className="ad-muted">
          What the assistant answers from, and the products and stock on the shop page. New chats use a saved change
          straight away; chats already open keep the old text.
        </p>
      </header>

      {error && <p className="ad-error ad-lines" role="alert">{error}</p>}

      {list && (
        <div className="ad-docs">
          <nav className="ad-doc-list" aria-label="Documents">
            {list.map((d) => (
              <button
                key={d.name}
                type="button"
                className={doc?.name === d.name ? 'ad-doc active' : 'ad-doc'}
                aria-current={doc?.name === d.name ? 'true' : undefined}
                onClick={() => open(d.name)}
              >
                <span>{d.title}</span>
                <span className="ad-muted ad-mono">{d.name}</span>
              </button>
            ))}
          </nav>

          {doc && (
            <div className="ad-doc-main">
              <div className="ad-card ad-editor">
                <div className="ad-card-head">
                  <h3>{doc.title}</h3>
                  <span className="ad-muted">Saved {dateTime(doc.updated_at)}</span>
                </div>
                <label htmlFor="doc-text" className="visually-hidden">
                  Text of {doc.title}
                </label>
                <textarea id="doc-text" spellCheck value={draft} onChange={(e) => setDraft(e.target.value)} />
                <div className="ad-actions">
                  <button type="button" className="ad-button primary" disabled={!changed || busy} onClick={() => finish(dashboardApi.saveDocument(doc.name, draft, doc.version), 'Saved. The search now uses the new text.')}>
                    {busy ? 'Saving…' : 'Save'}
                  </button>
                  {changed && (
                    <button type="button" className="ad-link" disabled={busy} onClick={() => setDraft(doc.text)}>
                      Discard changes
                    </button>
                  )}
                  {changed && <span className="ad-muted">Unsaved changes</span>}
                </div>
                {notice && <p className="ad-notice" role="status">{notice}</p>}
                {warnings.length > 0 && (
                  <ul className="ad-warnings" aria-label="Warnings">
                    {warnings.map((w) => (
                      <li key={w}>{w}</li>
                    ))}
                  </ul>
                )}
              </div>

              <div className="ad-doc-side">
                <section className="ad-card" aria-label="Sections">
                  <h3>Sections</h3>
                  <p className="ad-muted ad-help">Each "## " heading starts a section the search can find</p>
                  <ul className="ad-outline">
                    {doc.sections.map((s) => (
                      <li key={s.heading}>
                        <span>
                          {s.heading}
                          {doc.protected.includes(s.heading) && <span className="ad-flag">kept in step with order data</span>}
                        </span>
                        <span className={s.chars > SECTION_WARN_CHARS ? 'ad-mono ad-long' : 'ad-mono ad-muted'}>{s.chars.toLocaleString()}</span>
                      </li>
                    ))}
                  </ul>
                </section>

                <section className="ad-card" aria-label="Earlier versions">
                  <h3>Earlier versions</h3>
                  {doc.history.length === 0 ? (
                    <p className="ad-empty">No earlier versions yet. Each save keeps the text from before it</p>
                  ) : (
                    <ul className="ad-outline">
                      {doc.history.slice(0, 10).map((h) => (
                        <li key={h.id}>
                          <span>{dateTime(h.saved_at)}</span>
                          <button type="button" className="ad-link" onClick={() => view(h.id, h.saved_at)}>
                            View
                          </button>
                        </li>
                      ))}
                    </ul>
                  )}
                </section>
              </div>

              {earlier && (
                <section className="ad-card ad-earlier" aria-label="Earlier version">
                  <div className="ad-card-head">
                    <h3>Version from {dateTime(earlier.saved_at)}</h3>
                    <button type="button" className="ad-link" onClick={() => setEarlier(null)}>
                      Close
                    </button>
                  </div>
                  <pre>{earlier.text}</pre>
                  <div className="ad-actions">
                    <button
                      type="button"
                      className="ad-button"
                      disabled={busy}
                      onClick={() => finish(dashboardApi.restoreDocument(doc.name, earlier.id, doc.version), 'Restored. The search now uses this version, and the text before it was kept too.')}
                    >
                      Restore this version
                    </button>
                  </div>
                </section>
              )}
            </div>
          )}
        </div>
      )}
      {!list && !error && <p className="ad-muted">Loading…</p>}
    </section>
  )
}
