@echo off
echo =========================================
echo Cleaning Up Development Files
echo =========================================
echo.
echo This will delete:
echo  - Test files (test_*.py)
echo  - Python cache (__pycache__)
echo  - Generated config.json
echo  - Log files (*.log*)
echo  - Build cache (build folder)
echo.
echo The following will be KEPT:
echo  - Source code (sftp_monitor.py)
echo  - Build script (build_executable.bat)
echo  - Dependencies list (requirements.txt)
echo  - Documentation (README.md, ABOUT.txt)
echo  - PyInstaller spec (SFTP_Monitor.spec)
echo  - Final executable in dist\ folder
echo.
pause

echo.
echo Cleaning...
echo.

REM Delete test files
if exist test_*.py (
    del /f /q test_*.py
    echo ✓ Deleted test files
)

REM Delete Python cache
if exist __pycache__ (
    rmdir /s /q __pycache__
    echo ✓ Deleted Python cache
)

REM Delete config.json (will be auto-generated on first run)
if exist config.json (
    del /f /q config.json
    echo ✓ Deleted config.json
)

REM Delete log files
if exist *.log (
    del /f /q *.log*
    echo ✓ Deleted log files
)

REM Delete build cache
if exist build (
    rmdir /s /q build
    echo ✓ Deleted build cache
)

REM Clean dist folder except executable and essential files
if exist dist (
    if exist dist\*.log (
        del /f /q dist\*.log*
        echo ✓ Cleaned dist folder logs
    )
    if exist dist\config.json (
        del /f /q dist\config.json
        echo ✓ Cleaned dist folder config
    )
    if exist dist\__pycache__ (
        rmdir /s /q dist\__pycache__
        echo ✓ Cleaned dist folder cache
    )
)

echo.
echo =========================================
echo Cleanup Complete!
echo =========================================
echo.
echo Your workspace is now clean and ready for:
echo  - Fresh build (run build_executable.bat)
echo  - Git commit (no temp files)
echo  - Distribution (dist folder is clean)
echo.
pause
