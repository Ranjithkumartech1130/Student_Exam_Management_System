# Exam Portal - Django Backend with MySQL

A comprehensive exam management system built with Django and MySQL, featuring student login with Register Number and Date of Birth, and admin dashboard with full CRUD operations.

## Features

- **Student Login**: Students can retrieve their exam details using Register Number and Date of Birth
- **Admin Dashboard**: Full CRUD operations for managing exam records
- **MySQL Database**: Secure database connection with examdb
- **Clean Code Structure**: Well-organized Django project structure

## Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory**

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL Database**
   
   First, create the database in MySQL:
   ```sql
   CREATE DATABASE examdb;
   ```
   
   Make sure MySQL is running and accessible with the credentials:
   - User: `root`
   - Password: `dharsh@457`
   - Host: `localhost`
   - Port: `3306`

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```
   When prompted, create a user with:
   - Username: `Kgkite`
   - Password: `Kite@2025`
   - Email: (optional)

7. **Initialize sample data (optional)**
   ```bash
   python manage.py init_db
   ```

## Running the Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Student Endpoints
- `POST /api/student/login/` - Student login with Register Number and Date of Birth

### Admin Endpoints
- `POST /api/admin/login/` - Admin login
- `GET /api/admin/dashboard/` - Admin dashboard page
- `GET /api/admin/records/` - Get all exam records
- `GET /api/admin/records/<id>/` - Get a specific record
- `POST /api/admin/records/create/` - Create a new record
- `PUT /api/admin/records/<id>/update/` - Update a record
- `DELETE /api/admin/records/<id>/delete/` - Delete a record

## Database Schema

The `ExamRecord` model includes the following fields:
- `Record` (AutoField, Primary Key)
- `RegisterNo` (CharField)
- `StudentName` (CharField)
- `Coursecode` (CharField)
- `CourseTitle` (CharField)
- `ExamDate` (DateField)
- `ExamSession` (CharField)
- `ExamHallNumber` (CharField)
- `ExamSeatNumber` (CharField)
- `DateOfBirth` (DateField, optional)

## Usage

### Student Login
1. Navigate to the login page
2. Click on "Student" tab
3. Enter Register Number and Date of Birth
4. View exam details

### Admin Login
1. Navigate to the login page
2. Click on "Admin" tab
3. Enter credentials:
   - Username: `Kgkite`
   - Password: `Kite@2025`
4. Access the admin dashboard with full CRUD operations

## Project Structure

```
exam_portal/
├── exam_portal/          # Main project settings
│   ├── settings.py       # Django settings with MySQL config
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── exams/               # Exams app
│   ├── models.py       # ExamRecord model
│   ├── views.py        # API views
│   ├── urls.py         # App URL routing
│   ├── admin.py        # Django admin configuration
│   └── management/     # Custom management commands
├── templates/          # HTML templates
│   ├── login.html      # Login page
│   └── admin_dashboard.html  # Admin dashboard
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Configuration

Database credentials are configured in `exam_portal/settings.py`. To change them, modify:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'examdb',
        'USER': 'root',
        'PASSWORD': 'dharsh@457',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## Security Notes

- Change the `SECRET_KEY` in `settings.py` for production
- Set `DEBUG = False` in production
- Use environment variables for sensitive credentials
- Enable HTTPS in production
- Configure proper CORS settings for production

## Troubleshooting

### MySQL Connection Issues
- Ensure MySQL server is running
- Verify database credentials
- Check if MySQL client libraries are installed: `pip install mysqlclient`

### Migration Issues
- Run `python manage.py makemigrations` if models are changed
- Run `python manage.py migrate` to apply migrations

### Port Already in Use
- Change the port: `python manage.py runserver 8001`

## License

This project is for educational purposes.

