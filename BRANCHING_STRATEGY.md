# Branching Strategy for SFTP Monitor

## Overview

This project uses **Git Flow** branching strategy for organized development and stable releases.

---

## Branch Structure

```
master              Production-ready code (stable releases only)
  ├── v2.0          Tagged releases
  ├── v2.1
  └── v3.0
  
develop             Main development branch (latest features)
  ├── feature/      New features
  ├── bugfix/       Bug fixes
  └── hotfix/       Urgent production fixes
```

---

## Permanent Branches

### `master` - Production Branch
- **Purpose:** Production-ready, stable code only
- **Protected:** Never commit directly to master
- **Updates:** Only via merge from develop or hotfix
- **Tags:** All releases tagged here (v2.0, v2.1, etc.)

**Rules:**
- ✅ Always deployable
- ✅ Tagged with version numbers
- ✅ Each commit represents a release
- ❌ No direct commits
- ❌ No experimental code

### `develop` - Development Branch
- **Purpose:** Integration branch for features
- **Active:** Main working branch
- **Updates:** Merges from feature/bugfix branches
- **State:** Latest development version

**Rules:**
- ✅ Working code only (must compile/run)
- ✅ Integration of new features
- ✅ Pre-release testing
- ❌ No broken code
- ❌ No experimental/WIP code

---

## Temporary Branches

### Feature Branches: `feature/*`

**When to use:** Adding new functionality

**Naming convention:**
```
feature/credential-encryption
feature/log-rotation
feature/email-notifications
feature/multi-server-support
```

**Workflow:**
```bash
# Create from develop
git checkout develop
git checkout -b feature/new-feature-name

# Work on feature
# ... make changes ...
git add .
git commit -m "Implement feature X"

# Push to remote (for backup/collaboration)
git push -u origin feature/new-feature-name

# When complete, merge to develop
git checkout develop
git merge feature/new-feature-name

# Push develop
git push

# Delete feature branch
git branch -d feature/new-feature-name
git push origin --delete feature/new-feature-name
```

### Bugfix Branches: `bugfix/*`

**When to use:** Fixing bugs in develop

**Naming convention:**
```
bugfix/connection-timeout
bugfix/file-corruption
bugfix/memory-leak
```

**Workflow:**
```bash
# Same as feature branches
git checkout develop
git checkout -b bugfix/fix-description

# Fix bug and test
git commit -m "Fix: description of bug"

# Merge back to develop
git checkout develop
git merge bugfix/fix-description
git push

# Delete branch
git branch -d bugfix/fix-description
```

### Hotfix Branches: `hotfix/*`

**When to use:** Urgent fixes for production (master)

**Naming convention:**
```
hotfix/v2.0.1
hotfix/critical-security-fix
```

**Workflow:**
```bash
# Create from master (not develop!)
git checkout master
git checkout -b hotfix/v2.0.1

# Fix critical issue
git commit -m "Hotfix: critical issue description"

# Merge to BOTH master AND develop
git checkout master
git merge hotfix/v2.0.1
git tag -a v2.0.1 -m "Hotfix: description"
git push --tags

git checkout develop
git merge hotfix/v2.0.1

git push --all

# Delete hotfix branch
git branch -d hotfix/v2.0.1
```

---

## Complete Workflow Examples

### Example 1: Adding a New Feature

```bash
# 1. Start from latest develop
git checkout develop
git pull

# 2. Create feature branch
git checkout -b feature/email-notifications

# 3. Implement feature
# ... edit files ...
git add .
git commit -m "Add email notification system"
git commit -m "Add SMTP configuration"
git commit -m "Add notification templates"

# 4. Push for backup
git push -u origin feature/email-notifications

# 5. Merge to develop when ready
git checkout develop
git merge feature/email-notifications

# 6. Test on develop
# ... run tests ...

# 7. Push to cloud
git push

# 8. Cleanup
git branch -d feature/email-notifications
git push origin --delete feature/email-notifications
```

### Example 2: Creating a New Release

```bash
# 1. Ensure develop is ready
git checkout develop
git pull
# ... run all tests ...

# 2. Merge to master
git checkout master
git merge develop

# 3. Create release tag
git tag -a v2.1 -m "Version 2.1 - Email Notifications

New features:
- Email notification system
- SMTP configuration
- Custom notification templates

Bug fixes:
- Fixed connection timeout issue
- Improved error handling"

# 4. Push everything
git push
git push --tags

# 5. Update develop
git checkout develop
git merge master
git push
```

