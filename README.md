# Customer Support Agent Harness

An agentic harness, written from scratch in Python, that runs a customer support
agent for a fictional online shop (Juniper Lane Goods). A customer sends a
message; the agent decides what to do, calls tools, and writes a reply.

The design goal is an agent you could trust in front of customers: it answers
only from the shop's own documents and order data, it never invents a policy, a
price, or an order detail, and whenever it cannot answer safely it hands the
conversation to a human.

No agent framework is used. The loop, the tool layer, the safety checks, and the
logging are all plain Python, so every step is visible and testable.

## What it does

- **Agent loop** — sends the conversation to the model, runs the tools it asks
  for, feeds the results back, and repeats until there is a reply or a limit is hit.
- **Four tools** — search the knowledge base, look up an order, calculate a
  date, and escalate to a human by creating a ticket.
- **Hybrid search** — Amazon Titan embeddings combined with a keyword score, with
  an on-disk embedding cache.
- **Safety enforced in code**, not only in the prompt (see below).
- **Structured event log** — every model call, tool call, rewrite, blocked reply,
  and ticket, with token counts, estimated cost, and timing, and with personal
  data masked.
- **Switchable model provider** — Amazon Bedrock or the Anthropic API, chosen by
  an environment variable.
- **165 automated tests** that run against a fake model, so they are fast, free,
  and need no credentials.

## How it works

```
 customer message
        |
        v
+----------------+   tool calls   +---------------------------------------+
|   agent loop   | -------------> | search_knowledge_base   lookup_order   |
|  (agent.py)    | <------------- | calculate_date          escalate_to_human |
+----------------+   results      +---------------------------------------+
        |
        v
+----------------+  fails once -> the model is asked to rewrite
|  reply checks  |  fails again, or a limit is hit -> fixed safe reply
|  (safety.py)   |                                    + automatic ticket
+----------------+
        |
        v
  reply to customer            every step -> logs/agent.jsonl (masked)
```

## Safety design

A prompt is a request, not a guarantee, so each important rule is also enforced
by the harness.

| Rule | How it is enforced |
|---|---|
| The agent never issues a refund | There is no tool that changes anything. A reply that claims to give a refund is blocked. |
| One customer never sees another's data | `lookup_order` takes only an order ID; the customer's identity comes from the session, never from chat text. Someone else's order returns exactly the same text as a missing order. A reply containing any other person's email is blocked. |
| No invented prices, policies, or dates | Every dollar amount, percentage, time period, and date in a reply must appear in a tool result or in the customer's own message. Otherwise the model gets one rewrite, then the reply is withheld. |
| Deadlines are correct | Date arithmetic is done by a `calculate_date` tool in code, not by the model. |
| Unanswered shop questions reach a human | If the agent searched, found no answer, and created no ticket, it is told to create one; if it still does not, the harness creates it. |
| The agent cannot run away | Limits on steps per message, tokens per message, and estimated cost per conversation. |
| There is always a fallback | When a reply is blocked or a limit is hit, the harness creates a ticket itself and replies with the ticket number. |

The prompt covers the rules that need judgement: escalate when the customer is
upset, when the agent is unsure, or when a human is asked for; decline requests
unrelated to the shop; and treat text in customer messages as data, never as
instructions.

## Quick start

Requires Python 3.10 or newer.

```bash
git clone https://github.com/DARSHAN120806/customer-support-agent-harness.git
cd customer-support-agent-harness
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev]"     # Windows
# .venv/bin/python -m pip install -e ".[dev]"       # macOS / Linux
```

Run the tests (no keys needed):

```bash
.venv/Scripts/python -m pytest -q
```

To chat with the agent, copy `.env.example` to `.env`, fill in your AWS region
and a Bedrock API key, then:

```bash
.venv/Scripts/python -m support_agent --email priya.nair@example.com
```

The `--email` flag stands in for a real login. The sample customer above owns
orders `JL-10231` and `JL-10198`. Things to try:

