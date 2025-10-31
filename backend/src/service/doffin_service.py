"""Business logic for the Doffin data"""

import os
from dotenv import load_dotenv
from ..clients.doffin_client import DoffinClient
from ..service.ssb_service import SSBService

# Load environment variables
load_dotenv()

class DoffinService:
    """Handles Doffin business logic and data transformations"""

    def __init__(self):
        """Initialize service with API key from environment."""
        api_key = os.getenv("DOFFIN_API_KEY")
        if not api_key:
            raise ValueError("DOFFIN_API_KEY not found in environment variables.")
        
        self.client = DoffinClient(api_key=api_key)
        self.ssb_service = SSBService(version=2482)

    # TODO : Update the request parameters 
    def search_notices(
            self,
            search_str: str | None = None,
            cpv_codes: list[int] | None = None,
            location_ids: list[str] | None = None,
            status: list[str] | None = None,
            page: int | None  = 1,
            num_hits_per_page: int | None = 100,
    ) -> dict | None:
        """Search for notices with filters."""
        params = {
            "numHitsPerPage": num_hits_per_page,
            "page": page
        }

        if search_str:
            params["searchString"] = search_str

        if cpv_codes:
            params["cpvCode"] = cpv_codes

        if location_ids:
           # Convert location names to codes 
            params["location"] = self._process_location_ids(location_ids=location_ids)

        if status:
            params["status"] = status

        response_raw = self.client.search(params=params)

        return response_raw

        #return self._transform_results(response_raw)

    def _process_location_ids(self, location_ids: list[str]) -> list[str]:
        processed_locations = []
        for loc in location_ids:  
            # Check if it contains any digits (NUTS codes like 'NO081')
            if any(char.isdigit() for char in loc):
                # Already a code
                processed_locations.append(loc)
            else:
                # It's a name, look up the code
                code = self.ssb_service.get_code_by_name(loc, max_level=2)
                if code:
                    processed_locations.append(code)
                else:
                    print(f"Warning: Location '{loc}' not found")

        return processed_locations

    
    # TODO: Implement this when frontend ready to receive data
    def _transform_results(self, raw_data: dict) -> dict:
        ...

if __name__ == "__main__":

    cpv_codes = [72000000, 48000000]
    locations = ['NO081']
    string = "Forsvaret"
    status = ["ACTIVE"]

    service = DoffinService()

    service.search_notices(search_str=string, cpv_codes=cpv_codes,location_ids=locations, num_hits_per_page=5, status=status)