"""Custom exceptions package for BouvetRadar Backend.

This package provides a comprehensive exception hierarchy for handling
various error scenarios throughout the application.
"""

# Error codes
from exceptions.error_codes import ErrorCodes

# Base exception
from exceptions.bouvet_radar_ecxeption import BouvetRadarException

# Validation exceptions (1000-1999)
from exceptions.validation_exceptions import (
    ValidationError,
    MissingParameterError,
    InvalidParameterTypeError
)

# Internal API exceptions (2000-2999)
from exceptions.internal_api_exceptions import (
    InternalServerError,
    DatabaseError,
    ConfigurationError
)

# External API exceptions (3000-3999)
from exceptions.external_api_exceptions import (
    APITimeoutError,
    ExternalAPIError
)

# Processing exceptions (4000-4999)
from exceptions.processing_exceptions import (
    DataProcessingError,
    TransformationError,
    ParsingError
)

# Resource exceptions (5000-5999)
from exceptions.resource_exceptions import (
    NotFoundError,
    CPVCodeNotFoundError,
    NUTSCodeNotFoundError,
    STYRKCodeNotFoundError
)

__all__ = [
    # Error codes
    'ErrorCodes',
    
    # Base
    'BouvetRadarException',
    
    # Validation (1000-1999)
    'ValidationError',
    'MissingParameterError',
    'InvalidParameterTypeError',
    
    # Internal (2000-2999)
    'InternalServerError',
    'DatabaseError',
    'ConfigurationError',
    
    # External API (3000-3999)
    'APITimeoutError',
    'ExternalAPIError',
    
    # Processing (4000-4999)
    'DataProcessingError',
    'TransformationError',
    'ParsingError',
    
    # Resource (5000-5999)
    'NotFoundError',
    'CPVCodeNotFoundError',
    'NUTSCodeNotFoundError',
    'STYRKCodeNotFoundError'
]