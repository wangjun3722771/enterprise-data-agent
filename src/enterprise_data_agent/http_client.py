
import asyncio
import logging
import random

import httpx

logger = logging.getLogger(__name__)


class ResilientAPIClient:
    """支持超时、有限重试和日志的 HTTP 客户端。"""

    RETRYABLE_STATUS = {429, 500, 502, 503, 504}

    def __init__(
        self,
        base_url: str,
        max_retries: int = 2,
        timeout: float = 10.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        if max_retries < 0:
            raise ValueError("max_retries 不能为负数")

        self.max_retries = max_retries

        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=httpx.Timeout(timeout),
            transport=transport,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()

    async def get(self, path: str) -> dict | list:
        """只对 GET 请求进行自动重试。"""

        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.get(path)
                response.raise_for_status()

                logger.info(
                    "GET %s 成功，状态码=%s",
                    path,
                    response.status_code,
                )

                return response.json()

            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code

                if status not in self.RETRYABLE_STATUS:
                    logger.error(
                        "不可重试的 HTTP 错误：%s",
                        status,
                    )
                    raise

                error = exc

            except (
                httpx.ConnectTimeout,
                httpx.ReadTimeout,
                httpx.ConnectError,
                httpx.ReadError,
                httpx.RemoteProtocolError,
            ) as exc:
                error = exc

            # 已达到最大重试次数
            if attempt >= self.max_retries:
                logger.error(
                    "请求失败，重试次数已用尽：%s",
                    type(error).__name__,
                )
                raise error

            delay = min(
                5.0,
                0.5 * (2 ** attempt),
            )

            # 添加少量随机抖动
            delay *= random.uniform(0.8, 1.2)

            logger.warning(
                "GET %s 失败：%s，%.2f 秒后重试",
                path,
                type(error).__name__,
                delay,
            )

            await asyncio.sleep(delay)

        raise RuntimeError("不可达的重试状态")
