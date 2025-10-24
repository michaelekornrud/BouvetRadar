"""
API endpoints for STYRK codes
Provides RESTful access to STYRK data for frontend visualization
"""

from flask import jsonify, Blueprint
import sys
import os

# Add the parent directory to Python path to import constants
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.service.ssb_service import STYRKService, SSBLevel

styrk_bp = Blueprint('styrk', __name__, url_prefix='/api/styrk')

@styrk_bp.route('codes/level/<int:level>', methods=['GET'])
def get_structure_by_level(level: int):
    """Get hierarchical STYRK structure up to a specified level."""
    try:
        service = STYRKService()

        if level not in [lvl.value for lvl in SSBLevel]:
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