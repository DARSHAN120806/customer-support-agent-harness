import { useEffect, useState, type FormEvent, type ReactNode } from 'react'
import {
  ApiError,
  dashboardApi,
  type ConnectionResult,
  type ModelForm,
  type ModelView,
} from '../../api'
import { dateTime, ms } from '../../format'

// Shortcuts that fill in a service's web address. Model names are left to the
// admin: each service has its own list.
const CHAT_PRESETS = [
  { label: 'Ollama', base_url: 'http://localhost:11434/v1', local: true },
  { label: 'LM Studio', base_url: 'http://localhost:1234/v1', local: true },
  { label: 'OpenAI', base_url: 'https://api.openai.com/v1', local: false },
  { label: 'OpenRouter', base_url: 'https://openrouter.ai/api/v1', local: false },
  { label: 'Groq', base_url: 'https://api.groq.com/openai/v1', local: false },
]
const SEARCH_PRESETS = [
  { label: 'Ollama', base_url: 'http://localhost:11434/v1' },
  { label: 'LM Studio', base_url: 'http://localhost:1234/v1' },
  { label: 'OpenAI', base_url: 'https://api.openai.com/v1' },
]
const MODEL_EXAMPLES: Record<string, string> = {
  bedrock: 'global.anthropic.claude-haiku-4-5-20251001-v1:0',
  anthropic: 'claude-haiku-4-5',
  openai_compatible: 'llama3.1 for Ollama, gpt-4o-mini for OpenAI',
}

function formFrom(view: ModelView): ModelForm {
  const { key_hint: _chatKey, ...chat } = view.chat
  const { key_hint: _searchKey, ...search } = view.search
  return { chat: { ...chat, api_key: '' }, search: { ...search, api_key: '' } }
}

