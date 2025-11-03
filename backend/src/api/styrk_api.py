"""
API endpoints for STYRK codes
Provides RESTful access to STYRK data for frontend visualization
"""

import requests

from flask import jsonify, Blueprint, request
from ..service.ssb_service import STYRKService, SSBLevel
from ..validation.ssb_validators import validate_styrk_level

from exceptions import APITimeoutError, ExternalAPIError

styrk_bp = Blueprint('styrk', __name__, url_prefix='/api/styrk')

@styrk_bp.route('/codes', methods=['GET'])
def get_structure_by_level():
    """Get hierarchical STYRK structure up to a specified level."""

    level = validate_styrk_level(request.args.get('level'))
    try:
        service = STYRKService()
        structure = service.get_hierarchical_structure_by_level(SSBLevel(level))

        return jsonify({
            "success": True,
            "structure": structure,
            "total": len(structure)
        })
    except requests.Timeout:
        raise APITimeoutError(service="SSB STYRK", timeout_seconds=30)
    except requests.RequestException as e:
        raise ExternalAPIError(
            message="Error from SSB Klass API",
            service="SSB STYRK",
            original_error=e
        )