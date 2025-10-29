"""HTTP Client for SSB API interactions."""
import requests

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
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return ""