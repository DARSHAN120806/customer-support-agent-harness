// Simple drawings of the shop's products, made in code (SVG), so no photos or
// paid image services are needed. Flat shapes in the materials of each product:
// oak, ceramic, wool, cast iron, bamboo, linen, leather. No glows or gradients.
import { DRAWINGS } from './drawings'

export function ProductArt({ slug, name }: { slug: string; name: string }) {
  const drawing = DRAWINGS[slug]
  return (
    <svg className="product-art" viewBox="0 0 200 160" role="img" aria-label={name}>
      {drawing ?? <ellipse cx="100" cy="140" rx="60" ry="6" fill="rgba(31, 27, 22, 0.10)" />}
    </svg>
  )
}

