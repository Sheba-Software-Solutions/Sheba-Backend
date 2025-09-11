# Sheba Admin Dashboard API Documentation

## Overview
The Sheba Admin Dashboard API is built using Django REST Framework and provides comprehensive backend functionality for managing projects, clients, content, communication, and dashboard analytics.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The API uses Token-based authentication. Include the token in the Authorization header:
```
Authorization: Token your_token_here
```

### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}
```

**Response:**
```json
{
    "token": "your_auth_token",
    "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin"
    }
}
```

### Logout
```http
POST /api/auth/logout/
Authorization: Token your_token_here
```

## User Management

### List Users
```http
GET /api/auth/users/
Authorization: Token your_token_here
```

### Create User
```http
POST /api/auth/users/
Authorization: Token your_token_here
Content-Type: application/json

{
    "username": "newuser",
    "email": "user@example.com",
    "password": "password123",
    "role": "developer",
    "phone": "+1234567890"
}
```

### Update User
```http
PUT /api/auth/users/{id}/
Authorization: Token your_token_here
Content-Type: application/json

{
    "username": "updateduser",
    "email": "updated@example.com",
    "role": "manager"
}
```

## Client Management

### List Clients
```http
GET /api/clients/
Authorization: Token your_token_here
```

**Query Parameters:**
- `search`: Search by name, email, or company
- `status`: Filter by status (active, inactive, potential)
- `ordering`: Sort by field (name, created_at, -created_at)

### Create Client
```http
POST /api/clients/
Authorization: Token your_token_here
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "company": "Tech Corp",
    "status": "active",
    "address": "123 Main St, City, State"
}
```

### Get Client Details
```http
GET /api/clients/{id}/
Authorization: Token your_token_here
```

### Update Client
```http
PUT /api/clients/{id}/
Authorization: Token your_token_here
Content-Type: application/json

{
    "name": "John Smith",
    "status": "inactive"
}
```

### Delete Client
```http
DELETE /api/clients/{id}/
Authorization: Token your_token_here
```

### Client Statistics
```http
GET /api/clients/statistics/
Authorization: Token your_token_here
```

## Project Management

### List Projects
```http
GET /api/projects/
Authorization: Token your_token_here
```

**Query Parameters:**
- `search`: Search by name or description
- `status`: Filter by status (planning, in_progress, testing, completed, on_hold, cancelled)
- `priority`: Filter by priority (low, medium, high, urgent)
- `client`: Filter by client ID
- `assigned_to`: Filter by assigned user ID

### Create Project
```http
POST /api/projects/
Authorization: Token your_token_here
Content-Type: application/json

{
    "name": "E-commerce Platform",
    "description": "Modern e-commerce solution",
    "client": 1,
    "status": "planning",
    "priority": "high",
    "start_date": "2024-01-01",
    "end_date": "2024-06-01",
    "budget": 50000.00,
    "technologies": ["React", "Django", "PostgreSQL"]
}
```

### Get Project Details
```http
GET /api/projects/{id}/
Authorization: Token your_token_here
```

### Update Project
```http
PUT /api/projects/{id}/
Authorization: Token your_token_here
Content-Type: application/json

