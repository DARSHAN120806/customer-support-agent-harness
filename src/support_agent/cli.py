"""Chat with the agent in the terminal.

Run it with:  python -m support_agent --email priya.nair@example.com
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

from dotenv import load_dotenv

from . import event_log
from .app import create_agent, load_resources
from .config import PROJECT_ROOT, ConfigError, Settings
from .prompts import SHOP_NAME, fallback_reply
from .retry import ServiceError

EXIT_WORDS = {"quit", "exit"}


def main(argv: list[str] | None = None) -> int:
    # Make sure replies containing symbols such as "–" print correctly on Windows.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=f"Chat with the {SHOP_NAME} support agent.")
    parser.add_argument(
        "--email",
        help="The email of the signed-in customer. This stands in for a real login.",
    )
    args = parser.parse_args(argv)

    # Read settings from the .env file in the project folder, if there is one.
    load_dotenv(PROJECT_ROOT / ".env")

    try:
        settings = Settings.from_env()
        print("Loading the shop's documents...")
        resources = load_resources(settings)
    except ConfigError as error:
        print(f"Configuration problem: {error}", file=sys.stderr)
        return 1
    except ServiceError as error:
        print(f"Could not prepare the document search: {error}", file=sys.stderr)
        if not error.retryable:
            print("Check AWS_REGION and your AWS sign-in details in .env.", file=sys.stderr)
        return 1

    customer_email = args.email or _ask_for_email()
    if not customer_email:
        return 0
    agent, session = create_agent(settings, resources, customer_email)

    print(f"\n{SHOP_NAME} support chat ({settings.provider}, {settings.model})")
    print(f"Signed in as {session.customer_email}.")
    print(f"Conversation {session.logger.conversation_id}, logged to {settings.log_file}")
    print("Type your message and press Enter. Type 'quit' to leave.\n")

    history: list[dict[str, Any]] = []
    while True:
        try:
            customer_message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not customer_message:
            continue
        if customer_message.lower() in EXIT_WORDS:
            break

        messages_before = len(history)
        try:
            result = agent.run(customer_message, history)
        except Exception as error:
            # The agent handles the failures it expects (model down, limits,
            # blocked replies) itself. This is the last safety net for a bug:
            # the customer still gets a polite reply, the problem is logged,
            # and the chat carries on.
            event_log.log_error(session.logger, "agent_run", error)
            print(f"\nAgent: {fallback_reply()}")
            print(f"       [unexpected error: {type(error).__name__}]\n", file=sys.stderr)
            # Remove everything added for the unanswered message, so the next
            # attempt starts from a clean conversation.
            del history[messages_before:]
            continue

        print(f"\nAgent: {result.reply}")
        tools = ", ".join(result.tools_used) or "no tools"
        if result.auto_ticket_id:
            tools += f", automatic ticket {result.auto_ticket_id}"
        print(
            f"       [{result.outcome}, {result.steps} step(s), used: {tools}, "
            f"{result.input_tokens} tokens in, {result.output_tokens} tokens out]\n"
        )

    return 0


def _ask_for_email() -> str:
    print("\nWhich customer is signed in? (In a real shop this comes from the login.)")
    try:
        return input("Customer email: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return ""


if __name__ == "__main__":
    sys.exit(main())
