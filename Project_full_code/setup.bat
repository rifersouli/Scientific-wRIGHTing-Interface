@echo off
echo Setting up Scientific Writing Training Interface...

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

REM Check if backend directory exists
if not exist "backend" (
    echo [ERROR] Backend directory not found.
    echo [INFO] Please ensure you are running this script from the project root directory.
    pause
    exit /b 1
)

cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create Python virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies.
    echo [INFO] Please check your internet connection and try running 'pip install -r requirements.txt' manually.
    pause
    exit /b 1
)

echo [INFO] Backend setup complete

echo [STEP] 2. Setting up React frontend...

REM Check if frontend directory exists
if not exist "..\frontend\react-flask-app" (
    echo [ERROR] Frontend directory not found: ..\frontend\react-flask-app
    echo [INFO] Please ensure the project structure is correct.
    pause
    exit /b 1
)

cd ..\frontend\react-flask-app
echo [DEBUG] Changed to directory: %CD%

REM Check if package.json exists
if not exist "package.json" (
    echo [ERROR] package.json not found in frontend directory.
    echo [DEBUG] Current directory contents:
    dir /b
    echo [INFO] Please ensure the React app is properly set up.
    pause
    exit /b 1
)

echo [DEBUG] Found package.json, proceeding with npm install...

REM Check if node_modules already exists
if exist "node_modules" (
    echo [INFO] node_modules directory already exists, skipping npm install...
) else (
    REM Install Node.js dependencies
    echo [INFO] Installing Node.js dependencies...
    echo [DEBUG] Current directory: %CD%
    echo [DEBUG] Running: npm install
    npm install --verbose --no-audit --no-fund
    if errorlevel 1 (
        echo [ERROR] Failed to install Node.js dependencies.
        echo [INFO] Trying alternative installation method...
        npm install --legacy-peer-deps --no-audit --no-fund
        if errorlevel 1 (
            echo [ERROR] Both npm install methods failed.
            echo [INFO] Please check your internet connection and try running 'npm install' manually.
            echo [INFO] You can also try clearing npm cache: npm cache clean --force
            pause
            exit /b 1
        ) else (
            echo [INFO] Alternative npm install method succeeded
        )
    ) else (
        echo [INFO] npm install completed successfully
    )
)

echo [INFO] Frontend setup complete

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
    echo [INFO] Database 'tcc_sw' created successfully
)

echo [INFO] Loading database schema...
mysql -u root -p tcc_sw < backend\flaskr\schema.sql 2>nul
if errorlevel 1 (
    echo [WARNING] Failed to load schema. Please ensure the database exists and root password is correct.
    echo [INFO] You can manually load the schema later with:
    echo mysql -u root -p tcc_sw ^< backend\flaskr\schema.sql
    echo.
) else (
    echo [INFO] Database schema loaded successfully
)

echo [INFO] Loading database data...
mysql -u root -p tcc_sw < backend\inserts.sql 2>nul
if errorlevel 1 (
    echo [WARNING] Failed to load data. Please ensure the database exists and root password is correct.
    echo [INFO] You can manually load the data later with:
    echo mysql -u root -p tcc_sw ^< backend\inserts.sql
    echo.
) else (
    echo [INFO] Database data loaded successfully
)

echo [INFO] Database setup complete
echo.

echo [INFO] Setup complete! Run the start.bat file to start the application.
echo.
pause
