"""
API endpoints for NUTS codes
Provides RESTful access to NUTS data for frontend visualization
"""

import requests

from flask import jsonify, Blueprint, request
from ..service.ssb_service import NUTSService, SSBLevel
from ..validation.ssb_validators import validate_nuts_level

from exceptions import APITimeoutError, ExternalAPIError

nuts_bp = Blueprint('nuts', __name__, url_prefix='/api/nuts')
    
@nuts_bp.route('/codes', methods=['GET'])
def get_structure_by_level():
    """Get hierarchical NUTS structure up to a specified level."""

    # Validate level parameter
    level = validate_nuts_level(request.args.get('level'))
    try:
        service = NUTSService()
        structure = service.get_hierarchical_structure_by_level(SSBLevel(level))

        return jsonify({
            "success": True,
            "structure": structure,
            "total": len(structure)
        })
    except requests.Timeout:
        raise APITimeoutError(service="SSB NUTS", timeout_seconds=30)
    except requests.RequestException as e:
        raise ExternalAPIError(
            message="Failed to connect to SSB NUTS API",
            service="SSB NUTS",
            original_error=e
        )