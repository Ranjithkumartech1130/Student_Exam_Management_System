# Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: If you encounter issues installing `mysqlclient`, you may need to install MySQL development libraries first:
- **Windows**: Download MySQL Connector/C from MySQL website
- **Linux**: `sudo apt-get install default-libmysqlclient-dev python3-dev`
- **Mac**: `brew install mysql-client`

## Step 2: Create MySQL Database

Open MySQL command line or MySQL Workbench and run:

```sql
CREATE DATABASE examdb;
```

Verify your MySQL credentials match `exam_portal/settings.py`:
- User: `root`
- Password: `dharsh@457`
- Host: `localhost`
- Port: `3306`

## Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 4: Create Admin User and Sample Data

**Option A: Using the setup script**
```bash
python setup.py
```

**Option B: Manual setup**
```bash
# Create admin user
python manage.py createsuperuser
# Username: Kgkite
# Password: Kite@2025

# Create sample data
python manage.py init_db
```

## Step 5: Run the Server

```bash
python manage.py runserver
```

## Step 6: Access the Application

1. Open browser: `http://127.0.0.1:8000/`
2. **Student Login**: Use Register Number and Date of Birth
   - Example: `KGK2024001` with DOB `2002-05-15`
3. **Admin Login**: 
   - Username: `Kgkite`
   - Password: `Kite@2025`

## Sample Test Data

After running `init_db`, you can test with:

| Register No | Date of Birth | Student Name |
|------------|---------------|--------------|
| KGK2024001 | 2002-05-15 | John Doe |
| KGK2024002 | 2002-07-20 | Jane Smith |
| KGK2024003 | 2001-09-10 | Robert Johnson |
| KGK2024004 | 2002-11-25 | Emily Davis |
| KGK2024005 | 2001-03-08 | Michael Wilson |

## Troubleshooting

### MySQL Connection Error
- Ensure MySQL server is running
- Check credentials in `exam_portal/settings.py`
- Verify database `examdb` exists

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Module Not Found
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

