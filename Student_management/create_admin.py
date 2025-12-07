import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_portal.settings')
django.setup()

from django.contrib.auth.models import User

username = 'Kgkite'
password = 'password123'
email = 'admin@example.com'

try:
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists. Updating password...")
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
    else:
        print(f"Creating user '{username}'...")
        User.objects.create_superuser(username, email, password)
    
    print(f"Success! Username: {username}, Password: {password}")

except Exception as e:
    print(f"Error: {e}")
