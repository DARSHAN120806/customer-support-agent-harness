// The page's signature detail: order and ticket numbers set like a small parcel
// label, in a monospaced font with a hairline edge. Used only for those numbers.
export function Tag({ children }: { children: string }) {
  return <span className="parcel-tag">{children}</span>
}

// The same tag as a button, for a number that opens something (a ticket).
export function TagButton({ children, onClick, label }: { children: string; onClick: () => void; label: string }) {
  return (
    <button type="button" className="tag-button" onClick={onClick} aria-label={label}>
      <span className="parcel-tag">{children}</span>
    </button>
  )
}
