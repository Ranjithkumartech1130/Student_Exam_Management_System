"""
Diagnostic script to check the current state and identify issues
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from exams.models import ExamRecord, Room

print("=" * 80)
print("SEATING ALLOCATION DIAGNOSTIC REPORT")
print("=" * 80)

# Check students
total_students = ExamRecord.objects.count()
pending_students = ExamRecord.objects.filter(exam_hall_number='Pending').count()
allocated_students = ExamRecord.objects.exclude(exam_hall_number='Pending').count()

print(f"\n📊 STUDENT STATUS:")
print(f"   Total Students: {total_students}")
print(f"   Pending: {pending_students}")
print(f"   Allocated: {allocated_students}")

# Check departments
from collections import defaultdict
dept_counts = defaultdict(int)
for student in ExamRecord.objects.all():
    dept_counts[student.course_code] += 1

print(f"\n📚 DEPARTMENT BREAKDOWN:")
for dept, count in sorted(dept_counts.items()):
    dept_pending = ExamRecord.objects.filter(course_code=dept, exam_hall_number='Pending').count()
    print(f"   {dept}: {count} total ({dept_pending} pending)")

# Check rooms
total_rooms = Room.objects.count()
available_rooms = Room.objects.filter(is_available=True).count()
unavailable_rooms = Room.objects.filter(is_available=False).count()

print(f"\n🏢 ROOM STATUS:")
print(f"   Total Rooms: {total_rooms}")
print(f"   Available: {available_rooms}")
print(f"   Unavailable: {unavailable_rooms}")

if available_rooms > 0:
    total_capacity = sum(r.capacity for r in Room.objects.filter(is_available=True))
    print(f"   Total Capacity: {total_capacity} seats")
    
    print(f"\n📋 AVAILABLE ROOMS:")
    for room in Room.objects.filter(is_available=True).order_by('room_number')[:10]:
        print(f"   Room {room.room_number}: {room.capacity} seats")
    
    if available_rooms > 10:
        print(f"   ... and {available_rooms - 10} more rooms")
else:
    print(f"   ⚠️  WARNING: No rooms are marked as available!")

# Check if we have enough capacity
if available_rooms > 0:
    print(f"\n✅ CAPACITY CHECK:")
    if total_capacity >= pending_students:
        print(f"   ✓ Sufficient capacity: {total_capacity} seats for {pending_students} students")
    else:
        print(f"   ✗ Insufficient capacity: {total_capacity} seats for {pending_students} students")
        print(f"   Need {pending_students - total_capacity} more seats")

print("\n" + "=" * 80)
