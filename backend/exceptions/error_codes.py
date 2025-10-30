""" This module serves the purpose of defining and distributing
    the custom error codes. 
"""

from enum import Enum

class ErrorCodes(Enum):
    """Custom error codes."""

    # Validation errors (1000-1999)
    INVALID_INPUT = 1000
    MISSING_PARAMETER = 1001
    INVALID_PARAMETER_TYPE = 1002

    # Internal API errors (2000-2999)
    


    # External API errors (3000-3999)
    API_TIMEOUT = 3000
    DOFFIN_API_ERROR = 3001
    SSB_API_ERROR = 3002
    NAV_API_ERROR = 3003

    # Parsing errors (4000-4999)
    DATA_PROCESSING_ERROR = 4000

    # Resource errors (5000-5999)
    RESOURCE_NOT_FOUND = 5000
    CPV_CODE_NOT_FOUND = 5001
    NUTS_CODE_NOT_FOUND = 5002
    STYRK_CODE_NOT_FOUND = 5003

