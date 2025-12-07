"""
Check for duplicate students in the database
"""
import sys
import os
import django

# Add the project directory to the path
project_path = r'c:\Users\RANJITH KUMAR\OneDrive\Desktop\Exam-Management System\Student_management'
sys.path.insert(0, project_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from exams.models import ExamRecord
from collections import Counter

students = ExamRecord.objects.all()
print(f"Total records: {students.count()}")

# Check for duplicates by register number
register_nos = [s.register_no for s in students]
duplicates = [item for item, count in Counter(register_nos).items() if count > 1]

if duplicates:
    print(f"\n⚠️  Found {len(duplicates)} duplicate register numbers:")
    for dup in duplicates:
        records = ExamRecord.objects.filter(register_no=dup)
        print(f"\n  {dup}: {records.count()} occurrences")
        for rec in records:
            print(f"    - ID: {rec.record}, Name: {rec.student_name}, Course: {rec.course_code}")
else:
    print("\n✅ No duplicates found")

# Show all unique students
unique_students = {}
for s in students:
    if s.register_no not in unique_students:
        unique_students[s.register_no] = s

print(f"\n📊 Unique students: {len(unique_students)}")
for reg_no in sorted(unique_students.keys()):
    s = unique_students[reg_no]
    print(f"  {reg_no} - {s.student_name} ({s.course_code})")
