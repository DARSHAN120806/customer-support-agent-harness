// The cart, sliding in from the right. Checkout is switched off on purpose:
// this is a demo shop, and nothing can be bought.
import { useEffect, useRef } from 'react'
import { rupees, type CartLine } from './cart'

type Props = {
  lines: CartLine[]
  subtotal: number
  onQuantity: (id: string, quantity: number) => void
  onClose: () => void
}

// From the shop's shipping policy (shipping.md).
const FREE_SHIPPING_FROM = 5000 // ₹5,000, as in the Shipping Policy

export function CartPanel({ lines, subtotal, onQuantity, onClose }: Props) {
  const closeRef = useRef<HTMLButtonElement>(null)
  const onCloseRef = useRef(onClose)
  useEffect(() => {
    onCloseRef.current = onClose
  })

  // When the panel opens, keyboard focus moves into it, and Escape closes it.
  useEffect(() => {
    closeRef.current?.focus()
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onCloseRef.current()
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  return (
    <div className="sheet-layer">
      <button type="button" className="sheet-scrim" aria-label="Close cart" tabIndex={-1} onClick={onClose} />
      <aside className="sheet" role="dialog" aria-modal="true" aria-labelledby="cart-title">
        <header className="sheet-head">
          <h2 id="cart-title">Your cart</h2>
          <button ref={closeRef} type="button" className="text-button" onClick={onClose}>
            Close
          </button>
        </header>

        {lines.length === 0 ? (
          <p className="empty sheet-empty">Your cart is empty</p>
        ) : (
          <ul className="cart-lines">
            {lines.map((line) => (
              <li key={line.id} className="cart-line">
                <div>
                  <p className="row-title">{line.name}</p>
                  <p className="row-meta">{rupees(line.price)} each</p>
                </div>
                <div className="stepper" role="group" aria-label={`Quantity of ${line.name}`}>
                  <button type="button" aria-label="One fewer" onClick={() => onQuantity(line.id, line.quantity - 1)}>
                    −
                  </button>
                  <span aria-live="polite">{line.quantity}</span>
                  <button
                    type="button"
                    aria-label="One more"
                    disabled={line.quantity >= line.maxQuantity}
                    onClick={() => onQuantity(line.id, line.quantity + 1)}
                  >
                    +
                  </button>
                </div>
                <span className="row-figure">{rupees(line.price * line.quantity)}</span>
              </li>
            ))}
          </ul>
        )}

        <footer className="sheet-foot">
          <div className="sum-row">
            <span>Subtotal</span>
            <span className="row-figure">{rupees(subtotal)}</span>
          </div>
          <p className="row-meta">
            {subtotal >= FREE_SHIPPING_FROM || subtotal === 0
              ? 'Standard shipping is free on orders of ₹5,000 or more'
              : 'Standard shipping is ₹499, or free from ₹5,000'}
          </p>
          <button type="button" className="checkout" disabled>
            Checkout
          </button>
          <p className="row-meta checkout-note">Checkout is closed in this demo shop, so nothing is charged</p>
        </footer>
      </aside>
    </div>
  )
}
