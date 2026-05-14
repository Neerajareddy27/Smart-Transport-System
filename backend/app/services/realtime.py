"""
Day 8: Flask-SocketIO - Real-Time Alerts and Notifications
WebSocket communication for city-wide transportation alerts
"""
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from flask import current_app
import json
from datetime import datetime
from app.services.daos import AlertDAO, VehicleDAO, TrafficDataDAO
from app.models import AlertType, AlertPriority, VehicleStatus
import threading
import time


class RealtimeAlertsService:
    """Manages real-time WebSocket connections and alert broadcasting"""
    
    def __init__(self):
        self.socketio = None
        self.connected_users = {}
        self.subscribed_routes = {}
        self.alert_thread = None
        self.running = False
    
    def init_socketio(self, app):
        """Initialize SocketIO"""
        self.socketio = SocketIO(
            app,
            cors_allowed_origins=app.config.get('CORS_ORIGINS'),
            async_mode='threading',
            message_queue=app.config.get('SOCKETIO_MESSAGE_QUEUE')
        )
        
        @self.socketio.on('connect')
        def handle_connect():
            user_id = self.get_user_id()
            self.connected_users[user_id] = {
                'sid': user_id,
                'connected_at': datetime.utcnow(),
                'subscribed_routes': []
            }
            emit('connection_response', {
                'data': 'Connected to real-time alerts service',
                'timestamp': datetime.utcnow().isoformat()
            })
            print(f"Client connected: {user_id}")
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            user_id = self.get_user_id()
            if user_id in self.connected_users:
                del self.connected_users[user_id]
            print(f"Client disconnected: {user_id}")
        
        @self.socketio.on('subscribe_route')
        def handle_subscribe_route(data):
            route_id = data.get('routeId')
            user_id = self.get_user_id()
            
            if route_id not in self.subscribed_routes:
                self.subscribed_routes[route_id] = []
            
            self.subscribed_routes[route_id].append(user_id)
            
            if user_id in self.connected_users:
                self.connected_users[user_id]['subscribed_routes'].append(route_id)
            
            join_room(f'route_{route_id}')
            emit('subscribed', {
                'routeId': route_id,
                'message': f'Subscribed to route {route_id}'
            })
            print(f"User {user_id} subscribed to route {route_id}")
        
        @self.socketio.on('unsubscribe_route')
        def handle_unsubscribe_route(data):
            route_id = data.get('routeId')
            user_id = self.get_user_id()
            
            if route_id in self.subscribed_routes:
                self.subscribed_routes[route_id].remove(user_id)
            
            if user_id in self.connected_users:
                if route_id in self.connected_users[user_id]['subscribed_routes']:
                    self.connected_users[user_id]['subscribed_routes'].remove(route_id)
            
            leave_room(f'route_{route_id}')
            emit('unsubscribed', {'routeId': route_id})
        
        @self.socketio.on('get_connection_status')
        def handle_get_status():
            emit('status', {
                'connected': True,
                'connectedUsers': len(self.connected_users),
                'subscribedRoutes': len(self.subscribed_routes),
                'timestamp': datetime.utcnow().isoformat()
            })
        
        return self.socketio
    
    @staticmethod
    def get_user_id():
        """Get or generate user ID from request"""
        from flask import request
        return request.sid
    
    def broadcast_alert(self, alert_id, route_id=None):
        """Broadcast alert to subscribed users"""
        try:
            alert = AlertDAO.get_alert_by_id(alert_id)
            if not alert:
                return
            
            alert_data = {
                'id': alert.id,
                'type': alert.type.value,
                'title': alert.title,
                'message': alert.message,
                'priority': alert.priority.value,
                'timestamp': alert.timestamp.isoformat(),
                'isRead': alert.is_read
            }
            
            if route_id:
                # Send to specific route subscribers
                self.socketio.emit(
                    'new_alert',
                    alert_data,
                    room=f'route_{route_id}'
                )
            else:
                # Broadcast to all connected users
                self.socketio.emit(
                    'new_alert',
                    alert_data,
                    broadcast=True
                )
        except Exception as e:
            print(f"Error broadcasting alert: {str(e)}")
    
    def broadcast_traffic_update(self, route_id, traffic_data):
        """Broadcast traffic update to route subscribers"""
        try:
            self.socketio.emit(
                'traffic_update',
                {
                    'routeId': route_id,
                    'congestionLevel': traffic_data.congestion_level.value,
                    'averageSpeed': traffic_data.average_speed,
                    'vehicleCount': traffic_data.vehicle_count,
                    'timestamp': traffic_data.timestamp.isoformat()
                },
                room=f'route_{route_id}'
            )
        except Exception as e:
            print(f"Error broadcasting traffic update: {str(e)}")
    
    def broadcast_vehicle_update(self, vehicle_id, vehicle_data):
        """Broadcast vehicle location/status update"""
        try:
            route_id = vehicle_data.current_route_id
            if route_id:
                self.socketio.emit(
                    'vehicle_update',
                    {
                        'vehicleId': vehicle_id,
                        'routeId': route_id,
                        'status': vehicle_data.status.value,
                        'currentPassengers': vehicle_data.current_passengers,
                        'location': {
                            'latitude': vehicle_data.location.latitude if vehicle_data.location else None,
                            'longitude': vehicle_data.location.longitude if vehicle_data.location else None
                        },
                        'timestamp': datetime.utcnow().isoformat()
                    },
                    room=f'route_{route_id}'
                )
        except Exception as e:
            print(f"Error broadcasting vehicle update: {str(e)}")
    
    def broadcast_incident_alert(self, incident_id):
        """Broadcast incident alert"""
        try:
            from app.services.daos import IncidentDAO
            incident = IncidentDAO.get_incident_by_id(incident_id)
            if not incident:
                return
            
            incident_data = {
                'id': incident.id,
                'type': incident.type.value,
                'severity': incident.severity.value,
                'description': incident.description,
                'timestamp': incident.timestamp.isoformat(),
                'status': incident.status
            }
            
            if incident.route_id:
                self.socketio.emit(
                    'incident_alert',
                    incident_data,
                    room=f'route_{incident.route_id}'
                )
            else:
                self.socketio.emit(
                    'incident_alert',
                    incident_data,
                    broadcast=True
                )
        except Exception as e:
            print(f"Error broadcasting incident: {str(e)}")
    
    def start_background_updates(self):
        """Start background thread for periodic updates"""
        # Background updates are now event-driven via WebSocket
        # Real-time alerts are broadcasted when events occur
        self.running = True
        print("Real-time alert service started (event-driven mode)")
    
    def stop_background_updates(self):
        """Stop background thread"""
        self.running = False


# Global realtime service instance
realtime_service = RealtimeAlertsService()
