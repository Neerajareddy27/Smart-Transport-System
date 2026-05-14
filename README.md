# Smart City Transportation Management System

A comprehensive Angular-based web application for managing urban transportation systems in real-time. This application provides route planning, traffic monitoring, vehicle management, and administrative controls for a smart city's transit infrastructure.

## Features

### Day 1-2: User Interface & Interactive Maps
- **Route Planner**: Search for optimal routes with multiple filter options
- **Interactive Transit Map**: Real-time vehicle tracking and traffic visualization
- **Responsive Design**: Bootstrap and Angular Material for mobile-friendly UI
- **Dynamic Updates**: Client-side route option updates based on user interactions

### Day 3: Traffic Data Processing
- **Real-time Traffic Monitoring**: Live traffic data for all routes
- **Incident Management**: Report and track transportation incidents
- **Data Analytics**: Advanced traffic analytics and reporting
- **Alternative Routes**: Intelligent route suggestions based on traffic conditions

### Day 4: System Configuration
- **Flask-compatible Backend**: Ready for Python Flask backend integration
- **Session Management**: Secure user session handling
- **User Preferences**: Customizable user settings and accessibility options
- **Application Context**: Proper Angular service structure for data management

### Day 5: Administration Portal
- **Schedule Management**: Create and manage transit schedules
- **Route Administration**: Manage routes and their properties
- **Form Handling**: Reactive Forms for incident reporting and feedback
- **User Management**: Admin controls for user accounts and permissions

### Day 6: Data Modeling
- **SQLAlchemy-like Models**: TypeScript interfaces mirroring database models
- **Data Access Objects**: Services implementing CRUD operations
- **Complex Queries**: Advanced filtering and data aggregation
- **Relationships**: Proper model relationships (Routes, Vehicles, Schedules)

### Day 7: Microservices Architecture
- **Service-based Design**: Modular service architecture
- **Service Discovery**: Ready for microservices integration
- **Configuration Management**: Environment-based configuration
- **Scalability**: Designed for horizontal scaling

### Day 8: Real-time Alerts
- **WebSocket Integration**: Socket.IO for real-time alerts
- **Live Notifications**: City-wide transportation notifications
- **Alert Management**: Priority-based alert filtering and management
- **Connection Monitoring**: Real-time connection status monitoring

## Project Structure

```
smart-city-transport/
├── src/
│   ├── app/
│   │   ├── components/           # Angular components
│   │   │   ├── navigation/       # Top navigation bar
│   │   │   ├── dashboard/        # System dashboard
│   │   │   ├── route-planner/    # Route planning interface
│   │   │   ├── transit-map/      # Interactive map view
│   │   │   ├── admin-portal/     # Admin management panel
│   │   │   └── alerts/           # Alerts and notifications
│   │   ├── services/             # Data services
│   │   │   ├── route-planner.service.ts
│   │   │   ├── traffic-data.service.ts
│   │   │   ├── vehicle-management.service.ts
│   │   │   ├── realtime-alert.service.ts
│   │   │   ├── user-preference.service.ts
│   │   │   └── admin.service.ts
│   │   ├── models/              # TypeScript models/interfaces
│   │   │   └── transit.model.ts
│   │   ├── app.routes.ts        # Routing configuration
│   │   ├── app.config.ts        # Application configuration
│   │   ├── app.component.ts     # Root component
│   │   └── app.component.html
│   ├── styles.css               # Global styles
│   ├── index.html               # HTML entry point
│   └── main.ts                  # Bootstrap file
├── package.json                 # Dependencies
├── angular.json                 # Angular CLI config
├── tsconfig.json                # TypeScript config
└── README.md                    # This file
```

## Technology Stack

- **Framework**: Angular 17
- **Language**: TypeScript
- **Styling**: Bootstrap 5, Angular Material, CSS3
- **State Management**: RxJS Observables
- **Real-time**: Socket.IO for WebSocket communication
- **HTTP**: Angular HttpClient
- **Forms**: Reactive Forms (FormBuilder)
- **Routing**: Angular Router

## Getting Started

### Prerequisites
- Node.js (v18 or higher)
- npm (v9 or higher)
- Angular CLI (`npm install -g @angular/cli`)

### Installation

1. Navigate to the project directory:
```bash
cd smart-city-transport
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open your browser and navigate to `http://localhost:4200`

