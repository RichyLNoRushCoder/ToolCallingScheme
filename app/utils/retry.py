from collections.abc import Awaitable, Callable
from tenacity import AsyncRetrying, RetryError, stop_after_attempt, wait_exponential


async def retry_async(
    fn: Callable[[], Awaitable],
    attempts: int,
    min_wait: float = 0.2,
    max_wait: float = 1.5,
):
    try:
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(attempts),
            wait=wait_exponential(multiplier=min_wait, max=max_wait),
            reraise=True,
        ):
            with attempt:
                return await fn()
    except RetryError as exc:
        raise exc.last_attempt.exception()  # pragma: no cover
