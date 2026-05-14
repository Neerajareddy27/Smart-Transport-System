import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { UserPreference } from '../models/transit.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserPreferenceService {
  private apiUrl = environment.apiUrl;
  private userPreferenceSubject = new BehaviorSubject<UserPreference | null>(null);
  public userPreference$ = this.userPreferenceSubject.asObservable();

  constructor(private http: HttpClient) {}

  // Get user preferences
  getUserPreferences(userId: string): Observable<UserPreference> {
    return this.http.get<UserPreference>(`${this.apiUrl}/users/${userId}/preferences`);
  }

  // Save user preferences
  saveUserPreferences(userId: string, preference: UserPreference): Observable<UserPreference> {
    return this.http.post<UserPreference>(
      `${this.apiUrl}/users/${userId}/preferences`,
      preference
    );
  }

  // Update user preferences
  updateUserPreferences(userId: string, preference: Partial<UserPreference>): Observable<UserPreference> {
    return this.http.put<UserPreference>(
      `${this.apiUrl}/users/${userId}/preferences`,
      preference
    );
  }

  // Add favorite route
  addFavoriteRoute(userId: string, routeId: string): Observable<UserPreference> {
    return this.http.post<UserPreference>(
      `${this.apiUrl}/users/${userId}/favorites`,
      { routeId }
    );
  }

  // Remove favorite route
  removeFavoriteRoute(userId: string, routeId: string): Observable<UserPreference> {
    return this.http.delete<UserPreference>(
      `${this.apiUrl}/users/${userId}/favorites/${routeId}`
    );
  }

  // Update notification preferences
  updateNotificationPreferences(userId: string, preferences: any): Observable<UserPreference> {
    return this.http.patch<UserPreference>(
      `${this.apiUrl}/users/${userId}/notification-preferences`,
      preferences
    );
  }

  // Update user preference cache
  updateUserPreferenceCache(preference: UserPreference): void {
    this.userPreferenceSubject.next(preference);
  }

  // Get accessibility options
  getAccessibilityOptions(): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/accessibility-options`);
  }
}
