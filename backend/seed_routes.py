#!/usr/bin/env python3
"""
Seed database with sample routes and locations for testing
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import create_app
from app.models import db, Location, TransitRoute, VehicleType
import uuid

def seed_database():
    app, socketio = create_app()
    
    with app.app_context():
        print("🌱 Seeding database with routes...")
        
        # Clear existing data
        print("🗑️  Clearing existing data...")
        Location.query.delete()
        TransitRoute.query.delete()
        db.session.commit()
        
        # Create sample locations
        loc1 = Location(
            id="loc-chennai",
            latitude=13.0827,
            longitude=80.2707,
            address="Chennai Central",
            city="Chennai",
            zip_code="600001"
        )
        loc2 = Location(
            id="loc-hyderabad",
            latitude=17.3850,
            longitude=78.4867,
            address="Hyderabad Central",
            city="Hyderabad",
            zip_code="500001"
        )
        loc3 = Location(
            id="loc-bangalore",
            latitude=12.9716,
            longitude=77.5946,
            address="Bangalore Central",
            city="Bangalore",
            zip_code="560001"
        )
        db.session.add_all([loc1, loc2, loc3])
        db.session.commit()
        print(f"✓ Created 3 locations")
        
        # Create sample routes
        route1 = TransitRoute(
            id=str(uuid.uuid4()),
            route_number="101",
            name="Chennai to Hyderabad Express",
            start_location_id="loc-chennai",
            end_location_id="loc-hyderabad",
            distance=570.0,
            estimated_duration=540,  # 9 hours
            vehicle_type=VehicleType.BUS,
            is_active=True
        )
        route2 = TransitRoute(
            id=str(uuid.uuid4()),
            route_number="102",
            name="Hyderabad to Bangalore Express",
            start_location_id="loc-hyderabad",
            end_location_id="loc-bangalore",
            distance=560.0,
            estimated_duration=600,  # 10 hours
            vehicle_type=VehicleType.BUS,
            is_active=True
        )
        route3 = TransitRoute(
            id=str(uuid.uuid4()),
            route_number="103",
            name="Chennai to Bangalore Metro",
            start_location_id="loc-chennai",
            end_location_id="loc-bangalore",
            distance=350.0,
            estimated_duration=420,  # 7 hours
            vehicle_type=VehicleType.BUS,
            is_active=True
        )
        db.session.add_all([route1, route2, route3])
        db.session.commit()
        print(f"✓ Created 3 active routes")
        
        # Verify routes exist
        all_routes = TransitRoute.query.all()
        print(f"\n📍 Total routes in database: {len(all_routes)}")
        for route in all_routes:
            print(f"   - Route {route.route_number}: {route.name}")
        
        print("\n✅ Database seeded successfully!")
        print("\n📝 Test the search endpoint with:")
        print("   curl -X POST http://localhost:5000/api/routes/search \\")
        print('     -H "Content-Type: application/json" \\')
        print('     -d \'{"startLocation": {"id": "loc-chennai"}, "endLocation": {"id": "loc-hyderabad"}}\'')

if __name__ == '__main__':
    seed_database()
