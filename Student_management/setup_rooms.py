import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from exams.models import Room

# Create default rooms: Ground floor (G) + Floors 1-5, 9 rooms each
floors = ['G', '1', '2', '3', '4', '5']
room_numbers_per_floor = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
default_capacity = 30

print("Creating default room structure...")
created_count = 0

for floor in floors:
    for room_num in room_numbers_per_floor:
        room_name = f"{floor}{room_num}"
        
        # Check if room already exists
        if not Room.objects.filter(room_number=room_name).exists():
            Room.objects.create(
                room_number=room_name,
                capacity=default_capacity,
                is_available=True
            )
            created_count += 1
            print(f"✓ Created room {room_name}")
        else:
            print(f"- Room {room_name} already exists")

print(f"\n✅ Setup complete! Created {created_count} new rooms.")
print(f"Total rooms in system: {Room.objects.count()}")
