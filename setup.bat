@echo off
REM One-time setup for Jarvis. Double-click this file. Needs internet.
cd /d "%~dp0"
setlocal

echo.
echo ================================================
echo   JARVIS SETUP  -  this takes 10-30 minutes
echo   If Windows asks "allow changes?", click Yes.
echo ================================================

echo.
echo === 1/6  Python 3.12 ===
set "PY="
py -3.12 --version >nul 2>&1 && set "PY=py -3.12"
if not defined PY if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PY (
  echo Installing Python 3.12...
  winget install -e --id Python.Python.3.12 --scope user --silent --accept-package-agreements --accept-source-agreements
  if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)
if not defined PY (
  echo Python install didn't finish. Close this window and run setup.bat again.
  pause & exit /b 1
)
echo Using: %PY%

echo.
echo === 2/6  Ollama (the local AI engine) ===
set "OLLAMA=ollama"
where ollama >nul 2>&1 || set "OLLAMA=%LOCALAPPDATA%\Programs\Ollama\ollama.exe"
if not exist "%OLLAMA%" if not "%OLLAMA%"=="ollama" (
  echo Installing Ollama...
  winget install -e --id Ollama.Ollama --silent --accept-package-agreements --accept-source-agreements
)
where ollama >nul 2>&1 && set "OLLAMA=ollama"
curl -s http://localhost:11434 >nul 2>&1 || (
  echo Starting Ollama...
  start "" /min "%OLLAMA%" serve
  timeout /t 8 /nobreak >nul
)

echo.
echo === 3/6  Python packages ===
if not exist .venv %PY% -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt || (echo Package install failed. & pause & exit /b 1)

if not exist commands.json copy /y commands.example.json commands.json >nul

echo.
echo === 4/6  Jarvis's voice ===
if not exist voices mkdir voices
python -m piper.download_voices en_GB-alan-medium --data-dir voices

echo.
echo === 5/6  Speech and wake-word models ===
python -c "from faster_whisper import WhisperModel; WhisperModel('base.en', device='cpu', compute_type='int8'); print('speech model ready')"
python -c "import openwakeword.utils as u; u.download_models(['hey_jarvis']); print('wake word ready')"

echo.
echo === 6/6  The AI brain (biggest download, be patient) ===
"%OLLAMA%" pull gemma4:e2b

echo.
echo ================================================
echo   Setup complete! Jarvis now works offline.
echo   Double-click run_jarvis.bat to start.
echo ================================================
pause
