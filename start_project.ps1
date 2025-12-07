# Start Django Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'Student_management'; python manage.py runserver" -WorkingDirectory $PSScriptRoot

# Start Next.js Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'frontend'; npm run dev" -WorkingDirectory $PSScriptRoot

Write-Host "Servers are starting..."
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:3000"
Write-Host "Admin Login: http://localhost:3000/admin/login"
