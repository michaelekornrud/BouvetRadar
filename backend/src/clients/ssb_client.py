"""HTTP Client for SSB API interactions."""
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException

from utils import get_logger
from exceptions import ExternalAPIError, APITimeoutError

logger = get_logger(__name__)

class SSBClient:
    """Handles raw HTTP communication with the SSB Klass API."""
    
    BASE_URL = "https://data.ssb.no/api/klass/v1"
    DEFAULT_TIMEOUT = 30  # seconds
    
    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        """Initialize SSB client.
        
        Args:
            timeout: Request timeout in seconds (default: 30)
        """
        self.timeout = timeout
        self.headers = {
            'Accept': 'text/csv',
            'charset': 'ISO-8859-1'
        }
    
    def get_classification_version(self, version_id: str) -> requests.Response:
        """Fetch classification data for a specific version.
        
        Args:
            version_id: The classification version identifier (e.g., "1426")
            
        Returns:
            Response object containing CSV data
            
        Raises:
            APITimeoutError: If request times out
            ExternalAPIError: If API returns error or network issues occur
            
        Example:
            client = SSBClient()
            response = client.get_classification_version("1426")
            csv_data = response.text
        """
        url = f"{self.BASE_URL}/versions/{version_id}"
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response
            
        except Timeout as e:
            logger.exception(f"Timeout Error: {e}")
            raise APITimeoutError(
                service="SSB Klass API",
                timeout_seconds=self.timeout
            ) from e
            
        except HTTPError as e:
            logger.exception(f"HTTP Error: {e}")
            status_code = e.response.status_code if e.response is not None else 'unknown'
            raise ExternalAPIError(
                f"SSB API returned error status {status_code}",
                service="SSB Klass API",
                original_error=e
            ) from e
            
        except ConnectionError as e:
            logger.exception(f"Connection Error: {e}")
            raise ExternalAPIError(
                "Connection to SSB API failed",
                service="SSB Klass API",
                original_error=e
            ) from e
            
        except RequestException as e:
            logger.exception(f"Request Exception: {e}")
            raise ExternalAPIError(
                "Unexpected error calling SSB API",
                service="SSB Klass API",
                original_error=e
            ) from e