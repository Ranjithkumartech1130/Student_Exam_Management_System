"""
Quick fix: Remove duplicate student records and keep only unique ones
"""
import sys
import os
import django

# Setup Django
project_path = r'c:\Users\RANJITH KUMAR\OneDrive\Desktop\Exam-Management System\Student_management'
sys.path.insert(0, project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from exams.models import ExamRecord
from collections import defaultdict

print("Cleaning up duplicate records...")

# Get all records
all_records = ExamRecord.objects.all()
print(f"Total records before cleanup: {all_records.count()}")

# Group by register number
register_groups = defaultdict(list)
for record in all_records:
    register_groups[record.register_no].append(record)

# Keep only the first occurrence of each register number
kept = 0
deleted = 0

for register_no, records in register_groups.items():
    if len(records) > 1:
        # Keep the first one, delete the rest
        for record in records[1:]:
            record.delete()
            deleted += 1
        kept += 1
    else:
        kept += 1

print(f"\n✅ Cleanup complete!")
print(f"   Kept: {kept} unique students")
print(f"   Deleted: {deleted} duplicate records")
print(f"\nTotal records after cleanup: {ExamRecord.objects.count()}")

# Show the unique students
print(f"\n📋 Unique students in database:")
unique_students = ExamRecord.objects.all().order_by('register_no')
for student in unique_students:
    print(f"   {student.register_no} - {student.student_name} ({student.course_code})")
