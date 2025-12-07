"""
Set default Date of Birth for all students so they can login
Default DOB: 2002-01-01 (easy to remember for testing)
"""
import sys
import os
import django
from datetime import date

# Setup Django
project_path = r'c:\Users\RANJITH KUMAR\OneDrive\Desktop\Exam-Management System\Student_management'
sys.path.insert(0, project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from exams.models import ExamRecord

print("=" * 80)
print("SETTING DEFAULT DATE OF BIRTH FOR STUDENTS")
print("=" * 80)

# Set default DOB for all students
default_dob = date(2002, 1, 1)
students = ExamRecord.objects.all()

updated = 0
for student in students:
    if not student.date_of_birth:
        student.date_of_birth = default_dob
        student.save()
        updated += 1

print(f"\n✅ Updated {updated} students with default DOB: 2002-01-01")
print(f"\n📝 Student Login Credentials:")
print(f"   Username: Register Number (e.g., 24UAM101)")
print(f"   Password: 2002-01-01")
print("\n" + "=" * 80)
