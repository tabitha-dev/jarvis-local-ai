@echo off
setlocal
cd /d "%~dp0"
if errorlevel 1 (
 echo Could not open the project directory.
 pause
 exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
 echo No local Python environment found. Run setup.bat first.
 pause
 exit /b 1
)
".venv\Scripts\python.exe" -m unittest discover tests -v
set "CODE=%ERRORLEVEL%"
if not "%CODE%"=="0" echo Tests FAILED. Do not treat this as release-ready.
pause
exit /b %CODE%