// The admin's choice of AI model for the assistant, and of the model behind
// the document search. Keys are typed here but never shown again.
export function ModelSettings() {
  const [view, setView] = useState<ModelView | null>(null)
  const [form, setForm] = useState<ModelForm | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState<'test' | 'save' | 'reset' | null>(null)
  const [result, setResult] = useState<ConnectionResult | null>(null)
  const [notice, setNotice] = useState<string | null>(null)

  useEffect(() => {
    dashboardApi
      .model()
      .then((v) => {
        setView(v)
        setForm(formFrom(v))
      })
      .catch((e: ApiError) => setError(e.message))
  }, [])

  if (!form || !view) {
    return (
      <section aria-labelledby="model-title">
        <Head />
        {error ? <p className="ad-error" role="alert">{error}</p> : <p className="ad-muted">Loading…</p>}
      </section>
    )
  }

  const chat = form.chat
  const search = form.search
  const setChat = (change: Partial<ModelForm['chat']>) => setForm({ ...form, chat: { ...chat, ...change } })
  const setSearch = (change: Partial<ModelForm['search']>) => setForm({ ...form, search: { ...search, ...change } })
  const saved = formFrom(view)

  // Model names and addresses never carry over between services, so switching
  // service starts them empty, or brings back what is in use for that service.
  function switchChat(provider: ModelForm['chat']['provider']) {
    const inUse = saved.chat.provider === provider
    setChat({
      provider,
      model: inUse ? saved.chat.model : '',
      base_url: inUse ? saved.chat.base_url : '',
      api_key: '',
      ...(inUse ? { input_price: saved.chat.input_price, output_price: saved.chat.output_price } : {}),
    })
  }

  function switchSearch(provider: ModelForm['search']['provider']) {
    const inUse = saved.search.provider === provider
    setSearch({ provider, model: inUse ? saved.search.model : '', base_url: inUse ? saved.search.base_url : '', api_key: '' })
  }

  async function run(kind: 'test' | 'save' | 'reset', event?: FormEvent) {
    event?.preventDefault()
    setBusy(kind)
    setError(null)
    setNotice(null)
    if (kind !== 'test') setResult(null)
    try {
      if (kind === 'test') {
        setResult(await dashboardApi.testModel(form!))
      } else {
        const saved = kind === 'save' ? await dashboardApi.saveModel(form!) : await dashboardApi.resetModel()
        setView(saved)
        setForm(formFrom(saved))
        setNotice(
          kind === 'save'
            ? `Saved. New chats now use ${saved.chat.model}. Chats already open finish on the model they started with.`
            : 'Back to the settings in .env. New chats use them from now on.',
        )
      }
    } catch (e) {
      setError((e as ApiError).message)
    } finally {
      setBusy(null)
    }
  }

  return (
    <section aria-labelledby="model-title">
      <Head />

      <p className="ad-in-use">
        In use: <strong>{view.providers.chat[view.chat.provider]}</strong> · <span className="ad-mono">{view.chat.model}</span>
        <span className="ad-muted">
          {view.source === 'admin panel' && view.saved_at ? ` · saved here ${dateTime(view.saved_at)}` : ' · from the .env file'}
        </span>
      </p>

      <form className="ad-model-form" onSubmit={(e) => run('save', e)}>
        <fieldset className="ad-card">
          <legend>Chat model</legend>
          <p className="ad-muted ad-help">The model that reads the customer's message and writes the reply</p>

          <Choice
            label="Service"
            value={chat.provider}
            options={view.providers.chat}
            onChange={(provider) => switchChat(provider as ModelForm['chat']['provider'])}
          />

          {chat.provider === 'openai_compatible' && (
            <>
              <Presets
                presets={CHAT_PRESETS}
                onPick={(p) => setChat({ base_url: p.base_url, ...(p.local ? { input_price: 0, output_price: 0 } : {}) })}
              />
              <Field label="Web address" hint="Where the service answers, ending in /v1">
                <input value={chat.base_url ?? ''} onChange={(e) => setChat({ base_url: e.target.value })} placeholder="http://localhost:11434/v1" />
              </Field>
            </>
          )}

          {chat.provider === 'bedrock' ? (
            <>
              <Field label="AWS region" hint="Signs in with the AWS details in your .env file">
                <input value={chat.aws_region ?? ''} onChange={(e) => setChat({ aws_region: e.target.value })} placeholder="ap-southeast-2" />
              </Field>
            </>
          ) : (
            <KeyField
              value={chat.api_key}
              hint={view.chat.provider === chat.provider ? view.chat.key_hint : null}
              fallback={chat.provider === 'anthropic' ? 'Leave empty to use ANTHROPIC_API_KEY from .env' : 'Local models need no key'}
              onChange={(api_key) => setChat({ api_key })}
            />
          )}

          <Field label="Model name" hint={`For example ${MODEL_EXAMPLES[chat.provider]}`}>
            <input value={chat.model} onChange={(e) => setChat({ model: e.target.value })} required />
          </Field>

          <div className="ad-pair">
            <Field label="Price in, per million tokens (US$)">
              <input type="number" min="0" step="0.01" value={chat.input_price} onChange={(e) => setChat({ input_price: Number(e.target.value) })} />
            </Field>
            <Field label="Price out, per million tokens (US$)">
              <input type="number" min="0" step="0.01" value={chat.output_price} onChange={(e) => setChat({ output_price: Number(e.target.value) })} />
            </Field>
          </div>
          <p className="ad-muted ad-help">Used for the cost figures and the cost limit per chat. Use 0 for a local model</p>
        </fieldset>

        <fieldset className="ad-card">
          <legend>Search model</legend>
          <p className="ad-muted ad-help">
            The model that finds the right part of the shop documents. Changing it indexes the documents again when you save
          </p>

          <Choice
            label="Service"
            value={search.provider}
            options={view.providers.search}
            onChange={(provider) => switchSearch(provider as ModelForm['search']['provider'])}
          />

          {search.provider === 'openai_compatible' ? (
            <>
              <Presets presets={SEARCH_PRESETS} onPick={(p) => setSearch({ base_url: p.base_url })} />
              <Field label="Web address" hint="Where the service answers, ending in /v1">
                <input value={search.base_url ?? ''} onChange={(e) => setSearch({ base_url: e.target.value })} placeholder="http://localhost:11434/v1" />
              </Field>
              <KeyField
                value={search.api_key}
                hint={view.search.provider === search.provider ? view.search.key_hint : null}
                fallback="Local models need no key"
                onChange={(api_key) => setSearch({ api_key })}
              />
            </>
          ) : (
            <p className="ad-muted ad-help">Signs in with the AWS details in your .env file</p>
          )}

          <Field
            label="Model name"
            hint={search.provider === 'titan' ? 'For example amazon.titan-embed-text-v2:0' : 'For example nomic-embed-text for Ollama'}
          >
            <input value={search.model} onChange={(e) => setSearch({ model: e.target.value })} required />
          </Field>
        </fieldset>

        {error && <p className="ad-error" role="alert">{error}</p>}
        {notice && <p className="ad-notice" role="status">{notice}</p>}
        {result && <Results result={result} />}

        <div className="ad-actions">
          <button type="button" className="ad-button" disabled={busy !== null} onClick={() => run('test')}>
            {busy === 'test' ? 'Testing…' : 'Test connection'}
          </button>
          <button type="submit" className="ad-button primary" disabled={busy !== null}>
            {busy === 'save' ? 'Saving…' : 'Save and use for new chats'}
          </button>
          {view.source === 'admin panel' && (
            <button type="button" className="ad-link" disabled={busy !== null} onClick={() => run('reset')}>
              Go back to the .env settings
            </button>
          )}
        </div>
        <p className="ad-muted ad-help">
          The test sends two tiny requests to the chat model and one to the search model, a fraction of a cent on a paid
          service and free on a local one. Nothing changes until you save.
        </p>
      </form>
    </section>
  )
}

