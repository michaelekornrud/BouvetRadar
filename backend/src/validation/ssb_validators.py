"""Validation logic for SSB (STYRK & NUTS) related endpoints."""

from exceptions import ValidationError, InvalidParameterTypeError
from src.service.ssb_service import SSBLevel


def validate_nuts_level(level_str: str | None) -> SSBLevel:
    """Validate and convert NUTS level parameter.
    
    NUTS (Nomenclature of Territorial Units for Statistics) levels:
        1 = Landsdel (Region)
        2 = Fylke (County)
        3 = Kommune (Municipality)
    
    Args:
        level_str: String value from request
    
    Returns:
        Validated SSBLevel enum value
    
    Raises:
        InvalidParameterTypeError: If value is not a valid integer
        ValidationError: If value is not a valid NUTS level (1-3)
    """
    if level_str is None:
        raise ValidationError(
            "Parameter 'level' is required",
            field="level",
            value=None
        )
    
    # Convert to integer
    try:
        level = int(level_str)
    except ValueError as e:
        raise InvalidParameterTypeError(
            parameter="level",
            expected_type="integer",
            received_value=level_str
        ) from e
    
    # Validate NUTS level range (1-3)
    if not 1 <= level <= 3:
        raise ValidationError(
            "Parameter 'level' must be between 1 and 3 for NUTS classification",
            field="level",
            value=level
        )
    
    # Convert to enum (safe because we've validated the range)
    return SSBLevel(level)


def validate_styrk_level(level_str: str | None) -> SSBLevel:
    """Validate and convert STYRK level parameter.
    
    STYRK (Standard for yrkesklassifisering) levels:
        1 = Major group
        2 = Sub-major group
        3 = Minor group
        4 = Unit group
    
    Args:
        level_str: String value from request
    
    Returns:
        Validated SSBLevel enum value
    
    Raises:
        InvalidParameterTypeError: If value is not a valid integer
        ValidationError: If value is not a valid STYRK level (1-4)
    """
    if level_str is None:
        raise ValidationError(
            "Parameter 'level' is required",
            field="level",
            value=None
        )
    
    # Convert to integer
    try:
        level = int(level_str)
    except ValueError as e:
        raise InvalidParameterTypeError(
            parameter="level",
            expected_type="integer",
            received_value=level_str
        ) from e
    
    # Validate STYRK level range (1-4)
    if not 1 <= level <= 4:
        raise ValidationError(
            "Parameter 'level' must be between 1 and 4 for STYRK classification",
            field="level",
            value=level
        )
    
    # Convert to enum (safe because we've validated the range)
    return SSBLevel(level)