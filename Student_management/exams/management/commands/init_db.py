from django.core.management.base import BaseCommand
from exams.models import ExamRecord
from datetime import date


class Command(BaseCommand):
    help = 'Initialize database with sample exam records'

    def handle(self, *args, **options):
        self.stdout.write('Initializing database with sample data...')

        # Sample exam records
        sample_records = [
            {
                'register_no': '711724UAM113',
                'student_name': 'John Doe',
                'course_code': 'CS101',
                'course_title': 'Introduction to Computer Science',
                'exam_date': date(2024, 3, 15),
                'exam_session': 'Morning',
                'exam_hall_number': 'H101',
                'exam_seat_number': 'S001',
                'date_of_birth': date(2002, 5, 15),
            },
            {
                'register_no': '711724UAM139',
                'student_name': 'Jane Smith',
                'course_code': 'CS101',
                'course_title': 'Introduction to Computer Science',
                'exam_date': date(2024, 3, 15),
                'exam_session': 'Morning',
                'exam_hall_number': 'H101',
                'exam_seat_number': 'S002',
                'date_of_birth': date(2002, 7, 20),
            },
            {
                'register_no': '711724UAM101',
                'student_name': 'Robert Johnson',
                'course_code': 'MATH201',
                'course_title': 'Advanced Mathematics',
                'exam_date': date(2024, 3, 16),
                'exam_session': 'Afternoon',
                'exam_hall_number': 'H102',
                'exam_seat_number': 'S015',
                'date_of_birth': date(2001, 9, 10),
            },
            {
                'register_no': '711724UAM118',
                'student_name': 'Emily Davis',
                'course_code': 'PHY301',
                'course_title': 'Physics Fundamentals',
                'exam_date': date(2024, 3, 17),
                'exam_session': 'Morning',
                'exam_hall_number': 'H103',
                'exam_seat_number': 'S030',
                'date_of_birth': date(2002, 11, 25),
            },
            {
                'register_no': '711724UAM155',
                'student_name': 'Michael Wilson',
                'course_code': 'CS201',
                'course_title': 'Data Structures and Algorithms',
                'exam_date': date(2024, 3, 18),
                'exam_session': 'Afternoon',
                'exam_hall_number': 'H101',
                'exam_seat_number': 'S045',
                'date_of_birth': date(2001, 3, 8),
            },
        ]

        created_count = 0
        for record_data in sample_records:
            record, created = ExamRecord.objects.get_or_create(
                register_no=record_data['register_no'],
                defaults=record_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created record for {record_data["register_no"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Record {record_data["register_no"]} already exists')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} new records')
        )

