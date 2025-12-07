import random
from collections import defaultdict
from .models import ExamRecord, Room

def shuffle_students(students):
    """
    Ordered alternating seating arrangement for exam halls.
    
    Creates a pattern where roll numbers increment together across departments:
    - 24UAM101, 24UCS101, 24UPH101, 24UCH101, 24UEC101
    - 24UAM102, 24UCS102, 24UPH102, 24UCH102, 24UEC102
    - 24UAM103, 24UCS103, 24UPH103, 24UCH103, 24UEC103
    ...and so on
    
    This ensures:
    1. Different departments alternate perfectly
    2. Roll numbers increase in sync across all departments
    3. No sequential numbers from same department sit together
    """
    if not students:
        return []
    
    # Step 1: Group by Course Code (Department)
    dept_groups = defaultdict(list)
    for student in students:
        dept_groups[student.course_code].append(student)
    
    # Step 2: Sort each department by register number (ascending order)
    # Extract the numeric part for proper sorting
    def get_roll_number(student):
        try:
            # Extract numeric part from register number (e.g., "24UAM101" -> 101)
            return int(''.join(filter(str.isdigit, student.register_no[-3:])))
        except (ValueError, IndexError):
            return 0
    
    for course_code in dept_groups:
        dept_groups[course_code].sort(key=get_roll_number)
    
    # Step 3: Interleave departments in round-robin fashion
    # This creates the ordered alternating pattern
    shuffled_list = []
    dept_codes = sorted(dept_groups.keys())  # Sort department codes for consistency
    max_dept_size = max(len(group) for group in dept_groups.values())
    
    for i in range(max_dept_size):
        for dept_code in dept_codes:
            if i < len(dept_groups[dept_code]):
                shuffled_list.append(dept_groups[dept_code][i])
    
    return shuffled_list


def shuffle_students_for_room(students, departments):
    """
    Shuffle students from specific departments for a single room.
    Ensures alternating pattern between the 2-3 departments.
    """
    # Group by department
    dept_groups = defaultdict(list)
    for student in students:
        if student.course_code in departments:
            dept_groups[student.course_code].append(student)
    
    # Sort each group by roll number
    def get_roll_number(student):
        try:
            return int(''.join(filter(str.isdigit, student.register_no[-3:])))
        except (ValueError, IndexError):
            return 0
    
    for dept in dept_groups:
        dept_groups[dept].sort(key=get_roll_number)
    
    # Interleave departments
    shuffled = []
    dept_codes = sorted(departments)
    max_size = max((len(dept_groups[d]) for d in dept_codes if d in dept_groups), default=0)
    
    for i in range(max_size):
        for dept in dept_codes:
            if dept in dept_groups and i < len(dept_groups[dept]):
                shuffled.append(dept_groups[dept][i])
    
    return shuffled


def generate_seating_arrangement(selected_rooms):
    """
    Allocates seats ensuring each room has only 2-3 departments maximum.
    Students from the same 2-3 departments alternate within each room.
    """
    # Get all students that haven't been allocated yet
    all_students = list(ExamRecord.objects.filter(exam_hall_number='Pending'))
    
    if not all_students:
        return {'total_allocated': 0, 'allocations': []}
    
    # Group students by department
    dept_groups = defaultdict(list)
    for student in all_students:
        dept_groups[student.course_code].append(student)
    
    # Sort each department by register number
    def get_roll_number(student):
        try:
            return int(''.join(filter(str.isdigit, student.register_no[-3:])))
        except (ValueError, IndexError):
            return 0
    
    for dept_code in dept_groups:
        dept_groups[dept_code].sort(key=get_roll_number)
    
    # Get list of all departments
    all_depts = sorted(list(dept_groups.keys()))
    
    if not all_depts:
        return {'total_allocated': 0, 'allocations': []}
    
    # Track which students have been allocated (using 'record' as primary key)
    allocated_students = set()
    
    # Track department indices for each department
    dept_indices = {dept: 0 for dept in all_depts}
    
    # Allocate students to rooms
    allocation_summary = []
    total_allocated = 0
    dept_rotation_index = 0
    
    for room in selected_rooms:
        if not room.is_available:
            continue
        
        # Determine departments for this room (2-3 departments)
        num_depts = min(3, len(all_depts))
        if len(all_depts) == 2:
            num_depts = 2
        elif len(all_depts) == 1:
            num_depts = 1
        
        # Get departments for this room (rotate through all departments)
        room_depts = []
        for i in range(num_depts):
            dept_idx = (dept_rotation_index + i) % len(all_depts)
            room_depts.append(all_depts[dept_idx])
        
        dept_rotation_index = (dept_rotation_index + num_depts) % len(all_depts)
        
        # Collect students from these departments that haven't been allocated
        room_students_by_dept = defaultdict(list)
        for dept in room_depts:
            if dept in dept_groups:
                for student in dept_groups[dept]:
                    if student.record not in allocated_students:
                        room_students_by_dept[dept].append(student)
        
        # Interleave students from the departments for this room
        shuffled_room_students = []
        max_students_per_dept = max(
            (len(room_students_by_dept[d]) for d in room_depts if d in room_students_by_dept),
            default=0
        )
        
        for i in range(max_students_per_dept):
            for dept in room_depts:
                if dept in room_students_by_dept and i < len(room_students_by_dept[dept]):
                    shuffled_room_students.append(room_students_by_dept[dept][i])
        
        # Allocate to seats in this room
        capacity = room.capacity
        seats_filled = 0
        
        for seat_num in range(1, capacity + 1):
            if seats_filled >= len(shuffled_room_students):
                break
            
            student = shuffled_room_students[seats_filled]
            student.exam_hall_number = room.room_number
            student.exam_seat_number = str(seat_num)
            student.save()
            
            # Mark student as allocated (using 'record' as primary key)
            allocated_students.add(student.record)
            
            allocation_summary.append({
                'register_no': student.register_no,
                'room': room.room_number,
                'seat': seat_num
            })
            
            seats_filled += 1
            total_allocated += 1
    
    return {
        'total_allocated': total_allocated,
        'allocations': allocation_summary
    }
