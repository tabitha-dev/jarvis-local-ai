@echo off
setlocal
cd /d "%~dp0" || exit /b 1
if not exist ".venv\Scripts\python.exe" (
 echo No local Python environment found. Run setup.bat first.
 exit /b 1
)
".venv\Scripts\python.exe" jarvis.py %*
set "CODE=%ERRORLEVEL%"
if not "%CODE%"=="0" echo Jarvis exited with error %CODE%.
pause
exit /b %CODE%
