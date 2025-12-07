from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
import json
import csv
import io
from .utils import generate_seating_arrangement

from .models import ExamRecord, Room, Dataset


def admin_dashboard(request):
    """Admin dashboard page with CRUD operations."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized access'}, status=403)
    
    return render(request, 'admin_dashboard.html')


@csrf_exempt
@require_http_methods(["POST"])
def student_login(request):
    """Handle student login with Register Number and Date of Birth."""
    try:
        data = json.loads(request.body)
        register_no = data.get('register_no', '').strip().upper()
        date_of_birth = data.get('date_of_birth', '')
        
        if not register_no or not date_of_birth:
            return JsonResponse({
                'success': False,
                'error': 'Register Number and Date of Birth are required'
            }, status=400)
        
        # Parse date of birth
        try:
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }, status=400)
        
        # Query database for matching record
        try:
            exam_record = ExamRecord.objects.get(
                register_no=register_no,
                date_of_birth=dob
            )
            
            # Return student data
            return JsonResponse({
                'success': True,
                'data': {
                    'record': exam_record.record,
                    'register_no': exam_record.register_no,
                    'student_name': exam_record.student_name,
                    'course_code': exam_record.course_code,
                    'course_title': exam_record.course_title,
                    'exam_date': exam_record.exam_date.strftime('%Y-%m-%d'),
                    'exam_session': exam_record.exam_session,
                    'exam_hall_number': exam_record.exam_hall_number,
                    'exam_seat_number': exam_record.exam_seat_number,
                }
            })
        except ExamRecord.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'No record found with the provided Register Number and Date of Birth'
            }, status=404)
        except ExamRecord.MultipleObjectsReturned:
            # If multiple records exist, return the first one
            exam_record = ExamRecord.objects.filter(
                register_no=register_no,
                date_of_birth=dob
            ).first()
            return JsonResponse({
                'success': True,
                'data': {
                    'record': exam_record.record,
                    'register_no': exam_record.register_no,
                    'student_name': exam_record.student_name,
                    'course_code': exam_record.course_code,
                    'course_title': exam_record.course_title,
                    'exam_date': exam_record.exam_date.strftime('%Y-%m-%d'),
                    'exam_session': exam_record.exam_session,
                    'exam_hall_number': exam_record.exam_hall_number,
                    'exam_seat_number': exam_record.exam_seat_number,
                }
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def admin_login(request):
    """Handle admin login."""
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return JsonResponse({
                'success': False,
                'error': 'Username and password are required'
            }, status=400)
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'redirect_url': '/api/admin/dashboard/'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid credentials'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_all_records(request):
    """Get all exam records (Admin only)."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    records = ExamRecord.objects.all().order_by('-exam_date', 'register_no')
    data = [{
        'record': r.record,
        'register_no': r.register_no,
        'student_name': r.student_name,
        'course_code': r.course_code,
        'course_title': r.course_title,
        'exam_date': r.exam_date.strftime('%Y-%m-%d'),
        'exam_session': r.exam_session,
        'exam_hall_number': r.exam_hall_number,
        'exam_seat_number': r.exam_seat_number,
        'date_of_birth': r.date_of_birth.strftime('%Y-%m-%d') if r.date_of_birth else None,
    } for r in records]
    
    return JsonResponse({'success': True, 'data': data})


