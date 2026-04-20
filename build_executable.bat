@echo off
echo =========================================
echo Building Standalone Executable
echo =========================================
echo.
echo This will create an .exe that works on ANY Windows PC
echo (No Python or dependencies needed!)
echo.

echo Killing any running instances...
taskkill /F /IM SFTP_Monitor.exe >NUL 2>&1
taskkill /F /IM python.exe >NUL 2>&1
timeout /t 2 >nul

echo.
echo Deleting old executable...
del /f /q "dist\SFTP_Monitor.exe" >NUL 2>&1
timeout /t 1 >nul

echo.
echo Building... this may take a few minutes...
echo.

cd /d "%~dp0"

py -m PyInstaller --onefile --console --name "SFTP_Monitor" --icon=NONE ^
  --hidden-import=paramiko ^
  --hidden-import=schedule ^
  --hidden-import=cryptography ^
  --hidden-import=bcrypt ^
  --hidden-import=pynacl ^
  --hidden-import=invoke ^
  sftp_monitor.py --noconfirm

if %errorLevel% neq 0 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo =========================================
echo SUCCESS!
echo =========================================
echo.
echo Executable created: dist\SFTP_Monitor.exe
echo.
echo This .exe file:
echo  - Contains Python and all dependencies
echo  - Works on any Windows PC
echo  - No installation needed
echo.
echo Next steps:
echo  1. Go to "dist" folder
echo  2. Copy SFTP_Monitor.exe to new PC
echo  3. Double-click to run!
echo.
pause
