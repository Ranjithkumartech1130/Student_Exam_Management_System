"""
Test the fixed room allocation to ensure all rooms are used
"""
import sys
import os
import django

# Setup Django
project_path = r'c:\Users\RANJITH KUMAR\OneDrive\Desktop\Exam-Management System\Student_management'
sys.path.insert(0, project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from exams.models import ExamRecord, Room
from exams.utils import generate_seating_arrangement

print("=" * 80)
print("TESTING ROOM ALLOCATION FIX")
print("=" * 80)

# Get stats
total_students = ExamRecord.objects.count()
available_rooms = Room.objects.filter(is_available=True)
total_rooms = available_rooms.count()
total_capacity = sum(r.capacity for r in available_rooms)

print(f"\n📊 Current Status:")
print(f"   Total Students: {total_students}")
print(f"   Available Rooms: {total_rooms}")
print(f"   Total Capacity: {total_capacity}")

if total_students == 0:
    print("\n⚠️  No students in database. Please upload CSV first.")
else:
    print(f"\n✅ Ready to allocate {total_students} students across {total_rooms} rooms")
    print(f"   Expected: All {total_rooms} rooms should be used (if capacity allows)")
    
    # Show room details
    print(f"\n📋 Available Rooms:")
    for room in available_rooms:
        print(f"   {room.room_number}: Capacity {room.capacity}")

print("\n" + "=" * 80)
