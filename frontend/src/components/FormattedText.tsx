import type { ReactNode } from 'react'

// Shows the assistant's reply with simple formatting: paragraphs, "- " bullet
// lists, **bold** text, and ticket numbers highlighted. Text is always shown
// as text, never run as HTML, so nothing in a reply can harm the page.
const TICKET = /(TCK-\d{8}-[A-Z0-9]{6})/g
const BULLET = /^\s*[-•]\s+/

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

// Splits one block of lines into runs: plain lines become a paragraph, and
// bullet lines become a list. So "Refunds:" followed by "- ..." lines shows a
// heading line and then a real list.
function runs(lines: string[]): { bullets: boolean; lines: string[] }[] {
  const result: { bullets: boolean; lines: string[] }[] = []
  for (const line of lines) {
    const bullets = BULLET.test(line)
    const last = result.at(-1)
    if (last && last.bullets === bullets) last.lines.push(line)
    else result.push({ bullets, lines: [line] })
  }
  return result
}

export function FormattedText({ text }: { text: string }) {
  const blocks = text.trim().split(/\n\s*\n/)
  return (
    <>
      {blocks.flatMap((block, i) =>
        runs(block.split('\n')).map((run, k) =>
          run.bullets ? (
            <ul key={`${i}-${k}`}>
              {run.lines.map((line, j) => (
                <li key={j}>{inline(line.replace(BULLET, ''))}</li>
              ))}
            </ul>
          ) : (
            <p key={`${i}-${k}`}>
              {run.lines.map((line, j) => (
                <span key={j}>
                  {j > 0 && <br />}
                  {inline(line)}
                </span>
              ))}
            </p>
          ),
        ),
      )}
    </>
  )
}
