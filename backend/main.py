from flask import Flask, jsonify
from flask_cors import CORS

from src.api.cpv_api import cpv_bp
from src.api.nuts_api import nuts_bp
from src.api.styrk_api import styrk_bp
from src.api.doffin_api import doffin_bp

from exceptions import BouvetRadarException

    
def create_app():
    """Application factory."""
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
        return jsonify({
            "success": True,
            "message": "API is running",
            "version": "1.0.0"
        })
    
    @app.errorhandler(BouvetRadarException)
    def handle_bouvet_radar_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # Global error handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Endpoint not found"
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
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
