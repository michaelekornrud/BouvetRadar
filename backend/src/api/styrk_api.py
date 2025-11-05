"""
API endpoints for STYRK codes
Provides RESTful access to STYRK occupational classification data
"""

from flask import jsonify, Blueprint, request

from ..service.ssb_service import STYRKService
from ..validation.ssb_validators import validate_styrk_level
from utils import get_logger
from exceptions import (
    APITimeoutError, 
    ExternalAPIError,
    ValidationError,
    InvalidParameterTypeError
)

styrk_bp = Blueprint('styrk', __name__, url_prefix='/api/styrk')
logger = get_logger(__name__)

@styrk_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    """Handle validation errors."""
    logger.error(f"ValidationError: {e}")
    return jsonify({
        "success": False,
        "error": str(e)
    }), 400

@styrk_bp.errorhandler(InvalidParameterTypeError)
def handle_invalid_parameter_type(e):
    """Handle invalid parameter type errors."""
    logger.error(f"InvalidParameterTypeError: {e}")
    return jsonify({
        "success": False,
        "error": str(e)
    }), 400


@styrk_bp.errorhandler(ExternalAPIError)
def handle_external_api_error(e):
    """Handle external API errors."""
    logger.error(f"ExternalAPIError: {e}")
    return jsonify({
        "success": False,
        "error": "An error occurred while communicating with an external service"
    }), 502


@styrk_bp.errorhandler(APITimeoutError)
def handle_api_timeout(e):
    """Handle API timeout errors."""
    logger.error(f"APITimeoutError: {e}")
    return jsonify({
        "success": False,
        "error": "Request timed out"
    }), 504


@styrk_bp.errorhandler(500)
def handle_internal_error(e):
    """Handle unexpected internal errors."""
    logger.error(f"An internal server error occured: {e}")
    return jsonify({
        "success": False,
        "error": "An internal error occurred"
    }), 500

@styrk_bp.route('/codes', methods=['GET'])
def get_styrk_codes():
    """Get hierarchical STYRK occupational classification structure.
    
    Query Parameters:
        level (int): STYRK level to retrieve (1-4)
            1 = Major group
            2 = Sub-major group
            3 = Minor group
            4 = Unit group
    
    Returns:
        JSON response with hierarchical structure
        
    Example:
        GET /api/styrk/codes?level=2
    """

    level = validate_styrk_level(request.args.get('level'))

    service = STYRKService()
    structure = service.get_hierarchical_structure_by_level(level)

    return jsonify({
        "success": True,
        "data": structure,
        "total": len(structure),
        "level": level
    })