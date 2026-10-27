"""LLM provider abstraction (D-7).

Default is the deterministic mock provider — tests and CI never touch the network.
The Anthropic provider is only active when LLM_PROVIDER=anthropic and a key is present.
All consumer agents MUST schema-validate outputs and degrade gracefully on failure.
"""

import hashlib
import os
from typing import Protocol


class LLMClient(Protocol):
    async def complete(self, system: str, user: str) -> str: ...


class MockLLMClient:
    """Deterministic offline client. Returns a stable, clearly-marked mock response."""

    async def complete(self, system: str, user: str) -> str:
        digest = hashlib.sha256((system + "\n" + user).encode()).hexdigest()[:12]
        return f'{{"mock": true, "id": "{digest}", "summary": "mock mode: no LLM call made"}}'


class AnthropicLLMClient:
    def __init__(self, api_key: str, model: str) -> None:
        self._api_key = api_key
        self._model = model

    async def complete(self, system: str, user: str) -> str:
        import anthropic  # imported lazily so mock mode has no dependency

        client = anthropic.AsyncAnthropic(api_key=self._api_key)
        resp = await client.messages.create(
            model=self._model,
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(block.text for block in resp.content if block.type == "text")


def get_llm_client() -> LLMClient:
    provider = os.environ.get("LLM_PROVIDER", "mock").lower()
    if provider == "anthropic" and os.environ.get("ANTHROPIC_API_KEY"):
        return AnthropicLLMClient(
            api_key=os.environ["ANTHROPIC_API_KEY"],
            model=os.environ.get("LLM_MODEL", "claude-sonnet-4-5"),
        )
    return MockLLMClient()
