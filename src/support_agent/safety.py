"""Safety checks that are enforced in code.

The prompt tells the model what the rules are, but a prompt is a request, not a
guarantee. The checks here are the backstop: they run on every conversation no
matter what the model decides.

    Budget          stops a conversation that uses too many tokens or too much money
    check_reply     blocks a reply that leaks personal data, claims a refund, or
                    states a price or time period the tools never returned
"""

from __future__ import annotations

import calendar
import re
from dataclasses import dataclass
from typing import Any

from .prompts import AI_NOT_HUMAN_REPLY, IDENTITY_REPLY
from .refund_requests import APPROVED_MARKER

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

# Sentences where the agent itself claims to give, or to have given, a refund.
# Statements of fact from order data ("your refund was issued on 12 October")
# and refusals ("I can't issue refunds") are deliberately not matched.
_REFUND_ACTION = (
    r"(?:issue|process|approve|grant|authori[sz]e|arrange|give|send|credit|refund)(?:d|ed)?"
)
REFUND_CLAIM_PATTERNS = [
    re.compile(
        r"\bI(?:'ve| have|'ll| will|'m going to| am going to| can| just)?\s+"
        r"(?:(?:just|now|already|gone ahead and|go ahead and)\s+)*"
        + _REFUND_ACTION
        + r"\b[^.?!\n]{0,60}\b(?:refund|money back|reimburse)",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bI(?:'ve| have|'ll| will)\s+"
        r"(?:(?:just|now|already|gone ahead and|go ahead and)\s+)*refund(?:ed)?\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\byour (?:refund|return|cancellation)(?: request)? (?:has been|is now|is|was) "
        r"(?:approved|accepted|granted|authori[sz]ed|confirmed)\b",
        re.IGNORECASE,
    ),
]

# A request the shop's refund rules approved, as written in the tool result
# ("APPROVED BY THE SHOP'S REFUND RULES. Request RQ-20261121-1A2B3C: ...").
_APPROVED_REQUEST = re.compile(re.escape(APPROVED_MARKER) + r"\. Request (RQ-\d{8}-[0-9A-F]{6})")


def approved_request_ids(tool_text: str) -> set[str]:
    """The request numbers the refund rules approved, found in tool results."""
    return set(_APPROVED_REQUEST.findall(tool_text))


def claims_refund(reply: str, tool_text: str | None = None) -> bool:
    """True if the reply says a refund or return is given or approved, and that
    is not backed by the rules. A claim is backed only when the reply names a
    request number that the refund tool approved in this conversation; the AI
    cannot write tool results, so it cannot invent an approval."""
    if not any(pattern.search(reply) for pattern in REFUND_CLAIM_PATTERNS):
        return False
    approved = approved_request_ids(tool_text or "")
    return not any(request_id in reply for request_id in approved)


# An amount of money. The shop's prices are in Indian rupees ("₹699",
# "₹1,29,000", "Rs. 499", "INR 5,000"). A dollar amount ("$6.99") is caught too:
# the shop's sources never contain one, so a reply with one is always checked.
MONEY_PATTERN = re.compile(r"(?:\$|₹|\bRs\.?|\bINR)\s?(\d[\d,]*(?:\.\d+)?)", re.IGNORECASE)
# A number written with a decimal point, such as "42.0" in order data.
DECIMAL_PATTERN = re.compile(r"(?<![\d.])\d[\d,]*\.\d+(?![\d.])")
# A percentage, such as "20%".
PERCENT_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s?%")
# Any number, used to collect the figures that appear in the sources.
NUMBER_PATTERN = re.compile(r"\d[\d,]*(?:\.\d+)?")
# A time period, such as "30 days", "5-7 business days" or "1-year".
PERIOD_PATTERN = re.compile(
    r"(\d+)(?:\s*(?:-|–|—|to|or)\s*(\d+))?[\s-]*"
    r"(business day|working day|day|week|month|year|hour)s?\b",
    re.IGNORECASE,
)


