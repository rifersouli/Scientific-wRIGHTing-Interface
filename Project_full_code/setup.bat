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

echo [STEP] 3. Setting up MySQL database...
echo.

REM Check if MySQL is installed
mysql --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] MySQL is not installed or not in PATH. Please install MySQL/MariaDB and try again.
    echo [INFO] Download from: https://dev.mysql.com/downloads/
    pause
    exit /b 1
)

echo [INFO] Creating database 'tcc_sw'...
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS tcc_sw CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>nul
if errorlevel 1 (
    echo [WARNING] Failed to create database. Please ensure MySQL is running and root password is correct.
    echo [INFO] You can manually create the database later with:
    echo mysql -u root -p -e "CREATE DATABASE tcc_sw CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    echo.
) else (
    echo [INFO] Database 'tcc_sw' created successfully ✓
)

echo [INFO] Loading database schema...
mysql -u root -p tcc_sw ^< backend\flaskr\schema.sql 2>nul
if errorlevel 1 (
    echo [WARNING] Failed to load schema. Please ensure the database exists and root password is correct.
    echo [INFO] You can manually load the schema later with:
    echo mysql -u root -p tcc_sw ^< backend\flaskr\schema.sql
    echo.
) else (
    echo [INFO] Database schema loaded successfully ✓
)

echo [INFO] Loading database data...
mysql -u root -p tcc_sw ^< backend\inserts.sql 2>nul
if errorlevel 1 (
    echo [WARNING] Failed to load data. Please ensure the database exists and root password is correct.
    echo [INFO] You can manually load the data later with:
    echo mysql -u root -p tcc_sw ^< backend\inserts.sql
    echo.
) else (
    echo [INFO] Database data loaded successfully ✓
)

echo [INFO] Database setup complete ✓
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
