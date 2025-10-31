"""Validation logic for Doffin API endpoints."""

from exceptions import ValidationError, InvalidParameterTypeError


def validate_hits_per_page(hits_per_page_str: str) -> int:
    """Validate and convert hitsPerPage parameter.
    
    Args:
        hits_per_page_str: String value from request
        
    Returns:
        Validated integer value
        
    Raises:
        InvalidParameterTypeError: If value is not a valid integer
        ValidationError: If value is out of range
    """
    try:
        hits_per_page = int(hits_per_page_str)
        if hits_per_page < 1 or hits_per_page > 1000:
            raise ValidationError(
                "hitsPerPage must be between 1 and 1000",
                field="hitsPerPage",
                value=str(hits_per_page)
            )
        return hits_per_page
    except ValueError:
        raise InvalidParameterTypeError(
            parameter="hitsPerPage",
            expected_type="integer",
            received_value=hits_per_page_str
        )


def validate_page(page_str: str) -> int:
    """Validate and convert page parameter.
    
    Args:
        page_str: String value from request
        
    Returns:
        Validated integer value
        
    Raises:
        InvalidParameterTypeError: If value is not a valid integer
        ValidationError: If value is less than 1
    """
    try:
        page = int(page_str)
        if page < 1:
            raise ValidationError(
                "page must be greater than 0",
                field="page",
                value=str(page)
            )
        return page
    except ValueError:
        raise InvalidParameterTypeError(
            parameter="page",
            expected_type="integer",
            received_value=page_str
        )


def validate_search_str(search_str: str | None) -> str | None:
    """Validate search string parameter.
    
    Args:
        search_str: Search string from request
        
    Returns:
        Validated search string or None
        
    Raises:
        ValidationError: If search string is empty
    """
    if search_str and len(search_str.strip()) == 0:
        raise ValidationError(
            "search parameter cannot be empty",
            field="search"
        )
    return search_str


def validate_cpv_codes(cpv_codes_list: list[str] | None) -> list[str] | None:
    """Validate CPV codes parameter.
    
    CPV codes should be numeric strings (e.g., '48000000').
    
    Args:
        cpv_codes_list: List of CPV codes from request
        
    Returns:
        List of validated CPV codes or None
        
    Raises:
        ValidationError: If any CPV code format is invalid
    """
    if not cpv_codes_list:
        return None
    
    # Strip whitespace and filter empty strings
    cpv_codes = [code.strip() for code in cpv_codes_list if code and code.strip()]
    
    if not cpv_codes:
        return None
    
    # Find invalid codes (not all digits)
    invalid_codes = [code for code in cpv_codes if not code.isdigit()]
    
    if invalid_codes:
        raise ValidationError(
            f"Invalid CPV code format (must be numeric): {', '.join(invalid_codes)}",
            field="cpvCodes",
            value=str(invalid_codes)
        )
    
    return cpv_codes


def validate_location_ids(location_ids_list: list[str] | None) -> list[str] | None:
    """Validate location IDs parameter.
    
    Location IDs can be NUTS codes (alphanumeric, e.g., 'NO081') or location names.
    
    Args:
        location_ids_list: List of location IDs from request
        
    Returns:
        List of validated and stripped location IDs or None
        
    Raises:
        ValidationError: If location IDs are empty after stripping
    """
    if not location_ids_list:
        return None
    
    # Strip whitespace and filter empty strings
    location_ids = [loc.strip() for loc in location_ids_list if loc and loc.strip()]
    
    if not location_ids:
        raise ValidationError(
            "Location IDs cannot be empty",
            field="locationIds",
            value=str(location_ids_list)
        )
    
    return location_ids


def validate_status(status: list[str] | None) -> list[str] | None:
    """Validate status parameter.
    
    Args:
        status: Status string from request
        
    Returns:
        Validated status or None
        
    Raises:
        ValidationError: If status is not valid
    """
    if not status:
        return None
    status_list = []
    valid_statuses = ['active', 'expired', 'cancelled', 'awarded']
    for stat in status:
        if stat.lower() not in valid_statuses:
            raise ValidationError(
                f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
                field="status",
                value=status
            )
        status_list.append(stat.upper())
    return status_list
