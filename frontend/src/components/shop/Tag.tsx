// The page's signature detail: order and ticket numbers set like a small parcel
// label, in a monospaced font with a hairline edge. Used only for those numbers.
export function Tag({ children }: { children: string }) {
  return <span className="parcel-tag">{children}</span>
}
