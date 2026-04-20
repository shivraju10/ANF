# SFTP File Monitor - Version 2.0

Standalone Windows executable that monitors SFTP folders and downloads files automatically with advanced features.

**NO Python, NO dependencies, NO installation required!**

---

## ✨ NEW in Version 2.0

### 🔒 **Encrypted Credentials**
- Passwords encrypted using Fernet (AES-128)
- Machine-specific encryption key
- Credentials stored in `config.json` (auto-generated)

### 📊 **Daily Summary Reports**
- Automatic daily reports in `reports\` folder
- Success rates, error logs, disk space status
- Generated at midnight + on shutdown

### 🗂️ **Auto-Cleanup Old Files**
- Removes files older than 30 days from `OldVer\` folders
- Prevents disk space issues
- Configurable retention period

### 💾 **Disk Space Monitoring**
- Checks free space before downloads (minimum: 5GB)
- Warnings logged when space is low
- Included in daily summaries

### 🔌 **Connection Keep-Alive**
- Maintains persistent SFTP connection
- Reduces overhead from reconnections
- 30-second keep-alive interval

### ⏱️ **Connection Timeout Management**
- Configurable timeout (default: 30 seconds)
- Prevents hanging on network issues
- Graceful failure handling

### 📝 **Log Rotation**
- Automatic rotation at 10MB per file
- Keeps 5 backup logs
- Prevents unlimited log growth

### ⚙️ **External Configuration**
- All settings in `config.json`
- **NO REBUILD NEEDED** to change settings!
- Edit config and restart service

---

## 🚀 For New PC (Zero Installation)

### Just Copy and Run:

1. **Copy `dist` folder** to any Windows PC
2. **Double-click `SFTP_Monitor.exe`**
3. **Minimize the window**
4. Done!

The executable works on any Windows 7/8/10/11 (64-bit) PC without any setup.

---

## 📁 Folder Structure

### For Users (Deployment):
```
dist\
├── SFTP_Monitor.exe  ⭐ Run this! (14 MB - Everything included)
└── README.txt        📖 Simple instructions
```

### For Developers (Source & Build):
```
D:\VS_Code\SFTP_Monitor\
├── dist\                       - Final executable (give this to users)
├── sftp_monitor.py             - Source code
├── requirements.txt            - Python dependencies
├── install_dependencies.bat    - One-click dependency installer ⭐
├── build_executable.bat        - Rebuild script
├── CLEANUP.bat                 - Clean temp files ⭐
├── SFTP_Monitor.spec           - PyInstaller configuration
├── README.md                   - This file
└── ABOUT.txt                   - Complete feature documentation
```

---

## 🚀 Quick Start for Developers

### 1️⃣ Install Dependencies (One Click!)
```
Double-click: install_dependencies.bat
```
This will automatically install:
- paramiko (SFTP/SSH)
- schedule (task scheduling)
- cryptography (encryption)

### 2️⃣ Build Executable
```
Double-click: build_executable.bat
```

### 3️⃣ Clean Workspace
```
Double-click: CLEANUP.bat
```
Removes test files, cache, logs, and build artifacts.

---

## 🔧 Configuration & Settings

### NEW: No Rebuild Required! 🎉

Settings are now in `config.json` (auto-created on first run).

### To Change Settings:

1. **Stop** the service (Ctrl+C or close window)
2. **Edit** `config.json`:
   ```json
   {
     "sftp": {
       "host": "sftp.natcoglobal.com",
       "port": 222,
       "username": "AbercrombieLAX",
       "password_encrypted": "[AUTO-ENCRYPTED]",
       "connection_timeout": 30,
       "keepalive_interval": 30
     },
     "monitoring": {
       "interval_minutes": 1,
       "min_disk_space_gb": 5
     },
     "maintenance": {
       "old_version_retention_days": 30,
       "cleanup_enabled": true,
       "daily_summary_enabled": true
     }
   }
   ```
3. **Restart** SFTP_Monitor.exe
4. Done! No rebuild needed!

### For Source Code Changes:

1. **Edit** `sftp_monitor.py`
2. **Rebuild** executable:
   ```
   Double-click: build_executable.bat
   ```
3. **New executable** appears in `dist\` folder
4. **Copy `dist` folder** to target PCs

---

## 💡 How It Works

### On Any Windows PC:

1. **Double-click** `SFTP_Monitor.exe`
2. Window opens showing:
   ```
   2026-04-20 14:08:16 - SFTP Monitor Service v2.0 Starting...
   2026-04-20 14:08:19 - Successfully connected to SFTP server (with keep-alive enabled)
   2026-04-20 14:08:19 - Starting monitoring cycle
   2026-04-20 14:08:20 - Disk space OK: 48.52GB free
   ```
3. **Minimize** the window (keep it running)
4. Every 1 minute automatically:
   - Checks disk space availability
   - Connects to SFTP server (or reuses existing connection)
   - Checks remote folders
   - Downloads new files
   - Moves old versions to OldVer\ folders
   - Deletes from remote
   - Cleans up files older than 30 days
   - Logs all activity
5. At midnight:
   - Generates daily summary report

### To Stop:

Close the window or press Ctrl+C (generates final summary before exit)

---

## 📊 What Gets Monitored

**SFTP Server:** `sftp.natcoglobal.com:222`

**Remote Folders → Local Folders:**
- `ScriptTest/XML FILES` → `C:\A&F\XML FILES`
- `ScriptTest/EXCEL FILES` → `C:\A&F\EXCEL FILES`

**Check Interval:** Every 1 minute

**File Handling:**
- Downloads all files found
- Deletes from remote after successful download
- **Automatic Version Management:**
  - Detects updated files by timestamp (e.g., `China_Hang_Tag_131260041_04-18-2026_04-36-13.xls`)
  - When newer version found (e.g., `China_Hang_Tag_131260041_04-18-2026_04-40-22.xls`):
    - Moves old version to `OldVer\` subdirectory
    - Downloads latest version to main folder
    - **Auto-deletes files older than 30 days from OldVer\**
  - Works for both `.xls` and `.xml` files
- Renames non-versioned duplicates with timestamp (e.g., `file_20251117_143052.xml`)
- **Disk space check before each download (minimum: 5GB free)**
- **Connection keep-alive to reduce overhead**

---

## 📝 Logs & Reports

### Real-time Logs

**Log files:** `sftp_monitor.log` (with automatic rotation)

**Example log:**
```
2026-04-20 14:08:19 - Starting monitoring cycle
2026-04-20 14:08:20 - Disk space OK: 48.52GB free
2026-04-20 14:08:20 - Found 4 file(s) in ScriptTest/XML FILES
2026-04-20 14:08:21 - Found 1 existing version(s) of China_Hang_Tag_131260041.xml
2026-04-20 14:08:21 - Newer version detected: 04-18-2026_04-40-22 > 04-18-2026_04-36-13
2026-04-20 14:08:21 - Moved old version: China_Hang_Tag_131260041_04-18-2026_04-36-13.xml -> OldVer/
2026-04-20 14:08:22 - Downloaded: China_Hang_Tag_131260041_04-18-2026_04-40-22.xml -> C:\A&F\XML FILES\
2026-04-20 14:08:22 - Deleted from remote: China_Hang_Tag_131260041_04-18-2026_04-40-22.xml
2026-04-20 14:08:23 - Cleaned up 3 old version(s) from C:\A&F\XML FILES
2026-04-20 14:08:25 - Monitoring cycle complete. Total: 4 files
```

**Log rotation:** Logs automatically rotate at 10MB, keeping 5 backups.

### Daily Summary Reports 📊

**Location:** `reports\` folder

**Filename:** `YYYY-MM-DD_summary.txt`

**Generated:** Daily at midnight + when service stops

**Example Summary:**
```
======================================================================
SFTP Monitor Daily Summary - 2026-04-20
======================================================================

