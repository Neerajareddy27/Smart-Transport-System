// Transit Route Model
export interface TransitRoute {
  id: string;
  routeNumber: string;
  name: string;
  startLocation: Location;
  endLocation: Location;
  distance: number;
  estimatedDuration: number;
  stops: BusStop[];
  vehicleType: VehicleType;
  operatingHours: OperatingHours;
}

// Location Model
export interface Location {
  id: string;
  latitude: number;
  longitude: number;
  address: string;
  city: string;
  zipCode: string;
}

// Bus Stop Model
export interface BusStop {
  id: string;
  name: string;
  location: Location;
  arrivalTime: string;
  departureTime: string;
  capacity: number;
  currentPassengers: number;
}

// Vehicle Model
export interface Vehicle {
  id: string;
  vehicleNumber: string;
  type: VehicleType;
  capacity: number;
  currentPassengers: number;
  status: VehicleStatus;
  currentRoute: string;
  driver: Driver;
  location: Location;
  lastUpdated: Date;
}

// Traffic Data Model
export interface TrafficData {
  id: string;
  routeId: string;
  timestamp: Date;
  congestionLevel: CongestionLevel;
  averageSpeed: number;
  vehicles: number;
  incidents: Incident[];
}

// Incident Model
export interface Incident {
  id: string;
  type: IncidentType;
  severity: IncidentSeverity;
  description: string;
  location: Location;
  timestamp: Date;
  resolvedTime?: Date;
  affectedRoutes: string[];
}

// Schedule Model
export interface Schedule {
  id: string;
  routeId: string;
  dayOfWeek: number;
  departureTime: string;
  arrivalTime: string;
  frequency: number; // minutes
}

// User Preference Model
export interface UserPreference {
  id: string;
  userId: string;
  favoriteRoutes: string[];
  preferredTimeWindow: TimeWindow;
  accessibilityNeeds: string[];
  notificationPreferences: NotificationPreference;
}

// Route Query Model
export interface RouteQuery {
  startLocation: Location;
  endLocation: Location;
  departureTime?: Date;
  arrivalTime?: Date;
  preferences: UserPreference;
}

// Alternative Route Model
export interface AlternativeRoute {
  route: TransitRoute;
  totalDuration: number;
  transfers: number;
  departureTime: Date;
  arrivalTime: Date;
  price: number;
  trafficCondition: string;
}

// Driver Model
export interface Driver {
  id: string;
  name: string;
  licenseNumber: string;
  assignedVehicle: string;
  onDuty: boolean;
  shiftStartTime?: Date;
  shiftEndTime?: Date;
}

// Alert Model
export interface Alert {
  id: string;
  type: AlertType;
  title: string;
  message: string;
  timestamp: Date;
  routeIds: string[];
  priority: AlertPriority;
  read: boolean;
}

// Enums
export enum VehicleType {
  BUS = 'BUS',
  METRO = 'METRO',
  TRAM = 'TRAM',
  BIKE = 'BIKE'
}

export enum VehicleStatus {
  OPERATIONAL = 'OPERATIONAL',
  MAINTENANCE = 'MAINTENANCE',
  OUT_OF_SERVICE = 'OUT_OF_SERVICE',
  DELAYED = 'DELAYED'
}

export enum CongestionLevel {
  FREE = 'FREE',
  MODERATE = 'MODERATE',
  HEAVY = 'HEAVY',
  SEVERE = 'SEVERE'
}

export enum IncidentType {
  ACCIDENT = 'ACCIDENT',
  CONGESTION = 'CONGESTION',
  ROADWORK = 'ROADWORK',
  EVENT = 'EVENT',
  WEATHER = 'WEATHER'
}

export enum IncidentSeverity {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL'
}

export enum AlertType {
  DELAY = 'DELAY',
  INCIDENT = 'INCIDENT',
  SCHEDULE_CHANGE = 'SCHEDULE_CHANGE',
  SYSTEM_ALERT = 'SYSTEM_ALERT',
  WEATHER = 'WEATHER'
}

export enum AlertPriority {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH'
}

export interface TimeWindow {
  startTime: string;
  endTime: string;
}

export interface OperatingHours {
  monday: TimeWindow;
  tuesday: TimeWindow;
  wednesday: TimeWindow;
  thursday: TimeWindow;
  friday: TimeWindow;
  saturday: TimeWindow;
  sunday: TimeWindow;
}

export interface NotificationPreference {
  email: boolean;
  sms: boolean;
  inApp: boolean;
}
