"""
Day 6: SQLAlchemy ORM - Transit Data Models
This module defines all SQLAlchemy models for transit routes, schedules, vehicles, and traffic data.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, ForeignKey, DateTime, String, Integer, Float, Boolean, Enum
from sqlalchemy.orm import relationship
import enum

db = SQLAlchemy()


class VehicleType(enum.Enum):
    BUS = "BUS"
    METRO = "METRO"
    TRAM = "TRAM"
    BIKE = "BIKE"


class VehicleStatus(enum.Enum):
    OPERATIONAL = "OPERATIONAL"
    MAINTENANCE = "MAINTENANCE"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    DELAYED = "DELAYED"


class CongestionLevel(enum.Enum):
    FREE = "FREE"
    MODERATE = "MODERATE"
    HEAVY = "HEAVY"
    SEVERE = "SEVERE"


class IncidentType(enum.Enum):
    ACCIDENT = "ACCIDENT"
    CONGESTION = "CONGESTION"
    ROADWORK = "ROADWORK"
    EVENT = "EVENT"
    WEATHER = "WEATHER"


class IncidentSeverity(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AlertType(enum.Enum):
    DELAY = "DELAY"
    INCIDENT = "INCIDENT"
    SCHEDULE_CHANGE = "SCHEDULE_CHANGE"
    SYSTEM_ALERT = "SYSTEM_ALERT"
    WEATHER = "WEATHER"


class AlertPriority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# Location Model
class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(String(36), primary_key=True)
    latitude = db.Column(Float, nullable=False)
    longitude = db.Column(Float, nullable=False)
    address = db.Column(String(255), nullable=False)
    city = db.Column(String(100), nullable=False)
    zip_code = db.Column(String(20))
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    bus_stops = relationship('BusStop', back_populates='location')
    vehicles = relationship('Vehicle', back_populates='location')
    incidents = relationship('Incident', back_populates='location')
    
    __table_args__ = (
        Index('idx_location_coords', 'latitude', 'longitude'),
    )


# Bus Stop Model
class BusStop(db.Model):
    __tablename__ = 'bus_stops'
    
    id = db.Column(String(36), primary_key=True)
    name = db.Column(String(100), nullable=False)
    location_id = db.Column(String(36), ForeignKey('locations.id'), nullable=False)
    arrival_time = db.Column(String(10))
    departure_time = db.Column(String(10))
    capacity = db.Column(Integer, default=50)
    current_passengers = db.Column(Integer, default=0)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    location = relationship('Location', back_populates='bus_stops')
    route_stops = relationship('RouteStop', back_populates='bus_stop')


# Driver Model
class Driver(db.Model):
    __tablename__ = 'drivers'
    
    id = db.Column(String(36), primary_key=True)
    name = db.Column(String(100), nullable=False)
    license_number = db.Column(String(50), unique=True, nullable=False)
    on_duty = db.Column(Boolean, default=False)
    shift_start_time = db.Column(DateTime)
    shift_end_time = db.Column(DateTime)
    created_at = db.Column(DateTime, default=datetime.utcnow)


# Vehicle Model
class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(String(36), primary_key=True)
    vehicle_number = db.Column(String(50), unique=True, nullable=False)
    type = db.Column(Enum(VehicleType), nullable=False)
    capacity = db.Column(Integer, default=50)
    current_passengers = db.Column(Integer, default=0)
    status = db.Column(Enum(VehicleStatus), default=VehicleStatus.OPERATIONAL)
    current_route_id = db.Column(String(36), ForeignKey('transit_routes.id'))
    driver_id = db.Column(String(36), ForeignKey('drivers.id'))
    location_id = db.Column(String(36), ForeignKey('locations.id'))
    last_updated = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    driver = relationship('Driver', foreign_keys=[driver_id])
    location = relationship('Location', back_populates='vehicles')
    current_route = relationship('TransitRoute', back_populates='vehicles')
    
    __table_args__ = (
        Index('idx_vehicle_status', 'status'),
        Index('idx_vehicle_route', 'current_route_id'),
    )


# Transit Route Model
class TransitRoute(db.Model):
    __tablename__ = 'transit_routes'
    
    id = db.Column(String(36), primary_key=True)
    route_number = db.Column(String(50), unique=True, nullable=False)
    name = db.Column(String(100), nullable=False)
    start_location_id = db.Column(String(36), ForeignKey('locations.id'), nullable=False)
    end_location_id = db.Column(String(36), ForeignKey('locations.id'), nullable=False)
    distance = db.Column(Float, nullable=False)
    estimated_duration = db.Column(Integer)  # in minutes
    vehicle_type = db.Column(Enum(VehicleType), nullable=False)
    is_active = db.Column(Boolean, default=True)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stops = relationship('RouteStop', back_populates='route')
    schedules = relationship('Schedule', back_populates='route')
    traffic_data = relationship('TrafficData', back_populates='route')
    vehicles = relationship('Vehicle', back_populates='current_route')
    incidents = relationship('Incident', back_populates='route')
    
    __table_args__ = (
        Index('idx_route_number', 'route_number'),
        Index('idx_route_active', 'is_active'),
    )


# Route Stop Mapping
class RouteStop(db.Model):
    __tablename__ = 'route_stops'
    
    id = db.Column(String(36), primary_key=True)
    route_id = db.Column(String(36), ForeignKey('transit_routes.id'), nullable=False)
    bus_stop_id = db.Column(String(36), ForeignKey('bus_stops.id'), nullable=False)
    sequence = db.Column(Integer, nullable=False)
    arrival_time = db.Column(String(10))
    departure_time = db.Column(String(10))
    
    # Relationships
    route = relationship('TransitRoute', back_populates='stops')
    bus_stop = relationship('BusStop', back_populates='route_stops')


# Schedule Model
class Schedule(db.Model):
    __tablename__ = 'schedules'
    
    id = db.Column(String(36), primary_key=True)
    route_id = db.Column(String(36), ForeignKey('transit_routes.id'), nullable=False)
    day_of_week = db.Column(Integer, nullable=False)  # 0-6 (Monday-Sunday)
    departure_time = db.Column(String(10), nullable=False)
    arrival_time = db.Column(String(10), nullable=False)
    frequency = db.Column(Integer)  # in minutes
    is_active = db.Column(Boolean, default=True)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    route = relationship('TransitRoute', back_populates='schedules')
    
    __table_args__ = (
        Index('idx_schedule_route_day', 'route_id', 'day_of_week'),
    )


# Traffic Data Model
class TrafficData(db.Model):
    __tablename__ = 'traffic_data'
    
    id = db.Column(String(36), primary_key=True)
    route_id = db.Column(String(36), ForeignKey('transit_routes.id'), nullable=False)
    timestamp = db.Column(DateTime, default=datetime.utcnow)
    congestion_level = db.Column(Enum(CongestionLevel), default=CongestionLevel.FREE)
    average_speed = db.Column(Float)
    vehicle_count = db.Column(Integer, default=0)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    route = relationship('TransitRoute', back_populates='traffic_data')
    incidents = relationship('Incident', back_populates='traffic_data')
    
    __table_args__ = (
        Index('idx_traffic_route_timestamp', 'route_id', 'timestamp'),
        Index('idx_traffic_congestion', 'congestion_level'),
    )


# Incident Model
class Incident(db.Model):
    __tablename__ = 'incidents'
    
    id = db.Column(String(36), primary_key=True)
    type = db.Column(Enum(IncidentType), nullable=False)
    severity = db.Column(Enum(IncidentSeverity), nullable=False)
    description = db.Column(String(500))
    location_id = db.Column(String(36), ForeignKey('locations.id'), nullable=False)
    route_id = db.Column(String(36), ForeignKey('transit_routes.id'))
    traffic_data_id = db.Column(String(36), ForeignKey('traffic_data.id'))
    timestamp = db.Column(DateTime, default=datetime.utcnow)
    resolved_time = db.Column(DateTime)
    status = db.Column(String(20), default='ACTIVE')  # ACTIVE, RESOLVED
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    location = relationship('Location', back_populates='incidents')
    route = relationship('TransitRoute', back_populates='incidents')
    traffic_data = relationship('TrafficData', back_populates='incidents')
    alerts = relationship('Alert', back_populates='incident')
    
    __table_args__ = (
        Index('idx_incident_status_time', 'status', 'timestamp'),
        Index('idx_incident_severity', 'severity'),
    )


# Alert Model
class Alert(db.Model):
    __tablename__ = 'alerts'
    
    id = db.Column(String(36), primary_key=True)
    type = db.Column(Enum(AlertType), nullable=False)
    title = db.Column(String(100), nullable=False)
    message = db.Column(String(500), nullable=False)
    timestamp = db.Column(DateTime, default=datetime.utcnow)
    priority = db.Column(Enum(AlertPriority), default=AlertPriority.MEDIUM)
    is_read = db.Column(Boolean, default=False)
    incident_id = db.Column(String(36), ForeignKey('incidents.id'))
    created_at = db.Column(DateTime, default=datetime.utcnow)
    expires_at = db.Column(DateTime)
    
    # Relationships
    incident = relationship('Incident', back_populates='alerts')
    
    __table_args__ = (
        Index('idx_alert_priority_time', 'priority', 'timestamp'),
        Index('idx_alert_read_status', 'is_read'),
    )


# User Preference Model
class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    
    id = db.Column(String(36), primary_key=True)
    user_id = db.Column(String(36), unique=True, nullable=False)
    favorite_routes = db.Column(String(500))  # JSON string of route IDs
    preferred_start_time = db.Column(String(10))
    preferred_end_time = db.Column(String(10))
    accessibility_needs = db.Column(String(500))  # JSON string
    notification_email = db.Column(Boolean, default=True)
    notification_sms = db.Column(Boolean, default=False)
    notification_inapp = db.Column(Boolean, default=True)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