{
    "status": "in_progress",
    "progress": 25
}
```

### Project Tasks
```http
GET /api/projects/{id}/tasks/
POST /api/projects/{id}/tasks/
PUT /api/projects/{id}/tasks/{task_id}/
DELETE /api/projects/{id}/tasks/{task_id}/
Authorization: Token your_token_here
```

### Project Statistics
```http
GET /api/projects/statistics/
Authorization: Token your_token_here
```

## Content Management

### Website Content
```http
GET /api/content/website/
POST /api/content/website/
PUT /api/content/website/{id}/
DELETE /api/content/website/{id}/
Authorization: Token your_token_here
```

### Blog Posts
```http
GET /api/content/blog/
POST /api/content/blog/
PUT /api/content/blog/{id}/
DELETE /api/content/blog/{id}/
Authorization: Token your_token_here
```

**Create Blog Post:**
```json
{
    "title": "Web Development Trends 2024",
    "slug": "web-development-trends-2024",
    "content": "Blog post content here...",
    "excerpt": "Short description",
    "status": "published",
    "featured_image": "image_file",
    "tags": ["web", "development", "trends"],
    "seo_title": "SEO optimized title",
    "seo_description": "SEO description"
}
```

### Portfolio Projects
```http
GET /api/content/portfolio/
POST /api/content/portfolio/
PUT /api/content/portfolio/{id}/
DELETE /api/content/portfolio/{id}/
Authorization: Token your_token_here
```

### Services
```http
GET /api/content/services/
POST /api/content/services/
PUT /api/content/services/{id}/
DELETE /api/content/services/{id}/
Authorization: Token your_token_here
```

### Team Members
```http
GET /api/content/team/
POST /api/content/team/
PUT /api/content/team/{id}/
DELETE /api/content/team/{id}/
Authorization: Token your_token_here
```

### Content Statistics
```http
GET /api/content/statistics/
Authorization: Token your_token_here
```

## Communication Management

### Contact Submissions
```http
GET /api/communication/contacts/
POST /api/communication/contacts/
PUT /api/communication/contacts/{id}/
DELETE /api/communication/contacts/{id}/
Authorization: Token your_token_here
```

**Query Parameters:**
- `status`: Filter by status (new, in_progress, resolved, closed)
- `priority`: Filter by priority (low, medium, high, urgent)
- `assigned_to`: Filter by assigned user

### Email Templates
```http
GET /api/communication/email-templates/
POST /api/communication/email-templates/
PUT /api/communication/email-templates/{id}/
DELETE /api/communication/email-templates/{id}/
Authorization: Token your_token_here
```

### Newsletters
```http
GET /api/communication/newsletters/
POST /api/communication/newsletters/
PUT /api/communication/newsletters/{id}/
DELETE /api/communication/newsletters/{id}/
Authorization: Token your_token_here
```

### Newsletter Subscribers
```http
GET /api/communication/subscribers/
POST /api/communication/subscribers/
PUT /api/communication/subscribers/{id}/
DELETE /api/communication/subscribers/{id}/
Authorization: Token your_token_here
```

### Notifications
```http
GET /api/communication/notifications/
POST /api/communication/notifications/
PUT /api/communication/notifications/{id}/
DELETE /api/communication/notifications/{id}/
Authorization: Token your_token_here
```

### Communication Statistics
```http
GET /api/communication/statistics/
Authorization: Token your_token_here
```

## Dashboard Analytics

### Dashboard Overview
```http
GET /api/dashboard/overview/
Authorization: Token your_token_here
```

**Response:**
```json
{
    "projects": {
        "total": 10,
        "active": 5,
        "completed": 3,
        "completion_rate": 30.0
    },
    "clients": {
        "total": 15,
        "active": 12
    },
    "content": {
        "blog_posts": 25,
        "published_posts": 20
    },
    "communication": {
        "pending_contacts": 5
    },
    "activity": {
        "recent_activities": 50
    }
}
```

### Dashboard Metrics
```http
GET /api/dashboard/metrics/
POST /api/dashboard/metrics/
PUT /api/dashboard/metrics/{id}/
DELETE /api/dashboard/metrics/{id}/
Authorization: Token your_token_here
```

### Metrics Chart Data
```http
GET /api/dashboard/metrics/chart/
Authorization: Token your_token_here
```

### Activity Logs
```http
GET /api/dashboard/activities/
POST /api/dashboard/activities/
PUT /api/dashboard/activities/{id}/
DELETE /api/dashboard/activities/{id}/
Authorization: Token your_token_here
```

### Recent Activities
```http
GET /api/dashboard/activities/recent/
Authorization: Token your_token_here
```

## Error Responses

### 400 Bad Request
```json
{
    "field_name": ["This field is required."],
    "non_field_errors": ["Custom validation error."]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
    "detail": "A server error occurred."
}
```

## Pagination

All list endpoints support pagination:

**Request:**
```http
GET /api/projects/?page=2&page_size=10
```

**Response:**
```json
{
    "count": 50,
    "next": "http://localhost:8000/api/projects/?page=3",
    "previous": "http://localhost:8000/api/projects/?page=1",
    "results": [...]
}
```

## Filtering and Searching

Most list endpoints support filtering and searching:

**Examples:**
```http
GET /api/projects/?search=ecommerce&status=in_progress
GET /api/clients/?status=active&ordering=-created_at
GET /api/communication/contacts/?priority=high&assigned_to=1
```

## File Uploads

For endpoints that accept file uploads (images, documents):

```http
POST /api/content/blog/
Authorization: Token your_token_here
Content-Type: multipart/form-data

{
    "title": "Blog Post",
    "content": "Content here...",
    "featured_image": [file]
}
```

## Rate Limiting

The API implements rate limiting:
- 1000 requests per hour for authenticated users
- 100 requests per hour for anonymous users

## Testing

Use the provided test scripts to verify API functionality:

```bash
# Test all endpoints
python test_authentication_api.py
python test_clients_api.py
python test_projects_api.py
python test_content_api.py
python test_communication_api.py
python test_dashboard_api.py
```

## Sample Data

Populate the database with sample data:

```bash
python manage.py populate_authentication
python manage.py populate_clients
python manage.py populate_projects
python manage.py populate_content
python manage.py populate_communication
python manage.py populate_dashboard
```

## Environment Variables

Required environment variables:

```env
SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Dependencies

- Django 4.2+
- Django REST Framework 3.14+
- django-filter
- django-cors-headers
- Pillow (for image handling)
- python-decouple (for environment variables)

## Support

For API support and questions, contact the development team or refer to the Django REST Framework documentation at https://www.django-rest-framework.org/
