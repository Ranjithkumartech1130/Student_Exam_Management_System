"""
Remove ALL duplicate students - keep only one copy of each
"""
import sys
import os
import django

project_path = r'c:\Users\RANJITH KUMAR\OneDrive\Desktop\Exam-Management System\Student_management'
sys.path.insert(0, project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from exams.models import ExamRecord
from collections import defaultdict

print("=" * 80)
print("REMOVING DUPLICATE STUDENTS")
print("=" * 80)

all_records = ExamRecord.objects.all()
print(f"\nTotal records before: {all_records.count()}")

# Group by register number
register_groups = defaultdict(list)
for record in all_records:
    register_groups[record.register_no].append(record)

# Keep only first occurrence, delete rest
kept = 0
deleted = 0

for register_no, records in register_groups.items():
    # Keep the first one
    kept += 1
    # Delete duplicates
    for record in records[1:]:
        record.delete()
        deleted += 1

print(f"\n✅ Cleanup complete!")
print(f"   Unique students kept: {kept}")
print(f"   Duplicate records deleted: {deleted}")
print(f"   Total records after: {ExamRecord.objects.count()}")

print("\n" + "=" * 80)
print("NOW RE-GENERATE SEATING FROM ADMIN DASHBOARD")
print("=" * 80)
