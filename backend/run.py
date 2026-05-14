"""
Main Flask Application
Smart City Transportation Management System Backend
Day 6-8 Implementation
"""
import os
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from app.models import db
from app.config import config
from app.routes.routes import routes_bp
from app.routes.vehicles import vehicles_bp
from app.routes.traffic import traffic_bp
from app.routes.alerts import alerts_bp
from app.routes.analytics import analytics_bp
from app.routes.users import users_bp
from app.services.realtime import realtime_service
from app.microservices import ServiceRegistry, ConfigurationManager, HealthCheck

# Load environment variables
load_dotenv()


def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {"origins": app.config.get('CORS_ORIGINS', ['http://localhost:4200'])}
    })
    
    # Initialize SocketIO
    socketio = realtime_service.init_socketio(app)
    
    # Register API blueprints
    app.register_blueprint(routes_bp)
    app.register_blueprint(vehicles_bp)
    app.register_blueprint(traffic_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(users_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """System health check"""
        return jsonify({
            'status': 'healthy',
            'timestamp': __import__('datetime').datetime.utcnow().isoformat(),
            'services': HealthCheck.check_all_services()
        }), 200
    
    # Service registry endpoints
    @app.route('/api/services', methods=['GET'])
    def list_services():
        """List all registered microservices"""
        services = ServiceRegistry.list_services()
        return jsonify({
            'services': services,
            'count': len(services)
        }), 200
    
    @app.route('/api/services/<service_name>/status', methods=['GET'])
    def get_service_status(service_name):
        """Get service status"""
        status = ServiceRegistry.get_service_status(service_name)
        return jsonify(status), 200
    
    # Configuration endpoints
    @app.route('/api/config/current', methods=['GET'])
    def get_current_config():
        """Get current mode configuration"""
        config = ConfigurationManager.get_config()
        mode = ConfigurationManager.get_current_mode()
        return jsonify({
            'mode': mode,
            'config': config
        }), 200
    
    @app.route('/api/config/all', methods=['GET'])
    def get_all_configs():
        """Get all configurations"""
        configs = ConfigurationManager.get_all_configs()
        return jsonify(configs), 200
    
    @app.route('/api/config/<mode>', methods=['PUT'])
    def update_config(mode):
        """Update configuration for a mode"""
        data = request.get_json()
        if ConfigurationManager.update_config(mode, data):
            return jsonify({'message': f'Configuration for {mode} updated'}), 200
        return jsonify({'error': 'Invalid mode'}), 400
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # CLI command for initializing database
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        db.create_all()
        print('Initialized the database.')
    
    return app, socketio


if __name__ == '__main__':
    app, socketio = create_app()
    
    # Start background updates
    realtime_service.start_background_updates()
    
    # Run the application
    socketio.run(
        app,
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development',
        allow_unsafe_werkzeug=True
    )
