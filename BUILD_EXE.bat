@echo off
title Building CircularSender.exe
echo.
echo  ==========================================
echo    CircularSender — Building EXE...
echo  ==========================================
echo.

echo  [1/3] Installing dependencies...
pip install pyinstaller flask flask-cors pystray pillow --quiet
echo  Done.
echo.

echo  [2/3] Building EXE (this takes ~1-2 minutes)...
pyinstaller ^
  --onefile ^
  --noconsole ^
  --name "CircularSender" ^
  --add-data "CircularSender.html;." ^
  --hidden-import "pystray._win32" ^
  --hidden-import "PIL._tkinter_finder" ^
  "%~dp0server.py"

echo.
echo  [3/3] Done!
echo.
echo  Your EXE is at: dist\CircularSender.exe
echo.
echo  Just double-click it to run — no other files needed!
echo  Right-click the tray icon (bottom-right taskbar) to stop.
echo.
pause
