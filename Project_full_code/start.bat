@echo off
echo Starting Scientific Writing Training Interface...

echo.
echo [INFO] Starting Flask backend...
start "Flask Backend" cmd /k "cd backend && python app.py"

echo.
echo [INFO] Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak > nul

echo.
echo [INFO] Starting React frontend...
start "React Frontend" cmd /k "cd frontend\react-flask-app && npm start"

echo.
echo [INFO] Both services are starting!
echo [INFO] Backend: http://localhost:5000
echo [INFO] Frontend: http://localhost:3000
echo.
echo [INFO] Press any key to close this window...
pause > nul
