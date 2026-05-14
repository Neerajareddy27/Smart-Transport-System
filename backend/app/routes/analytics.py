"""
API Routes for Analytics Microservice
"""
from flask import Blueprint, request, jsonify
from app.services.analytics import AnalyticsService

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@analytics_bp.route('/routes/<route_id>/statistics', methods=['GET'])
def get_route_statistics(route_id):
    """Get detailed statistics for a route"""
    try:
        days = request.args.get('days', 7, type=int)
        stats = AnalyticsService.get_route_statistics(route_id, days=days)
        
        return jsonify({
            'routeId': route_id,
            'trafficStats': {
                'recordCount': stats['traffic_stats'][1] if stats['traffic_stats'] else 0,
                'avgSpeed': stats['traffic_stats'][2] if stats['traffic_stats'] else 0,
                'maxSpeed': stats['traffic_stats'][3] if stats['traffic_stats'] else 0,
                'minSpeed': stats['traffic_stats'][4] if stats['traffic_stats'] else 0,
                'avgVehicles': stats['traffic_stats'][5] if stats['traffic_stats'] else 0
            },
            'congestionDistribution': [
                {'level': c[0].value, 'count': c[1]} for c in stats['congestion_distribution']
            ] if stats['congestion_distribution'] else [],
            'incidentStats': {
                'totalIncidents': stats['incident_stats'][0] if stats['incident_stats'] else 0,
                'criticalIncidents': stats['incident_stats'][1] if stats['incident_stats'] else 0
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/routes/<route_id>/peak-hours', methods=['GET'])
def get_peak_hours(route_id):
    """Get peak hour traffic analysis"""
    try:
        days = request.args.get('days', 7, type=int)
        peak_hours = AnalyticsService.get_peak_hours_analysis(route_id, days=days)
        
        return jsonify([{
            'hour': int(ph[0]) if ph[0] else 0,
            'recordCount': ph[1],
            'avgVehicles': float(ph[2]) if ph[2] else 0,
            'avgSpeed': float(ph[3]) if ph[3] else 0,
            'maxCongestion': ph[4].value if ph[4] else None
        } for ph in peak_hours]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/fleet/health', methods=['GET'])
def get_fleet_health():
    """Get overall fleet health status"""
    try:
        health = AnalyticsService.get_fleet_health_status()
        return jsonify({
            'totalVehicles': health['total_vehicles'],
            'operational': health['operational'],
            'operationalPercentage': health['operational_percentage'],
            'inMaintenance': health['in_maintenance'],
            'statusDistribution': [
                {'status': s[0].value, 'count': s[1]} for s in health['status_distribution']
            ]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/routes/most-congested', methods=['GET'])
def get_most_congested_routes():
    """Get most congested routes"""
    try:
        limit = request.args.get('limit', 10, type=int)
        hours = request.args.get('hours', 1, type=int)
        routes = AnalyticsService.get_most_congested_routes(limit=limit, hours=hours)
        
        return jsonify([{
            'routeId': r[0],
            'routeNumber': r[1],
            'name': r[2],
            'congestionLevel': r[3].value,
            'avgSpeed': float(r[4]) if r[4] else 0,
            'reportCount': r[5]
        } for r in routes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/incidents/report', methods=['GET'])
def get_incident_report():
    """Generate incident report"""
    try:
        severity = request.args.get('severity')
        days = request.args.get('days', 7, type=int)
        
        incidents = AnalyticsService.get_incident_report(severity=severity, days=days)
        return jsonify([{
            'type': i[0].value,
            'severity': i[1].value,
            'count': i[2],
            'avgResolutionTime': float(i[3]) if i[3] else 0
        } for i in incidents]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/vehicles/utilization', methods=['GET'])
def get_vehicle_utilization():
    """Get vehicle utilization metrics"""
    try:
        days = request.args.get('days', 7, type=int)
        util = AnalyticsService.get_vehicle_utilization(days=days)
        
        return jsonify([{
            'vehicleId': v[0],
            'vehicleNumber': v[1],
            'type': v[2].value,
            'avgPassengers': float(v[3]) if v[3] else 0,
            'maxPassengers': v[4],
            'utilizationPercentage': float(v[5]) if v[5] else 0
        } for v in util]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/routes/performance-ranking', methods=['GET'])
def get_performance_ranking():
    """Get route performance ranking"""
    try:
        limit = request.args.get('limit', 20, type=int)
        routes = AnalyticsService.get_route_performance_ranking(limit=limit)
        
        return jsonify([{
            'routeId': r[0],
            'routeNumber': r[1],
            'name': r[2],
            'observations': r[3],
            'avgSpeed': float(r[4]) if r[4] else 0,
            'severeCongestionCount': r[5],
            'incidentCount': r[6],
            'performanceScore': float(r[7]) if r[7] else 0
        } for r in routes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/daily-report', methods=['GET'])
def get_daily_report():
    """Get comprehensive daily report"""
    try:
        report = AnalyticsService.generate_daily_report()
        return jsonify({
            'date': report['date'].isoformat(),
            'totalIncidents': report['total_incidents'],
            'resolvedIncidents': report['resolved_incidents'],
            'criticalIncidents': report['critical_incidents'],
            'activeAlerts': report['active_alerts'],
            'fleetHealth': report['fleet_health'],
            'topCongestedRoutes': [{
                'routeId': r[0],
                'routeNumber': r[1],
                'name': r[2],
                'congestionLevel': r[3].value
            } for r in report['peak_congested_routes']]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
