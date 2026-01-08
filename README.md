# Salon Backend - Django REST API

## 🎯 Project Overview
Professional salon management system with Django REST Framework and JWT authentication.

## 📁 Project Structure
```
salon-backend-django/
├── booking/                    # Main app
│   ├── models.py              # Database models
│   ├── admin.py               # Admin panel configuration
│   ├── views.py               # API views
│   ├── serializers.py         # Data serializers
│   ├── urls.py                # App URLs
│   └── migrations/            # Database migrations
├── salon_project/             # Django project
│   ├── settings.py           # Project settings
│   ├── urls.py               # Main URLs
│   └── wsgi.py               # WSGI configuration
├── staticfiles/              # Static files
├── templates/                # Template overrides
├── venv/                     # Virtual environment
├── requirements.txt          # Dependencies
├── .env                     # Environment variables
├── manage.py                # Django management
└── test_*.py                # Test scripts
```

## 🚀 Quick Start

### 1. Start MySQL (XAMPP)
- Open XAMPP Control Panel
- Start Apache and MySQL services

### 2. Activate Virtual Environment
```bash
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Start Server
```bash
python manage.py runserver
```

## 🔗 Access Points

### Admin Panel
- **URL:** http://127.0.0.1:8000/admin/
- **Login:** admin@salon.com / admin123

### API Endpoints
- **Health Check:** http://127.0.0.1:8000/api/health/
- **Authentication:** http://127.0.0.1:8000/api/auth/
- **Services:** http://127.0.0.1:8000/api/services/
- **Appointments:** http://127.0.0.1:8000/api/appointments/

## 📊 Database Models

### User Model
- Custom user with email authentication
- Roles: admin, staff, customer

### Core Models
- **Service:** Salon services with pricing
- **Staff:** Staff members and specializations
- **Appointment:** Booking management
- **Product:** Product inventory
- **Order:** Order management
- **AvailableSlot:** Time slot management

## 🔧 Features

### Admin Panel
- ✅ Enhanced admin interface
- ✅ Custom display methods
- ✅ Advanced filtering and search
- ✅ Relationship management

### API Features
- ✅ JWT Authentication
- ✅ RESTful endpoints
- ✅ Data serialization
- ✅ CORS support
- ✅ Pagination

### Security
- ✅ JWT token authentication
- ✅ CORS protection
- ✅ Password validation
- ✅ User role management

## 🛠 Tech Stack

- **Backend:** Django 4.2.16
- **API:** Django REST Framework
- **Authentication:** JWT (Simple JWT)
- **Database:** MySQL
- **Environment:** Virtual Environment

## 📱 Frontend Integration

### Authentication
```javascript
POST /api/auth/login/
{
  "email": "admin@salon.com",
  "password": "admin123"
}
```

### API Usage
```javascript
GET /api/services/
Headers: Authorization: Bearer <token>

POST /api/appointments/
{
  "service": 1,
  "appointment_date": "2024-01-01",
  "appointment_time": "10:00"
}
```

## 🎯 Ready for Production

Your salon backend is production-ready with:
- ✅ Secure authentication
- ✅ Professional admin panel
- ✅ Complete API endpoints
- ✅ Database management
- ✅ Static file serving

**🚀 Your salon backend is ready for frontend development!**
