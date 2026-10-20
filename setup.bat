@echo off
REM Windows-only setup for Jarvis. Review this script before executing it.
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0" || goto :failed

echo.
echo =================================================
echo  JARVIS SETUP - Windows development preview
echo  Requires internet and can take a while to finish.
echo  Review README and THIRD_PARTY_NOTICES first.
echo =================================================
echo.

echo === 1/6  Python 3.12 ===
call :find_python
if not errorlevel 1 goto :python_ready
echo Python 3.12 not detected. Checking winget...
where winget >nul 2>&1 || (echo winget is required to install Python. & goto :failed)
winget install --exact --id Python.Python.3.12 --scope user --silent --accept-package-agreements --accept-source-agreements
if errorlevel 1 goto :failed
call :find_python
if errorlevel 1 goto :failed
:python_ready
call :python --version
if errorlevel 1 goto :failed

echo.
echo === 2/6  Ollama (local model runner) ===
call :find_ollama
if defined OLLAMA_EXE goto :ollama_found
where winget >nul 2>&1 || (echo winget is required to install Ollama. & goto :failed)
winget install --exact --id Ollama.Ollama --silent --accept-package-agreements --accept-source-agreements
if errorlevel 1 goto :failed
call :find_ollama
if not defined OLLAMA_EXE (
    echo Ollama was installed but its executable was not located.
    echo Restart your command prompt or verify the Ollama installation.
    goto :failed
)
:ollama_found
"%OLLAMA_EXE%" --version
if errorlevel 1 goto :failed
curl --fail --silent --show-error "http://127.0.0.1:11434/api/tags" >nul 2>&1
if not errorlevel 1 goto :ollama_running
echo Starting Ollama local service...
start "" /min "%OLLAMA_EXE%" serve
for /L %%N in (1,1,15) do (
    curl --fail --silent --show-error "http://127.0.0.1:11434/api/tags" >nul 2>&1 && goto :ollama_running
    timeout /t 2 /nobreak >nul
)
echo Ollama API did not respond at 127.0.0.1:11434.
goto :failed
:ollama_running
echo Ollama responded on localhost.

echo.
echo === 3/6  Python environment and packages ===
if not exist ".venv\Scripts\python.exe" (
    call :python -m venv ".venv"
    if errorlevel 1 goto :failed
)
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :failed
set "REQS=requirements.txt"
if exist "requirements.lock.txt" (
    set "REQS=requirements.lock.txt"
    echo Using the pinned requirements.lock.txt from a verified Windows environment.
) else (
    echo NOTE: requirements.lock.txt is not available yet. Package versions are NOT pinned.
    echo This is a development install; complete Windows verification before public release.
)
echo Installing packages from %REQS%
".venv\Scripts\python.exe" -m pip install -r "%REQS%"
if errorlevel 1 goto :failed
if not exist "commands.json" (
    copy /y "commands.example.json" "commands.json" >nul
    if errorlevel 1 goto :failed
)

echo.
echo === 4/6  Choose your voice ===
echo Voice 1: Windows built-in (default; no voice download)
echo Voice 2: Cori - British female (optional Piper download)
echo          Public-domain training recordings; check docs\LICENSE_REVIEW.md.
echo Press 1, 2, or Enter. No input defaults to Windows after 25 seconds.
echo Your selection is saved to your personal commands.json.
".venv\Scripts\python.exe" tools\select_voice.py --timeout 25
if errorlevel 1 goto :failed

echo.
echo === 5/6  Speech model ===
".venv\Scripts\python.exe" -c "from faster_whisper import WhisperModel; WhisperModel('base.en', device='cpu', compute_type='int8'); print('Speech model ready')"
if errorlevel 1 goto :failed
echo The optional "Hey Jarvis" wake word is NOT downloaded. See README: Optional wake word.

echo.
echo === 6/6  Local Gemma AI model ===
"%OLLAMA_EXE%" pull gemma4:e2b
if errorlevel 1 goto :failed

echo.
echo =================================================
echo  Setup commands finished without reported failures.
echo  NEXT: run_tests.bat and validate on real Windows.
echo  Then run_jarvis.bat to test the HUD and audio.
echo  Local inference is distinct from online web actions.
echo =================================================
pause
exit /b 0

:find_python
set "PYTHON_EXE="
py -3.12 --version >nul 2>&1 && exit /b 0
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PYTHON_EXE if exist "%ProgramFiles%\Python312\python.exe" set "PYTHON_EXE=%ProgramFiles%\Python312\python.exe"
if not defined PYTHON_EXE exit /b 1
"%PYTHON_EXE%" --version >nul 2>&1
exit /b %errorlevel%

:python
if defined PYTHON_EXE (
    "%PYTHON_EXE%" %*
) else (
    py -3.12 %*
)
exit /b %errorlevel%

:find_ollama
set "OLLAMA_EXE="
for /f "delims=" %%P in ('where ollama 2^>nul') do if not defined OLLAMA_EXE set "OLLAMA_EXE=%%P"
if not defined OLLAMA_EXE if exist "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" set "OLLAMA_EXE=%LOCALAPPDATA%\Programs\Ollama\ollama.exe"
if not defined OLLAMA_EXE if exist "%ProgramFiles%\Ollama\ollama.exe" set "OLLAMA_EXE=%ProgramFiles%\Ollama\ollama.exe"
exit /b 0

:failed
echo.
echo SETUP INCOMPLETE. Review the error above before trying again.
echo Do not assume the models or dependencies are installed.
pause
exit /b 1
