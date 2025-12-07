from django.urls import path
from . import views

urlpatterns = [
    path('student/login/', views.student_login, name='student_login'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/records/', views.get_all_records, name='get_all_records'),
    path('admin/records/<int:record_id>/', views.get_record, name='get_record'),
    path('admin/records/create/', views.create_record, name='create_record'),
    path('admin/records/<int:record_id>/update/', views.update_record, name='update_record'),
    path('admin/records/<int:record_id>/delete/', views.delete_record, name='delete_record'),
    path('admin/rooms/', views.get_rooms, name='get_rooms'),
    path('admin/rooms/<int:room_id>/toggle/', views.toggle_room_status, name='toggle_room_status'),
    path('admin/rooms/add/', views.add_room, name='add_room'),
    path('admin/upload/', views.upload_csv, name='upload_csv'),
    path('admin/generate-seating/', views.generate_seating_api, name='generate_seating'),
    path('admin/refresh-allocation/', views.refresh_allocation, name='refresh_allocation'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
]
