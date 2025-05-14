@echo off
echo Starting Leymax POS System Backend...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the server with reload for development
uvicorn main:app --host 127.0.0.1 --port 8000 --reload 