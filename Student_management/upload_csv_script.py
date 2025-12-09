"""
Script to upload the CSV file directly to the database
"""
import os
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from exams.models import ExamRecord, Dataset
from datetime import datetime
import pandas as pd
import numpy as np

# Path to your CSV file
CSV_FILE = r"C:\Users\RANJITH KUMAR\OneDrive\Desktop\Exam-Management System\queryoutput_with_dob.csv"

def upload_csv():
    print(f"Reading CSV file: {CSV_FILE}")
    
    # Read CSV
    df = pd.read_csv(CSV_FILE)
    print(f"Total rows in CSV: {len(df)}")
    
    # Get or create dataset
    dataset = Dataset.objects.first()
    if not dataset:
        dataset = Dataset.objects.create(
            name="End Semester - 2025-12-09",
            exam_type="end_semester",
            description="Uploaded from queryoutput_with_dob.csv"
        )
        print(f"Created new dataset: {dataset.name}")
    else:
        print(f"Using existing dataset: {dataset.name}")
        # Clear existing records
        deleted = dataset.records.all().delete()
        print(f"Deleted {deleted[0]} existing records")
    
    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()
    print(f"Columns: {list(df.columns)}")
    
    # Replace NaN with None
    df = df.replace({np.nan: None})
    
    created_count = 0
    error_count = 0
    halls_found = {}
    
    
    for index, row in df.iterrows():
        try:
            # Get register number
            register_no = None
            for col in ['registerno', 'register-no', 'register no', 'regno']:
                if col in row and row[col]:
                    register_no = str(row[col]).strip().upper()
                    break
            
            if not register_no:
                continue
            
            # Get student name
            student_name = None
            for col in ['studentname', 'student name', 'name']:
                if col in row and row[col]:
                    student_name = str(row[col]).strip()
                    break
            
            # Get course code
            course_code = None
            for col in ['coursecode', 'course code', 'code']:
                if col in row and row[col]:
                    course_code = str(row[col]).strip()
                    break
            
            # Get course title
            course_title = None
            for col in ['coursetitle', 'course title', 'title']:
                if col in row and row[col]:
                    course_title = str(row[col]).strip()
                    break
            
            # Get exam date
            exam_date = None
            for col in ['examdate', 'exam date', 'date']:
                if col in row and row[col]:
                    try:
                        exam_date_str = str(row[col])
                        for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y']:
                            try:
                                exam_date = datetime.strptime(exam_date_str, fmt).date()
                                break
                            except ValueError:
                                continue
                        if not exam_date:
                            exam_date = pd.to_datetime(row[col]).date()
                    except:
                        pass
                    break
            
            # Get exam session
            exam_session = None
            for col in ['examsession', 'exam session', 'session']:
                if col in row and row[col]:
                    exam_session = str(row[col]).strip()
                    break
            
            # Get DOB
            date_of_birth = None
            for col in ['dob', 'date of birth', 'dateofbirth', 'birth date']:
                if col in row and row[col]:
                    try:
                        dob_str = str(row[col])
                        for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y', '%d/%m/%y']:
                            try:
                                date_of_birth = datetime.strptime(dob_str, fmt).date()
                                break
                            except ValueError:
                                continue
                        if not date_of_birth:
                            date_of_birth = pd.to_datetime(row[col]).date()
                    except:
                        pass
                    break
            
            # Get Hall Number and Seat Number
            exam_hall_number = None
            for col in ['examhallnumber', 'hallnumber', 'hall number', 'hall no', 'exam hall', 'hall']:
                if col in row and row[col]:
                    exam_hall_number = str(row[col]).strip()
                    break
            
            exam_seat_number = None
            for col in ['examseatnumber', 'seatnumber', 'seat number', 'seat no', 'exam seat', 'seat']:
                if col in row and row[col]:
                    exam_seat_number = str(row[col]).strip()
                    break

            # Create record
            ExamRecord.objects.create(
                dataset=dataset,
                register_no=register_no,
                student_name=student_name or 'Unknown',
                course_code=course_code or 'Unknown',
                course_title=course_title or 'Unknown',
                exam_date=exam_date or datetime.now().date(),
                exam_session=exam_session or 'FN',
                exam_hall_number=exam_hall_number or 'Pending',
                exam_seat_number=exam_seat_number or 'Pending',
                date_of_birth=date_of_birth
            )
            created_count += 1

            if register_no == '711724UAM139':
                print(f"DEBUG: Found 711724UAM139. Hall: '{exam_hall_number}', Seat: '{exam_seat_number}'")
                
            # Track hall and seat for Room creation
            if exam_hall_number:
                current_seat = 0
                try:
                    current_seat = int(exam_seat_number) if exam_seat_number and str(exam_seat_number).isdigit() else 0
                except:
                    pass
                
                if exam_hall_number not in halls_found:
                    halls_found[exam_hall_number] = current_seat
                else:
                    if current_seat > halls_found[exam_hall_number]:
                        halls_found[exam_hall_number] = current_seat
            
            if created_count % 50 == 0:
                print(f"Processed {created_count} records...")
                
        except Exception as e:
            error_count += 1
            print(f"Error on row {index}: {str(e)}")
            continue
    
    # Create/Update Rooms from valid collected halls
    new_rooms_count = 0
    from exams.models import Room  # Late import to avoid top-level circular issues if any
    
    for hall_name, max_seat in halls_found.items():
        if not hall_name or hall_name.lower() == 'pending':
            continue
            
        # Default capacity to at least 30, or max_seat
        inferred_capacity = max(max_seat, 30)
        
        room, created = Room.objects.get_or_create(
            room_number=hall_name,
            defaults={
                'capacity': inferred_capacity,
                'is_available': True
            }
        )
        if created:
            new_rooms_count += 1
            print(f"Created new room: {hall_name} (Cap: {inferred_capacity})")
        else:
            if max_seat > room.capacity:
                room.capacity = max_seat
                room.save()

    print(f"\nUpload complete!")
    print(f"  Created: {created_count} records")
    print(f"  Errors: {error_count}")
    print(f"  Dataset: {dataset.name}")
    print(f"  New Rooms: {new_rooms_count}")
    
    # Verify the specific student
    student = ExamRecord.objects.filter(register_no='711724UAM139').first()
    if student:
        print(f"\nFound verification student 711724UAM139:")
        print(f"  Name: {student.student_name}")
        print(f"  Hall: {student.exam_hall_number}")
        print(f"  Seat: {student.exam_seat_number}")
    else:
        print(f"\nVerification student 711724UAM139 not found!")

if __name__ == '__main__':
    upload_csv()
