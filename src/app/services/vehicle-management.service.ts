import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { Vehicle, Driver } from '../models/transit.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class VehicleManagementService {
  private apiUrl = environment.apiUrl;
  private vehiclesSubject = new BehaviorSubject<Vehicle[]>([]);
  public vehicles$ = this.vehiclesSubject.asObservable();

  constructor(private http: HttpClient) {}

  // Get all vehicles
  getAllVehicles(): Observable<Vehicle[]> {
    return this.http.get<Vehicle[]>(`${this.apiUrl}/vehicles`);
  }

  // Get vehicle by ID
  getVehicleById(vehicleId: string): Observable<Vehicle> {
    return this.http.get<Vehicle>(`${this.apiUrl}/vehicles/${vehicleId}`);
  }

  // Get vehicles by route
  getVehiclesByRoute(routeId: string): Observable<Vehicle[]> {
    return this.http.get<Vehicle[]>(`${this.apiUrl}/vehicles?routeId=${routeId}`);
  }

  // Update vehicle status
  updateVehicleStatus(vehicleId: string, status: string): Observable<Vehicle> {
    return this.http.patch<Vehicle>(
      `${this.apiUrl}/vehicles/${vehicleId}`,
      { status }
    );
  }

  // Track vehicle location
  getVehicleLocation(vehicleId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/vehicles/${vehicleId}/location`);
  }

  // Create new vehicle (admin)
  createVehicle(vehicle: Vehicle): Observable<Vehicle> {
    return this.http.post<Vehicle>(`${this.apiUrl}/vehicles`, vehicle);
  }

  // Update vehicle (admin)
  updateVehicle(vehicleId: string, vehicle: Partial<Vehicle>): Observable<Vehicle> {
    return this.http.put<Vehicle>(`${this.apiUrl}/vehicles/${vehicleId}`, vehicle);
  }

  // Delete vehicle (admin)
  deleteVehicle(vehicleId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/vehicles/${vehicleId}`);
  }

  // Get vehicles for maintenance
  getVehiclesForMaintenance(): Observable<Vehicle[]> {
    return this.http.get<Vehicle[]>(`${this.apiUrl}/vehicles/maintenance`);
  }

  // Update vehicles cache
  updateVehiclesCache(vehicles: Vehicle[]): void {
    this.vehiclesSubject.next(vehicles);
  }

  // Get vehicle metrics/analytics
  getVehicleAnalytics(vehicleId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/vehicles/${vehicleId}`);
  }
}
