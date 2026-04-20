@echo off
color 0A
echo ================================================================================
echo              SFTP MONITOR v2.0 - DEVELOPER QUICK START GUIDE
echo ================================================================================
echo.
echo Welcome! This guide will help you get started in 3 easy steps.
echo.
echo ================================================================================
echo STEP 1: Install Dependencies
echo ================================================================================
echo.
echo You need to install Python packages first.
echo.
choice /C YN /M "Do you want to install dependencies now"

if errorlevel 2 goto :skip_install
if errorlevel 1 goto :install

:install
echo.
echo Installing dependencies...
call install_dependencies.bat
goto :step2

:skip_install
echo.
echo Skipped installation. Run install_dependencies.bat manually later.
echo.

:step2
echo.
echo ================================================================================
echo STEP 2: Build Executable
echo ================================================================================
echo.
echo This will create SFTP_Monitor.exe in the dist\ folder.
echo.
choice /C YN /M "Do you want to build the executable now"

if errorlevel 2 goto :skip_build
if errorlevel 1 goto :build

:build
echo.
echo Building executable...
call build_executable.bat
goto :step3

:skip_build
echo.
echo Skipped build. Run build_executable.bat manually later.
echo.

:step3
echo.
echo ================================================================================
echo STEP 3: What's Next?
echo ================================================================================
echo.
echo You can now:
echo.
echo   [1] Test the Python script:
echo       py sftp_monitor.py
echo.
echo   [2] Run the built executable:
echo       dist\SFTP_Monitor.exe
echo.
echo   [3] Clean up temporary files:
echo       CLEANUP.bat
echo.
echo   [4] Read the documentation:
echo       README.md (for developers)
echo       ABOUT.txt (feature documentation)
echo.
echo ================================================================================
echo USEFUL FILES IN THIS FOLDER:
echo ================================================================================
echo.
echo   install_dependencies.bat  - Install Python packages (one-click)
echo   build_executable.bat      - Build standalone .exe file
echo   CLEANUP.bat               - Remove temp files and cache
echo   sftp_monitor.py           - Main source code
echo   config.json               - Auto-generated settings (edit to configure)
echo   requirements.txt          - List of Python dependencies
echo   README.md                 - Full developer documentation
echo   ABOUT.txt                 - Complete feature list
echo.
echo ================================================================================
echo                              SETUP COMPLETE!
echo ================================================================================
echo.
echo For support or questions, check:
echo  - README.md for detailed instructions
echo  - ABOUT.txt for feature documentation
echo.
pause
