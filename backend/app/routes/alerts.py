"""
API Routes for Alerts Microservice
"""
from flask import Blueprint, request, jsonify
from app.services.daos import AlertDAO
from app.models import AlertType, AlertPriority
import uuid

alerts_bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')


@alerts_bp.route('', methods=['POST'])
def create_alert():
    """Create a new alert"""
    try:
        data = request.get_json()
        data['type'] = AlertType[data['type'].upper()]
        data['priority'] = AlertPriority[data.get('priority', 'MEDIUM').upper()]
        
        alert = AlertDAO.create_alert(data)
        return jsonify({'id': alert.id, 'timestamp': alert.timestamp.isoformat()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@alerts_bp.route('', methods=['GET'])
def get_active_alerts():
    """Get all active alerts"""
    try:
        alerts = AlertDAO.get_active_alerts()
        return jsonify([{
            'id': a.id,
            'type': a.type.value,
            'title': a.title,
            'message': a.message,
            'priority': a.priority.value,
            'timestamp': a.timestamp.isoformat(),
            'isRead': a.is_read,
            'incidentId': a.incident_id
        } for a in alerts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@alerts_bp.route('/unread', methods=['GET'])
def get_unread_alerts():
    """Get all unread alerts"""
    try:
        alerts = AlertDAO.get_unread_alerts()
        return jsonify([{
            'id': a.id,
            'type': a.type.value,
            'title': a.title,
            'message': a.message,
            'priority': a.priority.value,
            'timestamp': a.timestamp.isoformat()
        } for a in alerts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@alerts_bp.route('/<alert_id>/read', methods=['PUT'])
def mark_alert_read(alert_id):
    """Mark alert as read"""
    try:
        alert = AlertDAO.mark_alert_as_read(alert_id)
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        return jsonify({'message': 'Alert marked as read'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@alerts_bp.route('/by-priority/<priority>', methods=['GET'])
def get_alerts_by_priority(priority):
    """Get alerts by priority"""
    try:
        prio = AlertPriority[priority.upper()]
        alerts = AlertDAO.get_alerts_by_priority(prio)
        return jsonify([{
            'id': a.id,
            'title': a.title,
            'message': a.message,
            'priority': a.priority.value,
            'timestamp': a.timestamp.isoformat()
        } for a in alerts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
