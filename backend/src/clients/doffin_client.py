"""HTTP Client for Doffin API"""

import requests

class DoffinClient:
    """Handles raw HTTP communication with the Doffin API."""
    
    BASE_URL = "https://api.doffin.no/public/v2"

    def __init__(self, api_key: str):
        """Initialize client with API key."""
        self.headers = {
            "Ocp-Apim-Subscription-Key" : api_key
        }

    def search(self, params: dict) -> dict:
        """Make search request to Doffin API."""
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/search",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred: {e}") from e


    def download(self, doffin_id: str) -> bytes:
        """Download the notice by Doffin ID."""

        response = requests.get(
            f"{self.BASE_URL}/download/{doffin_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.content