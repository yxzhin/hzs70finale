@echo off
cd /d "%~dp0"

REM Create venv if it doesn't exist
if not exist server\venv (
    python -m venv server\venv
)

REM Activate venv
call server\venv\Scripts\activate.bat

REM Install requirements
pip install -r server\requirements.txt

REM Run your app from project root
python -m server.run

pause