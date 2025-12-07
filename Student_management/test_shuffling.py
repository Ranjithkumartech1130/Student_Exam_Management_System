"""
Test script to verify the advanced shuffling algorithm
"""
import sys
import os
import django

# Add the project directory to the path
project_path = r'c:\Users\RANJITH KUMAR\OneDrive\Desktop\Exam-Management System\Student_management'
sys.path.insert(0, project_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from exams.models import ExamRecord
from exams.utils import shuffle_students

def test_shuffling():
    """Test the shuffling algorithm with current database records"""
    print("=" * 80)
    print("TESTING ADVANCED SHUFFLING ALGORITHM")
    print("=" * 80)
    
    # Get all students
    students = list(ExamRecord.objects.all())
    
    if not students:
        print("\n❌ No students found in database. Please upload CSV first.")
        return
    
    print(f"\n📊 Total Students: {len(students)}")
    
    # Group by department for analysis
    from collections import defaultdict
    dept_counts = defaultdict(int)
    for student in students:
        dept_counts[student.course_code] += 1
    
    print(f"\n📚 Department Distribution:")
    for dept, count in sorted(dept_counts.items()):
        print(f"   {dept}: {count} students")
    
    # Shuffle students
    print(f"\n🔀 Shuffling students...")
    shuffled = shuffle_students(students)
    
    # Analyze the shuffled result
    print(f"\n✅ Shuffled {len(shuffled)} students")
    print(f"\n📋 First 20 seats (showing alternating pattern):")
    print(f"{'Seat':<6} {'Register No':<15} {'Course':<10} {'Student Name':<25}")
    print("-" * 80)
    
    for i, student in enumerate(shuffled[:20], 1):
        print(f"{i:<6} {student.register_no:<15} {student.course_code:<10} {student.student_name:<25}")
    
    # Check for sequential register numbers sitting together
    print(f"\n🔍 Checking for sequential register numbers...")
    sequential_found = False
    for i in range(len(shuffled) - 1):
        curr_reg = shuffled[i].register_no
        next_reg = shuffled[i + 1].register_no
        
        # Check if they're from same department and sequential
        if shuffled[i].course_code == shuffled[i + 1].course_code:
            # Extract numeric part if possible
            try:
                curr_num = int(''.join(filter(str.isdigit, curr_reg)))
                next_num = int(''.join(filter(str.isdigit, next_reg)))
                if abs(curr_num - next_num) == 1:
                    print(f"   ⚠️  Sequential found: {curr_reg} → {next_reg} at positions {i+1}, {i+2}")
                    sequential_found = True
            except:
                pass
    
    if not sequential_found:
        print(f"   ✅ No sequential register numbers sitting together!")
    
    # Check department alternation
    print(f"\n🔄 Checking department alternation pattern...")
    same_dept_adjacent = 0
    for i in range(len(shuffled) - 1):
        if shuffled[i].course_code == shuffled[i + 1].course_code:
            same_dept_adjacent += 1
    
    alternation_rate = (1 - same_dept_adjacent / (len(shuffled) - 1)) * 100
    print(f"   Alternation Rate: {alternation_rate:.1f}%")
    
    if alternation_rate > 60:
        print(f"   ✅ Good alternation pattern!")
    else:
        print(f"   ⚠️  Low alternation rate - departments may not be well distributed")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    # Redirect output to file
    output_file = r'c:\Users\RANJITH KUMAR\OneDrive\Desktop\Exam-Management System\Student_management\test_results.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        import sys
        old_stdout = sys.stdout
        sys.stdout = f
        
        try:
            test_shuffling()
        finally:
            sys.stdout = old_stdout
    
    print(f"Test results written to: {output_file}")
    # Also print to console
    with open(output_file, 'r', encoding='utf-8') as f:
        print(f.read())

