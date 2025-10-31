""" Custom exceptions for external API handling in BouvetRadar Backend.

    All error codes defined in error_codes.py needs to be
    implemented here, else they are redundant. 
"""

from exceptions.error_codes import ErrorCodes
from exceptions.bouvet_radar_ecxeption import BouvetRadarException
    

class ExternalAPIError(BouvetRadarException):
    """Raised when an external API call fails."""
    def __init__(self, message: str, service: str, original_error: Exception | None = None):
        # Map service name to error code
        error_code_map = {
            "Doffin": ErrorCodes.DOFFIN_API_ERROR,
            "SSB": ErrorCodes.SSB_API_ERROR,
            "NAV": ErrorCodes.NAV_API_ERROR
        }
        error_code = error_code_map.get(service, ErrorCodes.DOFFIN_API_ERROR)
        
        details = {
            "service": service,
            "original_error": str(original_error) if original_error else None
        }
        
        super().__init__(
            f"{service} API Error: {message}",
            status_code=502,
            error_code=error_code,
            details=details
        )

class APITimeoutError(BouvetRadarException):
    """Raised when an external API call times out."""
    def __init__(self, service: str, timeout_seconds: int):
        super().__init__(
            f"{service} API request timed out after {timeout_seconds} seconds",
            status_code=504,
            error_code=ErrorCodes.API_TIMEOUT,
            details={
                "service": service,
                "timeout_seconds": timeout_seconds
            }
        )