function Head() {
  return (
    <header className="ad-page-head">
      <h2 id="model-title">Model</h2>
      <p className="ad-muted">The AI model behind the assistant, and the one behind the document search</p>
    </header>
  )
}

function Field({ label, hint, children }: { label: string; hint?: string; children: ReactNode }) {
  return (
    <label className="ad-field">
      <span>{label}</span>
      {children}
      {hint && <span className="ad-muted ad-hint">{hint}</span>}
    </label>
  )
}

type ChoiceProps = { label: string; value: string; options: Record<string, string>; onChange: (value: string) => void }

function Choice({ label, value, options, onChange }: ChoiceProps) {
  return (
    <div className="ad-choice" role="radiogroup" aria-label={label}>
      {Object.entries(options).map(([id, name]) => (
        <button key={id} type="button" role="radio" aria-checked={value === id} className={value === id ? 'selected' : ''} onClick={() => onChange(id)}>
          {name}
        </button>
      ))}
    </div>
  )
}

function Presets<P extends { label: string }>({ presets, onPick }: { presets: P[]; onPick: (preset: P) => void }) {
  return (
    <div className="ad-presets">
      <span className="ad-muted">Fill in for</span>
      {presets.map((p) => (
        <button key={p.label} type="button" className="ad-link" onClick={() => onPick(p)}>
          {p.label}
        </button>
      ))}
    </div>
  )
}

type KeyProps = { value: string; hint: string | null; fallback: string; onChange: (value: string) => void }

// The key is never shown: the box starts empty, and an empty box on save
// keeps the key saved before.
function KeyField({ value, hint, fallback, onChange }: KeyProps) {
  return (
    <Field label="Key" hint={hint ? `A key ending ${hint.replace('…', '')} is saved. Leave empty to keep it` : fallback}>
      <input type="password" autoComplete="off" value={value} onChange={(e) => onChange(e.target.value)} placeholder={hint ? `Saved key ${hint}` : ''} />
    </Field>
  )
}

function Results({ result }: { result: ConnectionResult }) {
  const { chat, search } = result
  return (
    <div className="ad-card ad-results" role="status" aria-label="Connection test">
      <h3>Connection test</h3>
      <ul>
        <li className={chat.ok ? '' : 'bad'}>
          <span className="ad-results-label">Chat model</span>
          {chat.ok ? (
            <span>
              Replied in {ms(chat.ms)}: <span className="ad-mono">{chat.reply || '(no text)'}</span>
            </span>
          ) : (
            <span>{chat.error}</span>
          )}
        </li>
        {chat.ok && (
          <li className={chat.tools_ok ? '' : 'bad'}>
            <span className="ad-results-label">Can use tools</span>
            {chat.tools_ok ? (
              <span>Yes. It asked to look up an order when told to</span>
            ) : (
              <span>
                No. It did not ask for a tool, so it could not look up orders or search the documents. The safety checks
                would then hand most questions to a person. Try a larger model
              </span>
            )}
          </li>
        )}
        <li className={search.ok ? '' : 'bad'}>
          <span className="ad-results-label">Search model</span>
          {search.ok ? (
            <span>
              Answered in {ms(search.ms)} ({search.dimensions?.toLocaleString()} numbers per text)
            </span>
          ) : (
            <span>{search.error}</span>
          )}
        </li>
      </ul>
    </div>
  )
}
