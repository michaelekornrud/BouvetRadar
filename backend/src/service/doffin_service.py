"""Business logic for the Doffin data."""

import os
import re

from dotenv import load_dotenv

from utils import get_logger
from ..clients.doffin_client import DoffinClient
from ..service.ssb_service import SSBService
from exceptions import ValidationError

# Load environment variables
load_dotenv()
logger = get_logger(__name__)

class DoffinService:
    """Handles Doffin business logic and data transformations."""

    # NUTS code format: 2 uppercase letters + digits (e.g., 'NO081', 'NO0301')
    NUTS_CODE_PATTERN = re.compile(r'^[A-Z]{2}\d+$')

    def __init__(self):
        """Initialize service with API key from environment.
        
        Raises:
            ValueError: If DOFFIN_API_KEY not found in environment
        """
        api_key = os.getenv("DOFFIN_API_KEY")
        if not api_key:
            raise ValueError("DOFFIN_API_KEY not found in environment variables")
        
        self.client = DoffinClient(api_key=api_key)
        self.ssb_service = SSBService(version=2482) 

    def search_notices(
        self,
        search_str: str | None = None,
        cpv_codes: list[str] | None = None, 
        location_ids: list[str] | None = None,
        status: list[str] | None = None,
        page: int = 1,
        num_hits_per_page: int = 100,
    ) -> dict:
        """Search for procurement notices with filters.
        
        Args:
            search_str: Full-text search string
            cpv_codes: List of CPV classification codes (e.g., ['72000000'])
            location_ids: List of NUTS codes (e.g., 'NO081') or names (e.g., 'Oslo')
            status: List of notice statuses (e.g., ['ACTIVE'])
            page: Page number (1-indexed)
            num_hits_per_page: Results per page (1-1000)
            
        Returns:
            Raw API response dictionary
            
        Raises:
            ValidationError: If any location cannot be resolved to a NUTS code
            
        Example:
            service.search_notices(
                search_str="IT services",
                cpv_codes=["72000000"],
                location_ids=["Oslo", "NO081"],  # Both work!
                status=["ACTIVE"]
            )
        """
        params = {
            "numHitsPerPage": num_hits_per_page,
            "page": page
        }

        if search_str:
            params["searchString"] = search_str

        if cpv_codes:
            params["cpvCode"] = cpv_codes

        if location_ids:
            # Convert all locations (codes or names) to validated NUTS codes
            params["location"] = self._resolve_location_ids(location_ids)

        if status:
            params["status"] = status

        logger.info(f"Searching Doffin notices with parameters: {params}")

        return self.client.search(params=params)

    def _resolve_location_ids(self, location_ids: list[str]) -> list[str]:
        """Convert location identifiers to validated NUTS codes.
        
        Accepts both NUTS codes and municipality names, validates them,
        and returns only valid NUTS codes.
        
        Args:
            location_ids: List of NUTS codes or municipality names
            
        Returns:
            List of validated NUTS codes
            
        Raises:
            ValidationError: If any location cannot be resolved
            
        Examples:
            _resolve_location_ids(["Oslo", "NO081"])  # → ["NO0301", "NO081"]
            _resolve_location_ids(["Akershusss"])     # → ValidationError
        """
        resolved_codes = []
        invalid_locations = []
        
        for location in location_ids:
            location = location.strip()
            
            # Case 1: Already a NUTS code format (e.g., 'NO081')
            if self._is_nuts_code_format(location):
                # Verify it exists in the database
                if self.ssb_service.get_description(location):
                    resolved_codes.append(location)
                else:
                    invalid_locations.append(location)
            
            # Case 2: County / Region name (e.g., 'Oslo', 'Akershus')
            else:
                code = self.ssb_service.get_code_by_name(location, max_level=2)
                if code:
                    resolved_codes.append(code)
                else:
                    invalid_locations.append(location)
        
        # Fail fast with clear error message
        if invalid_locations:
            raise ValidationError(
                f"Invalid location(s): '{', '.join(invalid_locations)}'. "
                f"Must be valid NUTS codes (e.g., 'NO081') or "
                f"Norwegian county / region names (e.g., 'Oslo').",
                field="location",
                value=invalid_locations
            )
        
        return resolved_codes

    def _is_nuts_code_format(self, value: str) -> bool:
        """Check if string matches NUTS code format.
        
        NUTS codes consist of:
        - 2 uppercase letters (country code, e.g., 'NO')
        - Followed by digits (hierarchical code, e.g., '081', '0301')
        
        Args:
            value: String to validate
            
        Returns:
            True if matches NUTS pattern, False otherwise
            
        Examples:
            _is_nuts_code_format("NO081")     # → True
            _is_nuts_code_format("NO0301")    # → True
            _is_nuts_code_format("Oslo")      # → False
            _is_nuts_code_format("Oslo123")   # → False (has letters after digits)
            _is_nuts_code_format("no081")     # → False (lowercase)
        """
        return bool(self.NUTS_CODE_PATTERN.match(value))


if __name__ == "__main__":
    # Example usage with both codes and names
    cpv_codes = ["72000000", "48000000"]  # ✅ Strings, not ints
    locations = ["NO081", "Oslo", "Akershus"]  # Mix of codes and names
    search_string = "Forsvaret"
    status = ["ACTIVE"]

    service = DoffinService()
    
    try:
        results = service.search_notices(
            search_str=search_string,
            cpv_codes=cpv_codes,
            location_ids=locations,
            num_hits_per_page=5,
            status=status
        )
        print(f"Found {results.get('totalHits', 0)} notices")
        
    except ValidationError as e:
        print(f"Validation error: {e}")