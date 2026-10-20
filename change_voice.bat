@echo off
REM Change the user's private voice choice without reinstalling Ollama or Jarvis.
setlocal
cd /d "%~dp0"
if errorlevel 1 goto :failed
if not exist ".venv\Scripts\python.exe" (
  echo Jarvis Python environment missing. Run setup.bat first.
  goto :failed
)
".venv\Scripts\python.exe" tools\select_voice.py --timeout 25
if errorlevel 1 goto :failed
 echo Your voice setting is saved. Restart Jarvis to hear the change.
 pause
 exit /b 0
:failed
 echo Could not change the voice. Your existing choice was preserved.
 pause
 exit /b 1
