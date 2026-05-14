import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, interval } from 'rxjs';
import { switchMap, shareReplay } from 'rxjs/operators';
import { TrafficData, Incident } from '../models/transit.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class TrafficDataService {
  private apiUrl = environment.apiUrl;
  private trafficDataSubject = new BehaviorSubject<TrafficData[]>([]);
  public trafficData$ = this.trafficDataSubject.asObservable();

  private incidentsSubject = new BehaviorSubject<Incident[]>([]);
  public incidents$ = this.incidentsSubject.asObservable();

  constructor(private http: HttpClient) {
    this.initializeRealTimeUpdates();
  }

  // Get traffic data for a specific route
  getTrafficDataByRoute(routeId: string): Observable<TrafficData> {
    return this.http.get<TrafficData>(`${this.apiUrl}/traffic/${routeId}`);
  }

  // Get all traffic data
  getAllTrafficData(): Observable<TrafficData[]> {
    return this.http.get<TrafficData[]>(`${this.apiUrl}/traffic`);
  }

  // Get incidents
  getIncidents(): Observable<Incident[]> {
    return this.http.get<Incident[]>(`${this.apiUrl}/incidents`);
  }

  // Get incidents by route
  getIncidentsByRoute(routeId: string): Observable<Incident[]> {
    return this.http.get<Incident[]>(`${this.apiUrl}/incidents?routeId=${routeId}`);
  }

  // Report an incident
  reportIncident(incident: Incident): Observable<Incident> {
    return this.http.post<Incident>(`${this.apiUrl}/incidents`, incident);
  }

  // Resolve incident
  resolveIncident(incidentId: string): Observable<Incident> {
    return this.http.patch<Incident>(`${this.apiUrl}/incidents/${incidentId}`, {
      resolvedTime: new Date()
    });
  }

  // Initialize real-time traffic updates (polling every 30 seconds)
  private initializeRealTimeUpdates(): void {
    interval(30000)
      .pipe(
        switchMap(() => this.getAllTrafficData()),
        shareReplay(1)
      )
      .subscribe(
        data => this.trafficDataSubject.next(data),
        error => console.error('Error fetching traffic data:', error)
      );
  }

  // Get real-time traffic data for analytics
  getTrafficAnalytics(routeId: string, duration: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/traffic`, {
      params: { routeId, duration: duration.toString() }
    });
  }

  // Update traffic data in cache
  updateTrafficDataCache(data: TrafficData[]): void {
    this.trafficDataSubject.next(data);
  }

  // Update incidents cache
  updateIncidentsCache(incidents: Incident[]): void {
    this.incidentsSubject.next(incidents);
  }
}
