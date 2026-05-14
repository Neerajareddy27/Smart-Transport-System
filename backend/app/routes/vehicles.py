"""
API Routes for Vehicle Management Microservice
"""
from flask import Blueprint, request, jsonify
from app.services.daos import VehicleDAO
from app.models import VehicleStatus, VehicleType
import uuid

vehicles_bp = Blueprint('vehicles', __name__, url_prefix='/api/vehicles')


@vehicles_bp.route('', methods=['GET'])
def get_all_vehicles():
    """Get all vehicles"""
    try:
        vehicles = VehicleDAO.get_all_vehicles()
        return jsonify([{
            'id': v.id,
            'vehicleNumber': v.vehicle_number,
            'type': v.type.value,
            'capacity': v.capacity,
            'currentPassengers': v.current_passengers,
            'status': v.status.value,
            'currentRouteId': v.current_route_id,
            'driverId': v.driver_id,
            'lastUpdated': v.last_updated.isoformat() if v.last_updated else None
        } for v in vehicles]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@vehicles_bp.route('/<vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    """Get vehicle by ID"""
    try:
        vehicle = VehicleDAO.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        return jsonify({
            'id': vehicle.id,
            'vehicleNumber': vehicle.vehicle_number,
            'type': vehicle.type.value,
            'capacity': vehicle.capacity,
            'currentPassengers': vehicle.current_passengers,
            'status': vehicle.status.value
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@vehicles_bp.route('', methods=['POST'])
def create_vehicle():
    """Create a new vehicle"""
    try:
        data = request.get_json()
        data['type'] = VehicleType[data['type'].upper()]
        new_vehicle = VehicleDAO.create_vehicle(data)
        
        return jsonify({
            'id': new_vehicle.id,
            'vehicleNumber': new_vehicle.vehicle_number,
            'status': new_vehicle.status.value
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@vehicles_bp.route('/<vehicle_id>/status', methods=['PUT'])
def update_vehicle_status(vehicle_id):
    """Update vehicle status"""
    try:
        data = request.get_json()
        status = VehicleStatus[data['status'].upper()]
        vehicle = VehicleDAO.update_vehicle_status(vehicle_id, status)
        
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        return jsonify({'message': 'Vehicle status updated', 'status': vehicle.status.value}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@vehicles_bp.route('/<vehicle_id>/location', methods=['PUT'])
def update_vehicle_location(vehicle_id):
    """Update vehicle location"""
    try:
        data = request.get_json()
        vehicle = VehicleDAO.update_vehicle_location(vehicle_id, data['locationId'])
        
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        return jsonify({'message': 'Vehicle location updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@vehicles_bp.route('/<vehicle_id>/passengers', methods=['PUT'])
def update_passengers(vehicle_id):
    """Update current passenger count"""
    try:
        data = request.get_json()
        vehicle = VehicleDAO.update_vehicle_passengers(vehicle_id, data['currentPassengers'])
        
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        return jsonify({'message': 'Passenger count updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@vehicles_bp.route('/by-route/<route_id>', methods=['GET'])
def get_vehicles_by_route(route_id):
    """Get vehicles assigned to a route"""
    try:
        vehicles = VehicleDAO.get_vehicles_by_route(route_id)
        return jsonify([{
            'id': v.id,
            'vehicleNumber': v.vehicle_number,
            'status': v.status.value,
            'currentPassengers': v.current_passengers,
            'capacity': v.capacity
        } for v in vehicles]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@vehicles_bp.route('/by-status/<status>', methods=['GET'])
def get_vehicles_by_status(status):
    """Get vehicles by status"""
    try:
        vehicle_status = VehicleStatus[status.upper()]
        vehicles = VehicleDAO.get_vehicles_by_status(vehicle_status)
        return jsonify([{
            'id': v.id,
            'vehicleNumber': v.vehicle_number,
            'type': v.type.value,
            'status': v.status.value
        } for v in vehicles]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
