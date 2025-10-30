"""
API endpoint(s) for Doffin data
Provides RESTful access to Doffin data for frontend visualization
"""

import requests

from flask import jsonify, Blueprint, request
from ..service.doffin_service import DoffinService
from ..validation.doffin_validators import (
    validate_hits_per_page,
    validate_page,
    validate_search_str,
    validate_cpv_codes,
    validate_location_ids,
    validate_status
)

from exceptions import APITimeoutError, ExternalAPIError

doffin_bp = Blueprint('doffin', __name__, url_prefix='/api/doffin')

@doffin_bp.route('/search', methods=['GET'])
def search_doffin_for_data():
    """Search for data based on input on the Doffin API"""
    
    # Validate all parameters
    search_str = validate_search_str(request.args.get('search'))
    cpv_codes = validate_cpv_codes(request.args.get('cpvCodes'))
    location_ids = validate_location_ids(request.args.get('locationIds'))
    status = validate_status(request.args.get('status'))
    hits_per_page = validate_hits_per_page(request.args.get('hitsPerPage', '100'))
    page = validate_page(request.args.get('page', '1'))
    
    # Call service
    try:
        service = DoffinService()
        result = service.search_notices(
            search_str=search_str,
            cpv_codes=cpv_codes,
            location_ids=location_ids,
            status=status,
            page=page,
            num_hits_per_page=hits_per_page
        )
        return jsonify(result)
    except requests.Timeout:
        raise APITimeoutError(service="Doffin", timeout_seconds=30)
    except requests.RequestException as e:
        raise ExternalAPIError(
            message="Failed to connect to Doffin API",
            service="Doffin",
            original_error=e
        )
    