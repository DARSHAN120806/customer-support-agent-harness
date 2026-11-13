"""The tool registry: the list of tools the agent is allowed to use.

A "tool" is an ordinary Python function plus a description the model can read.
The model never runs anything itself. It only asks, by name, for a tool to be
run, and this registry is the single place where that request is carried out.
If a tool is not registered here, the agent cannot use it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


class ToolError(Exception):
    """Raised by a tool when the request cannot be carried out, with a message
    that is safe for the model to read (for example "order_id is missing")."""


@dataclass(frozen=True)
class Tool:
    name: str
    # Read by the model to decide when to use the tool.
    description: str
    # A JSON Schema describing the inputs the tool accepts.
    input_schema: dict[str, Any]
    handler: Callable[[dict[str, Any]], str]
    # True for tools that only look information up. False for tools that do
    # something on the customer's behalf, such as creating a ticket.
    read_only: bool = True


@dataclass(frozen=True)
class ToolResult:
    content: str
    is_error: bool = False


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"A tool named '{tool.name}' is already registered.")
        self._tools[tool.name] = tool

    def names(self) -> list[str]:
        return list(self._tools)

    def is_read_only(self, name: str) -> bool:
        tool = self._tools.get(name)
        return tool is None or tool.read_only

    def definitions(self) -> list[dict[str, Any]]:
        """The tool list in the format the model expects."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema,
            }
            for tool in self._tools.values()
        ]

    def execute(self, name: str, tool_input: dict[str, Any]) -> ToolResult:
        """Run a tool. Never raises: a failure is returned as an error result,
        so the model can see what went wrong and decide what to do next."""
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(f"Error: there is no tool named '{name}'.", is_error=True)
        try:
            return ToolResult(tool.handler(tool_input))
        except ToolError as error:
            return ToolResult(f"Error: {error}", is_error=True)
        except Exception:
            # The details stay out of the conversation on purpose: an internal
            # error message could contain data the customer should not see.
            return ToolResult(f"Error: the tool '{name}' failed to run.", is_error=True)


def require_text(tool_input: dict[str, Any], field: str, max_length: int = 2000) -> str:
    """Read a required text input, or raise a ToolError the model can act on."""
    value = tool_input.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ToolError(f"'{field}' is required and must be text.")
    return value.strip()[:max_length]
