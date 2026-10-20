@echo off
REM Create a source-only release ZIP; refuse without an owner-approved LICENSE.
REM Does not delete folders, install models or publish anything.
setlocal
cd /d "%~dp0"
if errorlevel 1 (
 echo Could not open the project directory.
 pause
 exit /b 1
)
if not exist "LICENSE" (
 echo Choose a project LICENSE and verify clean Windows installation first.
 echo This script WILL NOT create an unlicensed public download.
 pause
 exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
 echo Python environment not found. Run setup.bat before packaging.
 pause
 exit /b 1
)
".venv\Scripts\python.exe" tools\package_release.py --output "%~dp0jarvis-local-ai-source.zip"
if errorlevel 1 (
 echo Source packaging failed. Do NOT publish a release.
 pause
 exit /b 1
)
echo Source ZIP created locally. Review contents and obtain creator public release approval.
pause
exit /b 0
