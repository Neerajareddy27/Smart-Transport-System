import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { VehicleManagementService } from '../../services/vehicle-management.service';
import { TrafficDataService } from '../../services/traffic-data.service';
import { Vehicle, TrafficData } from '../../models/transit.model';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-transit-map',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './transit-map.component.html',
  styleUrls: ['./transit-map.component.css']
})
export class TransitMapComponent implements OnInit, OnDestroy {
  vehicles: Vehicle[] = [];
  trafficData: TrafficData[] = [];
  selectedVehicle: Vehicle | null = null;
  selectedRoute: TrafficData | null = null;

  filters = {
    routeId: '',
    vehicleType: '',
    status: ''
  };

  isLoading = true;
  mapCenter = { lat: 40.7128, lng: -74.0060 }; // NYC Center
  mapZoom = 12;

  private destroy$ = new Subject<void>();

  constructor(
    private vehicleService: VehicleManagementService,
    private trafficService: TrafficDataService
  ) {}

  ngOnInit(): void {
    this.loadMapData();
    this.setupRealTimeUpdates();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private loadMapData(): void {
    // Load vehicles
    this.vehicleService.getAllVehicles()
      .pipe(takeUntil(this.destroy$))
      .subscribe(
        vehicles => {
          this.vehicles = vehicles;
          this.isLoading = false;
        },
        error => {
          console.error('Error loading vehicles:', error);
          this.isLoading = false;
        }
      );

    // Load traffic data
    this.trafficService.getAllTrafficData()
      .pipe(takeUntil(this.destroy$))
      .subscribe(
        data => this.trafficData = data,
        error => console.error('Error loading traffic data:', error)
      );
  }

  private setupRealTimeUpdates(): void {
    // Set up periodic updates for real-time data
    const updateInterval = setInterval(() => {
      this.loadMapData();
    }, 10000); // Update every 10 seconds

    this.destroy$.subscribe(() => clearInterval(updateInterval));
  }

  selectVehicle(vehicle: Vehicle): void {
    this.selectedVehicle = vehicle;
    // Update map center to vehicle location
    this.mapCenter = {
      lat: vehicle.location.latitude,
      lng: vehicle.location.longitude
    };
    this.mapZoom = 15;
  }

  selectRoute(traffic: TrafficData): void {
    this.selectedRoute = traffic;
  }

  getVehicleIcon(vehicleType: string): string {
    switch (vehicleType) {
      case 'BUS':
        return '🚌';
      case 'METRO':
        return '🚇';
      case 'TRAM':
        return '🚊';
      case 'BIKE':
        return '🚲';
      default:
        return '🚗';
    }
  }

  getStatusColor(status: string): string {
    switch (status) {
      case 'OPERATIONAL':
        return '#28a745';
      case 'DELAYED':
        return '#ffc107';
      case 'MAINTENANCE':
        return '#6c757d';
      case 'OUT_OF_SERVICE':
        return '#dc3545';
      default:
        return '#007bff';
    }
  }

  getCongestionColor(congestion: string): string {
    switch (congestion) {
      case 'FREE':
        return '#28a745';
      case 'MODERATE':
        return '#17a2b8';
      case 'HEAVY':
        return '#ffc107';
      case 'SEVERE':
        return '#dc3545';
      default:
        return '#6c757d';
    }
  }

  applyFilters(): void {
    // Filter vehicles based on criteria
    let filtered = [...this.vehicles];

    if (this.filters.vehicleType) {
      filtered = filtered.filter(v => v.type === this.filters.vehicleType);
    }

    if (this.filters.status) {
      filtered = filtered.filter(v => v.status === this.filters.status);
    }

    this.vehicles = filtered;
  }

  resetFilters(): void {
    this.filters = { routeId: '', vehicleType: '', status: '' };
    this.loadMapData();
  }

  zoomIn(): void {
    if (this.mapZoom < 20) this.mapZoom++;
  }

  zoomOut(): void {
    if (this.mapZoom > 1) this.mapZoom--;
  }

  centerMap(): void {
    this.mapCenter = { lat: 40.7128, lng: -74.0060 };
    this.mapZoom = 12;
  }

  getPassengerPercentage(vehicle: Vehicle): number {
    if (vehicle.capacity === 0) return 0;
    return Math.round((vehicle.currentPassengers / vehicle.capacity) * 100);
  }
}
