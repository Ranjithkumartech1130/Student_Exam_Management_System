from django.contrib import admin
from .models import ExamRecord


@admin.register(ExamRecord)
class ExamRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'register_no', 'student_name', 'course_code', 'course_title', 'exam_date', 'exam_session')
    list_filter = ('exam_date', 'exam_session', 'course_code')
    search_fields = ('register_no', 'student_name', 'course_code', 'course_title')
    readonly_fields = ('record',)
    ordering = ('-exam_date', 'register_no')
