@echo off
REM Builds a clean, shareable copy of Jarvis in ..\jarvis-release
REM (no .venv, no voices, no personal commands.json) - ready for GitHub.
cd /d "%~dp0"
set "OUT=%~dp0..\jarvis-release"
if exist "%OUT%" rmdir /s /q "%OUT%"
mkdir "%OUT%" "%OUT%\tests"

for %%F in (jarvis.py commands.py ui.html requirements.txt setup.bat run_jarvis.bat run_tests.bat commands.example.json .gitignore README.md THIRD_PARTY_NOTICES.md) do (
  if exist "%%F" copy /y "%%F" "%OUT%\" >nul
)
copy /y tests\*.py "%OUT%\tests\" >nul

REM Record the exact package versions that work on this PC
if exist .venv\Scripts\pip.exe (
  .venv\Scripts\pip.exe freeze > "%OUT%\requirements.lock.txt"
  echo Wrote requirements.lock.txt with your working versions.
)

echo.
echo Clean release folder: %OUT%
echo Check it for anything personal before you upload it.
pause
