""" Custom exceptions for resource handling in BouvetRadar Backend.

    All error codes defined in error_codes.py needs to be
    implemented here, else they are redundant. 
"""

from exceptions.error_codes import ErrorCodes
from exceptions.bouvet_radar_ecxeption import BouvetRadarException
    

class NotFoundError(BouvetRadarException):
    """Raised when a requested resource is not found."""
    def __init__(self, message: str, resource_type: str | None = None, resource_id: str | None = None):
        details = {}
        
        if resource_type:
            details["resource_type"] = resource_type
        if resource_id:
            details["resource_id"] = resource_id
            
        super().__init__(
            message,
            status_code=404,
            error_code=ErrorCodes.RESOURCE_NOT_FOUND,
            details=details
        )

class CPVCodeNotFoundError(BouvetRadarException):
    """Raised when a CPV code is not found."""
    def __init__(self, code: int):
        super().__init__(
            f"CPV code {code} not found",
            status_code=404,
            error_code=ErrorCodes.CPV_CODE_NOT_FOUND,
            details={"cpv_code": code}
        )

class NUTSCodeNotFoundError(BouvetRadarException):
    """Raised when a NUTS code is not found."""
    def __init__(self, code: str):
        super().__init__(
            f"NUTS code {code} not found",
            status_code=404,
            error_code=ErrorCodes.NUTS_CODE_NOT_FOUND,
            details={"nuts_code": code}
        )

class STYRKCodeNotFoundError(BouvetRadarException):
    """Raised when a STYRK code is not found."""
    def __init__(self, code: str):
        super().__init__(
            f"STYRK code {code} not found",
            status_code=404,
            error_code=ErrorCodes.STYRK_CODE_NOT_FOUND,
            details={"styrk_code": code}
        )

