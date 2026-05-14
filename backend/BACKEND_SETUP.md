# Smart City Transportation Backend - Setup & Documentation

## Backend Architecture Overview

This is a complete Flask microservices backend for the Smart City Transportation Management System.

### Day 6: SQLAlchemy ORM - Transit Data Modeling

**Files:**
- `app/models/__init__.py` - 11 SQLAlchemy models with proper relationships and indexes
- `app/services/daos.py` - 7 Data Access Objects (DAOs) for CRUD operations

**Models Implemented:**
- Location, BusStop, Driver, Vehicle, TransitRoute, RouteStop
- Schedule, TrafficData, Incident, Alert, UserPreference
- Enums: VehicleType, VehicleStatus, CongestionLevel, IncidentType, IncidentSeverity, AlertType, AlertPriority

**Key Features:**
- Foreign key relationships with cascading deletes
- Database indexes for performance optimization
- Enum support for status and type fields
- Timestamp tracking (created_at, updated_at)

**DAOs Implemented:**
- RouteDAO: CRUD for transit routes
- VehicleDAO: Vehicle management and status tracking
- TrafficDataDAO: Traffic monitoring and historical data
- IncidentDAO: Incident reporting and resolution
- ScheduleDAO: Schedule management
- AlertDAO: Alert creation and management

### Day 6: Task 3 - Advanced Analytics & Reporting

**File:** `app/services/analytics.py`

**Analytics Methods:**
- `get_route_statistics()` - Aggregate traffic data with speed/vehicle metrics
- `get_peak_hours_analysis()` - Hour-by-hour traffic pattern analysis
- `get_fleet_health_status()` - Vehicle operational status distribution
- `get_most_congested_routes()` - Route ranking by congestion
- `get_incident_report()` - Incident statistics and resolution times
- `get_vehicle_utilization()` - Passenger capacity utilization metrics
- `get_route_performance_ranking()` - Complex scoring algorithm
- `generate_daily_report()` - Comprehensive daily operations report

**Queries Used:**
- Complex GROUP BY aggregations
- Time-series bucketing with date_trunc
- Case statements for conditional counting
- JOINs between multiple tables
- Window functions and calculated fields

### Day 7: Flask Microservices Architecture

**File:** `app/microservices/__init__.py`

**Microservices:**
1. RouteService - Transit route management
2. TrafficService - Real-time traffic monitoring
3. VehicleService - Fleet vehicle management
4. AlertService - Alert distribution
5. AnalyticsService - Data analytics and reporting

**Service Registry:**
- `ServiceRegistry` class for service discovery
- Register/deregister services dynamically
- Get service status and list all services
- Health check system

**Configuration Management:**
- `ConfigurationManager` for peak/off-peak hour configs
- Different alert thresholds per time period
- Adaptive update frequencies
- Time-based mode switching (peak_hours, off_peak_hours, normal_hours)

### Day 7: Microservices Routes

**Files:**
- `app/routes/routes.py` - Route management endpoints
- `app/routes/vehicles.py` - Vehicle management endpoints
- `app/routes/traffic.py` - Traffic & incident endpoints
- `app/routes/alerts.py` - Alert endpoints
- `app/routes/analytics.py` - Analytics & reporting endpoints

**API Endpoints:**

**Routes Service:**
- GET `/api/routes` - List all routes
- GET `/api/routes/<id>` - Get route details
- POST `/api/routes` - Create new route
- PUT `/api/routes/<id>` - Update route
- DELETE `/api/routes/<id>` - Delete route
- POST `/api/routes/search` - Search routes

**Vehicles Service:**
- GET `/api/vehicles` - List all vehicles
- GET `/api/vehicles/<id>` - Get vehicle details
- POST `/api/vehicles` - Create vehicle
- PUT `/api/vehicles/<id>/status` - Update status
- PUT `/api/vehicles/<id>/location` - Update location
- PUT `/api/vehicles/<id>/passengers` - Update passengers
- GET `/api/vehicles/by-route/<route_id>` - Vehicles on route
- GET `/api/vehicles/by-status/<status>` - Vehicles by status

**Traffic Service:**
- POST `/api/traffic/record` - Create traffic record
- GET `/api/traffic/by-route/<route_id>` - Route traffic history
- GET `/api/traffic/current/<route_id>` - Current traffic
- GET `/api/traffic/by-congestion/<level>` - Routes by congestion

**Incidents:**
- POST `/api/traffic/incidents` - Report incident
- GET `/api/traffic/incidents` - Active incidents
- PUT `/api/traffic/incidents/<id>/resolve` - Resolve incident
- GET `/api/traffic/incidents/by-route/<route_id>` - Route incidents

**Alerts Service:**
- POST `/api/alerts` - Create alert
- GET `/api/alerts` - Active alerts
- GET `/api/alerts/unread` - Unread alerts
- PUT `/api/alerts/<id>/read` - Mark as read
- GET `/api/alerts/by-priority/<priority>` - Alerts by priority

