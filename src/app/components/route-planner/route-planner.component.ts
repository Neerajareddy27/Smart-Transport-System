import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RoutePlannerService } from '../../services/route-planner.service';
import { UserPreferenceService } from '../../services/user-preference.service';
import { RouteQuery, AlternativeRoute, Location, UserPreference } from '../../models/transit.model';

@Component({
  selector: 'app-route-planner',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './route-planner.component.html',
  styleUrls: ['./route-planner.component.css']
})
export class RoutePlannerComponent implements OnInit {
  routeForm: FormGroup;
  alternativeRoutes: AlternativeRoute[] = [];
  selectedRoute: AlternativeRoute | null = null;
  isSearching = false;
  errorMessage: string | null = null;
  userPreference: UserPreference | null = null;
  locations: Location[] = [];
  searchHistory: RouteQuery[] = [];

  constructor(
    private fb: FormBuilder,
    private routePlannerService: RoutePlannerService,
    private userPreferenceService: UserPreferenceService
  ) {
    this.routeForm = this.fb.group({
      startLocation: ['', Validators.required],
      endLocation: ['', Validators.required],
      departureTime: ['', Validators.required],
      preferAccessibleRoutes: [false],
      preferFewestTransfers: [false]
    });
  }

  ngOnInit(): void {
    this.loadLocations();
    this.loadUserPreferences();
  }

  private loadLocations(): void {
    this.routePlannerService.getLocations().subscribe(
      (locations) => {
        this.locations = locations;
        console.log('Loaded locations:', locations);
      },
      error => console.error('Error loading locations:', error)
    );
  }

  private loadUserPreferences(): void {
    // In a real app, would load actual user ID
    const userId = 'current-user'; // Placeholder
    this.userPreferenceService.getUserPreferences(userId).subscribe(
      pref => this.userPreference = pref,
      error => console.error('Error loading user preferences:', error)
    );
  }

  searchRoutes(): void {
    if (this.routeForm.invalid) {
      this.errorMessage = 'Please fill in all required fields';
      return;
    }

    this.isSearching = true;
    this.errorMessage = null;
    this.alternativeRoutes = [];

    const startLocationId = this.routeForm.get('startLocation')?.value;
    const endLocationId = this.routeForm.get('endLocation')?.value;
    const selectedStart = this.locations.find(l => l.id === startLocationId);
    const selectedEnd = this.locations.find(l => l.id === endLocationId);

    const query: RouteQuery = {
      startLocation: selectedStart || { id: startLocationId } as Location,
      endLocation: selectedEnd || { id: endLocationId } as Location,
      departureTime: new Date(this.routeForm.get('departureTime')?.value),
      preferences: this.userPreference || {} as UserPreference
    };

    this.routePlannerService.searchAlternativeRoutes(query).subscribe(
      routes => {
        this.alternativeRoutes = routes;
        this.addToSearchHistory(query);
        this.isSearching = false;

        if (routes.length === 0) {
          this.errorMessage = 'No routes found for the selected criteria';
        }
      },
      error => {
        this.errorMessage = 'Error searching routes. Please try again.';
        this.isSearching = false;
        console.error('Search error:', error);
      }
    );
  }

  selectRoute(route: AlternativeRoute): void {
    this.selectedRoute = route;
    // In a real app, would save selection and show next steps
    console.log('Route selected:', route);
  }

  addFavoriteRoute(routeId: string): void {
    if (!this.userPreference) return;

    const userId = 'current-user'; // Placeholder
    this.userPreferenceService.addFavoriteRoute(userId, routeId).subscribe(
      updated => {
        this.userPreference = updated;
        console.log('Route added to favorites');
      },
      error => console.error('Error adding favorite route:', error)
    );
  }

  private addToSearchHistory(query: RouteQuery): void {
    this.searchHistory.unshift(query);
    if (this.searchHistory.length > 5) {
      this.searchHistory.pop();
    }
  }

  clearFilters(): void {
    this.routeForm.reset();
    this.alternativeRoutes = [];
    this.selectedRoute = null;
    this.errorMessage = null;
  }

  getDurationDisplay(minutes: number): string {
    if (minutes < 60) return `${minutes} min`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  }

  getPriceDisplay(price: number): string {
    return `$${price.toFixed(2)}`;
  }

  getTrafficClass(traffic: string): string {
    switch (traffic.toLowerCase()) {
      case 'clear':
        return 'success';
      case 'light':
        return 'info';
      case 'moderate':
        return 'warning';
      case 'heavy':
        return 'danger';
      default:
        return 'secondary';
    }
  }
}