_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}  # fmt: skip
# Month names must start with a capital letter, so the verb "may" is not a month.
_MONTH_NAMES = "|".join(sorted((name.capitalize() for name in _MONTHS), key=len, reverse=True))
_DAY = r"(\d{1,2})(?:st|nd|rd|th)?"
_YEAR = r"(?:,?\s+(\d{4}))?"
ISO_DATE_PATTERN = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
DAY_MONTH_PATTERN = re.compile(rf"\b{_DAY}\s+(?:of\s+)?({_MONTH_NAMES})\.?{_YEAR}\b")
MONTH_DAY_PATTERN = re.compile(rf"\b({_MONTH_NAMES})\.?\s+{_DAY}{_YEAR}\b")


@dataclass(frozen=True)
class Violation:
    rule: str  # short name, for logs and tests
    detail: str  # what was found, written so it is safe to store
    # True if the model gets one chance to rewrite its reply. False if the reply
    # is withheld straight away.
    correctable: bool = False
    # What the model is told to do differently on its one rewrite.
    fix_hint: str = ""
    # True if a reply that still breaks the rule must not be shown. False if the
    # reply itself is fine and the harness only needs to add a ticket to it.
    blocks_reply: bool = True
    # A fixed reply to show instead, for rules where the customer's question
    # needs no ticket (for example "which AI are you?").
    safe_reply: str | None = None
    # A tool (name, input) the harness runs itself before the rewrite, so the
    # model has the facts in front of it on its second attempt.
    run_tool: tuple[str, dict[str, Any]] | None = None


# ---------------------------------------------------------------------------
# Names the assistant must never say about itself: AI models, AI companies, and
# cloud services. THIS IS THE ONE PLACE TO EDIT THE LIST. Each entry is matched
# as a whole word, ignoring capitals, so "AWS" does not match "laws" and "Titan"
# does not match "titanium". Plain "Amazon" is left out on purpose, because a
# customer may fairly mention the retailer ("it's cheaper on Amazon").
HIDDEN_TECH_TERMS = [
    "Claude",
    "Anthropic",
    "Bedrock",
    "AWS",
    "Amazon Web Services",
    "Titan",
    "GPT",
    "ChatGPT",
    "OpenAI",
    "Llama",
    "Gemini",
    "Mistral",
    "DeepSeek",
    # Names that models run through the admin panel's other services may use.
    # "Gemma" and "Phi" are left out on purpose: they are also people's names
    # and an ordinary word, and would stop the assistant greeting a customer.
    "Qwen",
    "Ollama",
    "LM Studio",
    "Groq",
    "Grok",
    "OpenRouter",
    "Meta AI",
    "LLM",
    "large language model",
    "language model",
]
# Patterns that a plain word cannot express. Model family names such as "Haiku"
# are ordinary words, so they only count when followed by a version number.
HIDDEN_TECH_PATTERNS = [
    r"gpt-?\d[\w.]*",
    r"(?:haiku|sonnet|opus)\s*\d",
]
_HIDDEN_TECH = re.compile(
    r"(?<![A-Za-z])(?:"
    + "|".join(
        [re.escape(term).replace(r"\ ", r"\s+") for term in HIDDEN_TECH_TERMS]
        + HIDDEN_TECH_PATTERNS
    )
    + r")(?![A-Za-z])",
    re.IGNORECASE,
)

# The assistant saying it is a human. "I'm not a real person" does not match.
HUMAN_CLAIM_PATTERNS = [
    re.compile(
        r"\bI(?:'m| am)\s+(?:(?:actually|indeed|definitely|really|also)\s+)*"
        r"(?:a |an )?(?:real |actual |live |human )*(?:human|person|human being)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bI(?:'m| am) not (?:a |an )?(?:bot|robot|chatbot|AI|machine|virtual assistant)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\byou(?:'re| are) (?:talking|speaking|chatting) (?:to|with) a (?:real )?(?:human|person)\b", re.IGNORECASE),
]


