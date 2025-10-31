"""Internal API exceptions for the backend module."""

from exceptions.error_codes import ErrorCodes
from exceptions.bouvet_radar_ecxeption import BouvetRadarException
    

class InternalServerError(BouvetRadarException):
    """Raised when an internal server error occurs."""
    def __init__(self, message: str = "An internal server error occurred", context: dict | None = None):
        super().__init__(
            message,
            status_code=500,
            error_code=ErrorCodes.INTERNAL_SERVER_ERROR,
            details=context or {}
        )

class DatabaseError(BouvetRadarException):
    """Raised when a database operation fails."""
    def __init__(self, message: str, operation: str | None = None, original_error: Exception | None = None):
        details = {}
        if operation:
            details["operation"] = operation
        if original_error:
            details["original_error"] = str(original_error)
            
        super().__init__(
            f"Database error: {message}",
            status_code=500,
            error_code=ErrorCodes.DATABASE_ERROR,
            details=details
        )

class ConfigurationError(BouvetRadarException):
    """Raised when there is a configuration issue."""
    def __init__(self, message: str, missing_config: str | None = None):
        details = {}
        if missing_config:
            details["missing_config"] = missing_config
            
        super().__init__(
            f"Configuration error: {message}",
            status_code=500,
            error_code=ErrorCodes.CONFIGURATION_ERROR,
            details=details
        )

