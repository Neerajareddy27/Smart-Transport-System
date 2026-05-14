"""
Seed sample data for testing
"""
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.getcwd())

# Create app using the factory
if __name__ == '__main__':
    # Use sys to import the app module from app.py
    import importlib.util
    spec = importlib.util.spec_from_file_location("app_module", "./app.py")
    app_module = importlib.util.module_from_spec(spec)
    sys.modules['app_module'] = app_module
    spec.loader.exec_module(app_module)
    
    create_app = app_module.create_app
    
    # Now import models
    from app.models import (
    db, Location, BusStop, Driver, Vehicle, TransitRoute, RouteStop, 
    Schedule, TrafficData, Incident, Alert, UserPreference,
    VehicleType, VehicleStatus, CongestionLevel, IncidentType, 
    IncidentSeverity, AlertType, AlertPriority
)
import uuid
from datetime import datetime, timedelta

app, socketio = create_app()

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    # Create sample locations
    loc1 = Location(
        id=str(uuid.uuid4()),
        latitude=40.7128,
        longitude=-74.0060,
        address="123 Main St",
        city="New York",
        zip_code="10001"
    )
    loc2 = Location(
        id=str(uuid.uuid4()),
        latitude=40.7580,
        longitude=-73.9855,
        address="456 Park Ave",
        city="New York",
        zip_code="10022"
    )
    loc3 = Location(
        id=str(uuid.uuid4()),
        latitude=40.6892,
        longitude=-74.0445,
        address="789 Broadway",
        city="New York",
        zip_code="10003"
    )
    db.session.add_all([loc1, loc2, loc3])
    db.session.commit()
    
    # Create bus stops
    stop1 = BusStop(
        id=str(uuid.uuid4()),
        name="Central Station",
        location_id=loc1.id,
        arrival_time="09:00",
        departure_time="09:05",
        capacity=100,
        current_passengers=45
    )
    stop2 = BusStop(
        id=str(uuid.uuid4()),
        name="Park Terminal",
        location_id=loc2.id,
        arrival_time="09:15",
        departure_time="09:20",
        capacity=100,
        current_passengers=67
    )
    stop3 = BusStop(
        id=str(uuid.uuid4()),
        name="Downtown Hub",
        location_id=loc3.id,
        arrival_time="09:30",
        departure_time="09:35",
        capacity=100,
        current_passengers=89
    )
    db.session.add_all([stop1, stop2, stop3])
    db.session.commit()
    
    # Create drivers
    driver1 = Driver(
        id=str(uuid.uuid4()),
        name="John Smith",
        license_number="DL123456",
        on_duty=True,
        shift_start_time=datetime.utcnow(),
        shift_end_time=datetime.utcnow() + timedelta(hours=8)
    )
    driver2 = Driver(
        id=str(uuid.uuid4()),
        name="Jane Doe",
        license_number="DL654321",
        on_duty=True,
        shift_start_time=datetime.utcnow(),
        shift_end_time=datetime.utcnow() + timedelta(hours=8)
    )
    driver3 = Driver(
        id=str(uuid.uuid4()),
        name="Mike Johnson",
        license_number="DL789012",
        on_duty=False
    )
    db.session.add_all([driver1, driver2, driver3])
    db.session.commit()
    
    # Create transit routes
    route1 = TransitRoute(
        id=str(uuid.uuid4()),
        route_number="101",
        name="Main Cross Town",
        start_location_id=loc1.id,
        end_location_id=loc2.id,
        distance=5.2,
        estimated_duration=25,
        vehicle_type=VehicleType.BUS,
        is_active=True
    )
    route2 = TransitRoute(
        id=str(uuid.uuid4()),
        route_number="202",
        name="Downtown Express",
        start_location_id=loc2.id,
        end_location_id=loc3.id,
        distance=3.8,
        estimated_duration=18,
        vehicle_type=VehicleType.BUS,
        is_active=True
    )
    route3 = TransitRoute(
        id=str(uuid.uuid4()),
        route_number="303",
        name="Uptown Limited",
        start_location_id=loc1.id,
        end_location_id=loc3.id,
        distance=8.5,
        estimated_duration=35,
        vehicle_type=VehicleType.METRO,
        is_active=True
    )
    db.session.add_all([route1, route2, route3])
    db.session.commit()
    
    # Create route stops
    rs1 = RouteStop(
        id=str(uuid.uuid4()),
        route_id=route1.id,
        bus_stop_id=stop1.id,
        stop_order=1,
        arrival_time="09:00",
        departure_time="09:05"
    )
    rs2 = RouteStop(
        id=str(uuid.uuid4()),
        route_id=route1.id,
        bus_stop_id=stop2.id,
        stop_order=2,
        arrival_time="09:15",
        departure_time="09:20"
    )
    db.session.add_all([rs1, rs2])
    db.session.commit()
    
    # Create vehicles
    vehicle1 = Vehicle(
        id=str(uuid.uuid4()),
        vehicle_number="BUS-001",
        type=VehicleType.BUS,
        capacity=50,
        current_passengers=35,
        status=VehicleStatus.OPERATIONAL,
        current_route_id=route1.id,
        driver_id=driver1.id,
        location_id=loc1.id
    )
    vehicle2 = Vehicle(
        id=str(uuid.uuid4()),
        vehicle_number="BUS-002",
        type=VehicleType.BUS,
        capacity=50,
        current_passengers=42,
        status=VehicleStatus.OPERATIONAL,
        current_route_id=route2.id,
        driver_id=driver2.id,
        location_id=loc2.id
    )
    vehicle3 = Vehicle(
        id=str(uuid.uuid4()),
        vehicle_number="METRO-001",
        type=VehicleType.METRO,
        capacity=120,
        current_passengers=98,
        status=VehicleStatus.MAINTENANCE,
        current_route_id=route3.id,
        location_id=loc3.id
    )
    db.session.add_all([vehicle1, vehicle2, vehicle3])
    db.session.commit()
    
    # Create schedules
    schedule1 = Schedule(
        id=str(uuid.uuid4()),
        route_id=route1.id,
        start_time="06:00",
        end_time="23:00",
        frequency_minutes=15,
        is_active=True
    )
    schedule2 = Schedule(
        id=str(uuid.uuid4()),
        route_id=route2.id,
        start_time="06:00",
        end_time="23:00",
        frequency_minutes=20,
        is_active=True
    )
    db.session.add_all([schedule1, schedule2])
    db.session.commit()
    
    # Create traffic data
    traffic1 = TrafficData(
        id=str(uuid.uuid4()),
        route_id=route1.id,
        congestion_level=CongestionLevel.MODERATE,
        average_speed=25.5,
        vehicle_count=8,
        timestamp=datetime.utcnow()
    )
    traffic2 = TrafficData(
        id=str(uuid.uuid4()),
        route_id=route2.id,
        congestion_level=CongestionLevel.HEAVY,
        average_speed=15.2,
        vehicle_count=12,
        timestamp=datetime.utcnow()
    )
    db.session.add_all([traffic1, traffic2])
    db.session.commit()
    
    # Create incidents
    incident1 = Incident(
        id=str(uuid.uuid4()),
        type=IncidentType.ACCIDENT,
        severity=IncidentSeverity.HIGH,
        location_id=loc2.id,
        route_id=route1.id,
        description="Minor accident on main street",
        reported_at=datetime.utcnow(),
        resolved_time=None,
        is_resolved=False
    )
    incident2 = Incident(
        id=str(uuid.uuid4()),
        type=IncidentType.CONGESTION,
        severity=IncidentSeverity.MEDIUM,
        location_id=loc3.id,
        route_id=route2.id,
        description="Heavy traffic due to construction",
        reported_at=datetime.utcnow(),
        resolved_time=None,
        is_resolved=False
    )
    db.session.add_all([incident1, incident2])
    db.session.commit()
    
    # Create alerts
    alert1 = Alert(
        id=str(uuid.uuid4()),
        type=AlertType.DELAY,
        title="Route 101 Delayed",
        message="Route 101 experiencing 10 minute delay due to traffic",
        priority=AlertPriority.HIGH,
        route_id=route1.id,
        incident_id=incident1.id,
        timestamp=datetime.utcnow(),
        is_read=False
    )
    alert2 = Alert(
        id=str(uuid.uuid4()),
        type=AlertType.INCIDENT,
        title="Accident on Route 202",
        message="Minor accident reported on Route 202",
        priority=AlertPriority.MEDIUM,
        route_id=route2.id,
        incident_id=incident2.id,
        timestamp=datetime.utcnow(),
        is_read=False
    )
    db.session.add_all([alert1, alert2])
    db.session.commit()
    
    # Create user preferences
    pref1 = UserPreference(
        id=str(uuid.uuid4()),
        user_id="user-1",
        preferred_routes=[route1.id, route2.id],
        notification_enabled=True,
        theme="dark"
    )
    db.session.add(pref1)
    db.session.commit()
    
    print("✅ Sample data created successfully!")
    print(f"  - Locations: 3")
    print(f"  - Bus Stops: 3")
    print(f"  - Drivers: 3")
    print(f"  - Routes: 3")
    print(f"  - Vehicles: 3")
    print(f"  - Schedules: 2")
    print(f"  - Traffic Data: 2")
    print(f"  - Incidents: 2")
    print(f"  - Alerts: 2")
    print(f"  - User Preferences: 1")
