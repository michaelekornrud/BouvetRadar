import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from src.utils import get_logger, setup_logging
from src.api.cpv_api import cpv_bp
from src.api.nuts_api import nuts_bp
from src.api.styrk_api import styrk_bp
from src.api.doffin_api import doffin_bp

from exceptions import BouvetRadarException



    
def create_app():
    """Application factory."""

    # Load environment varianles 
    load_dotenv()

    # Configure logging
    log_level = os.getenv("LOG_LEVEL", "INFO")
    setup_logging(log_level=log_level)

    # Create logger
    logger = get_logger(__name__)
    logger.info("Creating Flask Application")

    app = Flask(__name__)
    CORS(app) # Enable CORS for React frontend

    # Register blueprints
    app.register_blueprint(cpv_bp)
    app.register_blueprint(nuts_bp)
    app.register_blueprint(styrk_bp)
    app.register_blueprint(doffin_bp)

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        logger.debug("Health check requested")
        return jsonify({
            "success": True,
            "message": "API is running",
            "version": "1.0.0"
        })
    
    @app.errorhandler(BouvetRadarException)
    def handle_bouvet_radar_exception(error):
        logger.error(
            f"BouvetRadar exception: {error.message}",
            extra={
                "error_code": error.error_code.name if error.error_code else None,
                "status_code": error.status_code,
                "details": error.details
            }
        )
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # Global error handler
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"404 Not Found: {error}")
        return jsonify({
            "success": False,
            "error": "Endpoint not found"
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.exception(f"Internal Server Error: {error}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500
    
    return app
    

def main ():

    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)


if __name__ == "__main__":
    main()
