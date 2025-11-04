"""
API endpoints for CPV codes
Provides RESTful access to CPV data for frontend visualization
"""

from flask import jsonify, request, Blueprint
import sys
import os

from exceptions import CPVCodeNotFoundError, InvalidParameterTypeError



# Add the parent directory to Python path to import constants
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.service.cpv_service import CPVService, CPV_CODES

cpv_bp = Blueprint('cpv', __name__, url_prefix='/api/cpv')

# Error handlers for the blueprint
@cpv_bp.errorhandler(CPVCodeNotFoundError)
def handle_not_found(e):
    """Handle CPV code not found errors."""
    return jsonify({
        "success": False,
        "error": str(e)
    }), 404


@cpv_bp.errorhandler(InvalidParameterTypeError)
def handle_invalid_parameter(e):
    """Handle invalid parameter errors."""
    return jsonify({
        "success": False,
        "error": str(e)
    }), 400


@cpv_bp.errorhandler(500)
def handle_internal_error(e):
    """Handle unexpected internal errors."""
    # Log the error here for debugging
    return jsonify({
        "success": False,
        "error": "An internal error occurred"
    }), 500


@cpv_bp.route('/categories', methods=['GET'])
def get_main_categories():
    """Get main CPV categories for high-level visualization."""

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


@cpv_bp.route('/codes', methods=['GET'])
def get_all_codes():
    """Get all CPV codes with optional filtering."""
    
    service = CPVService()
    
    # Check for query parameters
    category = request.args.get('category')
    search = request.args.get('search')

    if category: 
        try: 
            category_int = int(category)
        except ValueError:
            raise InvalidParameterTypeError(
                parameter="category",
                expected_type="integer",
                received_value=category
            )
        
    if search and category:
        # Search within a category
        all_codes_in_category = service.get_codes_by_category(category_int)
        if not all_codes_in_category:
            raise CPVCodeNotFoundError(f"for category '{category}'")
        
        codes = {code: desc for code, desc in all_codes_in_category.items()
                    if search.lower() in desc.lower()}
        if not codes:
            raise CPVCodeNotFoundError(f"for search '{search}' in category '{category}'")
    
    elif search:
        # Search in descriptions
        codes = service.search_descriptions(search)
    elif category:
        # Filter by category
        codes = service.get_codes_by_category(category_int)
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
    

@cpv_bp.route('/codes/<int:code>', methods=['GET'])
def get_code_details(code: int):
    """Get details for a specific CPV code."""
    
    service = CPVService()
    description = service.get_description(code)
    
    if not description:
        raise CPVCodeNotFoundError(code)
    
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


@cpv_bp.route('/stats', methods=['GET'])
def get_cpv_statistics():
    """Get statistics about CPV codes for dashboard visualization."""
    
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
