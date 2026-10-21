@echo off
REM Local-only, minimal Windows release report. Never uploads data.
REM Avoid raw error logs, device names, full system paths or transcripts in the report.
REM A clean account is not necessarily a clean Windows PC; full install checks are manual.
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0.."
if errorlevel 1 (
  echo Could not locate the project directory.
  pause
  exit /b 1
)
set "OUT=windows-test-report.txt"
set "PY=.venv\Scripts\python.exe"
set "OLLAMA_EXE=ollama"
if exist "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" set "OLLAMA_EXE=%LOCALAPPDATA%\Programs\Ollama\ollama.exe"
set "STATUS=0"

> "%OUT%" echo Jarvis Windows local test report
>> "%OUT%" echo Generated: %DATE% %TIME%
>> "%OUT%" echo NOTE: This is a minimal local summary, NOT evidence of a clean install or voice quality.
>> "%OUT%" echo Review the report before sharing it. No files are uploaded.
>> "%OUT%" echo.
>> "%OUT%" echo === Windows version ===
ver >> "%OUT%" 2>nul
>> "%OUT%" echo.
>> "%OUT%" echo === Virtual environment ===
if not exist "%PY%" goto :no_python
"%PY%" --version >> "%OUT%" 2>nul
if errorlevel 1 set "STATUS=1"
goto :python_done
:no_python
>> "%OUT%" echo FAIL: Python virtual environment missing.
set "STATUS=1"
:python_done
>> "%OUT%" echo.
>> "%OUT%" echo === Ollama ===
"%OLLAMA_EXE%" --version >> "%OUT%" 2>nul
if errorlevel 1 (
  >> "%OUT%" echo FAIL: Ollama command unavailable.
  set "STATUS=1"
)
"%OLLAMA_EXE%" list 2>nul | findstr /i /c:"gemma4:e2b" >nul
if errorlevel 1 (
  >> "%OUT%" echo FAIL: Expected gemma4:e2b model not found.
  set "STATUS=1"
) else (
  >> "%OUT%" echo PASS: Expected Gemma model is listed.
)
>> "%OUT%" echo.
>> "%OUT%" echo === Piper voice files ===
if exist "voices\*.onnx" (
  >> "%OUT%" echo PRESENT: At least one voice file exists. Voice operation was not tested.
) else (
  >> "%OUT%" echo OPTIONAL: No Piper voice installed. Windows SAPI needs no voice download.
)
if not exist "%PY%" goto :report_end
>> "%OUT%" echo.
>> "%OUT%" echo === Audio ===
"%PY%" -c "import sounddevice as sd; print('Audio devices detected:', len(sd.query_devices()))" >> "%OUT%" 2>nul
if errorlevel 1 (
  >> "%OUT%" echo FAIL: Audio-device query did not succeed.
  set "STATUS=1"
)
>> "%OUT%" echo.
>> "%OUT%" echo === Dependencies ===
"%PY%" -m pip check >nul 2>&1
if errorlevel 1 (
  >> "%OUT%" echo FAIL: pip check. Run pip check locally and inspect the error before sharing.
  set "STATUS=1"
) else (
  >> "%OUT%" echo PASS: pip check.
)
>> "%OUT%" echo.
>> "%OUT%" echo === Unit tests ===
"%PY%" -m unittest discover tests >nul 2>&1
if errorlevel 1 (
  >> "%OUT%" echo FAIL: Unit tests. Run run_tests.bat locally for details; do not share raw paths.
  set "STATUS=1"
) else (
  >> "%OUT%" echo PASS: Unit tests. Still not a hardware/integration check.
)
:report_end
>> "%OUT%" echo.
>> "%OUT%" echo === Manual verification required ===
>> "%OUT%" echo Fresh user installation, HUD, local AI reply, microphone, playback, push-to-talk, app commands, permissions and third-party licensing need human confirmation.
if "%STATUS%"=="0" (
  echo Summary report saved: %OUT%
) else (
  echo Summary report saved with checks requiring attention: %OUT%
)
echo Please read the report before uploading it. No diagnostic logs or device names are included.
pause
exit /b %STATUS%
