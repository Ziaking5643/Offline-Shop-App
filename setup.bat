@echo off
REM Quick Setup Script - Run this once before first use

echo.
echo ========================================
echo   Shop Management System - Setup
echo ========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    echo Please install Python 3.8+ first
    pause
    exit /b 1
)

cd /d "%~dp0"

REM Create virtual environment
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install --upgrade pip --quiet
    pip install -q Django==5.2.4
    echo [+] Setup complete!
) else (
    echo [+] Virtual environment already exists
)

echo.
echo You can now run: run.bat
echo.
pause
