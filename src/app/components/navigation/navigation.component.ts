import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { RealtimeAlertService } from '../../services/realtime-alert.service';
import { Alert, AlertPriority } from '../../models/transit.model';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-navigation',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css']
})
export class NavigationComponent implements OnInit {
  alerts$: Observable<Alert[]>;
  connectionStatus$: Observable<boolean>;
  isCollapsed = true;
  unreadAlertCount = 0;
  highPriorityAlerts: Alert[] = [];

  constructor(private alertService: RealtimeAlertService) {
    this.alerts$ = this.alertService.getAllAlerts();
    this.connectionStatus$ = this.alertService.getConnectionStatus();
  }

  ngOnInit(): void {
    this.alerts$.subscribe(alerts => {
      this.unreadAlertCount = alerts.filter(a => !a.read).length;
      this.highPriorityAlerts = alerts.filter(
        a => a.priority === AlertPriority.HIGH && !a.read
      ).slice(0, 3);
    });
  }

  toggleNavbar(): void {
    this.isCollapsed = !this.isCollapsed;
  }

  markAlertAsRead(alert: Alert, event: Event): void {
    event.stopPropagation();
    this.alertService.markAlertAsRead(alert.id);
  }

  clearAllAlerts(): void {
    this.alertService.clearAllAlerts();
  }
}
