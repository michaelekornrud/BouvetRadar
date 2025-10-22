"""
API endpoints for NUTS codes
Provides RESTful access to NUTS data for frontend visualization
"""

from flask import jsonify, Blueprint
import sys
import os

# Add the parent directory to Python path to import constants
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.service.ssb_service import NUTSService

nuts_bp = Blueprint('nuts', __name__, url_prefix='/api/nuts')



@nuts_bp.route('/regions', methods=['GET'])
def get_regions():
    """Get regional NUTS codes for high-level visualization."""

    try:
        service = NUTSService()
        regions = service.get_regions()

        return jsonify({
            "success": True,
            "regions": regions,
            "total": len(regions)
        })
    except Exception as e:
        print(str(e))
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
@nuts_bp.route('/codes', methods=['GET'])
def get_codes():

    try:
        service = NUTSService()
        regions = service.get_hierarchical_structure()

        return jsonify({
            "success": True,
            "regions": regions,
            "total": len(regions)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
@nuts_bp.route('/counties', methods=['GET'])
def get_counties():
    """Get hierarchical structure for counties including regions."""

    try:
        service = NUTSService()
        regions = service.get_hierarcical_county_structure()

        return jsonify({
            "success": True,
            "regions": regions,
            "total": len(regions)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500