# ---------------------------------------------------------------------------
# Words in a customer's message that show they are upset. An upset customer
# must reach a human, so these trigger a ticket. Edit the list here.
UPSET_SIGNALS = [
    r"useless",
    r"ridiculous",
    r"unacceptable",
    r"outrageous",
    r"disgrace(?:ful)?",
    r"disgust(?:ed|ing)",
    r"furious",
    r"livid",
    r"fed up",
    r"sick of",
    r"worst",
    r"terrible",
    r"awful",
    r"appalling",
    r"pathetic",
    r"incompetent",
    r"scam(?:mers?)?",
    r"rip[- ]?off",
    r"waste of (?:time|money)",
    r"never (?:again|ordering|buying|shopping)",
    r"i(?:'m| am) done with",
    r"(?:nobody|no one) (?:ever )?(?:answers|helps|replies|responds|cares)",
    r"chargeback",
]
_UPSET = re.compile(r"\b(?:" + "|".join(UPSET_SIGNALS) + r")\b|!{2,}", re.IGNORECASE)

# Subjects that are shop policy. A reply about one of these must be based on
# something that was looked up, never on the model's general knowledge.
POLICY_TOPICS = re.compile(
    r"\b(?:polic(?:y|ies)|price[- ]match\w*|match(?:ing)? [^.]{0,25}prices?|refunds?|refunded|"
    r"returns?|returned|shipping|deliver(?:y|ies)|warrant(?:y|ies)|discounts?|cancel\w*|"
    r"payment|exchanges?|gift cards?|compensation)\b",
    re.IGNORECASE,
)
# Sentences that only offer help, such as "I can help with orders, shipping and
# returns", list topics without stating any policy, so they are skipped.
_OFFER_OF_HELP = re.compile(r"\b(?:help|assist)\w*\b", re.IGNORECASE)


# Sentences where the assistant says it is creating, or has created, a ticket or
# handed the chat over. Questions ("Would you like me to create a ticket?") are
# offers, not promises, and are not matched.
_TICKET_PROMISE = re.compile(
    r"\b(?:I(?:'ll| will|'m| am|'ve| have)?|let me|I need to|I'm going to|I am going to)\s+"
    r"(?:(?:now|just|already|also|go ahead and|gone ahead and)\s+)*"
    r"(?:creat|rais|open|log|submit|fil|start)\w*\s+(?:a|an|the|your|this)?\s*"
    r"(?:support\s+|new\s+)?(?:ticket|case|request)\b"
    r"|\b(?:I(?:'ll| will|'m| am|'ve| have)|let me|I need to|I'm going to|I am going to)\s+"
    r"(?:(?:now|just|already|also|go ahead and|gone ahead and)\s+)*"
    r"(?:pass\w*|hand\w*|escalat\w*|forward\w*|send\w*|refer\w*)\s+"
    r"(?:this|it|that|your\s+\w+(?:\s+\w+)?)\s+(?:on\s+|over\s+)?to\s+(?:our|the)\s+(?:human\s+|support\s+)*(?:support\s+)?team\b",
    re.IGNORECASE,
)


def promises_ticket(reply: str) -> bool:
    """True if a statement in the reply says a ticket is being or has been
    created, or the chat is being handed to the team."""
    for sentence in re.split(r"(?<=[.!?])\s+|\n+", reply):
        if sentence.rstrip().endswith("?"):
            continue
        if _TICKET_PROMISE.search(sentence):
            return True
    return False


