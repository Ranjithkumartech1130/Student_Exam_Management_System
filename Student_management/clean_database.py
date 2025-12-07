"""
Complete cleanup and fresh start
1. Delete ALL existing records
2. Upload fresh CSV data
3. Generate seating with proper ordering
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

print("=" * 80)
print("COMPLETE DATABASE CLEANUP")
print("=" * 80)

# Delete ALL records
count = ExamRecord.objects.count()
print(f"\n🗑️  Deleting {count} existing records...")
ExamRecord.objects.all().delete()

print(f"✅ All records deleted!")
print(f"📊 Current database: {ExamRecord.objects.count()} records")
print("\n" + "=" * 80)
print("DATABASE IS NOW CLEAN")
print("=" * 80)
print("\n💡 Next steps:")
print("   1. Go to admin dashboard")
print("   2. Upload large_students.csv")
print("   3. Generate seating")
print("   4. View the perfect ordered layout!")
