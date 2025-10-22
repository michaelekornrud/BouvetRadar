"""
API endpoints for STYRK codes
Provides RESTful access to STYRK data for frontend visualization
"""

from flask import jsonify, Blueprint
import sys
import os

# Add the parent directory to Python path to import constants
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.service.ssb_service import STYRKService

styrk_bp = Blueprint('styrk', __name__, url_prefix='/api/styrk')

@styrk_bp.route('/profession-groups', methods=['GET'])
def get_profession_groups():
    """Get profession groups for high-level visualization."""

    try:
        service = STYRKService()
        groups = service.get_major_groups()

        return jsonify({
            "success": True,
            "profession_groups": groups,
            "total": len(groups)
        })
    except Exception as e:
        print(str(e))
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
@styrk_bp.route('/sub-professions', methods=['GET'])
def get_sub_profesions():
    """Get hierarchical STYRK structure for profession groups - subgroups"""

    try:
        service = STYRKService()
        structure = service.get_hierarchical_subgroup_structure()

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

@styrk_bp.route('/roles', methods=['GET'])
def get_roles():
    """Get hierarchical STYRK structure for subgroups - roles"""

    try:
        service = STYRKService()
        structure = service.get_hierarchical_role_structure()

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
    
@styrk_bp.route('/titles', methods=['GET'])
def get_titles():
    """Get complete hierarchical STYRK structure"""

    try:
        service = STYRKService()
        structure = service.get_hierarchical_structure()

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