"""
API endpoint(s) for Doffin data
Provides RESTful access to Doffin data for frontend visualization
"""

from flask import jsonify, Blueprint, request
from ..service.doffin_service import DoffinService

doffin_bp = Blueprint('doffin', __name__, url_prefix='/api/doffin')

@doffin_bp.route('/search', methods=['GET'])
def search_doffin_for_data():
    """Search for data based on input on the Doffin API"""
    try:
        service = DoffinService()

        # Parse query parameters
        search_str = request.args.get('search')

        # Handle multiple values 
        cpv_codes = request.args.getlist('cpvCode') or None
        location_ids = request.args.getlist('location', type=str) or None
        status = request.args.getlist('status') or None

        # Paring integers with defaults
        page = request.args.get('page', default=1, type=int)
        num_hits_per_page = request.args.get('hitsPerPage', default=100, type=int)

        # Call Service
        results = service.search_notices(
            search_str=search_str,
            cpv_codes=cpv_codes,
            location_ids=location_ids,
            status=status,
            page=page,
            num_hits_per_page=num_hits_per_page
        )

        count = len(results.get('hits'))

        return jsonify({
            "success": True,
            "data" : results,
            "elements" : count
        })
    
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": f"Invalid input: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

