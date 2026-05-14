import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Schedule } from '../models/transit.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // Get all schedules
  getAllSchedules(): Observable<Schedule[]> {
    return this.http.get<Schedule[]>(`${this.apiUrl}/schedules`);
  }

  // Get schedule for a route
  getScheduleByRoute(routeId: string): Observable<Schedule[]> {
    return this.http.get<Schedule[]>(`${this.apiUrl}/schedules?routeId=${routeId}`);
  }

  // Create schedule
  createSchedule(schedule: Schedule): Observable<Schedule> {
    return this.http.post<Schedule>(`${this.apiUrl}/schedules`, schedule);
  }

  // Update schedule
  updateSchedule(scheduleId: string, schedule: Partial<Schedule>): Observable<Schedule> {
    return this.http.put<Schedule>(`${this.apiUrl}/schedules/${scheduleId}`, schedule);
  }

  // Delete schedule
  deleteSchedule(scheduleId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/schedules/${scheduleId}`);
  }

  // Get system statistics
  getSystemStatistics(): Observable<any> {
    return this.http.get(`${this.apiUrl}/admin/statistics`);
  }

  // Get peak hours data
  getPeakHoursData(): Observable<any> {
    return this.http.get(`${this.apiUrl}/admin/peak-hours`);
  }

  // Get route performance
  getRoutePerformance(routeId?: string): Observable<any> {
    const params = routeId ? `?routeId=${routeId}` : '';
    return this.http.get(`${this.apiUrl}/admin/route-performance${params}`);
  }

  // Generate report
  generateReport(reportType: string, params: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/admin/reports/${reportType}`, params);
  }

  // Export data
  exportData(dataType: string, format: string): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/admin/export/${dataType}?format=${format}`, {
      responseType: 'blob'
    });
  }

  // Get system configuration
  getSystemConfig(): Observable<any> {
    return this.http.get(`${this.apiUrl}/admin/config`);
  }

  // Update system configuration
  updateSystemConfig(config: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/admin/config`, config);
  }

  // Get user management data
  getAllUsers(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/admin/users`);
  }

  // Get user by ID
  getUserById(userId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/admin/users/${userId}`);
  }

  // Update user
  updateUser(userId: string, userData: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/admin/users/${userId}`, userData);
  }

  // Delete user
  deleteUser(userId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/admin/users/${userId}`);
  }
}
