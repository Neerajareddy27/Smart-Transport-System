import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RoutePlannerService } from '../../services/route-planner.service';
import { TrafficDataService } from '../../services/traffic-data.service';
import { VehicleManagementService } from '../../services/vehicle-management.service';
import { RealtimeAlertService } from '../../services/realtime-alert.service';
import { TransitRoute, TrafficData, Vehicle, Alert } from '../../models/transit.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  routes: TransitRoute[] = [];
  trafficData: TrafficData[] = [];
  vehicles: Vehicle[] = [];
  alerts: Alert[] = [];

  stats = {
    totalRoutes: 0,
    operationalVehicles: 0,
    activeIncidents: 0,
    systemHealth: 100
  };

  isLoading = true;
  errorMessage: string | null = null;

  constructor(
    private routePlannerService: RoutePlannerService,
    private trafficDataService: TrafficDataService,
    private vehicleService: VehicleManagementService,
    private alertService: RealtimeAlertService
  ) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  private loadDashboardData(): void {
    try {
      // Load routes
      this.routePlannerService.getAllRoutes().subscribe(
        routes => {
          this.routes = routes;
          this.stats.totalRoutes = routes.length;
        },
        error => console.error('Error loading routes:', error)
      );

      // Load traffic data
      this.trafficDataService.getAllTrafficData().subscribe(
        data => {
          this.trafficData = data;
        },
        error => console.error('Error loading traffic data:', error)
      );

      // Load vehicles
      this.vehicleService.getAllVehicles().subscribe(
        vehicles => {
          this.vehicles = vehicles;
          this.stats.operationalVehicles = vehicles.filter(v => v.status === 'OPERATIONAL').length;
        },
        error => console.error('Error loading vehicles:', error)
      );

      // Load alerts
      this.alertService.getAllAlerts().subscribe(
        alerts => {
          this.alerts = alerts;
          this.stats.activeIncidents = alerts.length;
          this.updateSystemHealth();
        }
      );

      this.isLoading = false;
    } catch (error) {
      this.errorMessage = 'Failed to load dashboard data';
      this.isLoading = false;
    }
  }

  private updateSystemHealth(): void {
    const healthScore = 100 - (this.stats.activeIncidents * 5);
    this.stats.systemHealth = Math.max(0, healthScore);
  }

  getCongestionStats(): any {
    const congestionLevels = this.trafficData.reduce((acc: any, data) => {
      acc[data.congestionLevel] = (acc[data.congestionLevel] || 0) + 1;
      return acc;
    }, {});
    return congestionLevels;
  }

  getHealthClass(): string {
    if (this.stats.systemHealth >= 80) return 'success';
    if (this.stats.systemHealth >= 50) return 'warning';
    return 'danger';
  }

  getStatusBadgeClass(status: string): string {
    switch (status) {
      case 'FREE':
        return 'success';
      case 'MODERATE':
        return 'info';
      case 'HEAVY':
        return 'warning';
      case 'SEVERE':
        return 'danger';
      default:
        return 'secondary';
    }
  }

  getAlertIcon(type: string): string {
    switch (type) {
      case 'DELAY':
        return 'hourglass-end';
      case 'INCIDENT':
        return 'exclamation-triangle';
      case 'SCHEDULE_CHANGE':
        return 'calendar-times';
      case 'WEATHER':
        return 'cloud-rain';
      default:
        return 'bell';
    }
  }
}