### Example 3: Emergency Production Fix

```bash
# 1. Create hotfix from master
git checkout master
git checkout -b hotfix/v2.0.1

# 2. Fix the critical bug
# ... make minimal changes ...
git commit -m "Hotfix: Fix critical security vulnerability"

# 3. Merge to master
git checkout master
git merge hotfix/v2.0.1

# 4. Tag hotfix release
git tag -a v2.0.1 -m "Hotfix: Security vulnerability patch"

# 5. Merge to develop too
git checkout develop
git merge hotfix/v2.0.1

# 6. Push everything
git push --all
git push --tags

# 7. Cleanup
git branch -d hotfix/v2.0.1
```

---

## Version Numbering (Semantic Versioning)

Format: `vMAJOR.MINOR.PATCH`

- **MAJOR** (v3.0): Breaking changes, major rewrites
- **MINOR** (v2.1): New features, backward compatible
- **PATCH** (v2.0.1): Bug fixes, hotfixes

Examples:
- `v2.0` - Initial full release
- `v2.1` - Added email notifications
- `v2.1.1` - Fixed email bug
- `v3.0` - Complete rewrite with breaking changes

---

## Current Branch Status

### Active Branches
- ✅ `master` - v2.0 (stable, production-ready)
- ✅ `develop` - Latest development (currently same as master)

### Available for Use
- `feature/*` - Create as needed for new features
- `bugfix/*` - Create as needed for bug fixes
- `hotfix/*` - Create only for production emergencies

---

## Quick Reference Commands

```bash
# Switch branches
git checkout master          # Production
git checkout develop         # Development

# Create feature
git checkout -b feature/name

# Create bugfix
git checkout -b bugfix/name

# Create hotfix
git checkout -b hotfix/vX.Y.Z

# View all branches
git branch -a

# Delete branch (local)
git branch -d branch-name

# Delete branch (remote)
git push origin --delete branch-name

# View current branch
git branch

# View branch history
git log --graph --all --oneline
```

---

## Best Practices

### Commit Messages
```bash
# Good
git commit -m "Add: Email notification feature"
git commit -m "Fix: Connection timeout in SFTP class"
git commit -m "Update: README with new features"
git commit -m "Refactor: Cleanup ConfigManager code"

# Bad
git commit -m "updates"
git commit -m "fix bug"
git commit -m "WIP"
```

### Branch Naming
- ✅ Use lowercase with hyphens: `feature/multi-server`
- ✅ Be descriptive: `bugfix/connection-timeout`
- ✅ Include issue numbers if applicable: `feature/123-add-logging`
- ❌ Avoid: `my-branch`, `test`, `temp`

### Before Merging
1. ✅ Test thoroughly
2. ✅ Update documentation
3. ✅ Resolve conflicts
4. ✅ Review changes
5. ✅ Run cleanup script

---

## Integration with Cloud (GitHub/GitLab)

### Pull Requests / Merge Requests
When working with a team:

1. Push feature branch to remote
2. Create Pull Request on GitHub
3. Request code review
4. Make changes if needed
5. Merge when approved
6. Delete branch

### Protected Branches
Configure on GitHub/GitLab:
- Protect `master` - require reviews, no force push
- Protect `develop` - require tests to pass

---

## Troubleshooting

### Merge Conflicts
```bash
# When merge fails with conflicts
git status                    # See conflicted files
# ... edit files to resolve ...
git add .
git commit -m "Resolve merge conflicts"
```

### Undo Last Commit (not pushed)
```bash
git reset --soft HEAD~1       # Keep changes
git reset --hard HEAD~1       # Discard changes
```

### See Branch Differences
```bash
git diff master develop       # Compare branches
git log master..develop       # Commits in develop not in master
```

---

## Summary

1. **Work on `develop`** for all new development
2. **Use feature branches** for larger features
3. **Merge to `master`** only for releases
4. **Tag all releases** on master (v2.0, v2.1, etc.)
5. **Use hotfix branches** for production emergencies
6. **Push regularly** to cloud backup

**Your workflow is now organized and professional!**