@csrf_exempt
@require_http_methods(["GET"])
def get_record(request, record_id):
    """Get a single exam record by ID."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        record = ExamRecord.objects.get(record=record_id)
        return JsonResponse({
            'success': True,
            'data': {
                'record': record.record,
                'register_no': record.register_no,
                'student_name': record.student_name,
                'course_code': record.course_code,
                'course_title': record.course_title,
                'exam_date': record.exam_date.strftime('%Y-%m-%d'),
                'exam_session': record.exam_session,
                'exam_hall_number': record.exam_hall_number,
                'exam_seat_number': record.exam_seat_number,
                'date_of_birth': record.date_of_birth.strftime('%Y-%m-%d') if record.date_of_birth else None,
            }
        })
    except ExamRecord.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Record not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def create_record(request):
    """Create a new exam record."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        
        # Parse date fields
        exam_date = datetime.strptime(data['exam_date'], '%Y-%m-%d').date()
        date_of_birth = None
        if data.get('date_of_birth'):
            date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        
        record = ExamRecord.objects.create(
            register_no=data['register_no'].strip().upper(),
            student_name=data['student_name'],
            course_code=data['course_code'],
            course_title=data['course_title'],
            exam_date=exam_date,
            exam_session=data['exam_session'],
            exam_hall_number=data['exam_hall_number'],
            exam_seat_number=data['exam_seat_number'],
            date_of_birth=date_of_birth,
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Record created successfully',
            'data': {
                'record': record.record,
                'register_no': record.register_no,
                'student_name': record.student_name,
            }
        }, status=201)
        
    except KeyError as e:
        return JsonResponse({
            'success': False,
            'error': f'Missing required field: {str(e)}'
        }, status=400)
    except ValueError as e:
        return JsonResponse({
            'success': False,
            'error': f'Invalid date format: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def update_record(request, record_id):
    """Update an existing exam record."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        record = ExamRecord.objects.get(record=record_id)
        data = json.loads(request.body)
        
        # Update fields if provided
        if 'register_no' in data:
            record.register_no = data['register_no'].strip().upper()
        if 'student_name' in data:
            record.student_name = data['student_name']
        if 'course_code' in data:
            record.course_code = data['course_code']
        if 'course_title' in data:
            record.course_title = data['course_title']
        if 'exam_date' in data:
            record.exam_date = datetime.strptime(data['exam_date'], '%Y-%m-%d').date()
        if 'exam_session' in data:
            record.exam_session = data['exam_session']
        if 'exam_hall_number' in data:
            record.exam_hall_number = data['exam_hall_number']
        if 'exam_seat_number' in data:
            record.exam_seat_number = data['exam_seat_number']
        if 'date_of_birth' in data:
            if data['date_of_birth']:
                record.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            else:
                record.date_of_birth = None
        
        record.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Record updated successfully',
            'data': {
                'record': record.record,
                'register_no': record.register_no,
                'student_name': record.student_name,
            }
        })
        
    except ExamRecord.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Record not found'}, status=404)
    except ValueError as e:
        return JsonResponse({
            'success': False,
            'error': f'Invalid date format: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_record(request, record_id):
    """Delete an exam record."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        record = ExamRecord.objects.get(record=record_id)
        record.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Record deleted successfully'
        })
        
    except ExamRecord.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Record not found'}, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_rooms(request):
    """Get all rooms with their status."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    rooms = Room.objects.all().order_by('room_number')
    data = [{
        'id': r.id,
        'room_number': r.room_number,
        'capacity': r.capacity,
        'is_available': r.is_available
    } for r in rooms]
    
    return JsonResponse({'success': True, 'data': data})


@csrf_exempt
@require_http_methods(["POST"])
def toggle_room_status(request, room_id):
    """Toggle room availability."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        room = Room.objects.get(id=room_id)
        room.is_available = not room.is_available
        room.save()
        return JsonResponse({
            'success': True, 
            'data': {'id': room.id, 'is_available': room.is_available}
        })
    except Room.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Room not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def upload_csv(request):
    """Upload CSV and populate ExamRecords."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if 'file' not in request.FILES:
        return JsonResponse({'success': False, 'error': 'No file uploaded'}, status=400)
    
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        return JsonResponse({'success': False, 'error': 'File is not CSV type'}, status=400)
    
    try:
        # Get active dataset
        active_id = request.session.get('active_dataset_id')
        if not active_id:
            # Try to get most recent dataset
            dataset = Dataset.objects.first()
            if not dataset:
                return JsonResponse({
                    'success': False, 
                    'error': 'No dataset available. Please create a dataset first.'
                }, status=400)
            request.session['active_dataset_id'] = dataset.id
        else:
            try:
                dataset = Dataset.objects.get(id=active_id)
            except Dataset.DoesNotExist:
                return JsonResponse({
                    'success': False, 
                    'error': 'Active dataset not found. Please select a dataset.'
                }, status=400)
        
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        reader = csv.DictReader(io_string)
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        for row in reader:
            register_no = row.get('Roll-no') or row.get('Roll No') or row.get('register_no')
            student_name = row.get('Name') or row.get('student_name')
            course_code = row.get('Course_code') or row.get('Course Code') or row.get('course_code')
            course_title = row.get('Course-name') or row.get('Course Name') or row.get('course_title')
            date_session = row.get('Date-Session') or row.get('Date Session')
            date_of_birth_str = row.get('Date-of-Birth') or row.get('Date of Birth') or row.get('date_of_birth')
            
            if register_no and student_name:
                exam_date = timezone.now().date()
                exam_session = 'Morning'
                date_of_birth = None
                
                # Parse date of birth
                if date_of_birth_str:
                    try:
                        date_of_birth = datetime.strptime(date_of_birth_str.strip(), '%Y-%m-%d').date()
                    except ValueError:
                        pass  # Skip invalid dates
                
                if date_session:
                    parts = date_session.split('-')
                    if len(parts) >= 3:
                        try:
                            # Attempt to find YYYY-MM-DD
                            date_str = "-".join(parts[:3])
                            exam_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                            if len(parts) > 3:
                                exam_session = parts[3]
                        except:
                            pass
                
                # Use get_or_create to prevent duplicates within this dataset
                record, created = ExamRecord.objects.get_or_create(
                    register_no=register_no.strip().upper(),
                    dataset=dataset,  # Link to active dataset
                    defaults={
                        'student_name': student_name.strip(),
                        'course_code': course_code.strip() if course_code else '',
                        'course_title': course_title.strip() if course_title else '',
                        'exam_date': exam_date,
                        'exam_session': exam_session,
                        'exam_hall_number': 'Pending',
                        'exam_seat_number': 'Pending',
                        'date_of_birth': date_of_birth
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    # Update existing record
                    record.student_name = student_name.strip()
                    record.course_code = course_code.strip() if course_code else ''
                    record.course_title = course_title.strip() if course_title else ''
                    record.exam_date = exam_date
                    record.exam_session = exam_session
                    record.date_of_birth = date_of_birth
                    record.save()
                    updated_count += 1
                
        return JsonResponse({
            'success': True, 
            'message': f'Created {created_count} new records, updated {updated_count} existing records in dataset "{dataset.name}"'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



@csrf_exempt
@require_http_methods(["POST"])
def generate_seating_api(request):
    """Trigger seating arrangement generation."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        selected_rooms = list(Room.objects.filter(is_available=True))
        
        if not selected_rooms:
            return JsonResponse({'success': False, 'error': 'No available rooms found for allocation'}, status=400)
            
        result = generate_seating_arrangement(selected_rooms)
        
        return JsonResponse({
            'success': True, 
            'message': f"Allocated {result['total_allocated']} students",
            'data': result
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def refresh_allocation(request):
    """Clear existing allocations and regenerate seating arrangement (Admin only)."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        # Step 1: Reset all existing allocations to "Pending"
        reset_count = ExamRecord.objects.all().update(
            exam_hall_number='Pending',
            exam_seat_number='Pending'
        )
        
        # Step 2: Get available rooms
        selected_rooms = list(Room.objects.filter(is_available=True))
        
        if not selected_rooms:
            return JsonResponse({
                'success': False, 
                'error': 'No available rooms found for allocation'
            }, status=400)
        
        # Step 3: Generate new seating arrangement
        result = generate_seating_arrangement(selected_rooms)
        
        return JsonResponse({
            'success': True,
            'message': f"Reset {reset_count} records and allocated {result['total_allocated']} students",
            'data': result
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def add_room(request):
    """Add a new room manually."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        room_number = data.get('room_number', '').strip()
        capacity = int(data.get('capacity', 0))
        
        if not room_number or capacity <= 0:
            return JsonResponse({'success': False, 'error': 'Invalid room details'}, status=400)
            
        if Room.objects.filter(room_number=room_number).exists():
            return JsonResponse({'success': False, 'error': 'Room already exists'}, status=400)
            
        room = Room.objects.create(
            room_number=room_number,
            capacity=capacity,
            is_available=True
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Room added successfully',
            'data': {'id': room.id, 'room_number': room.room_number, 'capacity': room.capacity, 'is_available': True}
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
@csrf_exempt
@require_http_methods(["POST"])
def admin_logout(request):
    """Handle admin logout."""
    try:
        from django.contrib.auth import logout as auth_logout
        auth_logout(request)
        return JsonResponse({'success': True, 'message': 'Logged out successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============ Dataset Management Endpoints ============

@csrf_exempt
@require_http_methods(["GET"])
def get_datasets(request):
    """Get all datasets with metadata."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    datasets = Dataset.objects.all()
    data = [{
        'id': d.id,
        'name': d.name,
        'exam_type': d.exam_type,
        'exam_type_display': d.get_exam_type_display(),
        'created_at': d.created_at.strftime('%Y-%m-%d %H:%M'),
        'is_active': d.is_active,
        'record_count': d.record_count,
        'description': d.description or ''
    } for d in datasets]
    
    return JsonResponse({'success': True, 'data': data})


@csrf_exempt
@require_http_methods(["POST"])
def create_dataset(request):
    """Create a new dataset."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        exam_type = data.get('exam_type', 'end_semester')
        description = data.get('description', '')
        
        # Auto-generate name based on exam type and timestamp
        exam_type_names = {
            'end_semester': 'End Semester',
            'arrear': 'Arrear',
            'internal': 'Internal'
        }
        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M')
        name = f"{exam_type_names.get(exam_type, 'Exam')} - {timestamp}"
        
        # Create dataset
        dataset = Dataset.objects.create(
            name=name,
            exam_type=exam_type,
            description=description,
            is_active=True
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Dataset "{name}" created successfully',
            'data': {
                'id': dataset.id,
                'name': dataset.name,
                'exam_type': dataset.exam_type,
                'record_count': 0
            }
        }, status=201)
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def switch_dataset(request, dataset_id):
    """Set a dataset as active (for session-based filtering)."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        
        # Store active dataset ID in session
        request.session['active_dataset_id'] = dataset.id
        
        return JsonResponse({
            'success': True,
            'message': f'Switched to dataset: {dataset.name}',
            'data': {
                'id': dataset.id,
                'name': dataset.name,
                'record_count': dataset.record_count
            }
        })
    except Dataset.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Dataset not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def refresh_dataset(request, dataset_id):
    """Clear all records from a dataset."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        deleted_count = dataset.records.count()
        dataset.records.all().delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Deleted {deleted_count} records from dataset "{dataset.name}"'
        })
    except Dataset.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Dataset not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_dataset(request, dataset_id):
    """Delete a dataset and all its records."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        dataset_name = dataset.name
        dataset.delete()
        
        # Clear from session if it was active
        if request.session.get('active_dataset_id') == dataset_id:
            request.session.pop('active_dataset_id', None)
        
        return JsonResponse({
            'success': True,
            'message': f'Dataset "{dataset_name}" deleted successfully'
        })
    except Dataset.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Dataset not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_active_dataset(request):
    """Get the currently active dataset."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        # Get active dataset from session, or use most recent
        active_id = request.session.get('active_dataset_id')
        
        if active_id:
            try:
                dataset = Dataset.objects.get(id=active_id)
            except Dataset.DoesNotExist:
                # If stored dataset doesn't exist, get most recent
                dataset = Dataset.objects.first()
                if dataset:
                    request.session['active_dataset_id'] = dataset.id
        else:
            # No active dataset in session, get most recent
            dataset = Dataset.objects.first()
            if dataset:
                request.session['active_dataset_id'] = dataset.id
        
        if dataset:
            return JsonResponse({
                'success': True,
                'data': {
                    'id': dataset.id,
                    'name': dataset.name,
                    'exam_type': dataset.exam_type,
                    'record_count': dataset.record_count
                }
            })
        else:
            return JsonResponse({
                'success': True,
                'data': None,
                'message': 'No datasets available'
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
