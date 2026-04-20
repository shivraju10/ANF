@echo off
echo =========================================
echo Installing Dependencies for SFTP Monitor
echo =========================================
echo.
echo This will install all required Python packages:
echo  - paramiko (SFTP/SSH connection)
echo  - schedule (task scheduling)
echo  - cryptography (secure credential storage)
echo.
pause

echo.
echo Installing packages...
echo.

py -m pip install --upgrade pip
py -m pip install -r requirements.txt

if %errorLevel% neq 0 (
    echo.
    echo =========================================
    echo ERROR: Installation failed!
    echo =========================================
    echo.
    echo Possible reasons:
    echo  1. Python is not installed
    echo  2. pip is not available
    echo  3. No internet connection
    echo.
    echo Try installing manually:
    echo   py -m pip install paramiko schedule cryptography
    echo.
    pause
    exit /b 1
)

echo.
echo =========================================
echo SUCCESS!
echo =========================================
echo.
echo All dependencies installed successfully!
echo.
echo Next steps:
echo  1. To build executable: run build_executable.bat
echo  2. To test directly: py sftp_monitor.py
echo.
pause
