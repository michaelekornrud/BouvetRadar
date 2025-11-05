"""BouvetRadar custom exceptions."""

from exceptions.error_codes import ErrorCodes

class BouvetRadarException(Exception):
    """Base exception for all BouvetRadar errors."""

    def __init__(
            self, 
            message: str,
            status_code: int = 500,
            error_code: ErrorCodes | None = None,
            details: dict | None = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Convert exception to dictionary response."""
        result = {
            "success": False,
            "error": self.message
        }
        if self.error_code:
            result["error_code"] = self.error_code.value
            result["error_name"] = self.error_code.name
        if self.details:
            result["details"] = self.details
        return result