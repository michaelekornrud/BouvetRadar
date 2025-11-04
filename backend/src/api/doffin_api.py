"""
API endpoint(s) for Doffin data
Provides RESTful access to Doffin data for frontend visualization
"""

from flask import jsonify, Blueprint, request
from ..service.doffin_service import DoffinService
from ..validation.doffin_validators import DoffinSearchParams

from exceptions import (
    APITimeoutError,
    ExternalAPIError, 
    ValidationError,
    InvalidParameterTypeError
)

doffin_bp = Blueprint('doffin', __name__, url_prefix='/api/doffin')

@doffin_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    """Handle validation errors."""
    return jsonify({
        "success": False,
        "error": str(e)
    }), 400


@doffin_bp.errorhandler(InvalidParameterTypeError)
def handle_invalid_parameter_type(e):
    """Handle invalid parameter type errors."""
    return jsonify({
        "success": False,
        "error": str(e)
    }), 400

# TODO: Add logger to log the error details
@doffin_bp.errorhandler(ExternalAPIError)
def handle_external_api_error(e):
    """Handle external API errors."""
    return jsonify({
        "success": False,
        "error": "An error occurred while communicating with an external service"
    }), 502

# TODO: Add logger to log the error details
@doffin_bp.errorhandler(APITimeoutError)
def handle_api_timeout(e):
    """Handle API timeout errors."""
    return jsonify({
        "success": False,
        "error": "Request timed out"
    }), 504

# TODO: Add logger to log the error details
@doffin_bp.errorhandler(500)
def handle_internal_error(e):
    """Handle unexpected internal errors."""
    # Log the error here for debugging
    return jsonify({
        "success": False,
        "error": "An internal error occurred"
    }), 500


@doffin_bp.route('/search', methods=['GET'])
def search_doffin_for_data():
    """Search for data based on input on the Doffin API"""
    
    # Validate all parameters
    params = DoffinSearchParams.from_request_args(request.args)
    
    # Call service
    service = DoffinService()
    result = service.search_notices(
        search_str=params.search_str,
        cpv_codes=params.cpv_codes,
        location_ids=params.location_ids,
        status=params.status,
        page=params.page,
        num_hits_per_page=params.hits_per_page
    )
    return jsonify(result)

    