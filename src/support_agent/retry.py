"""Retries: trying again when something fails for a temporary reason.

Calls to outside services sometimes fail through no fault of ours: the network
drops, the service is busy, or we are sending requests too quickly. Those
failures usually go away if we wait a moment and try again. Other failures,
such as a wrong key or a model that does not exist, will fail every time, so
retrying them only wastes time.

Each wait is longer than the one before ("exponential backoff"), with a little
randomness added ("jitter") so that many conversations retrying at once do not
all hit the service at the same instant.
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


class ServiceError(Exception):
    """A call to an outside service (the model or the embedding model) failed.

    `retryable` says whether trying again could help. `kind` is a short label
    for logs, such as "rate_limit" or "auth". `retry_after` is how many seconds
    the service asked us to wait, when it said.
    """

    def __init__(
        self,
        message: str,
        *,
        service: str,
        kind: str,
        retryable: bool,
        retry_after: float | None = None,
    ) -> None:
        super().__init__(message)
        self.service = service
        self.kind = kind
        self.retryable = retryable
        self.retry_after = retry_after


@dataclass(frozen=True)
class RetryPolicy:
    # Total tries, including the first. 1 means "never retry".
    max_attempts: int = 3
    # Wait before the first retry, in seconds. It doubles for each retry after.
    base_delay: float = 1.0
    # No single wait is longer than this; a customer is waiting for the reply.
    max_delay: float = 8.0
    sleep: Callable[[float], None] = time.sleep

    def delay_before_retry(self, retry_number: int, error: Exception) -> float:
        """How long to wait before retry number 1, 2, 3, ..."""
        asked = getattr(error, "retry_after", None)
        if asked is not None and asked > 0:
            return min(float(asked), self.max_delay)
        delay = min(self.base_delay * 2 ** (retry_number - 1), self.max_delay)
        return delay * random.uniform(0.5, 1.0)


# Called before each wait with: attempt that failed, total attempts, seconds
# to wait, and the error. Used to write the retry to the event log.
OnRetry = Callable[[int, int, float, Exception], None]


def is_retryable(error: Exception) -> bool:
    return bool(getattr(error, "retryable", False))


def call_with_retry(
    operation: Callable[[], T],
    policy: RetryPolicy,
    on_retry: OnRetry | None = None,
    retry_on: Callable[[Exception], bool] = is_retryable,
) -> T:
    """Run `operation`, trying again after temporary failures. When the attempts
    run out, or the failure is not a temporary one, the error is raised."""
    attempt = 1
    while True:
        try:
            return operation()
        except Exception as error:
            if attempt >= policy.max_attempts or not retry_on(error):
                raise
            delay = policy.delay_before_retry(attempt, error)
            if on_retry:
                on_retry(attempt, policy.max_attempts, delay, error)
            policy.sleep(delay)
            attempt += 1
