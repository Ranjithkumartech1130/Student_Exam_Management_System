"""
Enable all rooms for seating allocation
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from exams.models import Room

print("=" * 80)
print("ENABLING ALL ROOMS FOR ALLOCATION")
print("=" * 80)

# Get all rooms
all_rooms = Room.objects.all()
total_rooms = all_rooms.count()

if total_rooms == 0:
    print("\n❌ No rooms found in database!")
    print("   Run 'python setup_rooms.py' first to create rooms")
else:
    # Enable all rooms
    updated = Room.objects.all().update(is_available=True)
    
    print(f"\n✅ Enabled {updated} rooms")
    
    # Show summary
    total_capacity = sum(r.capacity for r in Room.objects.all())
    print(f"\n📊 SUMMARY:")
    print(f"   Total Rooms: {total_rooms}")
    print(f"   All Available: {Room.objects.filter(is_available=True).count()}")
    print(f"   Total Capacity: {total_capacity} seats")
    
    print(f"\n📋 ROOMS BY FLOOR:")
    floors = {}
    for room in Room.objects.all().order_by('room_number'):
        floor = room.room_number[0]
        if floor not in floors:
            floors[floor] = []
        floors[floor].append(room.room_number)
    
    for floor, rooms in sorted(floors.items()):
        print(f"   Floor {floor}: {len(rooms)} rooms - {', '.join(rooms[:5])}", end='')
        if len(rooms) > 5:
            print(f" ... +{len(rooms)-5} more")
        else:
            print()

print("\n" + "=" * 80)
print("✅ All rooms are now available for allocation!")
print("=" * 80)
