import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { io, Socket } from 'socket.io-client';
import { Alert, AlertType, AlertPriority } from '../models/transit.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RealtimeAlertService {
  private socket: Socket | null = null;
  private alertsSubject = new BehaviorSubject<Alert[]>([]);
  public alerts$ = this.alertsSubject.asObservable();

  private connectionStatusSubject = new BehaviorSubject<boolean>(false);
  public connectionStatus$ = this.connectionStatusSubject.asObservable();

  private socketUrl = environment.socketUrl;

  constructor() {
    this.initializeSocket();
  }

  // Initialize WebSocket connection
  private initializeSocket(): void {
    this.socket = io(this.socketUrl, {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    });

    this.socket.on('connect', () => {
      console.log('Connected to alert server');
      this.connectionStatusSubject.next(true);
      this.subscribeToAlerts();
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from alert server');
      this.connectionStatusSubject.next(false);
    });

    this.socket.on('alert', (alert: Alert) => {
      this.addAlert(alert);
    });

    this.socket.on('alerts-batch', (alerts: Alert[]) => {
      this.alertsSubject.next(alerts);
    });

    this.socket.on('alert-resolved', (alertId: string) => {
      this.removeAlert(alertId);
    });
  }

  // Subscribe to alerts for specific routes
  subscribeToRouteAlerts(routeIds: string[]): void {
    if (this.socket) {
      this.socket.emit('subscribe', { routes: routeIds });
    }
  }

  // Unsubscribe from route alerts
  unsubscribeFromRouteAlerts(routeIds: string[]): void {
    if (this.socket) {
      this.socket.emit('unsubscribe', { routes: routeIds });
    }
  }

  // Subscribe to all alerts
  private subscribeToAlerts(): void {
    if (this.socket) {
      this.socket.emit('get-all-alerts');
    }
  }

  // Get all current alerts
  getAllAlerts(): Observable<Alert[]> {
    return this.alerts$;
  }

  // Add alert locally
  private addAlert(alert: Alert): void {
    const currentAlerts = this.alertsSubject.value;
    const updatedAlerts = [alert, ...currentAlerts];
    this.alertsSubject.next(updatedAlerts);
  }

  // Remove alert locally
  private removeAlert(alertId: string): void {
    const currentAlerts = this.alertsSubject.value;
    const updatedAlerts = currentAlerts.filter(a => a.id !== alertId);
    this.alertsSubject.next(updatedAlerts);
  }

  // Mark alert as read
  markAlertAsRead(alertId: string): void {
    if (this.socket) {
      this.socket.emit('mark-alert-read', alertId);
    }
    const currentAlerts = this.alertsSubject.value;
    const updatedAlerts = currentAlerts.map(a =>
      a.id === alertId ? { ...a, read: true } : a
    );
    this.alertsSubject.next(updatedAlerts);
  }

  // Clear all alerts
  clearAllAlerts(): void {
    this.alertsSubject.next([]);
    if (this.socket) {
      this.socket.emit('clear-alerts');
    }
  }

  // Get connection status
  getConnectionStatus(): Observable<boolean> {
    return this.connectionStatus$;
  }

  // Reconnect to socket
  reconnect(): void {
    if (this.socket && !this.socket.connected) {
      this.socket.connect();
    }
  }

  // Disconnect from socket
  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
    }
  }
}
