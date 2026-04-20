# GitHub/GitLab Cloud Backup Setup Guide

## Current Status
✅ Git repository initialized
✅ Version v2.0 tagged
✅ Branches created (master, develop)
❌ Not yet linked to cloud (follow steps below)

---

## Option 1: GitHub Setup (Recommended)

### Step 1: Create GitHub Repository

1. Go to **https://github.com/new**
2. Fill in repository details:
   - **Repository name:** `SFTP-Monitor` (or your preferred name)
   - **Description:** "Automated SFTP file monitoring service with encryption, versioning, and auto-cleanup"
   - **Visibility:** Private (recommended for business code) or Public
   - **DO NOT** check "Initialize with README" (we already have one)
   - **DO NOT** add .gitignore or license (we have them)
3. Click **"Create repository"**

### Step 2: Link Your Local Repository

After creating the repository, GitHub will show commands. Use these:

```bash
# Add GitHub as remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/SFTP-Monitor.git

# Push all branches and tags
git push -u origin master
git push origin develop
git push --tags

# Verify remote is set
git remote -v
```

### Step 3: Set Up Authentication

**If using HTTPS (easier):**
- GitHub will prompt for username/password
- Use a **Personal Access Token** instead of password:
  1. Go to GitHub Settings → Developer settings → Personal access tokens
  2. Generate new token (classic)
  3. Select scopes: `repo` (full control of private repositories)
  4. Copy the token
  5. Use it as password when pushing

**If using SSH (more secure, one-time setup):**
```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
# Paste the key content

# Change remote to SSH
git remote set-url origin git@github.com:USERNAME/SFTP-Monitor.git
```

---

## Option 2: GitLab Setup

### Step 1: Create GitLab Repository

1. Go to **https://gitlab.com/projects/new**
2. Choose "Create blank project"
3. Fill in:
   - **Project name:** `SFTP-Monitor`
   - **Visibility:** Private or Public
   - **DO NOT** check "Initialize repository with a README"
4. Click **"Create project"**

### Step 2: Link Your Local Repository

```bash
# Add GitLab as remote (replace USERNAME)
git remote add origin https://gitlab.com/USERNAME/SFTP-Monitor.git

# Push everything
git push -u origin master
git push origin develop
git push --tags

# Verify
git remote -v
```

---

## Option 3: Azure DevOps / Other Platforms

### Azure DevOps
```bash
git remote add origin https://dev.azure.com/ORGANIZATION/PROJECT/_git/SFTP-Monitor
git push -u origin master
git push --tags
```

### Bitbucket
```bash
git remote add origin https://bitbucket.org/USERNAME/sftp-monitor.git
git push -u origin master
git push --tags
```

---

## Quick Setup Script

Save this as `setup_github.bat` in your project folder:

```batch
@echo off
echo ========================================
echo GitHub Remote Setup
echo ========================================
echo.
set /p USERNAME="Enter your GitHub username: "
set /p REPONAME="Enter repository name [SFTP-Monitor]: "
if "%REPONAME%"=="" set REPONAME=SFTP-Monitor

echo.
echo Adding remote: https://github.com/%USERNAME%/%REPONAME%.git
git remote add origin https://github.com/%USERNAME%/%REPONAME%.git

echo.
echo Pushing to GitHub...
git push -u origin master
git push origin develop
git push --tags

echo.
echo ========================================
echo Done! Check https://github.com/%USERNAME%/%REPONAME%
echo ========================================
pause
```

---

## Verify Cloud Backup

After pushing, verify everything is uploaded:

```bash
# Check remote connection
git remote -v

# Should show:
# origin  https://github.com/USERNAME/SFTP-Monitor.git (fetch)
# origin  https://github.com/USERNAME/SFTP-Monitor.git (push)

# View all branches (including remote)
git branch -a

# View tags
git tag
```

---

## Daily Workflow After Setup

### Making Changes
```bash
# 1. Make sure you're on develop branch
git checkout develop

# 2. Make your changes to files

# 3. Stage and commit
git add .
git commit -m "Add new feature X"

# 4. Push to cloud
git push
```

### Creating a New Feature
```bash
# Create feature branch from develop
git checkout develop
git checkout -b feature/new-feature-name

# Work on feature, commit changes
git add .
git commit -m "Implement feature"

# Push feature branch to cloud
git push -u origin feature/new-feature-name

# When ready, merge to develop
git checkout develop
git merge feature/new-feature-name
git push
```

### Creating a New Release
```bash
# Merge develop into master
git checkout master
git merge develop

# Create release tag
git tag -a v2.1 -m "Version 2.1 - Description of changes"

# Push everything
git push
git push --tags
```

---

## Troubleshooting

### Error: "remote origin already exists"
```bash
# Remove existing remote
git remote remove origin

# Add new one
git remote add origin YOUR_URL
```

### Error: "Permission denied (publickey)"
- Set up SSH key (see GitHub Setup, Step 3)
- Or use HTTPS with token instead

### Error: "Updates were rejected"
```bash
# Pull latest changes first
git pull origin master --rebase

# Then push
git push
```

### Large File Warning
If your .exe is very large (>100MB):
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.exe"
git add .gitattributes
git commit -m "Configure Git LFS"
git push
```

---

## Benefits of Cloud Backup

✅ **Disaster Recovery** - Code safe even if your PC fails
✅ **Access Anywhere** - Clone to any computer
✅ **Collaboration** - Share with team members
✅ **History** - Full version history in the cloud
✅ **Releases** - Download specific versions anytime
✅ **Issues/Wiki** - Use GitHub/GitLab features

---

## Next Steps

1. ✅ Choose platform (GitHub recommended)
2. ✅ Create repository on platform
3. ✅ Run commands from Step 2 above
4. ✅ Verify by visiting repository URL
5. ✅ Start using develop branch for changes

**Your project will be safely backed up in the cloud!**
