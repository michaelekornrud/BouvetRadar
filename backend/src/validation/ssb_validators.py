"""Validation module for SSB (STYRK & NUTS) related endpoints."""

from exceptions import ValidationError, InvalidParameterTypeError
from src.service.ssb_service import SSBLevel

def validate_nuts_level(level_str: str) -> int:
    """Validate and convert NUTS level parameter.
    
    Args:
        level_str: String value from request

    Returns:
        Validated integer value

    Raises:
        InvalidParameterTypeError: If value is not a valid integer 
        ValidationError: If value is out of range
    """

    try:
        level = int(level_str)
        if level not in [lvl.value for lvl in SSBLevel] or level > 3:
            raise ValidationError(
                "NUTS level must be between 1 and 3",
                field="level",
                value=str(level)
            )
        return level
    except ValueError:
        raise InvalidParameterTypeError(
            parameter="level",
            expected_type="integer",
            received_value=level_str
        )
    
def validate_styrk_level(level_str: str) -> int:
    """Validate and convert STYRK level parameter.
    
    Args:
        level_str: String value from request
    
    Returns:
        Validated integer value

    Raises:
        InvalidParameterTypeError: If value is not a valid integer
        ValidationError: If value is out of range
    """

    try:
        level = int(level_str)
        if level not in [lvl.value for lvl in SSBLevel]:
            raise ValidationError(
                "STYRK level must be between 1 and 4",
                field="level",
                value=str(level)
            )
        return level
    except ValueError:
        raise InvalidParameterTypeError(
            parameter="level",
            expected_type="integer",
            received_value=level_str
        )    
