"""
API Routes for Traffic Monitoring Microservice
"""
from flask import Blueprint, request, jsonify
from app.services.daos import TrafficDataDAO, IncidentDAO
from app.models import CongestionLevel
import uuid

traffic_bp = Blueprint('traffic', __name__, url_prefix='/api/traffic')


@traffic_bp.route('/record', methods=['POST'])
def create_traffic_record():
    """Create traffic data record"""
    try:
        data = request.get_json()
        data['congestion_level'] = CongestionLevel[data.get('congestionLevel', 'FREE').upper()]
        
        record = TrafficDataDAO.create_traffic_record(data)
        return jsonify({'id': record.id, 'timestamp': record.timestamp.isoformat()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@traffic_bp.route('/by-route/<route_id>', methods=['GET'])
def get_traffic_by_route(route_id):
    """Get traffic data for a route"""
    try:
        hours = request.args.get('hours', 1, type=int)
        traffic_data = TrafficDataDAO.get_traffic_by_route(route_id, hours=hours)
        
        return jsonify([{
            'id': t.id,
            'routeId': t.route_id,
            'timestamp': t.timestamp.isoformat(),
            'congestionLevel': t.congestion_level.value,
            'averageSpeed': t.average_speed,
            'vehicleCount': t.vehicle_count
        } for t in traffic_data]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@traffic_bp.route('/current/<route_id>', methods=['GET'])
def get_current_traffic(route_id):
    """Get most recent traffic for a route"""
    try:
        traffic = TrafficDataDAO.get_current_traffic(route_id)
        if not traffic:
            return jsonify({'error': 'No traffic data found'}), 404
        
        return jsonify({
            'id': traffic.id,
            'routeId': traffic.route_id,
            'timestamp': traffic.timestamp.isoformat(),
            'congestionLevel': traffic.congestion_level.value,
            'averageSpeed': traffic.average_speed,
            'vehicleCount': traffic.vehicle_count
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@traffic_bp.route('/by-congestion/<congestion_level>', methods=['GET'])
def get_traffic_by_congestion(congestion_level):
    """Get routes with specific congestion level"""
    try:
        level = CongestionLevel[congestion_level.upper()]
        traffic_data = TrafficDataDAO.get_traffic_by_congestion_level(level)
        
        return jsonify([{
            'id': t.id,
            'routeId': t.route_id,
            'congestionLevel': t.congestion_level.value,
            'vehicleCount': t.vehicle_count
        } for t in traffic_data]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Incident endpoints
@traffic_bp.route('/incidents', methods=['POST'])
def create_incident():
    """Create a new incident report"""
    try:
        data = request.get_json()
        from app.models import IncidentType, IncidentSeverity
        data['type'] = IncidentType[data['type'].upper()]
        data['severity'] = IncidentSeverity[data['severity'].upper()]
        
        incident = IncidentDAO.create_incident(data)
        return jsonify({'id': incident.id, 'status': incident.status}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@traffic_bp.route('/incidents', methods=['GET'])
def get_active_incidents():
    """Get all active incidents"""
    try:
        incidents = IncidentDAO.get_active_incidents()
        return jsonify([{
            'id': i.id,
            'type': i.type.value,
            'severity': i.severity.value,
            'description': i.description,
            'timestamp': i.timestamp.isoformat(),
            'locationId': i.location_id,
            'routeId': i.route_id,
            'status': i.status
        } for i in incidents]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@traffic_bp.route('/incidents/<incident_id>/resolve', methods=['PUT'])
def resolve_incident(incident_id):
    """Mark incident as resolved"""
    try:
        incident = IncidentDAO.resolve_incident(incident_id)
        if not incident:
            return jsonify({'error': 'Incident not found'}), 404
        
        return jsonify({'message': 'Incident resolved', 'status': incident.status}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@traffic_bp.route('/incidents/by-route/<route_id>', methods=['GET'])
def get_incidents_by_route(route_id):
    """Get incidents affecting a route"""
    try:
        incidents = IncidentDAO.get_incidents_by_route(route_id)
        return jsonify([{
            'id': i.id,
            'type': i.type.value,
            'severity': i.severity.value,
            'description': i.description
        } for i in incidents]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
