@echo off
title Margdarshak AI - Offline Launcher
echo ========================================================
echo   Starting Margdarshak AI in Offline Mode (No Internet Needed)
echo ========================================================
echo.
echo Starting backend server on http://localhost:8000...
start " http://localhost:8000
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
pause
