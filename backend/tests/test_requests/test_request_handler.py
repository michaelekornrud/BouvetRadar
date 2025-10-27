import pytest
from asyncio.exceptions import TimeoutError as AsyncTimeoutError, CancelledError
from aiohttp import ClientError

from requests.request_handler import AsyncRequestHandler, SyncRequestHandler

# -------- AsyncRequestHandler tests --------

@pytest.mark.asyncio
async def test_async_fetch_success(patch_client_session):
    patch_client_session(text="OK")
    handler = AsyncRequestHandler(timeout=1)
    assert await handler.fetch("http://example.com") == "OK"

@pytest.mark.asyncio
async def test_async_fetch_timeout_returns_empty(patch_client_session):
    patch_client_session(exc=AsyncTimeoutError())
    handler = AsyncRequestHandler(timeout=1)
    assert await handler.fetch("http://example.com") == ""

@pytest.mark.asyncio
async def test_async_fetch_client_error_returns_empty(patch_client_session):
    patch_client_session(exc=ClientError("boom"))
    handler = AsyncRequestHandler(timeout=1)
    assert await handler.fetch("http://example.com") == ""

@pytest.mark.asyncio
async def test_async_fetch_cancelled_returns_empty(patch_client_session):
    patch_client_session(exc=CancelledError())
    handler = AsyncRequestHandler(timeout=1)
    assert await handler.fetch("http://example.com") == ""

# -------- SyncRequestHandler tests --------

def test_sync_fetch_success(install_requests):
    install_requests(text="Hello")
    handler = SyncRequestHandler(timeout=1)
    assert handler.fetch("http://example.com") == "Hello"

def test_sync_fetch_http_error_returns_empty(install_requests):
    # Simulate requests.exceptions.HTTPError
    from conftest import _FakeRequests  # type: ignore
    install_requests(exc=_FakeRequests.exceptions.HTTPError("bad"))
    handler = SyncRequestHandler(timeout=1)
    assert handler.fetch("http://example.com") == ""

def test_sync_fetch_timeout_returns_empty(install_requests):
    from conftest import _FakeRequests  # type: ignore
    install_requests(exc=_FakeRequests.exceptions.Timeout())
    handler = SyncRequestHandler(timeout=1)
    assert handler.fetch("http://example.com") == ""