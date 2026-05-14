"""
Day 6: Task 3 - Complex SQLAlchemy Queries for Advanced Data Analytics and Reporting
"""
from datetime import datetime, timedelta
from sqlalchemy import and_, or_, func, case, desc
from app.models import (
    db, TransitRoute, Vehicle, TrafficData, Incident, 
    Schedule, Alert, VehicleStatus, CongestionLevel, IncidentSeverity
)


class AnalyticsService:
    """Advanced analytics and reporting service"""
    
    @staticmethod
    def get_route_statistics(route_id, days=7):
        """Get detailed statistics for a route"""
        time_threshold = datetime.utcnow() - timedelta(days=days)
        
        # Query traffic data with aggregation
        traffic_stats = db.session.query(
            TrafficData.route_id,
            func.count(TrafficData.id).label('record_count'),
            func.avg(TrafficData.average_speed).label('avg_speed'),
            func.max(TrafficData.average_speed).label('max_speed'),
            func.min(TrafficData.average_speed).label('min_speed'),
            func.avg(TrafficData.vehicle_count).label('avg_vehicles')
        ).filter(
            and_(
                TrafficData.route_id == route_id,
                TrafficData.timestamp >= time_threshold
            )
        ).group_by(TrafficData.route_id).first()
        
        # Congestion distribution
        congestion_dist = db.session.query(
            TrafficData.congestion_level,
            func.count(TrafficData.id).label('count')
        ).filter(
            and_(
                TrafficData.route_id == route_id,
                TrafficData.timestamp >= time_threshold
            )
        ).group_by(TrafficData.congestion_level).all()
        
        # Incident statistics
        incident_stats = db.session.query(
            func.count(Incident.id).label('total_incidents'),
            func.count(case([(Incident.severity == IncidentSeverity.CRITICAL, 1)])).label('critical_incidents')
        ).filter(
            and_(
                Incident.route_id == route_id,
                Incident.timestamp >= time_threshold
            )
        ).first()
        
        return {
            'traffic_stats': traffic_stats,
            'congestion_distribution': congestion_dist,
            'incident_stats': incident_stats
        }
    
    @staticmethod
    def get_peak_hours_analysis(route_id, days=7):
        """Analyze peak hour traffic patterns"""
        time_threshold = datetime.utcnow() - timedelta(days=days)
        
        peak_hours = db.session.query(
            func.hour(TrafficData.timestamp).label('hour'),
            func.count(TrafficData.id).label('record_count'),
            func.avg(TrafficData.vehicle_count).label('avg_vehicles'),
            func.avg(TrafficData.average_speed).label('avg_speed'),
            func.max(TrafficData.congestion_level).label('max_congestion')
        ).filter(
            and_(
                TrafficData.route_id == route_id,
                TrafficData.timestamp >= time_threshold
            )
        ).group_by(
            func.hour(TrafficData.timestamp)
        ).order_by('hour').all()
        
        return peak_hours
    
    @staticmethod
    def get_fleet_health_status():
        """Get overall fleet health status"""
        vehicle_status_dist = db.session.query(
            Vehicle.status,
            func.count(Vehicle.id).label('count')
        ).group_by(Vehicle.status).all()
        
        total_vehicles = db.session.query(func.count(Vehicle.id)).scalar()
        operational = db.session.query(func.count(Vehicle.id)).filter_by(
            status=VehicleStatus.OPERATIONAL
        ).scalar()
        maintenance = db.session.query(func.count(Vehicle.id)).filter_by(
            status=VehicleStatus.MAINTENANCE
        ).scalar()
        
        return {
            'total_vehicles': total_vehicles,
            'operational': operational,
            'operational_percentage': (operational / total_vehicles * 100) if total_vehicles > 0 else 0,
            'in_maintenance': maintenance,
            'status_distribution': vehicle_status_dist
        }
    
    @staticmethod
    def get_most_congested_routes(limit=10, hours=1):
        """Get most congested routes"""
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        
        congested = db.session.query(
            TransitRoute.id,
            TransitRoute.route_number,
            TransitRoute.name,
            TrafficData.congestion_level,
            func.avg(TrafficData.average_speed).label('avg_speed'),
            func.count(TrafficData.id).label('report_count')
        ).join(
            TrafficData, TransitRoute.id == TrafficData.route_id
        ).filter(
            TrafficData.timestamp >= time_threshold
        ).group_by(
            TransitRoute.id,
            TransitRoute.route_number,
            TransitRoute.name,
            TrafficData.congestion_level
        ).order_by(
            desc(TrafficData.congestion_level)
        ).limit(limit).all()
        
        return congested
    
    @staticmethod
    def get_incident_report(severity=None, days=7):
        """Generate incident report with optional severity filter"""
        time_threshold = datetime.utcnow() - timedelta(days=days)
        
        query = db.session.query(
            Incident.type,
            Incident.severity,
            func.count(Incident.id).label('count'),
            func.avg(
                func.extract('epoch', Incident.resolved_time - Incident.timestamp)
            ).label('avg_resolution_time')
        ).filter(
            Incident.timestamp >= time_threshold
        )
        
        if severity:
            query = query.filter(Incident.severity == severity)
        
        incidents = query.group_by(
            Incident.type,
            Incident.severity
        ).all()
        
        return incidents
    
    @staticmethod
    def get_schedule_compliance(route_id, days=7):
        """Analyze schedule adherence and delay patterns"""
        time_threshold = datetime.utcnow() - timedelta(days=days)
        
        # Analyze alerts related to delays
        delay_alerts = db.session.query(
            func.count(Alert.id).label('delay_count'),
            func.avg(
                func.extract('epoch', Alert.timestamp - func.cast(Alert.timestamp, db.String))
            ).label('avg_delay_duration')
        ).filter(
            and_(
                Alert.type.like('DELAY%'),
                Alert.timestamp >= time_threshold
            )
        ).first()
        
        return delay_alerts
    
    @staticmethod
    def get_vehicle_utilization(days=7):
        """Get vehicle utilization metrics"""
        time_threshold = datetime.utcnow() - timedelta(days=days)
        
        utilization = db.session.query(
            Vehicle.id,
            Vehicle.vehicle_number,
            Vehicle.type,
            func.avg(Vehicle.current_passengers).label('avg_passengers'),
            func.max(Vehicle.current_passengers).label('max_passengers'),
            (func.avg(Vehicle.current_passengers) / func.avg(Vehicle.capacity) * 100).label('utilization_percentage')
        ).group_by(
            Vehicle.id,
            Vehicle.vehicle_number,
            Vehicle.type,
            Vehicle.capacity
        ).all()
        
        return utilization
    
    @staticmethod
    def get_route_performance_ranking(limit=20):
        """Rank routes by performance metrics"""
        # Complex query combining multiple metrics
        performance = db.session.query(
            TransitRoute.id,
            TransitRoute.route_number,
            TransitRoute.name,
            func.count(TrafficData.id).label('observations'),
            func.avg(TrafficData.average_speed).label('avg_speed'),
            func.count(case([
                (TrafficData.congestion_level == CongestionLevel.SEVERE, 1)
            ])).label('severe_congestion_count'),
            func.count(case([
                (Incident.id.isnot(None), 1)
            ])).label('incident_count'),
            (
                100 * (func.avg(TrafficData.average_speed) / 60) * 
                (1 - func.count(case([
                    (TrafficData.congestion_level == CongestionLevel.SEVERE, 1)
                ])) / func.count(TrafficData.id))
            ).label('performance_score')
        ).outerjoin(
            TrafficData, TransitRoute.id == TrafficData.route_id
        ).outerjoin(
            Incident, TransitRoute.id == Incident.route_id
        ).group_by(
            TransitRoute.id,
            TransitRoute.route_number,
            TransitRoute.name
        ).order_by(
            desc('performance_score')
        ).limit(limit).all()
        
        return performance
    
    @staticmethod
    def get_time_series_data(route_id, metric='congestion', hours=24):
        """Get time series data for visualization"""
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        
        if metric == 'congestion':
            timeseries = db.session.query(
                func.date_trunc('hour', TrafficData.timestamp).label('time_bucket'),
                func.avg(TrafficData.vehicle_count).label('avg_vehicles'),
                TrafficData.congestion_level,
                func.count(TrafficData.id).label('record_count')
            ).filter(
                and_(
                    TrafficData.route_id == route_id,
                    TrafficData.timestamp >= time_threshold
                )
            ).group_by(
                func.date_trunc('hour', TrafficData.timestamp),
                TrafficData.congestion_level
            ).order_by('time_bucket').all()
        
        return timeseries
    
    @staticmethod
    def generate_daily_report():
        """Generate comprehensive daily operations report"""
        today = datetime.utcnow().date()
        
        report = {
            'date': today,
            'total_incidents': db.session.query(func.count(Incident.id)).filter(
                func.cast(Incident.timestamp, db.Date) == today
            ).scalar(),
            'resolved_incidents': db.session.query(func.count(Incident.id)).filter(
                and_(
                    func.cast(Incident.timestamp, db.Date) == today,
                    Incident.status == 'RESOLVED'
                )
            ).scalar(),
            'critical_incidents': db.session.query(func.count(Incident.id)).filter(
                and_(
                    func.cast(Incident.timestamp, db.Date) == today,
                    Incident.severity == IncidentSeverity.CRITICAL
                )
            ).scalar(),
            'active_alerts': db.session.query(func.count(Alert.id)).filter(
                and_(
                    func.cast(Alert.timestamp, db.Date) == today,
                    Alert.is_read == False
                )
            ).scalar(),
            'fleet_health': AnalyticsService.get_fleet_health_status(),
            'peak_congested_routes': AnalyticsService.get_most_congested_routes(limit=5, hours=24)
        }
        
        return report
