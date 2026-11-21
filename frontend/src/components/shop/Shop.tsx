// The page a customer sees after signing in: the shop's products, a cart that
// can never check out, and their own orders and support tickets.
import { useCallback, useEffect, useMemo, useRef, useState, type MouseEvent } from 'react'
import { api, ApiError, type CustomerTicket, type Product, type Session } from '../../api'
import { YourOrders, YourTickets } from './Account'
import { useCart } from './cart'
import { CartPanel } from './CartPanel'
import { ProductCard } from './ProductCard'
import { SupportChat } from '../support/SupportChat'

type Props = {
  session: Session
  onSignOut: () => void
  onSessionExpired: () => void
}

const ALL = 'All'
// Whether the chat window is open is remembered for this tab, so a refresh
// does not close it.
const CHAT_OPEN_KEY = 'juniper-lane-chat-open'

export function Shop({ session, onSignOut, onSessionExpired }: Props) {
  const [products, setProducts] = useState<Product[] | null>(null)
  const [productsError, setProductsError] = useState<string | null>(null)
  const [tickets, setTickets] = useState<CustomerTicket[] | null>(null)
  const [ticketsError, setTicketsError] = useState<string | null>(null)
  const [category, setCategory] = useState(ALL)
  const [cartOpen, setCartOpen] = useState(false)
  const cart = useCart(session.customer.email)
  const [chatOpen, setChatOpenState] = useState(() => sessionStorage.getItem(CHAT_OPEN_KEY) === 'open')
  const [question, setQuestion] = useState<{ text: string; id: number } | null>(null)

  function setChatOpen(open: boolean) {
    sessionStorage.setItem(CHAT_OPEN_KEY, open ? 'open' : 'closed')
    setChatOpenState(open)
  }

  function askAbout(text: string) {
    setQuestion((current) => ({ text, id: (current?.id ?? 0) + 1 }))
    setChatOpen(true)
  }
  // The latest "session expired" handler, without re-running the loading below.
  const expiredRef = useRef(onSessionExpired)
  useEffect(() => {
    expiredRef.current = onSessionExpired
  })

  const loadTickets = useCallback(() => {
    api
      .myTickets(session.session_id)
      .then(setTickets)
      .catch((e: ApiError) => (e.status === 404 ? expiredRef.current() : setTicketsError(e.message)))
  }, [session.session_id])

  useEffect(() => {
    api
      .products()
      .then(setProducts)
      .catch((e: ApiError) => setProductsError(e.message))
    loadTickets()
  }, [loadTickets])

  const categories = useMemo(() => {
    const counts = new Map<string, number>()
    for (const p of products ?? []) counts.set(p.category, (counts.get(p.category) ?? 0) + 1)
    return [[ALL, products?.length ?? 0] as const, ...counts.entries()]
  }, [products])

  const shown = (products ?? []).filter((p) => category === ALL || p.category === category)
  const quantityOf = (id: string) => cart.lines.find((l) => l.id === id)?.quantity ?? 0

  return (
    <div className="shop">
      <header className="shop-bar">
        <p className="wordmark">Juniper Lane Goods</p>
        <nav className="shop-nav" aria-label="Page sections">
          <a href="#products" onClick={(e) => jump(e, 'products')}>Shop</a>
          <a href="#orders" onClick={(e) => jump(e, 'orders')}>Orders</a>
          <a href="#tickets" onClick={(e) => jump(e, 'tickets')}>Tickets</a>
        </nav>
        <div className="shop-actions">
          <button
            type="button"
            className={cart.count > 0 ? 'cart-button filled' : 'cart-button'}
            onClick={() => setCartOpen(true)}
            aria-label={`Cart, ${cart.count} item${cart.count === 1 ? '' : 's'}`}
          >
            Cart <span className="cart-count">{cart.count}</span>
          </button>
          <button type="button" className="text-button" onClick={onSignOut}>
            Sign out
          </button>
        </div>
      </header>

      <main className="shop-main">
        <section id="products" aria-labelledby="shop-title">
          <div className="shop-intro">
            <h1 id="shop-title">Homeware, furniture and electronics</h1>
            <p className="shop-lede">
              Chosen to be simple, durable and fairly priced. Prices are in Indian rupees and include GST
            </p>
          </div>

          <div className="filters" role="group" aria-label="Category">
            {categories.map(([name, count]) => (
              <button
                key={name}
                type="button"
                className={name === category ? 'filter selected' : 'filter'}
                aria-pressed={name === category}
                onClick={() => setCategory(name)}
              >
                {name} <span className="filter-count">{count}</span>
              </button>
            ))}
          </div>

          {productsError ? (
            <p className="empty" role="alert">{productsError}</p>
          ) : products == null ? (
            <p className="empty">Loading products…</p>
          ) : (
            <div className="product-grid">
              {shown.map((product) => (
                <ProductCard key={product.slug} product={product} quantityOf={quantityOf} onAdd={cart.add} />
              ))}
            </div>
          )}
        </section>

        <div className="account">
          <YourOrders orders={session.orders} onAsk={(id) => askAbout(`What's the status of my order ${id}?`)} />
          <YourTickets
            tickets={tickets}
            error={ticketsError}
            onReply={async (ticketId, text) => {
              const updated = await api.replyToTicket(session.session_id, ticketId, text)
              setTickets((current) => current?.map((t) => (t.ticket_id === ticketId ? updated : t)) ?? null)
            }}
          />
        </div>
      </main>

      <SupportChat
        session={session}
        open={chatOpen}
        onOpenChange={setChatOpen}
        question={question}
        onTicketCreated={loadTickets}
        onSessionExpired={onSessionExpired}
      />

      {cartOpen && (
        <CartPanel
          lines={cart.lines}
          subtotal={cart.subtotal}
          onQuantity={cart.setQuantity}
          onClose={() => setCartOpen(false)}
        />
      )}
    </div>
  )
}

// Scroll to a section without changing the address (the address picks the page).
function jump(event: MouseEvent, id: string) {
  event.preventDefault()
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