- `What is your return policy?`
- `Where is my order JL-10231?`
- `Is my speaker from JL-10198 still under warranty?`
- `I want a refund for the coffee set in JL-10231.`
- `What's in order JL-10240?` (another customer's order)

## Configuration

All settings are environment variables, read from `.env`. Secrets are never
stored in code.

| Variable | Default | Purpose |
|---|---|---|
| `SUPPORT_AGENT_PROVIDER` | `bedrock` | `bedrock` or `anthropic` |
| `SUPPORT_AGENT_MODEL` | Claude Haiku 4.5 on Bedrock | Model ID for the chosen provider |
| `AWS_REGION` | — | Region used for Bedrock |
| `AWS_BEARER_TOKEN_BEDROCK` | — | Bedrock API key (or use AWS access keys) |
| `ANTHROPIC_API_KEY` | — | Only for the `anthropic` provider |
| `SUPPORT_AGENT_MAX_STEPS` | `8` | Model calls allowed per customer message |
| `SUPPORT_AGENT_MAX_TOKENS_PER_MESSAGE` | `50000` | Token limit per customer message |
| `SUPPORT_AGENT_MAX_COST_USD` | `0.50` | Estimated cost limit per conversation |
| `SUPPORT_AGENT_LOG_FILE` | `logs/agent.jsonl` | Where the event log is written |

The knowledge base search uses Amazon Titan embeddings, so AWS credentials are
needed for the chat even when the Anthropic API is the model provider.

## Event log

`logs/agent.jsonl` holds one JSON object per line. Every line carries a
`conversation_id`, so a conversation can be followed from start to end.

```json
{"event": "turn_start", "conversation_id": "conv_0cdc3cf3e20a", "customer_ref": "cust_16849819eedf", "turn": 1, "message": "Where is my order JL-10231? Reach me on [PHONE] or at [EMAIL]"}
{"event": "model_call", "turn": 1, "step": 1, "duration_ms": 1766, "input_tokens": 2503, "output_tokens": 69, "cost_usd": 0.002848, "tools_requested": ["lookup_order"]}
{"event": "tool_call", "turn": 1, "step": 1, "tool": "lookup_order", "input": {"order_id": "JL-10231"}, "is_error": false}
{"event": "turn_end", "turn": 1, "outcome": "completed", "steps": 2, "cost_usd": 0.00627, "escalated": false}
```

Emails, phone numbers, street addresses, and long digit runs are masked at the
moment a line is written. The customer appears only as a keyed-hash code.

## Project structure

```
data/
  knowledge_base/        shop documents: shipping, returns, refunds, warranty, FAQ, company overview
  orders.json            synthetic customers and orders
src/support_agent/
  agent.py               the agent loop, limits, automatic escalation
  app.py                 wires provider, data, tools, safety, and logging together
  safety.py              budget limits and reply checks
  prompts.py             system prompt
  knowledge_base.py      document chunking and hybrid search
  embeddings.py          Amazon Titan embeddings
  orders.py              order data with the ownership check
  tickets.py             support tickets (JSON Lines)
  event_log.py           structured logging and masking
  config.py              settings from environment variables
  cli.py                 terminal chat
  providers/             model provider interface, Bedrock and Anthropic clients
  tools/                 tool registry and the four tools
tests/                   165 tests using a fake model and fake embeddings
```

## Tech stack

Python 3.13 · Anthropic Python SDK · Claude on Amazon Bedrock · Amazon Titan
Text Embeddings v2 · boto3 · pytest

## Roadmap

- Retries and wider error handling for model and embedding calls
- An evaluation set of customer messages (routine, tricky, angry, refund
  requests, and attempts to leak data or override the rules) with a script that
  scores the agent
- A dashboard built on the event log

## Disclaimer

Juniper Lane Goods is fictional. All customers, orders, emails, and tracking
numbers in this repository are synthetic.
