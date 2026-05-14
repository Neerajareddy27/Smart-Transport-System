import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { TransitRoute, RouteQuery, AlternativeRoute, Location } from '../models/transit.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RoutePlannerService {
  private apiUrl = environment.apiUrl;
  private routesSubject = new BehaviorSubject<TransitRoute[]>([]);
  public routes$ = this.routesSubject.asObservable();

  constructor(private http: HttpClient) {}

  // Get all available locations
  getLocations(): Observable<Location[]> {
    return this.http.get<Location[]>(`${this.apiUrl}/routes/locations`);
  }

  // Get all available routes
  getAllRoutes(): Observable<TransitRoute[]> {
    return this.http.get<TransitRoute[]>(`${this.apiUrl}/routes`);
  }

  // Get route by ID
  getRouteById(routeId: string): Observable<TransitRoute> {
    return this.http.get<TransitRoute>(`${this.apiUrl}/routes/${routeId}`);
  }

  // Search for alternative routes based on query
  searchAlternativeRoutes(query: RouteQuery): Observable<AlternativeRoute[]> {
    return this.http.post<AlternativeRoute[]>(
      `${this.apiUrl}/routes/search`,
      query
    );
  }

  // Create a new route (admin)
  createRoute(route: TransitRoute): Observable<TransitRoute> {
    return this.http.post<TransitRoute>(`${this.apiUrl}/routes`, route);
  }

  // Update route
  updateRoute(routeId: string, route: Partial<TransitRoute>): Observable<TransitRoute> {
    return this.http.put<TransitRoute>(`${this.apiUrl}/routes/${routeId}`, route);
  }

  // Delete route (admin)
  deleteRoute(routeId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/routes/${routeId}`);
  }

  // Update routes in cache
  updateRoutesCache(routes: TransitRoute[]): void {
    this.routesSubject.next(routes);
  }
}
