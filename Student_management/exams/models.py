from django.db import models
from django.core.validators import RegexValidator


class Dataset(models.Model):
    """Model to manage different datasets for exam records (e.g., End Semester, Arrear, Internal)."""
    
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text='Name of the dataset (e.g., "End Semester - 2025-12-07")'
    )
    exam_type = models.CharField(
        max_length=50,
        choices=[
            ('end_semester', 'End Semester Exam'),
            ('arrear', 'Arrear Exam'),
            ('internal', 'Internal Exam'),
        ],
        help_text='Type of examination'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When this dataset was created'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this dataset is currently active'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Optional description of this dataset'
    )
    
    class Meta:
        db_table = 'Dataset'
        verbose_name = 'Dataset'
        verbose_name_plural = 'Datasets'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_exam_type_display()})"
    
    @property
    def record_count(self):
        """Get the number of records in this dataset."""
        return self.records.count()


class ExamRecord(models.Model):
    """Model for storing exam records with all required fields."""
    
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='records',
        null=True,  # Temporarily nullable for migration
        blank=True,
        help_text='Dataset this record belongs to'
    )
    
    record = models.AutoField(primary_key=True, db_column='Record')
    register_no = models.CharField(
        max_length=50,
        db_column='RegisterNo',
        validators=[RegexValidator(regex=r'^[A-Z0-9]+$', message='Register number must be alphanumeric')],
        help_text='Student registration number'
    )
    student_name = models.CharField(
        max_length=200,
        db_column='StudentName',
        help_text='Full name of the student'
    )
    course_code = models.CharField(
        max_length=20,
        db_column='Coursecode',
        help_text='Course code identifier'
    )
    course_title = models.CharField(
        max_length=200,
        db_column='CourseTitle',
        help_text='Full title of the course'
    )
    exam_date = models.DateField(
        db_column='ExamDate',
        help_text='Date of the examination'
    )
    exam_session = models.CharField(
        max_length=50,
        db_column='ExamSession',
        help_text='Session of the exam (e.g., Morning, Afternoon)'
    )
    exam_hall_number = models.CharField(
        max_length=20,
        db_column='ExamHallNumber',
        help_text='Hall number where exam is conducted'
    )
    exam_seat_number = models.CharField(
        max_length=20,
        db_column='ExamSeatNumber',
        help_text='Seat number assigned to the student'
    )
    date_of_birth = models.DateField(
        db_column='DateOfBirth',
        null=True,
        blank=True,
        help_text='Date of birth for authentication'
    )

    class Meta:
        db_table = 'ExamRecord'
        verbose_name = 'Exam Record'
        verbose_name_plural = 'Exam Records'
        indexes = [
            models.Index(fields=['register_no'], name='idx_register_no'),
            models.Index(fields=['exam_date'], name='idx_exam_date'),
        ]

    def __str__(self):
        return f"{self.register_no} - {self.student_name} - {self.course_code}"


class Room(models.Model):
    """Model to manage exam rooms and their availability."""
    room_number = models.CharField(max_length=20, unique=True, help_text="Room number or name")
    capacity = models.IntegerField(help_text="Seating capacity of the room")
    is_available = models.BooleanField(default=True, help_text="Is the room available for exam allocation?")

    def __str__(self):
        return f"{self.room_number} ({self.capacity})"
