@echo off
REM Shop Management System - Windows Batch Runner
REM This script sets up and runs the Django development server

echo.
echo ========================================
echo    Shop Management System
echo    Offline Mode - Local Installation
echo ========================================
echo.

REM Set the project directory
set PROJECT_DIR=%~dp0

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [*] Python found!
echo.

REM Navigate to project directory
cd /d "%PROJECT_DIR%"

REM Check if virtual environment exists
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
    echo [+] Virtual environment created!
)

echo.
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Installing/updating required packages...
pip install --upgrade pip --quiet
pip install -q Django==5.2.4

echo [+] Packages ready!
echo.

REM Run migrations
echo [*] Applying database migrations...
python manage.py migrate --noinput

echo [+] Database ready!
echo.

REM Create admin user if needed
echo [*] Checking admin account...
python manage.py shell -c "from django.contrib.auth.models import User; print('Admin exists' if User.objects.filter(username='admin').exists() else '')" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Creating default admin account...
    echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None | python manage.py shell
)

echo.
echo ========================================
echo   Starting Development Server
echo ========================================
echo.
echo [+] Server is running at: http://127.0.0.1:8000/
echo.
echo [+] Admin Panel: http://127.0.0.1:8000/admin/
echo    Username: admin
echo    Password: admin123
echo.
echo [!] Press Ctrl+C to stop the server
echo.

REM Start the development server
python manage.py runserver 0.0.0.0:8000

pause
