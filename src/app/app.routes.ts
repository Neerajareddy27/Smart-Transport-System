import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { RoutePlannerComponent } from './components/route-planner/route-planner.component';
import { TransitMapComponent } from './components/transit-map/transit-map.component';
import { AdminPortalComponent } from './components/admin-portal/admin-portal.component';
import { AlertsComponent } from './components/alerts/alerts.component';

export const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'route-planner', component: RoutePlannerComponent },
  { path: 'transit-map', component: TransitMapComponent },
  { path: 'admin', component: AdminPortalComponent },
  { path: 'alerts', component: AlertsComponent },
];
