"""
API Routes for Transit Routes Management Microservice
"""
from flask import Blueprint, request, jsonify
from app.services.daos import RouteDAO
from app.models import db, TransitRoute, Location
import uuid

routes_bp = Blueprint('routes', __name__, url_prefix='/api/routes')


@routes_bp.route('/locations', methods=['GET'])
def get_all_locations():
    """Get all available locations"""
    try:
        locations = Location.query.all()
        return jsonify([{
            'id': loc.id,
            'address': loc.address,
            'city': loc.city,
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'zipCode': loc.zip_code
        } for loc in locations]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes_bp.route('', methods=['GET'])
def get_all_routes():
    """Get all active routes"""
    try:
        routes = RouteDAO.get_all_routes(active_only=True)
        return jsonify([{
            'id': route.id,
            'routeNumber': route.route_number,
            'name': route.name,
            'distance': route.distance,
            'estimatedDuration': route.estimated_duration,
            'vehicleType': route.vehicle_type.value,
            'startLocationId': route.start_location_id,
            'endLocationId': route.end_location_id
        } for route in routes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes_bp.route('/<route_id>', methods=['GET'])
def get_route(route_id):
    """Get route by ID"""
    try:
        route = RouteDAO.get_route_by_id(route_id)
        if not route:
            return jsonify({'error': 'Route not found'}), 404
        
        return jsonify({
            'id': route.id,
            'routeNumber': route.route_number,
            'name': route.name,
            'distance': route.distance,
            'estimatedDuration': route.estimated_duration,
            'vehicleType': route.vehicle_type.value,
            'startLocationId': route.start_location_id,
            'endLocationId': route.end_location_id,
            'isActive': route.is_active
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes_bp.route('', methods=['POST'])
def create_route():
    """Create a new route"""
    try:
        data = request.get_json()
        new_route = RouteDAO.create_route(data)
        
        return jsonify({
            'id': new_route.id,
            'routeNumber': new_route.route_number,
            'name': new_route.name
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@routes_bp.route('/<route_id>', methods=['PUT'])
def update_route(route_id):
    """Update route information"""
    try:
        data = request.get_json()
        updated_route = RouteDAO.update_route(route_id, data)
        
        if not updated_route:
            return jsonify({'error': 'Route not found'}), 404
        
        return jsonify({'message': 'Route updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@routes_bp.route('/<route_id>', methods=['DELETE'])
def delete_route(route_id):
    """Delete route (soft delete)"""
    try:
        if RouteDAO.delete_route(route_id):
            return jsonify({'message': 'Route deleted successfully'}), 200
        return jsonify({'error': 'Route not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@routes_bp.route('/search', methods=['POST'])
def search_routes():
    """Search routes by start and end location"""
    try:
        data = request.get_json()
        
        # Handle both location object and location ID formats
        start_location_id = None
        end_location_id = None
        
        # If frontend sends location objects
        if isinstance(data.get('startLocation'), dict):
            start_location_id = data['startLocation'].get('id')
        else:
            start_location_id = data.get('startLocationId')
        
        if isinstance(data.get('endLocation'), dict):
            end_location_id = data['endLocation'].get('id')
        else:
            end_location_id = data.get('endLocationId')
        
        if not start_location_id or not end_location_id:
            return jsonify({'error': 'startLocationId and endLocationId are required'}), 400
        
        routes = RouteDAO.search_routes(
            start_location_id,
            end_location_id,
            data.get('vehicleType')
        )
        
        return jsonify([{
            'id': route.id,
            'routeNumber': route.route_number,
            'name': route.name,
            'distance': route.distance,
            'estimatedDuration': route.estimated_duration
        } for route in routes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
