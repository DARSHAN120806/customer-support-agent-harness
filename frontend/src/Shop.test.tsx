// Tests for the shop page customers see after signing in. The API is a fake,
// so no server is needed.
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import App from './App'
import type { CustomerTicket, Product, Session } from './api'
import { DRAWN_PRODUCTS } from './components/shop/drawings'

const SESSION: Session = {
  role: 'customer',
  session_id: 'session-abc',
  conversation_id: 'conv_000000000001',
  customer: { name: 'Priya Nair', email: 'priya.nair@example.com', order_count: 2 },
  orders: [
    { order_id: 'JL-10198', placed_on: '2026-09-14', status: 'delivered', total: 44.98, items: ['Bluetooth Speaker Mini'] },
    { order_id: 'JL-10231', placed_on: '2026-11-03', status: 'delivered', total: 60.5, items: ['Ceramic Pour-Over Coffee Set', 'Linen Napkins (Set of 4)'] },
  ],
  transcript: [],
  assistant_name: 'Juniper Lane Goods virtual assistant',
}

function product(name: string, overrides: Partial<Product> = {}): Product {
  return {
    slug: name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''),
    name,
    category: 'Homeware',
    price: 20,
    price_options: [],
    warranty: 'None',
    stock_status: 'In stock',
    units_in_stock: 100,
    ...overrides,
  }
}

const PRODUCTS: Product[] = [
  product('Bluetooth Speaker Mini', { category: 'Electronics', price: 39.99, warranty: '1 year' }),
  product('Cast Iron Skillet', { price: 55 }),
  product('Wool Throw Blanket', { price: 68, stock_status: 'Out of stock', units_in_stock: 0 }),
  product('Ceramic Planter Set', { price: 32, stock_status: 'Low stock', units_in_stock: 2 }),
  product('Juniper Lane Gift Card', { category: 'Gift card', price: null, price_options: [25, 50, 100], warranty: 'Not applicable', units_in_stock: null }),
]

const TICKETS: CustomerTicket[] = [
  { ticket_id: 'TCK-20261120-AB12CD', created_at: '2026-11-20T10:00:00+00:00', status: 'open', topic: 'Refund request', summary: 'Wants a refund for the coffee set.', order_id: 'JL-10231', source: 'chat' },
  { ticket_id: 'TK-60029', created_at: '2026-06-21T10:39', status: 'closed', topic: 'Customer asked for a human', summary: 'Handled by support team by email', order_id: 'JL-10198', source: 'records' },
]

type Route = { status?: number; body?: unknown }

function fakeApi(overrides: Record<string, Route> = {}) {
  const calls: string[] = []
  vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, init) => {
    const url = String(input)
    const method = init?.method ?? 'GET'
    calls.push(`${method} ${url}`)
    const route: Route =
      overrides[url] ??
      (url === '/api/sessions' && method === 'POST'
        ? { status: 201, body: SESSION }
        : url === '/api/products'
          ? { body: PRODUCTS }
          : url === '/api/sessions/session-abc/tickets'
            ? { body: TICKETS }
            : method === 'DELETE'
              ? { status: 204 }
              : url === '/api/sessions/session-abc'
                ? { body: SESSION }
                : { status: 404, body: { detail: 'Not found' } })
    const { status = 200, body } = route
    return new Response(status === 204 ? null : JSON.stringify(body), { status })
  })
  return calls
}

async function openShop() {
  const user = userEvent.setup()
  render(<App />)
  await user.type(screen.getByLabelText('Email'), SESSION.customer.email)
  await user.type(screen.getByLabelText('Password'), 'test-pass')
  await user.click(screen.getByRole('button', { name: 'Sign in' }))
  await screen.findByRole('heading', { name: 'Homeware, furniture and electronics' })
  await screen.findByRole('article', { name: 'Cast Iron Skillet' })
  return user
}

const card = (name: string) => screen.getByRole('article', { name })
const cartButton = () => screen.getByRole('button', { name: /^Cart,/ })

