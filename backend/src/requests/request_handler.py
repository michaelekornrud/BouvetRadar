"""Backend request handler module."""

from aiohttp.client import ClientSession, ClientTimeout
from aiohttp import ClientResponseError, ClientConnectorError, ClientError
from asyncio.exceptions import TimeoutError, CancelledError


class AsyncRequestHandler:
    """Asynchronous HTTP request handler using aiohttp."""

    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout

    async def fetch(self, url: str) -> str:
        """Fetch data from the given URL asynchronously."""
        timeout = ClientTimeout(total=self.timeout)
        async with ClientSession(timeout=timeout) as session:
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.text()
            except (ClientResponseError, ClientConnectorError, TimeoutError, ClientError) as e:
                print(f"Request failed: {e}")
                return ""
            except CancelledError:
                print("Request was cancelled.")
                return ""   


class SyncRequestHandler:
    """Synchronous HTTP request handler using requests."""

    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout

    def fetch(self, url: str) -> str:
        """Fetch data from the given URL synchronously."""
        import requests

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return ""