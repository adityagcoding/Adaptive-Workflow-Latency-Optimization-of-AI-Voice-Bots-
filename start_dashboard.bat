@echo off
title Adaptive Workflow AI Voice Bot Dashboard
echo ======================================================================
echo    STARTING ADAPTIVE WORKFLOW AI VOICE BOT DASHBOARD
echo ======================================================================
echo.
echo 1. Starting FastAPI Backend Server in the background...
start /b python server.py
echo.
echo 2. Waiting 3 seconds for server to initialize engines and models...
timeout /t 3 /nobreak >nul
echo.
echo 3. Opening Dashboard in your browser at http://127.0.0.1:8000 ...
start "" "http://127.0.0.1:8000"
echo.
echo ======================================================================
echo    SERVER IS ACTIVE!
echo    URL: http://127.0.0.1:8000
echo    KEEP THIS WINDOW OPEN WHILE TESTING.
echo    (To stop the server, press Ctrl+C or close this window)
echo ======================================================================
echo.
:: Keep the terminal alive
python -c "import time; time.sleep(86400)"
