"""General test utilities and fixtures."""

import sys
from pathlib import Path
import pytest


# Ensure "backend/src" is on sys.path so tests can import the module
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class FakeAiohttpResponse:
    """A fake aiohttp response for testing purposes."""
    
    def __init__(self, text="", raise_exc: Exception | None = None):
        self._text = text
        self._raise_exc = raise_exc

    async def __aenter__(self):
        if self._raise_exc:
            raise self._raise_exc
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        return False
    
    def raise_for_status(self):
        if self._raise_exc:
            raise self._raise_exc
    
    async def text(self):
        return self._text
    

class FakeAiohttpSession:
    """A fake aiohttp ClientSession for testing purposes."""
    
    def __init__(self, response_or_exc):
        self._response_or_exc = response_or_exc

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        return False
    
    def get(self, url: str):
        if isinstance(self._response_or_exc, BaseException):
            raise self._response_or_exc
        return self._response_or_exc
    

@pytest.fixture
def patch_client_session(monkeypatch):
    """Factory to patch aiohttp.ClientSession with a fake."""
    def _apply(*, text: str | None = None, exc: BaseException | None = None):
        # Patch in the request_handler module where ClientSession is imported
        import requests.request_handler as rh
        obj = exc if exc is not None else FakeAiohttpResponse(text or "OK")
        monkeypatch.setattr(rh, "ClientSession", lambda timeout=None: FakeAiohttpSession(obj))
    return _apply


class _FakeResp:
    def __init__(self, text="OK", raise_exc: Exception | None = None):
        self.text = text
        self._raise_exc = raise_exc
    def raise_for_status(self):
        if self._raise_exc:
            raise self._raise_exc

class _FakeRequests:
    class exceptions:
        class RequestException(Exception): ...
        class Timeout(RequestException): ...
        class HTTPError(RequestException): ...
    def __init__(self, resp_or_exc):
        self._resp_or_exc = resp_or_exc
    def get(self, url, timeout=None):
        if isinstance(self._resp_or_exc, BaseException):
            raise self._resp_or_exc
        return self._resp_or_exc

@pytest.fixture
def install_requests(monkeypatch):
    """Factory to inject a fake 'requests' module with desired behavior."""
    def _apply(*, text: str | None = None, exc: BaseException | None = None):
        fake = _FakeRequests(_FakeResp(text or "OK")) if exc is None else _FakeRequests(exc)
        monkeypatch.setitem(sys.modules, "requests", fake)
        return fake
    return _apply        

if __name__ == "__main__":

    print(f"TESTS: ROOT={ROOT}, SRC={SRC}")