"""
API endpoints for CPV codes
Provides RESTful access to CPV data for frontend visualization
"""

from flask import jsonify, request, Blueprint
import sys
import os



# Add the parent directory to Python path to import constants
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.service.cpv_service import CPVService, CPV_CODES

cpv_bp = Blueprint('cpv', __name__, url_prefix='/api/cpv')

@cpv_bp.route('/categories', methods=['GET'])
def get_main_categories():
    """Get main CPV categories for high-level visualization."""
    try:
        service = CPVService()
        categories = service.get_main_categories()
        
        # Format for frontend consumption
        result = [
            {
                "code": code,
                "name": service.get_category_for_code(code),
                "description": CPV_CODES.get(code, "")
            }
            for code, _ in categories
        ]
        
        return jsonify({
            "success": True,
            "data": result,
            "total": len(result)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    



@cpv_bp.route('/codes', methods=['GET'])
def get_all_codes():
    """Get all CPV codes with optional filtering."""
    try:
        service = CPVService()
        
        # Check for query parameters
        category = request.args.get('category')
        search = request.args.get('search')
        
        if search:
            # Search in descriptions
            codes = service.search_descriptions(search)
        elif category:
            # Filter by category
            codes = service.get_codes_by_category(int(category))
        else:
            # Get all codes
            codes = service.get_all_codes()
        
        # Format for frontend
        result = [
            {
                "code": code,
                "description": desc,
                "category": service.get_category_for_code(code)
            }
            for code, desc in codes.items()
        ]
        
        # Sort by code
        result.sort(key=lambda x: x['code'])
        
        return jsonify({
            "success": True,
            "data": result,
            "total": len(result),
            "filters": {
                "category": category,
                "search": search
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@cpv_bp.route('/codes/<int:code>', methods=['GET'])
def get_code_details(code: int):
    """Get details for a specific CPV code."""
    try:
        service = CPVService()
        description = service.get_description(code)
        
        if not description:
            return jsonify({
                "success": False,
                "error": "CPV code not found"
            }), 404
        
        # Get related codes in the same category
        related_codes = service.get_codes_by_category(code)
        related_codes.pop(code, None)  # Remove the current code
        
        result = {
            "code": code,
            "description": description,
            "category": service.get_category_for_code(code),
            "related_codes": [
                {"code": c, "description": d}
                for c, d in list(related_codes.items())
            ]
        }
        
        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@cpv_bp.route('/stats', methods=['GET'])
def get_cpv_statistics():
    """Get statistics about CPV codes for dashboard visualization."""
    try:
        service = CPVService()
        all_codes = service.get_all_codes()
        
        # Count codes by main category
        category_stats = {}
        for code in all_codes.keys():
            category = service.get_category_for_code(code)
            category_stats[category] = category_stats.get(category, 0) + 1
        
        # Get top-level categories (first 2 digits)
        top_level_stats = {}
        for code in all_codes.keys():
            top_level = str(code)[:2]
            top_level_stats[top_level] = top_level_stats.get(top_level, 0) + 1
        
        result = {
            "total_codes": len(all_codes),
            "main_categories": category_stats,
            "top_level_distribution": top_level_stats,
            "category_details": [
                {
                    "code": code,
                    "name": service.get_category_for_code(code),
                    "description": CPV_CODES.get(code, ""),
                    "count": category_stats.get(service.get_category_for_code(code), 0)
                }
                for code, _ in service.get_main_categories()
            ]
        }
        
        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
