// A packing slip drawn in code: the one "moment" on the sign-in page. It shows
// real products and prices from the shop's catalogue (company_overview.md), not
// a real customer's order, so it gives nothing away about anyone. Prices are in
// rupees, like the rest of the shop (they were left in dollars until 26 Nov 2026).
import { rupees } from './shop/cart'

const ITEMS = [
  { name: 'Ceramic Pour-Over Coffee Set', price: 4200 },
  { name: 'Wool Throw Blanket', price: 6800 },
  { name: 'Bamboo Cutting Board', price: 2400 },
]

export function PackingSlip() {
  const subtotal = ITEMS.reduce((sum, item) => sum + item.price, 0)
  return (
    <figure className="slip">
      <header className="slip-head">
        <span className="slip-shop">Juniper Lane Goods</span>
        <span className="slip-kind">Packing slip</span>
      </header>

      <table className="slip-items">
        <thead>
          <tr>
            <th scope="col">Item</th>
            <th scope="col">Qty</th>
            <th scope="col">Price</th>
          </tr>
        </thead>
        <tbody>
          {ITEMS.map((item) => (
            <tr key={item.name}>
              <td>{item.name}</td>
              <td>1</td>
              <td>{rupees(item.price)}</td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr>
            <td colSpan={2}>Standard shipping</td>
            <td>Free</td>
          </tr>
          <tr className="slip-total">
            <td colSpan={2}>Total</td>
            <td>{rupees(subtotal)}</td>
          </tr>
        </tfoot>
      </table>

      <footer className="slip-foot">Packed in Columbus, Ohio</footer>
    </figure>
  )
}