Files Downloaded: 47
Files Failed: 2
Folders Checked: 48
Success Rate: 95.92%

Errors (2): 
======================================================================
1. Download failed: ScriptTest/XML FILES/test.xml - Connection timeout
2. Low disk space: 3.24GB

Disk Space Status:
======================================================================
C:\A&F\XML FILES:
  Free: 48.52GB / 500.00GB (9.7% free)
C:\A&F\EXCEL FILES:
  Free: 48.52GB / 500.00GB (9.7% free)

======================================================================
Report generated at: 2026-04-21 00:01:15
```

---

## 🛠️ Maintenance & Development

### Install Dependencies (One Click!)
```
Double-click: install_dependencies.bat
```
Automatically installs all required Python packages:
- paramiko (SFTP/SSH connection)
- schedule (task scheduling)  
- cryptography (credential encryption)

### Clean Temporary Files
```
Double-click: CLEANUP.bat
```
Removes all development artifacts:
- Test files (test_*.py)
- Python cache (__pycache__)
- Generated config.json
- Log files (*.log*)
- Build cache (build folder)

Workspace will be clean for fresh builds or Git commits.

### Rebuild Executable
```
Double-click: build_executable.bat
```
Creates new `SFTP_Monitor.exe` in `dist\` folder.

### Build Requirements
- Python 3.7+
- Dependencies installed (use install_dependencies.bat)
- PyInstaller: Installed automatically with dependencies

---

## ✨ Benefits

✅ **Portable** - Works on any Windows PC
✅ **No Installation** - Just copy and run
✅ **No Dependencies** - Everything bundled (~14 MB)
✅ **Universal** - Windows 7/8/10/11 (64-bit)
✅ **Simple** - Double-click to start
✅ **Automatic** - Monitors every 1 minute
✅ **Reliable** - Logs all activity, daily reports
✅ **Secure** - Encrypted SFTP connection + encrypted credentials
✅ **Configurable** - Edit config.json without rebuilding
✅ **Smart** - Auto-cleanup, disk space monitoring, version management

---

## 🎯 Quick Reference

| Task | Action |
|------|--------|
| **Install dependencies** | Run `install_dependencies.bat` |
| **Build executable** | Run `build_executable.bat` |
| **Clean workspace** | Run `CLEANUP.bat` |
| **Deploy to new PC** | Copy `dist` folder, run `SFTP_Monitor.exe` |
| **Start monitoring** | Double-click `SFTP_Monitor.exe` |
| **Stop monitoring** | Close window or Ctrl+C |
| **View logs** | Open `sftp_monitor.log` |
| **View daily reports** | Check `reports\` folder |
| **Change settings** | Edit `config.json`, restart service |
| **Change code** | Edit `sftp_monitor.py`, rebuild |
| **Clean temp files** | Run `CLEANUP.bat` |

---

## 📦 Distribution

**Give to users:** Just the `dist` folder
**No setup needed:** Users just double-click the .exe

---

**The `dist` folder is ready to copy to any Windows PC and run immediately!**
