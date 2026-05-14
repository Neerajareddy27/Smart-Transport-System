import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RealtimeAlertService } from '../../services/realtime-alert.service';
import { Alert, AlertType, AlertPriority } from '../../models/transit.model';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-alerts',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './alerts.component.html',
  styleUrls: ['./alerts.component.css']
})
export class AlertsComponent implements OnInit {
  alerts$: Observable<Alert[]>;
  connectionStatus$: Observable<boolean>;

  filterPriority: AlertPriority | '' = '';
  filterType: AlertType | '' = '';
  searchTerm = '';

  sortBy: 'recent' | 'priority' = 'recent';

  alertPriorities = Object.values(AlertPriority);
  alertTypes = Object.values(AlertType);

  constructor(private alertService: RealtimeAlertService) {
    this.alerts$ = this.alertService.getAllAlerts();
    this.connectionStatus$ = this.alertService.getConnectionStatus();
  }

  ngOnInit(): void {}

  getAlertIcon(type: AlertType): string {
    switch (type) {
      case AlertType.DELAY:
        return 'hourglass-end';
      case AlertType.INCIDENT:
        return 'exclamation-triangle';
      case AlertType.SCHEDULE_CHANGE:
        return 'calendar-times';
      case AlertType.WEATHER:
        return 'cloud-rain';
      case AlertType.SYSTEM_ALERT:
        return 'cog';
      default:
        return 'bell';
    }
  }

  getAlertBadgeClass(priority: AlertPriority): string {
    switch (priority) {
      case AlertPriority.HIGH:
        return 'danger';
      case AlertPriority.MEDIUM:
        return 'warning';
      case AlertPriority.LOW:
        return 'info';
      default:
        return 'secondary';
    }
  }

  markAsRead(alert: Alert): void {
    this.alertService.markAlertAsRead(alert.id);
  }

  clearAllAlerts(): void {
    if (confirm('Are you sure you want to clear all alerts?')) {
      this.alertService.clearAllAlerts();
    }
  }

  getFilteredAndSortedAlerts(alerts: Alert[]): Alert[] {
    let filtered = alerts;

    // Apply priority filter
    if (this.filterPriority) {
      filtered = filtered.filter(a => a.priority === this.filterPriority);
    }

    // Apply type filter
    if (this.filterType) {
      filtered = filtered.filter(a => a.type === this.filterType);
    }

    // Apply search term
    if (this.searchTerm.trim()) {
      const term = this.searchTerm.toLowerCase();
      filtered = filtered.filter(
        a => a.title.toLowerCase().includes(term) ||
             a.message.toLowerCase().includes(term)
      );
    }

    // Apply sorting
    if (this.sortBy === 'priority') {
      const priorityOrder: any = { HIGH: 0, MEDIUM: 1, LOW: 2 };
      filtered.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);
    } else {
      filtered.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
    }

    return filtered;
  }

  getUnreadCount(alerts: Alert[]): number {
    return alerts.filter(a => !a.read).length;
  }

  getHighPriorityCount(alerts: Alert[]): number {
    return alerts.filter(a => a.priority === AlertPriority.HIGH && !a.read).length;
  }

  getAlertCount(alerts: Alert[]): number {
    return alerts.length;
  }
}
