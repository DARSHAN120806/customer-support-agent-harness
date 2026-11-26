# Customer Support Agent Harness

An AI support assistant for **Juniper Lane Goods**, a made-up online shop.

A customer asks a question in the shop's chat. The assistant looks up the answer
in the shop's own documents and the customer's orders, then replies. It never
makes up policies, prices or order details. If it can't help, it hands the
customer to a real support person.

## Features

- **Shop page:** customers sign in and see the products (priced in Indian rupees), a cart, their orders
  and their support tickets.
- **Support chat:** a "Chat with us" button answers questions about orders,
  shipping, returns, refunds and warranties. It opens beside the shop, and
  "Expand" makes it fill the whole page.
- **Privacy:** each customer can see only their own orders.
- **Safety checks:** every reply is checked before the customer sees it.
- **Returns and refunds in the chat:** the assistant collects the details and the
  shop's rules, written in plain code, decide: simple returns are approved straight
  away with the exact amount, others go to a person, and some are not allowed.
  Staff approve or decline the waiting ones in the admin panel, and customers see
  where each request stands under their orders.
- **Hand-over to a person:** the assistant creates a ticket when it can't help
  or when someone asks for a person.
- **Staff chat:** support staff sign in, take a ticket, see who the customer is
  and their orders, and chat with them.
- **Admin panel:** statistics, tickets, conversation replays, editing the shop's
  documents, looking up orders, and choosing the AI model (including local models).

## How to use it

You need **Python 3.10+**, **Node.js 20+** and an **AWS account with Amazon
Bedrock** (or another AI service, chosen later in the admin panel).

1. Download and install:

   ```bash
   git clone https://github.com/DARSHAN120806/customer-support-agent-harness.git
   cd customer-support-agent-harness
   python -m venv .venv
   .venv/Scripts/python -m pip install -e ".[web]"
   npm --prefix frontend install
   ```

   On macOS or Linux, use `.venv/bin/python` instead of `.venv/Scripts/python`.

2. Copy `.env.example` to `.env` and fill in your AWS region and Bedrock key.

3. Create test passwords for the sample accounts:

   ```bash
   .venv/Scripts/python scripts/create_test_passwords.py
   ```

   They are saved in `private/test_passwords.csv` on your computer.

4. Start the app in two terminals:

   ```bash
   .venv/Scripts/python -m uvicorn support_agent.web.api:create_app --factory --port 8000
   ```

   ```bash
   npm --prefix frontend run dev
   ```

5. Open http://localhost:5173 and sign in with an email and password from
   `private/test_passwords.csv`. Customers see the shop; the admin and staff
   accounts see the admin panel.

This is meant to run on your own computer only. All shop data is made up.
