import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AdminService } from '../../services/admin.service';
import { TrafficDataService } from '../../services/traffic-data.service';
import { Schedule, Incident, IncidentType, IncidentSeverity } from '../../models/transit.model';

@Component({
  selector: 'app-admin-portal',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './admin-portal.component.html',
  styleUrls: ['./admin-portal.component.css']
})
export class AdminPortalComponent implements OnInit {
  activeTab = 'dashboard';

  // Dashboard
  systemStats: any = {
    totalRoutes: 0,
    totalVehicles: 0,
    activeIncidents: 0,
    systemHealth: 100
  };

  // Schedules
  schedules: Schedule[] = [];
  scheduleForm: FormGroup;
  editingSchedule: Schedule | null = null;

  // Incidents
  incidents: Incident[] = [];
  incidentForm: FormGroup;

  // Form visibility
  showScheduleForm = false;
  showIncidentForm = false;

  isLoading = false;
  successMessage: string | null = null;
  errorMessage: string | null = null;

  incidentTypes = Object.values(IncidentType);
  incidentSeverities = Object.values(IncidentSeverity);

  constructor(
    private fb: FormBuilder,
    private adminService: AdminService,
    private trafficService: TrafficDataService
  ) {
    this.scheduleForm = this.fb.group({
      routeId: ['', Validators.required],
      dayOfWeek: ['', Validators.required],
      departureTime: ['', Validators.required],
      arrivalTime: ['', Validators.required],
      frequency: ['', Validators.required]
    });

    this.incidentForm = this.fb.group({
      type: ['', Validators.required],
      severity: ['', Validators.required],
      description: ['', Validators.required],
      affectedRoutes: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.loadDashboardData();
    this.loadSchedules();
    this.loadIncidents();
  }

  private loadDashboardData(): void {
    this.adminService.getSystemStatistics().subscribe(
      stats => this.systemStats = stats,
      error => console.error('Error loading statistics:', error)
    );
  }

  private loadSchedules(): void {
    this.adminService.getAllSchedules().subscribe(
      schedules => this.schedules = schedules,
      error => console.error('Error loading schedules:', error)
    );
  }

  private loadIncidents(): void {
    this.trafficService.getIncidents().subscribe(
      incidents => this.incidents = incidents,
      error => console.error('Error loading incidents:', error)
    );
  }

  // Schedule Management
  openScheduleForm(schedule?: Schedule): void {
    if (schedule) {
      this.editingSchedule = schedule;
      this.scheduleForm.patchValue(schedule);
    } else {
      this.editingSchedule = null;
      this.scheduleForm.reset();
    }
    this.showScheduleForm = true;
  }

  saveSchedule(): void {
    if (this.scheduleForm.invalid) {
      this.errorMessage = 'Please fill in all required fields';
      return;
    }

    this.isLoading = true;
    const formData = this.scheduleForm.value;

    if (this.editingSchedule) {
      this.adminService.updateSchedule(this.editingSchedule.id, formData).subscribe(
        updated => {
          const index = this.schedules.findIndex(s => s.id === this.editingSchedule!.id);
          if (index > -1) {
            this.schedules[index] = updated;
          }
          this.successMessage = 'Schedule updated successfully';
          this.closeScheduleForm();
        },
        error => {
          this.errorMessage = 'Error updating schedule';
          console.error(error);
        },
        () => this.isLoading = false
      );
    } else {
      this.adminService.createSchedule(formData).subscribe(
        created => {
          this.schedules.push(created);
          this.successMessage = 'Schedule created successfully';
          this.closeScheduleForm();
        },
        error => {
          this.errorMessage = 'Error creating schedule';
          console.error(error);
        },
        () => this.isLoading = false
      );
    }
  }

  deleteSchedule(scheduleId: string): void {
    if (confirm('Are you sure you want to delete this schedule?')) {
      this.adminService.deleteSchedule(scheduleId).subscribe(
        () => {
          this.schedules = this.schedules.filter(s => s.id !== scheduleId);
          this.successMessage = 'Schedule deleted successfully';
        },
        error => {
          this.errorMessage = 'Error deleting schedule';
          console.error(error);
        }
      );
    }
  }

  closeScheduleForm(): void {
    this.showScheduleForm = false;
    this.scheduleForm.reset();
    this.editingSchedule = null;
  }

  // Incident Management
  reportIncident(): void {
    if (this.incidentForm.invalid) {
      this.errorMessage = 'Please fill in all required fields';
      return;
    }

    this.isLoading = true;
    const formData = {
      ...this.incidentForm.value,
      timestamp: new Date(),
      affectedRoutes: this.incidentForm.value.affectedRoutes.split(',').map((r: string) => r.trim())
    };

    this.trafficService.reportIncident(formData).subscribe(
      incident => {
        this.incidents.unshift(incident);
        this.successMessage = 'Incident reported successfully';
        this.closeIncidentForm();
      },
      error => {
        this.errorMessage = 'Error reporting incident';
        console.error(error);
      },
      () => this.isLoading = false
    );
  }

  resolveIncident(incidentId: string): void {
    this.trafficService.resolveIncident(incidentId).subscribe(
      updated => {
        const index = this.incidents.findIndex(i => i.id === incidentId);
        if (index > -1) {
          this.incidents[index] = updated;
        }
        this.successMessage = 'Incident resolved successfully';
      },
      error => {
        this.errorMessage = 'Error resolving incident';
        console.error(error);
      }
    );
  }

  closeIncidentForm(): void {
    this.showIncidentForm = false;
    this.incidentForm.reset();
  }

  // Tab Navigation
  selectTab(tab: string): void {
    this.activeTab = tab;
    this.clearMessages();
  }

  private clearMessages(): void {
    this.successMessage = null;
    this.errorMessage = null;
  }

  getHealthClass(): string {
    if (this.systemStats.systemHealth >= 80) return 'success';
    if (this.systemStats.systemHealth >= 50) return 'warning';
    return 'danger';
  }

  getSeverityBadgeClass(severity: string): string {
    switch (severity) {
      case 'LOW':
        return 'info';
      case 'MEDIUM':
        return 'warning';
      case 'HIGH':
        return 'danger';
      case 'CRITICAL':
        return 'dark';
      default:
        return 'secondary';
    }
  }
}
