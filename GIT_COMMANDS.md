# Git Commands Reference for SFTP Monitor Project

## Repository Status

Your Git repository is now initialized and all project files are committed!

**Commit ID:** da7f605  
**Branch:** master  
**Status:** Clean (no uncommitted changes)

---

## Common Git Commands

### Check Status
```bash
git status                  # See what's changed
git log --oneline          # View commit history
git log --graph --all      # Visual commit tree
```

### Make Changes
```bash
# After editing files:
git add .                  # Stage all changes
git add file.py            # Stage specific file
git commit -m "message"    # Commit with message

# Quick commit all changes:
git commit -am "message"   # Add + commit in one step
```

### View Changes
```bash
git diff                   # See unstaged changes
git diff --staged          # See staged changes
git diff HEAD~1            # Compare to previous commit
```

### Undo Changes
```bash
git checkout -- file.py    # Discard changes to file
git reset HEAD file.py     # Unstage file
git reset --hard HEAD      # Discard all changes (dangerous!)
git revert <commit-id>     # Create new commit that undoes changes
```

### Branching
```bash
git branch feature-name    # Create new branch
git checkout feature-name  # Switch to branch
git checkout -b new-branch # Create and switch in one step
git merge feature-name     # Merge branch into current
git branch -d feature-name # Delete branch
```

---

## Recommended Workflow

### 1. Before Making Changes
```bash
git status                 # Check current state
git pull                   # Get latest changes (if using remote)
```

### 2. While Working
```bash
# Make small, logical commits
git add specific_file.py
git commit -m "Add feature X"

# Or commit everything
git commit -am "Update configuration system"
```

### 3. Good Commit Messages
```bash
# Good examples:
git commit -m "Add disk space monitoring feature"
git commit -m "Fix connection timeout bug in SFTP class"
git commit -m "Update README with v2.0 features"

# Bad examples (avoid):
git commit -m "updates"
git commit -m "fix"
git commit -m "WIP"
```

---

## Files Currently Tracked

✅ **Source Code:**
- sftp_monitor.py
- SFTP_Monitor.spec
- requirements.txt

✅ **Scripts:**
- install_dependencies.bat
- build_executable.bat
- CLEANUP.bat
- START_HERE.bat

✅ **Documentation:**
- README.md
- ABOUT.txt
- .gitignore

✅ **Distribution:**
- dist/SFTP_Monitor.exe
- dist/README.txt

---

## Files Automatically Ignored (.gitignore)

These files are NOT tracked (and that's good!):
- `build/` - PyInstaller build cache
- `__pycache__/` - Python cache
- `*.log*` - Log files
- `config.json` - Generated configuration
- `reports/` - Generated reports
- `test_*.py` - Test files

---

## Setting Up Remote Repository (GitHub, GitLab, etc.)

### On GitHub/GitLab:
1. Create new repository (don't initialize with README)
2. Copy the repository URL

### Link Your Local Repo:
```bash
# Add remote
git remote add origin https://github.com/username/sftp-monitor.git

# Push your code
git push -u origin master

# Future pushes (after commits):
git push
```

---

## Useful Tips

### View File History
```bash
git log --follow sftp_monitor.py
git log -p sftp_monitor.py    # Show changes in each commit
```

### Tag Releases
```bash
git tag -a v2.0 -m "Version 2.0 - Full feature release"
git tag                        # List all tags
git push --tags               # Push tags to remote
```

### Stash Changes (Save work without committing)
```bash
git stash                      # Save current changes
git stash list                 # View stashed changes
git stash pop                  # Restore stashed changes
git stash drop                 # Delete stashed changes
```

### Compare Versions
```bash
git diff v1.0 v2.0             # Compare two tags/commits
git diff HEAD~3 HEAD           # Compare 3 commits ago to now
```

---

## Your Git Configuration

**User Name:** SHIVA  
**User Email:** shiva@sftp-monitor.local  
**Scope:** Local (this repository only)

### To Change User Info:
```bash
# For this repository only:
git config user.name "Your Name"
git config user.email "your.email@example.com"

# For all repositories (global):
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Emergency Commands

### Completely Reset to Last Commit
```bash
git reset --hard HEAD
git clean -fd                  # Remove untracked files
```

### Go Back to Previous Commit
```bash
git checkout <commit-id>       # Detached HEAD state
git checkout master            # Return to current
```

### Recover Deleted Commit
```bash
git reflog                     # Find lost commit
git checkout <commit-id>       # Restore it
```

---

## Next Steps

1. ✅ Git repository initialized
2. ✅ Initial commit created
3. ⏭️ Consider setting up remote repository (GitHub/GitLab)
4. ⏭️ Create tags for releases (v2.0, v2.1, etc.)
5. ⏭️ Use branches for new features

**Your project is now protected with version control!**