**Analytics Service:**
- GET `/api/analytics/routes/<id>/statistics` - Route statistics
- GET `/api/analytics/routes/<id>/peak-hours` - Peak hour analysis
- GET `/api/analytics/fleet/health` - Fleet health
- GET `/api/analytics/routes/most-congested` - Congested routes
- GET `/api/analytics/incidents/report` - Incident report
- GET `/api/analytics/vehicles/utilization` - Vehicle utilization
- GET `/api/analytics/routes/performance-ranking` - Performance ranking
- GET `/api/analytics/daily-report` - Daily report

### Day 8: Flask-SocketIO - Real-Time Communication

**File:** `app/services/realtime.py`

**Features:**
- WebSocket connections with automatic reconnection
- Route subscription system
- Real-time event broadcasting

**WebSocket Events:**

**Server -> Client:**
- `connection_response` - Connection confirmed
- `new_alert` - Alert broadcast
- `traffic_update` - Traffic data updates
- `vehicle_update` - Vehicle location/status
- `incident_alert` - Incident notifications
- `status` - System status

**Client -> Server:**
- `connect` - Connection event
- `disconnect` - Disconnection event
- `subscribe_route` - Subscribe to route updates
- `unsubscribe_route` - Unsubscribe from route
- `get_connection_status` - Request status

**Background Service:**
- Continuous alert broadcasting
- Periodic traffic updates
- Vehicle status monitoring
- Incident notifications

### System Architecture

```
Angular Frontend (port 4200)
        ↓
    HTTP/REST API
        ↓
Flask Backend (port 5000)
    ├── Routes Service
    ├── Vehicles Service
    ├── Traffic Service
    ├── Alerts Service
    └── Analytics Service
        ↓
    SQLAlchemy ORM
        ↓
    SQLite/PostgreSQL/MySQL Database

    WebSocket (SocketIO)
        ↓
Real-time Alert Broadcasting
```

## Installation & Setup

### 1. Create Virtual Environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Edit .env file with your database and settings
```

### 4. Initialize Database
```bash
flask db upgrade  # Or run init_db command
```

### 5. Run the Application
```bash
python app.py
# Or
flask run
```

The backend will start on `http://localhost:5000`

## Database Models

### Entities

**Location**
- latitude, longitude
- address, city, zip_code
- Foreign keys: bus_stops, vehicles, incidents

**BusStop**
- name, location (FK)
- arrival_time, departure_time
- capacity, current_passengers

**Driver**
- name, license_number (unique)
- assigned_vehicle_id (FK)
- shift tracking

**Vehicle**
- vehicle_number (unique)
- type (enum), capacity, status
- current_passengers
- current_route (FK), driver (FK), location (FK)
- last_updated tracking

**TransitRoute**
- route_number (unique), name
- start_location, end_location
- distance, estimated_duration
- vehicle_type

**RouteStop**
- route (FK), bus_stop (FK)
- sequence ordering
- arrival/departure times

**Schedule**
- route (FK)
- day_of_week
- departure/arrival times
- frequency (minutes)

**TrafficData**
- route (FK)
- congestion_level, average_speed, vehicle_count
- Time-series indexed

**Incident**
- type, severity (enums)
- location (FK), route (FK)
- status (ACTIVE/RESOLVED)
- resolution tracking

**Alert**
- type, title, message
- priority level
- incident link
- expiration tracking

**UserPreference**
- user_id
- favorite_routes (JSON)
- notification preferences

## Configuration Management

### Peak Hours (7-10 AM)
- Alert threshold: 0.8 (80% congestion)
- Update frequency: 5 seconds
- Cache duration: 60 seconds

### Normal Hours (10 AM - 10 PM)
- Alert threshold: 0.6 (60%)
- Update frequency: 15 seconds
- Cache duration: 120 seconds

### Off-Peak Hours (10 PM - 7 AM)
- Alert threshold: 0.5 (50%)
- Update frequency: 30 seconds
- Cache duration: 300 seconds

## Performance Optimizations

- Database indexes on frequently queried columns
- DAO pattern for centralized queries
- Time-series data aggregation
- Lazy loading relationships
- Connection pooling
- Real-time caching with SocketIO

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Deployment

For production:
1. Use PostgreSQL instead of SQLite
2. Set `FLASK_ENV=production`
3. Use Redis for SocketIO message queue
4. Enable HTTPS/TLS
5. Set up proper CORS origins
6. Use a production WSGI server (Gunicorn, uWSGI)

## Integration with Frontend

The backend integrates with the Angular frontend via:

1. **REST API** - Standard HTTP requests for CRUD operations
2. **WebSocket (SocketIO)** - Real-time alerts and updates
3. **CORS** - Cross-origin requests enabled

Frontend services call corresponding backend endpoints:
- RouteService → `/api/routes`
- VehicleManagementService → `/api/vehicles`
- TrafficDataService → `/api/traffic`
- RealtimeAlertService → WebSocket + `/api/alerts`
- AdminService → Multiple endpoints

## Next Steps

- Add authentication/authorization
- Implement request validation middleware
- Add comprehensive logging
- Set up monitoring and alerting
- Deploy to cloud infrastructure
- Add GraphQL layer (optional)
