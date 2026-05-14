"""
Day 6: Task 2 - Data Access Objects (DAOs) with SQLAlchemy CRUD operations
"""
from datetime import datetime, timedelta
from sqlalchemy import and_, or_, desc, func
from app.models import (
    db, TransitRoute, Vehicle, TrafficData, Incident, 
    Schedule, Alert, Location, BusStop, Driver, UserPreference,
    VehicleStatus, CongestionLevel, IncidentSeverity, AlertPriority
)
import uuid


class RouteDAO:
    """Transit Route Data Access Object"""
    
    @staticmethod
    def create_route(route_data):
        """Create a new transit route"""
        route = TransitRoute(
            id=str(uuid.uuid4()),
            route_number=route_data['route_number'],
            name=route_data['name'],
            start_location_id=route_data['start_location_id'],
            end_location_id=route_data['end_location_id'],
            distance=route_data['distance'],
            estimated_duration=route_data.get('estimated_duration'),
            vehicle_type=route_data['vehicle_type'],
            is_active=route_data.get('is_active', True)
        )
        db.session.add(route)
        db.session.commit()
        return route
    
    @staticmethod
    def get_route_by_id(route_id):
        """Retrieve route by ID"""
        return TransitRoute.query.filter_by(id=route_id).first()
    
    @staticmethod
    def get_all_routes(active_only=True):
        """Get all routes"""
        query = TransitRoute.query
        if active_only:
            query = query.filter_by(is_active=True)
        return query.all()
    
    @staticmethod
    def get_routes_by_vehicle_type(vehicle_type):
        """Get routes by vehicle type"""
        return TransitRoute.query.filter_by(vehicle_type=vehicle_type, is_active=True).all()
    
    @staticmethod
    def update_route(route_id, update_data):
        """Update route information"""
        route = RouteDAO.get_route_by_id(route_id)
        if route:
            for key, value in update_data.items():
                if hasattr(route, key):
                    setattr(route, key, value)
            db.session.commit()
        return route
    
    @staticmethod
    def delete_route(route_id):
        """Soft delete route"""
        route = RouteDAO.get_route_by_id(route_id)
        if route:
            route.is_active = False
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def search_routes(start_loc_id, end_loc_id, vehicle_type=None):
        """Search routes by start, end location and optional vehicle type"""
        query = TransitRoute.query.filter(
            and_(
                TransitRoute.start_location_id == start_loc_id,
                TransitRoute.end_location_id == end_loc_id,
                TransitRoute.is_active == True
            )
        )
        if vehicle_type:
            query = query.filter_by(vehicle_type=vehicle_type)
        return query.all()


class VehicleDAO:
    """Vehicle Data Access Object"""
    
    @staticmethod
    def create_vehicle(vehicle_data):
        """Create a new vehicle"""
        vehicle = Vehicle(
            id=str(uuid.uuid4()),
            vehicle_number=vehicle_data['vehicle_number'],
            type=vehicle_data['type'],
            capacity=vehicle_data.get('capacity', 50),
            status=vehicle_data.get('status', VehicleStatus.OPERATIONAL),
            driver_id=vehicle_data.get('driver_id')
        )
        db.session.add(vehicle)
        db.session.commit()
        return vehicle
    
    @staticmethod
    def get_vehicle_by_id(vehicle_id):
        """Get vehicle by ID"""
        return Vehicle.query.filter_by(id=vehicle_id).first()
    
    @staticmethod
    def get_all_vehicles():
        """Get all vehicles"""
        return Vehicle.query.all()
    
    @staticmethod
    def get_vehicles_by_status(status):
        """Get vehicles by status"""
        return Vehicle.query.filter_by(status=status).all()
    
    @staticmethod
    def get_vehicles_by_route(route_id):
        """Get vehicles assigned to a route"""
        return Vehicle.query.filter_by(current_route_id=route_id).all()
    
    @staticmethod
    def update_vehicle_status(vehicle_id, status):
        """Update vehicle status"""
        vehicle = VehicleDAO.get_vehicle_by_id(vehicle_id)
        if vehicle:
            vehicle.status = status
            vehicle.last_updated = datetime.utcnow()
            db.session.commit()
        return vehicle
    
    @staticmethod
    def update_vehicle_location(vehicle_id, location_id):
        """Update vehicle location"""
        vehicle = VehicleDAO.get_vehicle_by_id(vehicle_id)
        if vehicle:
            vehicle.location_id = location_id
            vehicle.last_updated = datetime.utcnow()
            db.session.commit()
        return vehicle
    
    @staticmethod
    def update_vehicle_passengers(vehicle_id, current_passengers):
        """Update current passenger count"""
        vehicle = VehicleDAO.get_vehicle_by_id(vehicle_id)
        if vehicle:
            vehicle.current_passengers = current_passengers
            db.session.commit()
        return vehicle


