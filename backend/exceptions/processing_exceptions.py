"""Processing exceptions for the backend module."""


from exceptions.error_codes import ErrorCodes
from exceptions.bouvet_radar_ecxeption import BouvetRadarException
    
class DataProcessingError(BouvetRadarException):
    """Raised when a data processing error occurs."""
    def __init__(self, massage: str, operation:str | None = None):
        details = {}

        if operation:
            details["operation"] = operation

        super().__init__(
            message=massage,
            status_code=500,
            error_code=ErrorCodes.DATA_PROCESSING_ERROR,
            details=details
        )

class TransformationError(BouvetRadarException):
    """Raised when data transformation fails."""
    def __init__(self, message: str, source_format: str | None = None, target_format: str | None = None):
        details = {}

        if source_format:
            details["source_format"] = source_format
        if target_format:
            details["target_format"] = target_format
            
        super().__init__(
            message,
            status_code=500,
            error_code=ErrorCodes.TRANSFORMATION_ERROR,
            details=details
        )

class ParsingError(BouvetRadarException):
    """Raised when data parsing fails."""
    def __init__(self, message: str, data_type: str | None = None):
        details = {}
        
        if data_type:
            details["data_type"] = data_type
            
        super().__init__(
            message,
            status_code=500,
            error_code=ErrorCodes.PARSING_ERROR,
            details=details
        )