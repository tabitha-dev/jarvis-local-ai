@echo off
REM Create a source-only release ZIP; refuse without an owner-approved LICENSE.
REM Does not delete folders, install models or publish anything.
setlocal
cd /d "%~dp0" || exit /b 1
if not exist "LICENSE" (
 echo Choose a project LICENSE and verify clean Windows installation first.
 echo This script WILL NOT create an unlicensed public download.
 exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
 echo Python environment not found. Run setup.bat before packaging.
 exit /b 1
)
".venv\Scripts\python.exe" tools\package_release.py --output "%~dp0jarvis-local-ai-source.zip"
if errorlevel 1 (
 echo Source packaging failed. Do NOT publish a release.
 exit /b 1
)
echo Source ZIP created locally. Review contents and obtain creator public release approval.
exit /b 0
