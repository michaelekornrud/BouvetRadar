""" Custom exceptiosn for BouvetRadar Backend.

    All error codes defined in error_codes.py needs to be
    implemented here, else they are redundant. 
"""


from exceptions.error_codes import ErrorCodes
from exceptions import BouvetRadarException
    

class ValidationError(BouvetRadarException):
    """Raised when input validation fails."""
    def __init__(self, message: str, field: str | None = None, value: str | None = None):
        details = {}
        
        if field:
            details["field"] = field
        if value is not None:
            details["received_value"] = str(value)
        
        super().__init__(
            message, 
            status_code=400,
            error_code=ErrorCodes.INVALID_INPUT,
            details=details
        )

class MissingParameterError(BouvetRadarException):
    """Raised when required parameters are missing."""
    def __init__(self, parameter: str):
        super().__init__(
            f"Missing required parameter: {parameter}",
            status_code=400,
            error_code=ErrorCodes.MISSING_PARAMETER,
            details={"missing_parameter": parameter}
        )

class InvalidParameterTypeError(BouvetRadarException):
    """Raised when parameter has wring type"""
    def __init__(self, parameter: str, expected_type: str, received_value: str):
        super().__init__(
            f"Invalid type for parameter '{parameter}'. Expected {expected_type}",
            status_code=400,
            error_code=ErrorCodes.INVALID_PARAMETER_TYPE,
            details={
                "parameter": parameter,
                "expected_type": expected_type,
                "received_value": received_value
            }
        )

