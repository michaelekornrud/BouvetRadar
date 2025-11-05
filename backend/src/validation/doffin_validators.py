"""Validation logic for Doffin API endpoints."""

from dataclasses import dataclass

from exceptions import ValidationError, InvalidParameterTypeError


@dataclass
class DoffinSearchParams:
    """Validated search parameters for Doffin API requests."""
    
    search_str: str | None = None
    cpv_codes: list[str] | None = None
    location_ids: list[str] | None = None
    status: list[str] | None = None
    hits_per_page: int = 100
    page: int = 1

    @classmethod
    def validate_and_create(cls, args) -> 'DoffinSearchParams':
        """Create validated parameters from Flask request.args.
        
        Args:
            args: Flask request.args object
            
        Returns:
            Validated DoffinSearchParams instance
            
        Raises:
            ValidationError: If any parameter fails validation
            InvalidParameterTypeError: If parameter has wrong type
        """
        return cls(
            search_str=validate_search_str(args.get('search')),
            cpv_codes=validate_cpv_codes(args.getlist('cpvCode')),
            location_ids=validate_location_ids(args.getlist('location')),
            status=validate_status(args.getlist('status')),
            hits_per_page=validate_hits_per_page(args.get('hitsPerPage', '100')),
            page=validate_page(args.get('page', '1'))
        )


def validate_hits_per_page(hits_per_page_str: str) -> int:
    """Validate and convert hitsPerPage parameter.
    
    Args:
        hits_per_page_str: String value from request
        
    Returns:
        Validated integer between 1 and 1000
        
    Raises:
        InvalidParameterTypeError: If value is not a valid integer
        ValidationError: If value is out of valid range
    """
    try:
        hits_per_page = int(hits_per_page_str)
    except ValueError as e:
        raise InvalidParameterTypeError(
            parameter="hitsPerPage",
            expected_type="integer",
            received_value=hits_per_page_str
        ) from e
    
    # Validate range after successful conversion
    if not 1 <= hits_per_page <= 1000:
        raise ValidationError(
            "Parameter 'hitsPerPage' must be between 1 and 1000",
            field="hitsPerPage",
            value=hits_per_page
        )
    
    return hits_per_page


def validate_page(page_str: str) -> int:
    """Validate and convert page parameter.
    
    Args:
        page_str: String value from request
        
    Returns:
        Validated integer greater than 0
        
    Raises:
        InvalidParameterTypeError: If value is not a valid integer
        ValidationError: If value is less than 1
    """
    try:
        page = int(page_str)
    except ValueError as e:
        raise InvalidParameterTypeError(
            parameter="page",
            expected_type="integer",
            received_value=page_str
        ) from e
    
    # Validate range after successful conversion
    if page < 1:
        raise ValidationError(
            "Parameter 'page' must be greater than 0",
            field="page",
            value=page
        )
    
    return page


def validate_search_str(search_str: str | None) -> str | None:
    """Validate search string parameter.
    
    Args:
        search_str: Search string from request
        
    Returns:
        Validated search string or None if not provided/empty
    """
    if not search_str:
        return None
    
    stripped = search_str.strip()
    return stripped if stripped else None


def validate_cpv_codes(cpv_codes_list: list[str]) -> list[str] | None:
    """Validate CPV codes parameter.
    
    CPV codes must be numeric strings (e.g., '48000000').
    
    Args:
        cpv_codes_list: List of CPV codes from request
        
    Returns:
        List of validated CPV codes or None if empty
        
    Raises:
        ValidationError: If any CPV code format is invalid
    """
    if not cpv_codes_list:
        return None
    
    # Strip whitespace and filter empty strings
    cpv_codes = [code.strip() for code in cpv_codes_list if code and code.strip()]
    
    if not cpv_codes:
        return None
    
    # Find all invalid codes at once
    invalid_codes = [code for code in cpv_codes if not code.isdigit()]
    
    if invalid_codes:
        raise ValidationError(
            f"Invalid CPV code format (must be numeric): {', '.join(invalid_codes)}",
            field="cpvCode",
            value=invalid_codes
        )
    
    return cpv_codes


def validate_location_ids(location_ids_list: list[str]) -> list[str] | None:
    """Validate location IDs parameter.
    
    Location IDs can be NUTS codes (e.g., 'NO0301') or county / region names.
    
    Args:
        location_ids_list: List of location IDs from request
        
    Returns:
        List of validated location IDs or None if empty
        
    Raises:
        ValidationError: If all location IDs are empty after stripping
    """

    if not location_ids_list:
        return None
    
    # Strip whitespace and filter empty strings
    location_ids = [loc.strip() for loc in location_ids_list if loc and loc.strip()]
    
    # Consistent with validate_cpv_codes: return None if empty after filtering
    if not location_ids:
        return None
    
    return location_ids


def validate_status(status_list: list[str]) -> list[str] | None:
    """Validate status parameter.
    
    Valid statuses: ACTIVE, EXPIRED, CANCELLED, AWARDED (case-insensitive)
    
    Args:
        status_list: List of status values from request
        
    Returns:
        List of validated statuses in uppercase or None if empty
        
    Raises:
        ValidationError: If any status value is invalid
    """
    if not status_list:
        return None
    
    valid_statuses = {'ACTIVE', 'EXPIRED', 'CANCELLED', 'AWARDED'}
    result = []
    
    for status in status_list:
        status = status.strip().upper()
        if not status:
            continue  # Skip empty strings
        
        if status not in valid_statuses:
            raise ValidationError(
                f"Invalid status '{status}'. Must be one of: {', '.join(sorted(valid_statuses))}",
                field="status",
                value=status
            )
        
        result.append(status)
    
    return result if result else None