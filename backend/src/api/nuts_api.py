"""
API endpoints for NUTS codes
Provides RESTful access to NUTS data for frontend visualization
"""

from flask import jsonify, Blueprint
from ..service.ssb_service import NUTSService, SSBLevel

nuts_bp = Blueprint('nuts', __name__, url_prefix='/api/nuts')
    
@nuts_bp.route('/codes/level/<int:level>', methods=['GET'])
def get_structure_by_level(level: int):
    """Get hierarchical NUTS structure up to a specified level."""
    try:
        service = NUTSService()

        if level not in [lvl.value for lvl in SSBLevel] or level > 3:
            return jsonify({
                "success": False,
                "error": "Invalid level specified"
            }), 400

        structure = service.get_hierarchical_structure_by_level(SSBLevel(level))

        return jsonify({
            "success": True,
            "structure": structure,
            "total": len(structure)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500