@echo off
echo Setting up Leymax POS System...

REM Remove existing venv if it exists
@REM if exist "venv" (
@REM     echo Removing existing virtual environment...
@REM     rmdir /s /q venv
@REM )

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    exit /b 1
)

REM Install requirements
echo Installing requirements...
@REM python -m pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements
    exit /b 1
)

REM Initialize database
echo Initializing database...
python init_db.py
if errorlevel 1 (
    echo Failed to initialize database
    exit /b 1
)

REM Run the server
echo Starting server...
python run.py 