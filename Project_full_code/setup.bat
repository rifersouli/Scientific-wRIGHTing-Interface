@echo off
echo 🎓 Setting up Scientific Writing Training Interface...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 16+ and try again.
    pause
    exit /b 1
)

echo [STEP] 1. Setting up Python backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt

echo [INFO] Backend setup complete ✓

echo [STEP] 2. Setting up React frontend...
cd ..\frontend\react-flask-app

REM Install Node.js dependencies
echo [INFO] Installing Node.js dependencies...
npm install

echo [INFO] Frontend setup complete ✓

cd ..\..

echo [STEP] 3. Database setup instructions...
echo.
echo [INFO] Please run these commands to set up the database:
echo.
echo mysql -u root -p
echo CREATE DATABASE tcc_sw CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
echo exit
echo.
echo mysql -u root -p tcc_sw ^< backend\flaskr\schema.sql
echo.

echo [STEP] 4. Starting the application...
echo.
echo [INFO] To start the application:
echo.
echo [INFO] Terminal 1 - Backend:
echo cd backend
echo venv\Scripts\activate
echo python app.py
echo.
echo [INFO] Terminal 2 - Frontend:
echo cd frontend\react-flask-app
echo npm start
echo.

echo [INFO] 🎉 Setup complete!
echo [INFO] Backend will be available at: http://localhost:5000
echo [INFO] Frontend will be available at: http://localhost:3000
pause
