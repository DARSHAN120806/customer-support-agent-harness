// The packing slip on the sign-in page shows catalogue prices in rupees.
import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { PackingSlip } from './components/PackingSlip'

describe('the packing slip on the sign-in page', () => {
  it('shows prices in rupees, never dollars', () => {
    const { container } = render(<PackingSlip />)

    expect(screen.getByText('₹4,200')).toBeInTheDocument()
    expect(screen.getByText('₹13,400')).toBeInTheDocument() // the total
    expect(container.textContent).not.toContain('$')
  })
})
