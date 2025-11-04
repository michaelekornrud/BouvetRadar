"""
API endpoints for NUTS codes
Provides RESTful access to NUTS data for frontend visualization
"""

from flask import jsonify, Blueprint, request

from ..service.ssb_service import NUTSService
from ..validation.ssb_validators import validate_nuts_level
from exceptions import (
    APITimeoutError, 
    ExternalAPIError, 
    ValidationError, 
    InvalidParameterTypeError
)

nuts_bp = Blueprint('nuts', __name__, url_prefix='/api/nuts')

@nuts_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    """Handle validation errors."""
    return jsonify({
        "success": False,
        "error": str(e)
    }), 400

@nuts_bp.errorhandler(InvalidParameterTypeError)
def handle_invalid_parameter_type(e):
    """Handle invalid parameter type errors."""
    return jsonify({
        "success": False,
        "error": str(e)
    }), 400

@nuts_bp.errorhandler(ExternalAPIError)
def handle_external_api_error(e):
    """Handle external API errors."""
    # TODO: Add logger to log the error details
    return jsonify({
        "success": False,
        "error": "An error occurred while communicating with an external service"
    }), 502

@nuts_bp.errorhandler(APITimeoutError)
def handle_api_timeout(e):
    """Handle API timeout errors."""
    # TODO: Add logger to log the error details
    return jsonify({
        "success": False,
        "error": "Request timed out"
    }), 504

@nuts_bp.errorhandler(500)
def handle_internal_error(e):
    """Handle unexpected internal errors."""
    # TODO: Add logger to log the error details
    return jsonify({
        "success": False,
        "error": "An internal error occurred"
    }), 500
    
@nuts_bp.route('/codes', methods=['GET'])
def get_nuts_codes():
    """Get hierarchical NUTS geographical structure.
    
    Query Parameters:
        level (int): NUTS level to retrieve (1-3)
            1 = Region
            2 = County
            3 = Municipality
    
    Returns:
        JSON response with hierarchical structure
        
    Example:
        GET /api/nuts/codes?level=2
    """

    # Validate level parameter
    level = validate_nuts_level(request.args.get('level'))
    
    service = NUTSService()
    structure = service.get_hierarchical_structure_by_level(level)

    return jsonify({
        "success": True,
        "data": structure,
        "total": len(structure),
        "level": level
    })