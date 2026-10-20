@echo off
REM Runs Jarvis's tests. Nothing opens or launches - everything is faked.
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python -m unittest discover tests -v
pause
