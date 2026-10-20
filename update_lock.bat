@echo off
REM Create requirements.lock.txt from a VERIFIED Windows environment.
REM Do not generate a public lock file from CI or a different OS.
setlocal
cd /d "%~dp0"
if errorlevel 1 (
 echo Could not open the project directory.
 pause
 exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
 echo Python environment not found. Run setup.bat and verify Jarvis on Windows first.
 pause
 exit /b 1
)
REM Write to a temp file first so pip failures never overwrite a good lock.
".venv\Scripts\python.exe" -m pip freeze --exclude-editable > "requirements.lock.tmp"
if errorlevel 1 goto :freeze_failed
for %%F in ("requirements.lock.tmp") do if %%~zF EQU 0 goto :freeze_failed
".venv\Scripts\python.exe" -m pip check
if errorlevel 1 goto :freeze_failed
move /Y "requirements.lock.tmp" "requirements.lock.txt" >nul
if errorlevel 1 goto :freeze_failed
echo requirements.lock.txt saved. Review the package versions, test a fresh Windows install, then commit it.
pause
exit /b 0
:freeze_failed
echo Could not generate a valid requirements.lock.txt. The existing lock file was not overwritten.
if exist "requirements.lock.tmp" del /q "requirements.lock.tmp"
pause
exit /b 1
