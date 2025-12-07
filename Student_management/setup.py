"""
Setup script to initialize the Django project
Run this after installing dependencies to set up the database and admin user
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from django.contrib.auth.models import User
from exams.models import ExamRecord
from datetime import date


def create_admin_user():
    """Create the admin user if it doesn't exist"""
    username = 'Kgkite'
    password = 'Kite@2025'
    
    if User.objects.filter(username=username).exists():
        print(f'Admin user "{username}" already exists')
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f'Password updated for admin user "{username}"')
    else:
        User.objects.create_superuser(
            username=username,
            email='admin@kgkite.ac.in',
            password=password
        )
        print(f'Admin user "{username}" created successfully')


def create_sample_data():
    """Create sample exam records"""
    sample_records = [
        {
            'register_no': '711724UAM113',
            'student_name': 'Dharshini',
            'course_code': 'CS101',
            'course_title': 'Introduction to Computer Science',
            'exam_date': date(2025, 12, 09),
            'exam_session': 'Morning',
            'exam_hall_number': 'H101',
            'exam_seat_number': 'S001',
            'date_of_birth': date(2007, 5, 4),
        },
        {
            'register_no': '711724UAM139',
            'student_name': 'Ranjith',
            'course_code': 'CS101',
            'course_title': 'Introduction to Computer Science',
            'exam_date': date(2025, 12, 09),
            'exam_session': 'Morning',
            'exam_hall_number': 'H101',
            'exam_seat_number': 'S002',
            'date_of_birth': date(2007, 01, 11),
        },
        {
            'register_no': '711724UAM118',
            'student_name': 'Gopika ',
            'course_code': 'MATH201',
            'course_title': 'Advanced Mathematics',
            'exam_date': date(2025, 12, 10),
            'exam_session': 'Afternoon',
            'exam_hall_number': 'H102',
            'exam_seat_number': 'S015',
            'date_of_birth': date(2005, 10, 15),
        },
        {
            'register_no': '711724UAM155',
            'student_name': 'Sree Nivetha ',
            'course_code': 'PHY301',
            'course_title': 'Physics Fundamentals',
            'exam_date': date(2025, 12, 11),
            'exam_session': 'Morning',
            'exam_hall_number': 'H103',
            'exam_seat_number': 'S030',
            'date_of_birth': date(2005, 09, 19),
        },
        {
            'register_no': '711724UAM134',
            'student_name': 'Nandhini',
            'course_code': 'CS201',
            'course_title': 'Data Structures and Algorithms',
            'exam_date': date(2025, 12, 12),
            'exam_session': 'Afternoon',
            'exam_hall_number': 'H101',
            'exam_seat_number': 'S045',
            'date_of_birth': date(2007, 12, 19),
        },
    ]

    created_count = 0
    for record_data in sample_records:
        record, created = ExamRecord.objects.get_or_create(
            register_no=record_data['register_no'],
            defaults=record_data
        )
        if created:
            created_count += 1
            print(f'Created record for {record_data["register_no"]}')
        else:
            print(f'Record {record_data["register_no"]} already exists')

    print(f'\nCreated {created_count} new sample records')


if __name__ == '__main__':
    print('=' * 50)
    print('Django Exam Portal Setup')
    print('=' * 50)
    
    print('\n1. Creating admin user...')
    create_admin_user()
    
    print('\n2. Creating sample data...')
    create_sample_data()
    
    print('\n' + '=' * 50)
    print('Setup completed successfully!')
    print('=' * 50)
    print('\nYou can now run: python manage.py runserver')
    print('Admin credentials:')
    print('  Username: Kgkite')
    print('  Password: Kite@2025')

