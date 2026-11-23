
import asyncio

import httpx
import pytest

from enterprise_data_agent.http_client import (
    ResilientAPIClient,
)


def test_successful_request():
    """正常 HTTP 请求。"""

    def handler(request):
        return httpx.Response(
            status_code=200,
            json={"status": "ok"},
        )

    async def scenario():
        transport = httpx.MockTransport(handler)

        async with ResilientAPIClient(
            base_url="https://example.com",
            transport=transport,
        ) as client:
            return await client.get("/health")

    result = asyncio.run(scenario())

    assert result == {"status": "ok"}


def test_retry_after_503():
    """第一次 503，第二次 200。"""

    attempts = 0

    def handler(request):
        nonlocal attempts
        attempts += 1

        if attempts == 1:
            return httpx.Response(
                status_code=503,
                json={"error": "temporarily unavailable"},
            )

        return httpx.Response(
            status_code=200,
            json={"result": "success"},
        )

    async def scenario():
        transport = httpx.MockTransport(handler)

        async with ResilientAPIClient(
            base_url="https://example.com",
            max_retries=2,
            transport=transport,
        ) as client:
            return await client.get("/test")

    result = asyncio.run(scenario())

    assert result == {"result": "success"}
    assert attempts == 2


def test_401_is_not_retried():
    """401 是认证错误，不应自动重试。"""

    attempts = 0

    def handler(request):
        nonlocal attempts
        attempts += 1

        return httpx.Response(
            status_code=401,
            json={"error": "unauthorized"},
        )

    async def scenario():
        transport = httpx.MockTransport(handler)

        async with ResilientAPIClient(
            base_url="https://example.com",
            max_retries=2,
            transport=transport,
        ) as client:
            await client.get("/protected")

    with pytest.raises(httpx.HTTPStatusError):
        asyncio.run(scenario())

    assert attempts == 1


def test_retry_limit():
    """持续 503，必须在最大尝试次数后停止。"""

    attempts = 0

    def handler(request):
        nonlocal attempts
        attempts += 1

        return httpx.Response(
            status_code=503,
            json={"error": "unavailable"},
        )

    async def scenario():
        transport = httpx.MockTransport(handler)

        async with ResilientAPIClient(
            base_url="https://example.com",
            max_retries=2,
            transport=transport,
        ) as client:
            await client.get("/unavailable")

    with pytest.raises(httpx.HTTPStatusError):
        asyncio.run(scenario())

    # 首次请求 + 2 次重试
    assert attempts == 3