# Ways a customer asks to be passed to a person. "Am I talking to a real
# person?" asks what the assistant is, not for a hand-over, so it is not matched
# ("talking" is not the plain verb "talk").
_PERSON = (
    r"(?:a |an |the |your |one of your |some )?(?:real |actual |live )?"
    r"(?:human|person|people|agent|someone|somebody|manager|supervisor|representative|rep|staff(?: member)?|"
    r"team member|support team|operator)"
)
_ASKS_FOR_HUMAN = re.compile(
    r"\b(?:talk|speak|chat)\s+(?:to|with)\s+" + _PERSON + r"\b"
    r"|\b(?:get|give|put|connect|transfer|pass|send|escalate)\s+me\s+(?:to\s+|through\s+to\s+|with\s+)?" + _PERSON + r"\b"
    r"|\b(?:want|need|like|request)\s+(?:a |an |to (?:talk|speak) to (?:a |an )?)?(?:real |actual |live )?"
    r"(?:human|person|manager|supervisor|representative)\b"
    r"|\bhuman,? please\b"
    r"|\b(?:don't|do not) want (?:a |to talk to a |to speak to a )?(?:bot|robot|machine|chatbot)\b",
    re.IGNORECASE,
)


def asks_for_human(customer_message: str) -> bool:
    """True if the customer asks to be handed over to a person."""
    return bool(_ASKS_FOR_HUMAN.search(customer_message))


def asks_about_policy(customer_message: str) -> bool:
    """True if the customer's message is about a policy subject (refunds,
    shipping, price matching, discounts, and so on)."""
    return bool(POLICY_TOPICS.search(customer_message))


def is_upset(customer_message: str) -> bool:
    return bool(_UPSET.search(customer_message))


def states_policy_without_sources(reply: str, shop_text: str) -> bool:
    """True when nothing has been looked up in this conversation (`shop_text` is
    empty) and the reply still makes a statement about a policy subject.
    Questions and offers of help are not statements."""
    if shop_text.strip():
        return False
    for sentence in re.split(r"(?<=[.!?])\s+|\n+", reply):
        if sentence.rstrip().endswith("?") or _OFFER_OF_HELP.search(sentence):
            continue
        if POLICY_TOPICS.search(sentence):
            return True
    return False


def customer_messages(messages: list[dict[str, Any]]) -> list[str]:
    """What the customer typed in this conversation, oldest first."""
    return [
        message["content"]
        for message in messages
        if message.get("role") == "user" and isinstance(message.get("content"), str)
    ]


def find_hidden_tech_terms(reply: str, shop_text: str = "") -> list[str]:
    """Return the AI model, company, and cloud names found in the reply.

    A name that appears in the shop's own documents or order data (`shop_text`)
    is allowed, so a product that happened to be called "Titan Kettle" could
    still be discussed.
    """
    allowed = {match.lower() for match in _HIDDEN_TECH.findall(shop_text)}
    found = {match for match in _HIDDEN_TECH.findall(reply) if match.lower() not in allowed}
    return sorted(found, key=str.lower)


def claims_to_be_human(reply: str) -> bool:
    return any(pattern.search(reply) for pattern in HUMAN_CLAIM_PATTERNS)


def collect_tool_results(messages: list[dict[str, Any]]) -> str:
    """Gather everything the tools returned in this conversation: the shop's
    documents and the customer's order data."""
    parts: list[str] = []
    for message in messages:
        content = message.get("content")
        if message.get("role") == "user" and isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    parts.append(str(block.get("content", "")))
    return "\n".join(parts)


# Phrases that mean "the shop's documents did not answer this".
NO_ANSWER_PATTERNS = [
    re.compile(
        r"\b(?:do not|don't|does not|doesn't) (?:currently |actually )?have "
        r"(?:any |that |this |specific |enough |the |more )?(?:information|info|details)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:could not|couldn't|cannot|can't|unable to|was not able to|wasn't able to) find "
        r"(?:any |that |specific |more )?(?:information|info|details|anything|mention)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:is not|isn't|are not|aren't|not) (?:covered|mentioned|listed|included|specified|stated) "
        r"in (?:our|the) (?:shop'?s? )?(?:documents?|documentation|polic(?:y|ies)|knowledge base|faq)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bnot able to say whether\b|\b(?:cannot|can't) (?:confirm|say) whether\b", re.IGNORECASE),
    re.compile(r"\b(?:I'm|I am) not (?:sure|certain)\b", re.IGNORECASE),
]


