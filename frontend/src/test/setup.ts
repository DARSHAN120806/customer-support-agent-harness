import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach, vi } from 'vitest'

afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
  sessionStorage.clear()
  window.location.hash = ''
})

// The chart library measures its box with ResizeObserver, which the test
// browser does not have. A do-nothing stand-in is enough for the tests.
class ResizeObserverStandIn {
  observe() {}
  unobserve() {}
  disconnect() {}
}
globalThis.ResizeObserver ??= ResizeObserverStandIn as unknown as typeof ResizeObserver