class TrafficDataDAO:
    """Traffic Data Access Object"""
    
    @staticmethod
    def create_traffic_record(traffic_data):
        """Create traffic data record"""
        record = TrafficData(
            id=str(uuid.uuid4()),
            route_id=traffic_data['route_id'],
            congestion_level=traffic_data.get('congestion_level', CongestionLevel.FREE),
            average_speed=traffic_data.get('average_speed'),
            vehicle_count=traffic_data.get('vehicle_count', 0)
        )
        db.session.add(record)
        db.session.commit()
        return record
    
    @staticmethod
    def get_traffic_by_route(route_id, hours=1):
        """Get latest traffic data for a route"""
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        return TrafficData.query.filter(
            and_(
                TrafficData.route_id == route_id,
                TrafficData.timestamp >= time_threshold
            )
        ).order_by(desc(TrafficData.timestamp)).all()
    
    @staticmethod
    def get_current_traffic(route_id):
        """Get most recent traffic for a route"""
        return TrafficData.query.filter_by(
            route_id=route_id
        ).order_by(desc(TrafficData.timestamp)).first()
    
    @staticmethod
    def get_traffic_by_congestion_level(congestion_level):
        """Get routes with specific congestion level"""
        time_threshold = datetime.utcnow() - timedelta(minutes=15)
        return TrafficData.query.filter(
            and_(
                TrafficData.congestion_level == congestion_level,
                TrafficData.timestamp >= time_threshold
            )
        ).all()


class IncidentDAO:
    """Incident Data Access Object"""
    
    @staticmethod
    def create_incident(incident_data):
        """Create a new incident"""
        incident = Incident(
            id=str(uuid.uuid4()),
            type=incident_data['type'],
            severity=incident_data['severity'],
            description=incident_data.get('description'),
            location_id=incident_data['location_id'],
            route_id=incident_data.get('route_id'),
            status='ACTIVE'
        )
        db.session.add(incident)
        db.session.commit()
        return incident
    
    @staticmethod
    def get_incident_by_id(incident_id):
        """Get incident by ID"""
        return Incident.query.filter_by(id=incident_id).first()
    
    @staticmethod
    def get_active_incidents():
        """Get all active incidents"""
        return Incident.query.filter_by(status='ACTIVE').all()
    
    @staticmethod
    def get_incidents_by_route(route_id):
        """Get incidents affecting a route"""
        return Incident.query.filter_by(route_id=route_id, status='ACTIVE').all()
    
    @staticmethod
    def get_incidents_by_severity(severity):
        """Get incidents by severity level"""
        return Incident.query.filter_by(severity=severity, status='ACTIVE').all()
    
    @staticmethod
    def resolve_incident(incident_id):
        """Mark incident as resolved"""
        incident = IncidentDAO.get_incident_by_id(incident_id)
        if incident:
            incident.status = 'RESOLVED'
            incident.resolved_time = datetime.utcnow()
            db.session.commit()
        return incident


class ScheduleDAO:
    """Schedule Data Access Object"""
    
    @staticmethod
    def create_schedule(schedule_data):
        """Create a new schedule"""
        schedule = Schedule(
            id=str(uuid.uuid4()),
            route_id=schedule_data['route_id'],
            day_of_week=schedule_data['day_of_week'],
            departure_time=schedule_data['departure_time'],
            arrival_time=schedule_data['arrival_time'],
            frequency=schedule_data.get('frequency'),
            is_active=schedule_data.get('is_active', True)
        )
        db.session.add(schedule)
        db.session.commit()
        return schedule
    
    @staticmethod
    def get_schedule_by_id(schedule_id):
        """Get schedule by ID"""
        return Schedule.query.filter_by(id=schedule_id).first()
    
    @staticmethod
    def get_schedules_by_route(route_id):
        """Get all schedules for a route"""
        return Schedule.query.filter_by(route_id=route_id, is_active=True).all()
    
    @staticmethod
    def get_schedules_by_day(day_of_week):
        """Get schedules for a specific day"""
        return Schedule.query.filter_by(day_of_week=day_of_week, is_active=True).all()
    
    @staticmethod
    def update_schedule(schedule_id, update_data):
        """Update schedule"""
        schedule = ScheduleDAO.get_schedule_by_id(schedule_id)
        if schedule:
            for key, value in update_data.items():
                if hasattr(schedule, key):
                    setattr(schedule, key, value)
            db.session.commit()
        return schedule
    
    @staticmethod
    def delete_schedule(schedule_id):
        """Soft delete schedule"""
        schedule = ScheduleDAO.get_schedule_by_id(schedule_id)
        if schedule:
            schedule.is_active = False
            db.session.commit()
        return schedule


class AlertDAO:
    """Alert Data Access Object"""
    
    @staticmethod
    def create_alert(alert_data):
        """Create a new alert"""
        alert = Alert(
            id=str(uuid.uuid4()),
            type=alert_data['type'],
            title=alert_data['title'],
            message=alert_data['message'],
            priority=alert_data.get('priority', AlertPriority.MEDIUM),
            incident_id=alert_data.get('incident_id'),
            expires_at=alert_data.get('expires_at')
        )
        db.session.add(alert)
        db.session.commit()
        return alert
    
    @staticmethod
    def get_alert_by_id(alert_id):
        """Get alert by ID"""
        return Alert.query.filter_by(id=alert_id).first()
    
    @staticmethod
    def get_unread_alerts():
        """Get all unread alerts"""
        return Alert.query.filter_by(is_read=False).order_by(desc(Alert.timestamp)).all()
    
    @staticmethod
    def get_active_alerts():
        """Get active (non-expired) alerts"""
        now = datetime.utcnow()
        return Alert.query.filter(
            or_(
                Alert.expires_at.is_(None),
                Alert.expires_at > now
            )
        ).order_by(desc(Alert.priority)).all()
    
    @staticmethod
    def mark_alert_as_read(alert_id):
        """Mark alert as read"""
        alert = AlertDAO.get_alert_by_id(alert_id)
        if alert:
            alert.is_read = True
            db.session.commit()
        return alert
    
    @staticmethod
    def get_alerts_by_priority(priority):
        """Get alerts by priority"""
        return Alert.query.filter_by(priority=priority, is_read=False).all()
