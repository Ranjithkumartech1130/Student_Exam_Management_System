"""
Reset all student allocations back to Pending status
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from exams.models import ExamRecord

# Reset all students to Pending
updated = ExamRecord.objects.all().update(
    exam_hall_number='Pending',
    exam_seat_number='Pending'
)

print(f"✅ Reset {updated} student records to Pending status")
print(f"📊 Total students in database: {ExamRecord.objects.count()}")
print(f"🔄 All students are now ready for reallocation")
print("\nNext steps:")
print("1. Go to your admin dashboard")
print("2. Make sure all rooms are selected (marked as available)")
print("3. Click 'Generate Seating Arrangement'")
print("4. All 150 students should now be allocated!")