def is_unanswered_shop_question(reply: str, tools_used: list[str]) -> bool:
    """True when the agent searched the shop's documents, told the customer the
    answer was not there, and did not hand over to a human.

    A search having been run is what separates a shop question from an
    unrelated request such as the weather, which is declined without a ticket.
    """
    if "escalate_to_human" in tools_used or "search_knowledge_base" not in tools_used:
        return False
    return any(pattern.search(reply) for pattern in NO_ANSWER_PATTERNS)


def collect_sources(messages: list[dict[str, Any]]) -> str:
    """Gather the text the agent is allowed to take figures from: everything the
    tools returned in this conversation, plus the customer's own messages."""
    parts: list[str] = []
    for message in messages:
        if message.get("role") != "user":
            continue
        content = message.get("content")
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    parts.append(str(block.get("content", "")))
    return "\n".join(parts)


def find_ungrounded_figures(reply: str, sources: str) -> list[str]:
    """Return the amounts of money, percentages, time periods, and dates in the
    reply that do not appear in the sources.

    This is the code-level backstop for "never invent prices, policies, or order
    details". It is strict on purpose: a figure the model worked out in its
    head, such as a total or a deadline, also counts as ungrounded. Deadlines
    are meant to come from the calculate_date tool, whose result is a source.
    """
    # An amount counts as found only if the sources show it as money: with a
    # currency sign (policies, "₹1,299") or with a decimal point (order data,
    # "4200.0"). Matching any bare number would let "₹3" pass because of "3-5 days".
    source_money = {_to_number(match) for match in MONEY_PATTERN.findall(sources)} | {
        _to_number(match) for match in DECIMAL_PATTERN.findall(sources)
    }
    source_periods = set(_periods(sources))

    ungrounded = [
        match.group(0)
        for match in MONEY_PATTERN.finditer(reply)
        if _to_number(match.group(1)) not in source_money
    ]
    source_percentages = {_to_number(match) for match in PERCENT_PATTERN.findall(sources)}
    ungrounded += [
        f"{percentage}%"
        for percentage in PERCENT_PATTERN.findall(reply)
        if _to_number(percentage) not in source_percentages
    ]
    ungrounded += [
        f"{number} {unit}" for number, unit in _periods(reply) if (number, unit) not in source_periods
    ]

    source_dates = _dates(sources)
    for year, month, day in _dates(reply):
        grounded = any(
            (month, day) == (source_month, source_day)
            and (year is None or source_year is None or year == source_year)
            for source_year, source_month, source_day in source_dates
        )
        if not grounded:
            month_name = calendar.month_name[month]
            ungrounded.append(f"the date {day} {month_name}" + (f" {year}" if year else ""))
    return ungrounded


def _dates(text: str) -> list[tuple[int | None, int, int]]:
    """Every calendar date in the text as (year, month, day). The year is None
    when the text does not give one, as in "7 December"."""
    found: list[tuple[int | None, int, int]] = [
        (int(year), int(month), int(day)) for year, month, day in ISO_DATE_PATTERN.findall(text)
    ]
    for day, month, year in DAY_MONTH_PATTERN.findall(text):
        found.append((int(year) if year else None, _MONTHS[month.lower()], int(day)))
    for month, day, year in MONTH_DAY_PATTERN.findall(text):
        found.append((int(year) if year else None, _MONTHS[month.lower()], int(day)))
    return found


def _to_number(text: str) -> float:
    return float(text.replace(",", "").rstrip("."))


def _periods(text: str) -> list[tuple[int, str]]:
    """Every (number, unit) time period in the text. A range such as "5-7
    business days" gives both (5, "business day") and (7, "business day")."""
    found: list[tuple[int, str]] = []
    for first, second, unit in PERIOD_PATTERN.findall(text):
        unit = unit.lower().replace("working day", "business day")
        found.append((int(first), unit))
        if second:
            found.append((int(second), unit))
    return found


