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


def validate_cpv_codes(cpv_codes_str: str | None) -> list[str] | None:
    """Validate CPV codes parameter.
    
    Args:
        cpv_codes_str: Comma-separated CPV codes from request
        
    Returns:
        List of validated CPV codes or None
        
    Raises:
        ValidationError: If CPV codes format is invalid
    """
    if not cpv_codes_str:
        return None
    
    try:
        cpv_list = [code.strip() for code in cpv_codes_str.split(',')]
        for code in cpv_list:
            if not code.isdigit():
                raise ValidationError(
                    f"Invalid CPV code format: {code}",
                    field="cpvCodes",
                    value=code
                )
        return cpv_list
    except ValidationError:
        raise
    except Exception:
        raise ValidationError(
            "Invalid CPV codes format",
            field="cpvCodes",
            value=cpv_codes_str
        )


def validate_location_ids(location_ids_str: str | None) -> list[str] | None:
    """Validate location IDs parameter.
    
    Args:
        location_ids_str: Comma-separated location IDs from request
        
    Returns:
        List of validated location IDs or None
        
    Raises:
        ValidationError: If location IDs format is invalid
    """
    if not location_ids_str:
        return None
    
    try:
        location_list = [loc.strip() for loc in location_ids_str.split(',')]
        for loc in location_list:
            if not loc.isdigit():
                raise ValidationError(
                    f"Invalid location ID format: {loc}",
                    field="locationIds",
                    value=loc
                )
        return location_list
    except ValidationError:
        raise
    except Exception:
        raise ValidationError(
            "Invalid location IDs format",
            field="locationIds",
            value=location_ids_str
        )


def validate_status(status: str | None) -> str | None:
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
    
    valid_statuses = ['active', 'expired', 'cancelled', 'awarded']
    if status.lower() not in valid_statuses:
        raise ValidationError(
            f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
            field="status",
            value=status
        )
    return status.lower()