import httpx
# from httpx import RequestError, HTTPStatusError
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import Any
from app.schemas.message import MessageSchema


# Retry up to 3 times, with exponential backoff (1s > 2s > 4s) on exceptions
@retry(stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=1, max=10))
async def send_to_provider(payload: MessageSchema) -> Any:
    """
    Sends the given MessageSchema payload to the external provider API.
    Raises on network or HTTP errors, allowing Tenacity to retry on failures.
    """
    url = "https://provider.app/api/messages"  # 3rd party URL
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(url, json=payload.model_dump(mode="json"))
        response.raise_for_status()
        return response.json()