def check_reply(
    reply: str,
    allowed_emails: set[str],
    sources: str | None = None,
    tools_used: list[str] | None = None,
    shop_text: str | None = None,
    customer_message: str | None = None,
    has_ticket: bool = False,
) -> list[Violation]:
    """Check a reply against the rules enforced in code. An empty list means the
    reply is fine. When `sources` is given, figures in the reply are checked
    against it. When `tools_used` is given, the reply is also checked for a shop
    question that went unanswered without a hand-over. `shop_text` is what the
    tools returned; names found there are not treated as identity leaks."""
    violations: list[Violation] = []

    in_conversation = tools_used is not None  # False when a reply is checked on its own

    nothing_looked_up = shop_text is not None and not shop_text.strip()
    if in_conversation and shop_text is not None and (
        states_policy_without_sources(reply, shop_text)
        # Also when the customer asked about policy and the model avoided the
        # question without stating anything: nothing was checked either way.
        or (nothing_looked_up and customer_message is not None and asks_about_policy(customer_message))
    ):
        violations.append(
            Violation(
                "unverified_policy",
                "the customer's question or the reply concerned shop policy, but "
                "nothing had been looked up in the shop's documents or order data",
                correctable=True,
                fix_hint=(
                    "The shop's documents have now been searched for the customer's "
                    "message, and the results are in the conversation. Answer only from "
                    "those results. Do not describe what the shop or its support team "
                    "does, or cannot do, from memory. If the results do not cover the "
                    "question, say so and hand over with escalate_to_human."
                ),
                # Telling the model to search was not reliable, so the harness
                # runs the search itself before the rewrite.
                run_tool=(
                    ("search_knowledge_base", {"query": customer_message[:500]})
                    if customer_message
                    else None
                ),
            )
        )

    if (
        in_conversation
        and customer_message is not None
        and not has_ticket
        and "escalate_to_human" not in tools_used
        and asks_for_human(customer_message)
    ):
        violations.append(
            Violation(
                "human_request_not_escalated",
                "the customer asked for a person and no ticket was created",
                correctable=True,
                fix_hint=(
                    "The customer asked to be handed over to a person. Do not only "
                    "offer it or ask what they need first: call escalate_to_human now "
                    "with the reason human_requested, and give them the ticket number. "
                    "You may then ask for any details the team will need."
                ),
                # Whatever the reply says, it is safe to show; it only lacks the ticket.
                blocks_reply=False,
            )
        )

    if in_conversation and not has_ticket and "escalate_to_human" not in tools_used and promises_ticket(reply):
        violations.append(
            Violation(
                "promised_ticket_missing",
                "the reply said a ticket was being created or the chat handed over, "
                "but no ticket exists",
                correctable=True,
                fix_hint=(
                    "Your reply says you are creating a ticket or handing over to the "
                    "team, but you have not done it. Call escalate_to_human now, with a "
                    "summary of what the customer wants, and give them the ticket "
                    "number. You may also ask for details the team will need."
                ),
                # The reply is fine; it is only missing the ticket it promised.
                blocks_reply=False,
            )
        )

    if (
        in_conversation
        and customer_message is not None
        and not has_ticket
        and "escalate_to_human" not in tools_used
        and is_upset(customer_message)
    ):
        violations.append(
            Violation(
                "upset_customer_not_escalated",
                "the customer is upset and no ticket was created",
                correctable=True,
                fix_hint=(
                    "The customer is upset. Acknowledge how they feel, then call "
                    "escalate_to_human now with the reason upset_customer, summarising "
                    "what they said, and give them the ticket number. You may also ask "
                    "for details the team will need, such as an order ID."
                ),
                # The reply itself is fine; it is only missing the ticket.
                blocks_reply=False,
            )
        )

    hidden_terms = find_hidden_tech_terms(reply, shop_text or "")
    if hidden_terms:
        violations.append(
            Violation(
                "identity_leak",
                "reply named an AI model, AI company, or cloud service: "
                + ", ".join(hidden_terms),
                correctable=True,
                fix_hint=(
                    "Do not name, confirm, or deny any AI model, AI company, or cloud "
                    "service, and do not repeat such a name from the customer's message. "
                    f'If asked what you are, say: "{IDENTITY_REPLY}" If asked about '
                    "something unrelated to the shop, say you can only help with shop "
                    "questions."
                ),
                safe_reply=IDENTITY_REPLY,
            )
        )

    if claims_to_be_human(reply):
        violations.append(
            Violation(
                "human_claim",
                "reply said or implied the assistant is a human",
                correctable=True,
                fix_hint=(
                    "You are an AI. Say you are an AI virtual assistant for the shop and "
                    "offer to hand over to a human team member."
                ),
                safe_reply=AI_NOT_HUMAN_REPLY,
            )
        )

    if tools_used is not None and is_unanswered_shop_question(reply, tools_used):
        violations.append(
            Violation(
                "handover_missing",
                "the shop's documents did not answer the customer's question and no "
                "ticket was created",
                correctable=True,
                fix_hint=(
                    "Call escalate_to_human now with the reason outside_shop_documents, "
                    "then tell the customer what you could not find and give them the "
                    "ticket number. Do not ask whether they would like a ticket, and do "
                    "not point them to the support email instead."
                ),
                # The reply is honest; it is only missing the ticket.
                blocks_reply=False,
            )
        )

    if sources is not None:
        ungrounded = find_ungrounded_figures(reply, sources)
        if ungrounded:
            violations.append(
                Violation(
                    "ungrounded_figure",
                    "reply contained figures or dates not found in the shop's documents, "
                    f"order data, or a tool result: {', '.join(sorted(set(ungrounded)))}",
                    # Often an honest slip or a figure the model worked out
                    # itself, so it is worth one rewrite.
                    correctable=True,
                    fix_hint=(
                        "Use only prices, percentages, time periods, and dates that "
                        "appear in the tool results. For a deadline, call calculate_date "
                        "and quote the date it returns. List amounts as the policy states "
                        "them instead of calculating a total."
                    ),
                )
            )

    allowed = {email.lower() for email in allowed_emails}
    leaked = {email for email in EMAIL_PATTERN.findall(reply) if email.lower() not in allowed}
    if leaked:
        # The addresses themselves are not put in the detail, so they are not
        # copied into tickets or logs.
        violations.append(
            Violation("personal_data", f"reply contained {len(leaked)} email address(es) of other people")
        )

    if claims_refund(reply, shop_text):
        violations.append(
            Violation(
                "refund_claim",
                "reply said a refund or return is given or approved, but the refund rules did not approve it",
            )
        )

    return violations


