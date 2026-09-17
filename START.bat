@echo off
title Circular Sender
echo.
echo  ==========================================
echo    Circular Sender — Starting up...
echo  ==========================================
echo.

REM Check if Flask is installed, install if missing
python -c "import flask" 2>nul
if errorlevel 1 (
    echo  Installing required packages...
    pip install flask flask-cors --quiet
    echo  Done.
    echo.
)

echo  Starting server + opening browser...
echo  To stop: close this window or press CTRL+C
echo.

python "%~dp0server.py"
pause
