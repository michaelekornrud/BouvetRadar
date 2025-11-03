"""HTTP Client for SSB API interactions."""
import requests

from exceptions import ExternalAPIError, APITimeoutError

class SSBClient:
    """Handles raaw HTTP communication with the SSB API."""
    BASE_URL = "https://data.ssb.no/api/klass/v1/versions/"

    def get_version(self, version: str) -> str:
        """Fetch data for a specific version from the SSB API."""
        url = f"{self.BASE_URL}{version}"
        headers = {
            'Accept': 'text/csv',
            'charset': 'ISO-8859-1'
        }

        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise ExternalAPIError("Failed to fetch data from external API.", service="SSB Service", original_error=e) from e
        except requests.Timeout:
            raise APITimeoutError(service="SSB NUTS", timeout_seconds=30) 