@dataclass
class Budget:
    """Tracks spending for one conversation and says when to stop.

    There are two limits: tokens used for a single customer message (catches an
    agent going round in circles), and estimated cost of the whole conversation
    (catches a very long or abusive chat).
    """

    max_tokens_per_message: int
    max_cost_per_conversation_usd: float
    input_price_per_million_tokens: float
    output_price_per_million_tokens: float
    message_tokens: int = 0
    conversation_cost_usd: float = 0.0

    def start_message(self) -> None:
        self.message_tokens = 0

    def cost_of(self, input_tokens: int, output_tokens: int) -> float:
        """Estimated cost in US dollars of the given number of tokens."""
        cost = (
            input_tokens * self.input_price_per_million_tokens
            + output_tokens * self.output_price_per_million_tokens
        ) / 1_000_000
        return round(cost, 6)

    def record(self, input_tokens: int, output_tokens: int) -> None:
        self.message_tokens += input_tokens + output_tokens
        self.conversation_cost_usd += self.cost_of(input_tokens, output_tokens)

    def exceeded(self) -> str | None:
        """Return a short description of the limit that was hit, or None."""
        if self.message_tokens >= self.max_tokens_per_message:
            return f"token limit for one message reached ({self.message_tokens} tokens)"
        if self.conversation_cost_usd >= self.max_cost_per_conversation_usd:
            return f"cost limit for the conversation reached (${self.conversation_cost_usd:.4f})"
        return None
