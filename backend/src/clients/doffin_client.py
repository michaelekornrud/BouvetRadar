"""HTTP Client for Doffin API"""

import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException

from src.utils import get_logger
from exceptions import ExternalAPIError, APITimeoutError

logger = get_logger(__name__)

class DoffinClient:
    """Handles raw HTTP communication with the Doffin API."""

    
    BASE_URL = "https://api.doffin.no/public/v2"
    DEFAULT_TIMEOUT = 30  # seconds

    def __init__(self, api_key: str, timeout: int = DEFAULT_TIMEOUT):
        """Initialize client with API key."""
        self.headers = {
            "Ocp-Apim-Subscription-Key" : api_key
        }
        self.timeout = timeout

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with consistent error handling.
    
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
            
        Raises:
            APITimeoutError: If request times out
            ExternalAPIError: If API returns error or network issues occur
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response
            
        except Timeout as e:
            logger.exception(f"Timeout exception: {e}")
            raise APITimeoutError(
                f"Doffin API request timed out after {self.timeout}s"
            ) from e
            
        except HTTPError as e:
            # HTTP errors (4xx/5xx responses)
            logger.exception(f"HTTP Error: {e}")
            status_code = e.response.status_code if e.response is not None else 'unknown'
            raise ExternalAPIError(
                f"Doffin API returned error status {status_code}",
                service="Doffin Client",
            ) from e
            
        except ConnectionError as e:
            # Network/connection errors
            logger.exception(f"Failed to connect to Doffin API : {e}")
            status_code = e.response.status_code if e.response is not None else 'unknown'
            raise ExternalAPIError(
                f"Connection to Doffin API failed with status {status_code}",
                service="Doffin Client",
            ) from e
            
        except RequestException as e:
            # Catch-all for any other requests exceptions
            logger.exception(f"Unexpected error callig Doffin API: {e}")
            status_code = e.response.status_code if e.response is not None else 'unknown'
            raise ExternalAPIError(
                f"Unexpected error calling Doffin API, status {status_code}",
                service="Doffin Client",
            ) from e

    def search(self, params: dict) -> dict:
        """Make search request to Doffin API."""
        response = self._make_request('GET', 'search', params=params)
        return response.json()

    def download(self, doffin_id: str) -> bytes:
        """Download notice PDF by Doffin ID."""
        response = self._make_request('GET', f'download/{doffin_id}')
        return response.content