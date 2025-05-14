@echo off
echo Cleaning up Leymax POS System...

REM Try to deactivate virtual environment if active
call venv\Scripts\deactivate.bat 2>nul

REM Wait a moment to ensure processes are released
timeout /t 2 /nobreak >nul

REM Remove virtual environment with force flag
echo Removing virtual environment...
rmdir /s /q venv 2>nul
if exist "venv" (
    echo Warning: Could not remove venv folder completely
    echo Please close any programs that might be using it and try again
) else (
    echo Virtual environment removed successfully
)

echo Cleanup complete. Run setup.bat to reinstall. 