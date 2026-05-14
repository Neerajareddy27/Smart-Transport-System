"""
Day 7: Task 1 - Flask Microservices Architecture for Scalable Traffic Monitoring
"""
import os
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from flask_socketio import SocketIO
from app.models import db
from app.config import config


def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": config[config_name].CORS_ORIGINS}})
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app


# Microservice: Route Service
class RouteService(Blueprint):
    def __init__(self):
        super().__init__('route_service', __name__, url_prefix='/api/routes')


# Microservice: Traffic Monitoring Service
class TrafficService(Blueprint):
    def __init__(self):
        super().__init__('traffic_service', __name__, url_prefix='/api/traffic')


# Microservice: Vehicle Management Service
class VehicleService(Blueprint):
    def __init__(self):
        super().__init__('vehicle_service', __name__, url_prefix='/api/vehicles')


# Microservice: Alert Service
class AlertService(Blueprint):
    def __init__(self):
        super().__init__('alert_service', __name__, url_prefix='/api/alerts')


# Microservice: Analytics Service
class AnalyticsServiceMS(Blueprint):
    def __init__(self):
        super().__init__('analytics_service', __name__, url_prefix='/api/analytics')


# Service Registry for service discovery
class ServiceRegistry:
    """Simple service registry for service discovery"""
    
    _services = {}
    
    @classmethod
    def register_service(cls, service_name, service_instance, config):
        """Register a microservice"""
        cls._services[service_name] = {
            'instance': service_instance,
            'config': config,
            'status': 'RUNNING',
            'timestamp': os.urandom(16).hex()
        }
    
    @classmethod
    def get_service(cls, service_name):
        """Get a registered service"""
        return cls._services.get(service_name, {}).get('instance')
    
    @classmethod
    def list_services(cls):
        """List all registered services"""
        return list(cls._services.keys())
    
    @classmethod
    def get_service_status(cls, service_name):
        """Get service status"""
        service = cls._services.get(service_name)
        return {
            'service': service_name,
            'status': service['status'] if service else 'NOT_FOUND',
            'timestamp': service['timestamp'] if service else None
        }
    
    @classmethod
    def deregister_service(cls, service_name):
        """Deregister a service"""
        if service_name in cls._services:
            del cls._services[service_name]
            return True
        return False


# Configuration Management for Peak/Off-Peak Hours
class ConfigurationManager:
    """Manages microservices configurations for peak and off-peak hours"""
    
    _configs = {
        'peak_hours': {
            'start': 7,
            'end': 10,
            'alert_threshold': 0.8,
            'update_frequency': 5,  # seconds
            'cache_duration': 60  # seconds
        },
        'off_peak_hours': {
            'start': 22,
            'end': 6,
            'alert_threshold': 0.5,
            'update_frequency': 30,
            'cache_duration': 300
        },
        'normal_hours': {
            'start': 10,
            'end': 22,
            'alert_threshold': 0.6,
            'update_frequency': 15,
            'cache_duration': 120
        }
    }
    
    @classmethod
    def get_current_mode(cls):
        """Determine current operation mode"""
        from datetime import datetime
        current_hour = datetime.utcnow().hour
        
        if cls._configs['peak_hours']['start'] <= current_hour < cls._configs['peak_hours']['end']:
            return 'peak_hours'
        elif cls._configs['off_peak_hours']['start'] <= current_hour or current_hour < cls._configs['off_peak_hours']['end']:
            return 'off_peak_hours'
        else:
            return 'normal_hours'
    
    @classmethod
    def get_config(cls):
        """Get current mode configuration"""
        mode = cls.get_current_mode()
        return cls._configs[mode]
    
    @classmethod
    def get_all_configs(cls):
        """Get all configurations"""
        return cls._configs
    
    @classmethod
    def update_config(cls, mode, config_data):
        """Update configuration for a specific mode"""
        if mode in cls._configs:
            cls._configs[mode].update(config_data)
            return True
        return False
    
    @classmethod
    def get_alert_threshold(cls):
        """Get current alert threshold"""
        config = cls.get_config()
        return config['alert_threshold']
    
    @classmethod
    def get_update_frequency(cls):
        """Get data update frequency in seconds"""
        config = cls.get_config()
        return config['update_frequency']


# Health Check Service
class HealthCheck:
    """Microservice health check"""
    
    @staticmethod
    def check_route_service():
        return {'service': 'route_service', 'status': 'healthy'}
    
    @staticmethod
    def check_traffic_service():
        return {'service': 'traffic_service', 'status': 'healthy'}
    
    @staticmethod
    def check_vehicle_service():
        return {'service': 'vehicle_service', 'status': 'healthy'}
    
    @staticmethod
    def check_alert_service():
        return {'service': 'alert_service', 'status': 'healthy'}
    
    @staticmethod
    def check_analytics_service():
        return {'service': 'analytics_service', 'status': 'healthy'}
    
    @staticmethod
    def check_all_services():
        """Health check for all microservices"""
        return {
            'route_service': HealthCheck.check_route_service(),
            'traffic_service': HealthCheck.check_traffic_service(),
            'vehicle_service': HealthCheck.check_vehicle_service(),
            'alert_service': HealthCheck.check_alert_service(),
            'analytics_service': HealthCheck.check_analytics_service()
        }
