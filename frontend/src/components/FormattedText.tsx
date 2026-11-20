import type { ReactNode } from 'react'

// Shows the assistant's reply with simple formatting: paragraphs, "- " bullet
// lists, **bold** text, and ticket numbers highlighted. Text is always shown
// as text, never run as HTML, so nothing in a reply can harm the page.
const TICKET = /(TCK-\d{8}-[A-Z0-9]{6})/g

function inline(text: string): ReactNode[] {
  return text.split(/(\*\*[^*]+\*\*)/g).flatMap((part, i) => {
    const bold = part.startsWith('**') && part.endsWith('**') && part.length > 4
    const content = bold ? part.slice(2, -2) : part
    const pieces = content.split(TICKET).map((piece, j) =>
      TICKET.test(piece) ? (
        <span key={`${i}-${j}`} className="ticket-ref">{piece}</span>
      ) : (
        piece
      ),
    )
    TICKET.lastIndex = 0
    return bold ? [<strong key={i}>{pieces}</strong>] : pieces
  })
}

export function FormattedText({ text }: { text: string }) {
  const blocks = text.trim().split(/\n\s*\n/)
  return (
    <>
      {blocks.map((block, i) => {
        const lines = block.split('\n')
        if (lines.every((line) => /^\s*[-•]\s+/.test(line))) {
          return (
            <ul key={i}>
              {lines.map((line, j) => (
                <li key={j}>{inline(line.replace(/^\s*[-•]\s+/, ''))}</li>
              ))}
            </ul>
          )
        }
        return (
          <p key={i}>
            {lines.map((line, j) => (
              <span key={j}>
                {j > 0 && <br />}
                {inline(line)}
              </span>
            ))}
          </p>
        )
      })}
    </>
  )
}
