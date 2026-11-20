# Front end

The customer chat page for the Juniper Lane Goods support agent, built with
React, TypeScript, and Vite. It talks to the Python web API in
`src/support_agent/web/`, which runs the same agent as the terminal chat.

Style: soft pastel colours, no gradients, and frosted-glass panels. Charts use
Recharts with flat pastel bars.

Pages: the customer chat at http://localhost:5173 and the support dashboard at
http://localhost:5173/#/dashboard.

## Run it

Two terminals, from the project folder:

```bash
.venv/Scripts/python -m uvicorn support_agent.web.api:create_app --factory --port 8000
```

```bash
npm --prefix frontend install
npm --prefix frontend run dev
```

Then open http://localhost:5173. Vite passes every `/api` request on to the API
on port 8000.

## Test and build

```bash
npm --prefix frontend test
npm --prefix frontend run build
```

The tests replace the API with a fake, so they need no server and cost nothing.

## Files

| File | What it does |
|---|---|
| `src/api.ts` | Every call to the API, and the shapes of its answers |
| `src/App.tsx` | Chooses between sign-in and chat; restores a chat after a refresh |
| `src/components/SignIn.tsx` | Demo sign-in: search for a customer and chat as them |
| `src/components/Chat.tsx` | The chat: messages, typing indicator, ticket notes, message box |
| `src/components/OrdersSidebar.tsx` | The signed-in customer's own orders |
| `src/components/BehindTheScenes.tsx` | The panel showing what the harness did for a reply |
| `src/components/dashboard/` | Support dashboard: `Dashboard`, `Tickets`, `Conversations` (list and replay), `Evaluations` (charts) |
| `src/format.ts`, `src/turns.ts` | Shared labels and formatting; grouping log lines into messages |
| `src/components/FormattedText.tsx` | Safe formatting of replies (never runs HTML) |
| `src/index.css` | All styling |
| `src/*.test.tsx` | Tests (33) |

The sign-in is a demo: anyone can choose any customer. Run it on your own
computer only.