### Build for Production

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## API Integration

The application is designed to work with a Flask backend. Update the API URLs in service files:

```typescript
private apiUrl = 'http://localhost:3000/api';
```

### Expected Backend Endpoints

**Routes:**
- `GET /api/routes` - Get all routes
- `GET /api/routes/:id` - Get route by ID
- `POST /api/routes/search` - Search routes
- `POST /api/routes` - Create route (admin)
- `PUT /api/routes/:id` - Update route (admin)
- `DELETE /api/routes/:id` - Delete route (admin)

**Traffic Data:**
- `GET /api/traffic` - Get all traffic data
- `GET /api/traffic/:routeId` - Get traffic by route
- `GET /api/incidents` - Get all incidents
- `POST /api/incidents` - Report incident
- `PATCH /api/incidents/:id` - Resolve incident

**Vehicles:**
- `GET /api/vehicles` - Get all vehicles
- `GET /api/vehicles/:id` - Get vehicle by ID
- `GET /api/vehicles?routeId=:id` - Get vehicles by route
- `PATCH /api/vehicles/:id` - Update vehicle
- `POST /api/vehicles` - Create vehicle (admin)
- `DELETE /api/vehicles/:id` - Delete vehicle (admin)

**Admin:**
- `GET /api/admin/statistics` - System statistics
- `GET /api/schedules` - Get all schedules
- `POST /api/schedules` - Create schedule
- `PUT /api/schedules/:id` - Update schedule
- `DELETE /api/schedules/:id` - Delete schedule
- `GET /api/admin/config` - System configuration

## Real-time Alerts

The application uses Socket.IO for real-time alerts. Configure the WebSocket URL in `realtime-alert.service.ts`:

```typescript
private socketUrl = 'http://localhost:3001';
```

### Socket Events

- `connect` - Connected to alert server
- `alert` - Receive a new alert
- `alerts-batch` - Receive batch of alerts
- `alert-resolved` - Alert was resolved

## Features in Detail

### Route Planner
- Search routes by origin and destination
- Filter by departure/arrival time
- Accessibility and transfer preferences
- View alternative routes with cost and duration
- Save favorite routes

### Transit Map
- Real-time vehicle positioning
- Traffic congestion visualization
- Filter vehicles by type and status
- View vehicle details and capacity
- Zoom and pan controls
- Traffic status for each route

### Admin Portal
- Schedule management (create, edit, delete)
- System statistics and health monitoring
- Incident reporting and tracking
- Peak hour analysis
- Route performance metrics
- User management

### Alerts
- Real-time alert notifications
- Priority-based filtering
- Alert search and filtering
- Connection status monitoring
- Mark alerts as read
- Bulk alert management

## Styling & Customization

### Global Styles
- Modify `src/styles.css` for global styling
- Component-specific styles in respective CSS files
- Bootstrap classes for responsive design
- Dark mode support (can be extended)

### Customizing Colors
Update Bootstrap variables or create custom themes in `styles.css`:

```css
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  /* Add more color variables */
}
```

## Performance Optimization

- Lazy loading routes (can be implemented)
- OnPush change detection strategy
- RxJS operators for efficient data flow
- AOT compilation in production
- Tree-shaking and minification

## Accessibility

- ARIA labels on interactive elements
- Semantic HTML structure
- Keyboard navigation support
- Color contrast compliance
- Screen reader friendly

## Testing

Tests can be added using Angular testing utilities:

```bash
npm run test
```

## Deployment

### Docker Deployment
Create a `Dockerfile`:

```dockerfile
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist/smart-city-transport /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Environment Configuration

Create environment-specific configurations:
- `src/environments/environment.ts` - Development
- `src/environments/environment.prod.ts` - Production

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request
4. Ensure all tests pass

## License

MIT License - feel free to use this project for educational and commercial purposes

## Support

For issues, questions, or suggestions, please create an issue in the project repository.

## Future Enhancements

- [ ] Google Maps integration
- [ ] Advanced analytics dashboard
- [ ] Machine learning for traffic prediction
- [ ] Multi-language support
- [ ] Dark mode theme
- [ ] Mobile native app
- [ ] AI-powered chatbot support
- [ ] Payment integration
- [ ] User feedback and ratings
- [ ] Integration testing suite
