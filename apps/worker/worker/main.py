"""Worker entry point (arq). Queue functions are registered by their owning workstreams."""

import os
from typing import ClassVar

from arq.connections import RedisSettings


def parse_redis_url(url: str) -> RedisSettings:
    from urllib.parse import urlparse

    parsed = urlparse(url)
    return RedisSettings(
        host=parsed.hostname or "localhost",
        port=parsed.port or 6379,
        database=int((parsed.path or "/0").lstrip("/")),
    )


class WorkerSettings:
    """arq worker settings. Functions are added here as workstreams land them."""

    functions: ClassVar[list] = []
    redis_settings = parse_redis_url(os.environ.get("REDIS_URL", "redis://localhost:6379/0"))


def main() -> None:
    from arq import run_worker

    run_worker(WorkerSettings)  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
