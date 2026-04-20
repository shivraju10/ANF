@echo off
color 0B
echo ========================================
echo GitHub Remote Setup for SFTP Monitor
echo ========================================
echo.
echo This will link your local Git repository to GitHub for cloud backup.
echo.
echo Prerequisites:
echo  1. GitHub account created
echo  2. New repository created on GitHub (empty, no README)
echo  3. GitHub username and repository name ready
echo.
pause

:input
echo.
set /p USERNAME="Enter your GitHub username: "
if "%USERNAME%"=="" (
    echo Error: Username cannot be empty!
    goto input
)

set /p REPONAME="Enter repository name [SFTP-Monitor]: "
if "%REPONAME%"=="" set REPONAME=SFTP-Monitor

echo.
echo ========================================
echo Configuration:
echo ========================================
echo  Username: %USERNAME%
echo  Repository: %REPONAME%
echo  URL: https://github.com/%USERNAME%/%REPONAME%.git
echo.
choice /C YN /M "Is this correct"
if errorlevel 2 goto input

echo.
echo ========================================
echo Step 1: Adding Remote
echo ========================================
git remote add origin https://github.com/%USERNAME%/%REPONAME%.git
if %errorLevel% neq 0 (
    echo.
    echo Remote 'origin' already exists. Removing and re-adding...
    git remote remove origin
    git remote add origin https://github.com/%USERNAME%/%REPONAME%.git
)
echo ✓ Remote added successfully

echo.
echo ========================================
echo Step 2: Pushing Master Branch
echo ========================================
git push -u origin master
if %errorLevel% neq 0 (
    echo.
    echo ERROR: Failed to push master branch!
    echo.
    echo Common reasons:
    echo  1. Repository name is wrong
    echo  2. Authentication failed (need Personal Access Token)
    echo  3. Repository is not empty on GitHub
    echo.
    echo To get a Personal Access Token:
    echo  1. Go to GitHub Settings
    echo  2. Developer settings → Personal access tokens
    echo  3. Generate new token (classic)
    echo  4. Select 'repo' scope
    echo  5. Use token as password when prompted
    echo.
    pause
    exit /b 1
)
echo ✓ Master branch pushed

echo.
echo ========================================
echo Step 3: Pushing Develop Branch
echo ========================================
git push origin develop
if %errorLevel% neq 0 (
    echo ✗ Failed to push develop branch
) else (
    echo ✓ Develop branch pushed
)

echo.
echo ========================================
echo Step 4: Pushing Tags
echo ========================================
git push --tags
if %errorLevel% neq 0 (
    echo ✗ Failed to push tags
) else (
    echo ✓ Tags pushed (including v2.0)
)

echo.
echo ========================================
echo Verification
echo ========================================
git remote -v
echo.
git branch -a
echo.

echo ========================================
echo SUCCESS!
echo ========================================
echo.
echo Your repository is now backed up to the cloud!
echo.
echo View it at: https://github.com/%USERNAME%/%REPONAME%
echo.
echo Next steps:
echo  1. Visit the URL above to verify
echo  2. Use 'git push' after commits to sync
echo  3. Work on 'develop' branch for new features
echo  4. See BRANCHING_STRATEGY.md for workflow
echo.
pause