describe('the shop page', () => {
  it('is the first page after signing in, with every product and its price', async () => {
    fakeApi()
    await openShop()

    expect(window.location.hash).toBe('#/')
    expect(screen.getAllByRole('article')).toHaveLength(PRODUCTS.length)
    expect(within(card('Bluetooth Speaker Mini')).getByText('$39.99')).toBeInTheDocument()
    expect(within(card('Bluetooth Speaker Mini')).getByText('Electronics · 1 year warranty')).toBeInTheDocument()
    expect(within(card('Cast Iron Skillet')).getByText('Homeware')).toBeInTheDocument() // no "None warranty"
    expect(within(card('Cast Iron Skillet')).getByRole('img', { name: 'Cast Iron Skillet' })).toBeInTheDocument()
  })

  it('cannot add an item that is out of stock, and says when stock is low', async () => {
    fakeApi()
    await openShop()

    expect(within(card('Wool Throw Blanket')).getByRole('button', { name: 'Out of stock' })).toBeDisabled()
    expect(within(card('Ceramic Planter Set')).getByText('Only 2 left')).toBeInTheDocument()
  })

  it('filters by category', async () => {
    fakeApi()
    const user = await openShop()

    await user.click(screen.getByRole('button', { name: /^Electronics/ }))
    expect(screen.getAllByRole('article').map((a) => a.getAttribute('aria-label'))).toEqual(['Bluetooth Speaker Mini'])

    await user.click(screen.getByRole('button', { name: /^All/ }))
    expect(screen.getAllByRole('article')).toHaveLength(PRODUCTS.length)
  })

  it('shows your orders with their numbers, newest first', async () => {
    fakeApi()
    await openShop()

    const orders = screen.getByRole('region', { name: 'Your orders' })
    const rows = within(orders).getAllByRole('listitem')
    expect(rows[0]).toHaveTextContent('JL-10231')
    expect(rows[0]).toHaveTextContent('Placed 3 Nov 2026 · Delivered')
    expect(rows[0]).toHaveTextContent('$60.50')
    expect(rows[1]).toHaveTextContent('JL-10198')
  })

  it('shows your tickets, from chat and from the shop records', async () => {
    fakeApi()
    await openShop()

    const tickets = screen.getByRole('region', { name: 'Your tickets' })
    expect(await within(tickets).findByText('TCK-20261120-AB12CD')).toBeInTheDocument()
    expect(within(tickets).getByText('Refund request')).toBeInTheDocument()
    expect(within(tickets).getByText('Open')).toBeInTheDocument()
    expect(within(tickets).getByText('TK-60029')).toBeInTheDocument()
    expect(within(tickets).getByText('Closed')).toBeInTheDocument()
  })

  it('says so when there are no tickets', async () => {
    fakeApi({ '/api/sessions/session-abc/tickets': { body: [] } })
    await openShop()

    expect(await screen.findByText('No support tickets yet')).toBeInTheDocument()
  })

  it('goes back to sign-in if the session has ended', async () => {
    fakeApi({ '/api/sessions/session-abc/tickets': { status: 404, body: { detail: 'This chat has ended.' } } })
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByLabelText('Email'), SESSION.customer.email)
    await user.type(screen.getByLabelText('Password'), 'test-pass')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByRole('status')).toHaveTextContent(/idle for a while/)
  })

  it('shows the product list error instead of an empty page', async () => {
    fakeApi({ '/api/products': { status: 500, body: { detail: 'The product list is not available.' } } })
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByLabelText('Email'), SESSION.customer.email)
    await user.type(screen.getByLabelText('Password'), 'test-pass')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByText('The product list is not available.')).toBeInTheDocument()
  })
})

describe('the cart', () => {
  it('adds items, counts them, and totals them', async () => {
    fakeApi()
    const user = await openShop()

    await user.click(within(card('Cast Iron Skillet')).getByRole('button', { name: 'Add to cart' }))
    await user.click(within(card('Cast Iron Skillet')).getByRole('button', { name: 'Add to cart' }))
    await user.click(within(card('Bluetooth Speaker Mini')).getByRole('button', { name: 'Add to cart' }))

    expect(cartButton()).toHaveAccessibleName('Cart, 3 items')
    expect(within(card('Cast Iron Skillet')).getByText('2 in your cart')).toBeInTheDocument()

    await user.click(cartButton())
    const cart = screen.getByRole('dialog', { name: 'Your cart' })
    expect(within(cart).getByText('Cast Iron Skillet')).toBeInTheDocument()
    expect(within(cart).getByText('$110.00')).toBeInTheDocument()
    expect(within(cart).getByText('$149.99')).toBeInTheDocument() // the subtotal
  })

  it('can never check out', async () => {
    const calls = fakeApi()
    const user = await openShop()
    await user.click(within(card('Cast Iron Skillet')).getByRole('button', { name: 'Add to cart' }))
    await user.click(cartButton())

    const cart = screen.getByRole('dialog', { name: 'Your cart' })
    expect(within(cart).getByRole('button', { name: 'Checkout' })).toBeDisabled()
    expect(within(cart).getByText(/Checkout is closed in this demo shop/)).toBeInTheDocument()
    expect(calls.filter((c) => c.startsWith('POST') && !c.endsWith('/api/sessions'))).toEqual([])
  })

  it('changes quantities and removes a line at zero', async () => {
    fakeApi()
    const user = await openShop()
    await user.click(within(card('Cast Iron Skillet')).getByRole('button', { name: 'Add to cart' }))
    await user.click(cartButton())
    const cart = screen.getByRole('dialog', { name: 'Your cart' })

    await user.click(within(cart).getByRole('button', { name: 'One more' }))
    expect(within(cart).getByRole('group', { name: 'Quantity of Cast Iron Skillet' })).toHaveTextContent('2')
    await user.click(within(cart).getByRole('button', { name: 'One fewer' }))
    await user.click(within(cart).getByRole('button', { name: 'One fewer' }))
    expect(within(cart).getByText('Your cart is empty')).toBeInTheDocument()
  })

  it('stops at the stock that is left', async () => {
    fakeApi()
    const user = await openShop()
    const add = within(card('Ceramic Planter Set')).getByRole('button', { name: 'Add to cart' })

    await user.click(add)
    await user.click(add)

    expect(within(card('Ceramic Planter Set')).getByRole('button', { name: 'Limit reached' })).toBeDisabled()
  })

  it('adds the gift card amount you pick', async () => {
    fakeApi()
    const user = await openShop()
    const giftCard = card('Juniper Lane Gift Card')

    await user.click(within(giftCard).getByRole('button', { name: '$100' }))
    expect(within(giftCard).getByRole('button', { name: '$100' })).toHaveAttribute('aria-pressed', 'true')
    await user.click(within(giftCard).getByRole('button', { name: 'Add to cart' }))
    await user.click(cartButton())

    expect(within(screen.getByRole('dialog')).getByText('Juniper Lane Gift Card ($100.00)')).toBeInTheDocument()
  })

  it('closes with Escape and is remembered for this tab', async () => {
    fakeApi()
    const user = await openShop()
    await user.click(within(card('Cast Iron Skillet')).getByRole('button', { name: 'Add to cart' }))
    await user.click(cartButton())

    await user.keyboard('{Escape}')
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    const saved = JSON.parse(sessionStorage.getItem('juniper-lane-cart:priya.nair@example.com') ?? '[]')
    expect(saved).toMatchObject([{ id: 'cast-iron-skillet', quantity: 1, price: 55 }])
  })
})

