"""
Generate a large realistic student dataset for testing seating arrangements
This will create 150 students across 5 departments to fill one floor
"""
import csv
import random
from datetime import datetime

# Department configurations
departments = [
    {'code': 'UAM', 'name': 'B.Sc Applied Mathematics', 'count': 30},
    {'code': 'UCS', 'name': 'B.Sc Computer Science', 'count': 40},
    {'code': 'UPH', 'name': 'B.Sc Physics', 'count': 30},
    {'code': 'UCH', 'name': 'B.Sc Chemistry', 'count': 25},
    {'code': 'UEC', 'name': 'B.Sc Electronics', 'count': 25},
]

# Indian first names
first_names = [
    'Aarav', 'Vivaan', 'Aditya', 'Arjun', 'Sai', 'Arnav', 'Ayaan', 'Krishna', 'Ishaan', 'Shaurya',
    'Atharv', 'Advik', 'Pranav', 'Reyansh', 'Vihaan', 'Aadhya', 'Ananya', 'Pari', 'Anika', 'Navya',
    'Diya', 'Myra', 'Sara', 'Ira', 'Riya', 'Aarohi', 'Saanvi', 'Kiara', 'Prisha', 'Avni',
    'Rohan', 'Aryan', 'Kabir', 'Dhruv', 'Karan', 'Advait', 'Vedant', 'Shivansh', 'Aarush', 'Laksh',
    'Anvi', 'Ishika', 'Tara', 'Shanaya', 'Aaradhya', 'Kavya', 'Siya', 'Nisha', 'Meera', 'Zara'
]

# Indian last names
last_names = [
    'Sharma', 'Verma', 'Patel', 'Kumar', 'Singh', 'Reddy', 'Gupta', 'Joshi', 'Iyer', 'Nair',
    'Mehta', 'Desai', 'Rao', 'Pillai', 'Agarwal', 'Bansal', 'Malhotra', 'Kapoor', 'Chopra', 'Bhatia',
    'Saxena', 'Jain', 'Sinha', 'Mishra', 'Pandey', 'Tiwari', 'Dubey', 'Shukla', 'Trivedi', 'Bhatt'
]

students = []
student_id = 1

print("Generating large student dataset...")

for dept in departments:
    dept_code = dept['code']
    dept_name = dept['name']
    count = dept['count']
    
    print(f"  Creating {count} students for {dept_code}...")
    
    for i in range(count):
        # Generate sequential register numbers for each department
        register_no = f"24{dept_code}{101 + i:03d}"
        
        # Generate random name
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        full_name = f"{first_name} {last_name}"
        
        # Generate random date of birth (students born between 2001-2003)
        year = random.randint(2001, 2003)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Safe day range for all months
        dob = f"{year}-{month:02d}-{day:02d}"
        
        # Create student record
        students.append({
            'Roll-no': register_no,
            'Name': full_name,
            'Course_code': dept_code,
            'Course-name': dept_name,
            'Date-Session': '2025-12-15-Morning',
            'Date-of-Birth': dob
        })
        
        student_id += 1

# DO NOT shuffle - keep students in proper sequential order for correct seating
# random.shuffle(students)

# Write to CSV
output_file = r'c:\Users\RANJITH KUMAR\OneDrive\Desktop\Exam-Management System\large_students.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Roll-no', 'Name', 'Course_code', 'Course-name', 'Date-Session', 'Date-of-Birth'])
    writer.writeheader()
    writer.writerows(students)

print(f"\n✅ Successfully created {len(students)} students!")
print(f"📁 File saved to: {output_file}")
print(f"\n📊 Department breakdown:")
for dept in departments:
    print(f"   {dept['code']}: {dept['count']} students")
print(f"\n💡 This dataset will fill approximately 3-4 exam halls (assuming 40-50 seats per hall)")
