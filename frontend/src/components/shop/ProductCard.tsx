import { useState } from 'react'
import type { Product } from '../../api'
import { rupees, lineFor, type CartLine } from './cart'
import { ProductArt } from './ProductArt'

type Props = {
  product: Product
  // How many of a cart line (a product, or a gift card amount) are in the cart.
  quantityOf: (lineId: string) => number
  onAdd: (line: CartLine) => void
}

export function ProductCard({ product, quantityOf, onAdd }: Props) {
  const choosesAmount = product.price == null
  const [amount, setAmount] = useState(product.price_options[1] ?? product.price_options[0])
  const soldOut = product.stock_status === 'Out of stock'
  const line = lineFor(product, amount)
  const inCart = line ? quantityOf(line.id) : 0
  const full = line != null && inCart >= line.maxQuantity

  const meta = [product.category]
  if (product.warranty && !['None', 'Not applicable'].includes(product.warranty)) {
    meta.push(`${product.warranty} warranty`)
  }

  return (
    <article className="product" aria-label={product.name}>
      <div className="product-tile">
        <ProductArt slug={product.slug} name={product.name} />
      </div>

      <div className="product-body">
        <h3 className="product-name">{product.name}</h3>
        <p className="product-meta">{meta.join(' · ')}</p>

        <div className="product-buy">
          {choosesAmount ? (
            // The gift card's amounts take the place of a single price.
            <div className="amounts" role="group" aria-label="Gift card amount">
              {product.price_options.map((option) => (
                <button
                  key={option}
                  type="button"
                  className={option === amount ? 'amount selected' : 'amount'}
                  aria-pressed={option === amount}
                  onClick={() => setAmount(option)}
                >
                  {rupees(option)}
                </button>
              ))}
            </div>
          ) : (
            <span className="price">{rupees(product.price ?? 0)}</span>
          )}
          <button
            type="button"
            className="add-button"
            disabled={soldOut || full || line == null}
            onClick={() => line && onAdd(line)}
          >
            {soldOut ? 'Out of stock' : full ? 'Limit reached' : 'Add to cart'}
          </button>
        </div>

        <p className="stock-note" aria-live="polite">
          {[
            product.stock_status === 'Low stock' && product.units_in_stock != null
              ? `Only ${product.units_in_stock} left`
              : null,
            inCart > 0 ? `${inCart} in your cart` : null,
          ]
            .filter(Boolean)
            .join(' · ') || ' '}
        </p>
      </div>
    </article>
  )
}