describe('the support chat', () => {
  it('opens from the button at the bottom right and closes again', async () => {
    fakeApi()
    const user = await openShop()
    // Closed, the window is hidden from the page and from screen readers.
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Chat with us' }))
    const chat = screen.getByRole('dialog', { name: 'Juniper Lane Goods virtual assistant' })
    expect(chat).toBeVisible()
    expect(screen.getByLabelText('Your message')).toHaveFocus()
    expect(screen.queryByRole('button', { name: 'Chat with us' })).not.toBeInTheDocument()

    await user.click(within(chat).getByRole('button', { name: 'Close' }))
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Chat with us' })).toHaveFocus()
  })

  it('closes with Escape and keeps the conversation', async () => {
    fakeApi({ '/api/sessions/session-abc/messages': { body: { reply: 'Hello from the shop.', outcome: 'completed', new_ticket_ids: [] } } })
    const user = await openShop()
    await user.click(screen.getByRole('button', { name: 'Chat with us' }))
    await user.type(screen.getByLabelText('Your message'), 'Hi{Enter}')
    await screen.findByText('Hello from the shop.')

    await user.keyboard('{Escape}')
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Chat with us' }))
    expect(screen.getByText('Hello from the shop.')).toBeVisible()
    expect(sessionStorage.getItem('juniper-lane-chat-open')).toBe('open')
  })

  it('asks about an order from the orders list', async () => {
    fakeApi()
    const user = await openShop()
    const orders = screen.getByRole('region', { name: 'Your orders' })

    await user.click(within(orders).getAllByRole('button', { name: 'Ask about this order' })[0])

    expect(screen.getByRole('dialog', { name: /virtual assistant/ })).toBeVisible()
    expect(screen.getByLabelText('Your message')).toHaveValue("What's the status of my order JL-10231?")
  })

  it('updates your tickets when the chat creates one', async () => {
    let ticketCalls = 0
    const created: CustomerTicket = { ...TICKETS[0], ticket_id: 'TCK-20261121-NEW123', topic: 'Asked for a person' }
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, init) => {
      const url = String(input)
      const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status })
      if (url === '/api/sessions' && init?.method === 'POST') return json(SESSION, 201)
      if (url === '/api/products') return json(PRODUCTS)
      if (url.endsWith('/tickets')) return json(ticketCalls++ === 0 ? [] : [created])
      if (url.endsWith('/messages')) {
        return json({ reply: 'Your ticket is TCK-20261121-NEW123.', outcome: 'completed', new_ticket_ids: ['TCK-20261121-NEW123'] })
      }
      return json({ detail: 'Not found' }, 404)
    })
    const user = await openShop()
    expect(await screen.findByText('No support tickets yet')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Chat with us' }))
    await user.type(screen.getByLabelText('Your message'), 'I want a person{Enter}')

    const tickets = screen.getByRole('region', { name: 'Your tickets' })
    expect(await within(tickets).findByText('TCK-20261121-NEW123')).toBeInTheDocument()
    expect(screen.getByText(/Our team will reply by email/)).toHaveTextContent('TCK-20261121-NEW123')
  })
})

describe('product drawings', () => {
  it('exist for every product in the shop document', () => {
    const shopProducts = [
      'bluetooth-speaker-mini', 'wireless-earbuds-pro', 'led-desk-lamp', 'electric-kettle-1-7l',
      'smart-plug-2-pack', 'oak-side-table', 'wool-throw-blanket', 'cast-iron-skillet',
      'ceramic-pour-over-coffee-set', 'ceramic-planter-set', 'bamboo-cutting-board',
      'linen-napkins-set-of-4', 'adjustable-phone-stand', 'scented-soy-candle',
      'personalised-leather-notebook', 'juniper-lane-gift-card',
    ]
    expect([...DRAWN_PRODUCTS].sort()).toEqual([...shopProducts].sort())
  })
})
