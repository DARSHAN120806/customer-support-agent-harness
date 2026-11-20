// The shopping cart. It lives only in this browser tab (sessionStorage): this
// is a demo shop, so nothing is ever sent to the server and nothing is bought.
import { useEffect, useState } from 'react'
import type { Product } from '../../api'

export type CartLine = {
  id: string // the product, plus the amount for a gift card ("juniper-lane-gift-card:50")
  slug: string
  name: string
  price: number
  quantity: number
  maxQuantity: number
}

// The shop's documents say orders of more than 10 of one product may be cancelled.
export const MAX_PER_ITEM = 10

export function cartKey(email: string) {
  return `juniper-lane-cart:${email}`
}

function read(key: string): CartLine[] {
  try {
    const saved = JSON.parse(sessionStorage.getItem(key) ?? '[]')
    return Array.isArray(saved) ? saved : []
  } catch {
    return []
  }
}

export function lineFor(product: Product, amount?: number): CartLine | null {
  const price = product.price ?? amount
  if (price == null || product.stock_status === 'Out of stock') return null
  const stock = product.units_in_stock ?? MAX_PER_ITEM
  return {
    id: product.price == null ? `${product.slug}:${price}` : product.slug,
    slug: product.slug,
    name: product.price == null ? `${product.name} (${dollars(price)})` : product.name,
    price,
    quantity: 1,
    maxQuantity: Math.max(0, Math.min(MAX_PER_ITEM, stock)),
  }
}

export function useCart(email: string) {
  const key = cartKey(email)
  const [lines, setLines] = useState<CartLine[]>(() => read(key))

  useEffect(() => {
    sessionStorage.setItem(key, JSON.stringify(lines))
  }, [key, lines])

  function add(line: CartLine) {
    setLines((current) => {
      const existing = current.find((l) => l.id === line.id)
      if (!existing) return [...current, line]
      return current.map((l) =>
        l.id === line.id ? { ...l, quantity: Math.min(l.quantity + 1, l.maxQuantity) } : l,
      )
    })
  }

  function setQuantity(id: string, quantity: number) {
    setLines((current) =>
      quantity <= 0
        ? current.filter((l) => l.id !== id)
        : current.map((l) => (l.id === id ? { ...l, quantity: Math.min(quantity, l.maxQuantity) } : l)),
    )
  }

  const count = lines.reduce((sum, l) => sum + l.quantity, 0)
  const subtotal = lines.reduce((sum, l) => sum + l.price * l.quantity, 0)
  return { lines, add, setQuantity, count, subtotal }
}

export function dollars(amount: number): string {
  return amount.toLocaleString('en-US', { style: 'currency', currency: 'USD' })
}
