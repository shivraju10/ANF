================================================================================
                SFTP FILE MONITOR - VERSION 2.0 - PORTABLE
================================================================================

NO INSTALLATION NEEDED!
Works on ANY Windows PC without Python or any dependencies.

NEW in v2.0:
 🔒 Encrypted credentials (stored in config.json)
 📊 Daily summary reports (in reports\ folder)
 🗂️ Auto-cleanup old files after 30 days
 💾 Disk space monitoring
 🔌 Connection keep-alive
 📝 Log rotation (no more huge log files!)
 ⚙️ Easy configuration (edit config.json - no rebuild needed!)

================================================================================
HOW TO USE
================================================================================

FIRST TIME:
1. Copy this entire folder to any Windows PC
2. Double-click: SFTP_Monitor.exe
3. config.json will be created automatically with default settings
4. A window opens showing monitoring status - minimize it

TO STOP:
 - Close the window, or
 - Press Ctrl+C

TO CHANGE SETTINGS:
1. Stop the service
2. Edit config.json (see below)
3. Restart SFTP_Monitor.exe
4. NO REBUILD NEEDED!

That's it!

================================================================================
WHAT IT DOES
================================================================================

Every 1 minute:
  ✓ Checks disk space (minimum 5GB required)
  ✓ Connects to sftp.natcoglobal.com:222 (persistent connection)
  ✓ Checks folder: ScriptTest/XML FILES
  ✓ Checks folder: ScriptTest/EXCEL FILES
  ✓ Downloads any files found
  ✓ Moves old versions to OldVer\ subdirectory
  ✓ Deletes files from SFTP after successful download
  ✓ Cleans up files older than 30 days from OldVer\ folders

Downloaded files go to:
  - XML files   -> C:\A&F\XML FILES
  - Excel files -> C:\A&F\EXCEL FILES
  - Old versions -> OldVer\ subdirectory (auto-cleaned after 30 days)

File versioning example:
  - First:  China_Hang_Tag_131260041_04-18-2026_04-36-13.xls
  - Newer:  China_Hang_Tag_131260041_04-18-2026_04-40-22.xls
  - Old version automatically moved to OldVer\

At midnight:
  ✓ Generates daily summary report in reports\ folder

================================================================================
CONFIGURATION (config.json)
================================================================================

After first run, edit config.json to change settings:

{
  "sftp": {
    "host": "sftp.natcoglobal.com",
    "port": 222,
    "username": "AbercrombieLAX",
    "password_encrypted": "[AUTO-ENCRYPTED - don't edit]",
    "connection_timeout": 30,
    "keepalive_interval": 30
  },
  "monitoring": {
    "interval_minutes": 1,          ← Change check frequency
    "min_disk_space_gb": 5          ← Minimum free space required
  },
  "maintenance": {
    "old_version_retention_days": 30,  ← Auto-cleanup age
    "cleanup_enabled": true,            ← Enable/disable cleanup
    "daily_summary_enabled": true       ← Enable/disable reports
  }
}

IMPORTANT: To change password, stop service, delete config.json,
           edit sftp_monitor.py source, then rebuild executable.

================================================================================
VIEW ACTIVITY
================================================================================

REAL-TIME LOGS:
  File: sftp_monitor.log (rotates at 10MB, keeps 5 backups)

Example:
  2026-04-20 14:08:19 - SFTP Monitor Service v2.0 Starting...
  2026-04-20 14:08:20 - Successfully connected (with keep-alive enabled)
  2026-04-20 14:08:20 - Disk space OK: 48.52GB free
  2026-04-20 14:08:20 - Found 4 file(s) in ScriptTest/XML FILES
  2026-04-20 14:08:21 - Newer version detected: 04-40-22 > 04-36-13
  2026-04-20 14:08:21 - Moved old version to OldVer/
  2026-04-20 14:08:22 - Downloaded: China_Hang_Tag_131260041_04-40-22.xls
  2026-04-20 14:08:23 - Cleaned up 3 old version(s)
  2026-04-20 14:08:25 - Monitoring cycle complete. Total: 4 files

DAILY SUMMARY REPORTS:
  Location: reports\YYYY-MM-DD_summary.txt
  
Example report includes:
  - Files downloaded today
  - Success/failure rates
  - Error logs
  - Disk space status
  - Generated daily at midnight

================================================================================
FOLDER STRUCTURE
================================================================================

After running:

dist\
├── SFTP_Monitor.exe       ⭐ The program
├── config.json            📝 Settings (auto-created, editable)
├── sftp_monitor.log       📋 Current log
├── sftp_monitor.log.1     📋 Rotated log backup
├── ...
└── reports\               📊 Daily summaries
    ├── 2026-04-19_summary.txt
    └── 2026-04-20_summary.txt

C:\A&F\XML FILES\
├── [Current XML files]
└── OldVer\                🗂️ Old versions (auto-cleaned after 30 days)

C:\A&F\EXCEL FILES\
├── [Current Excel files]
└── OldVer\                🗂️ Old versions (auto-cleaned after 30 days)

================================================================================
TROUBLESHOOTING
================================================================================

Files not downloading:
  ✓ Check sftp_monitor.log for errors
  ✓ Check network connection
  ✓ Verify SFTP server is accessible
  ✓ Check disk space (minimum 5GB required)
  ✓ Review daily summary in reports\ folder

Can't find downloads:
  ✓ Look in: C:\A&F\XML FILES
  ✓ Look in: C:\A&F\EXCEL FILES
  ✓ Old versions moved to OldVer\ subdirectories

Window closes immediately:
  ✓ Check if antivirus blocked the .exe
  ✓ Run as administrator (right-click -> Run as administrator)
  ✓ Check sftp_monitor.log for startup errors

Low disk space warning:
  ✓ Free up space on C:\ drive
  ✓ OldVer\ folders automatically cleaned after 30 days
  ✓ Adjust min_disk_space_gb in config.json if needed

Connection keeps dropping:
  ✓ Check network stability
  ✓ Keep-alive is enabled (30 seconds)
  ✓ Check connection_timeout in config.json

================================================================================
TECHNICAL DETAILS
================================================================================

Version: 2.0
- Portable standalone executable (~14 MB)
- No Python installation required
- No dependencies required
- Works on Windows 7, 8, 10, 11 (64-bit)
- Checks every 1 minute (configurable)
- Uses encrypted SFTP connection (port 222)
- Fernet encryption for stored credentials
- Log rotation: 10MB max per file, 5 backups
- Connection keep-alive: 30 seconds
- Connection timeout: 30 seconds
- Auto-cleanup: 30 days retention for old versions
- Daily reports generated at midnight

Dependencies (bundled):
- paramiko (SFTP/SSH)
- schedule (task scheduling)
- cryptography (credential encryption)

================================================================================
SECURITY NOTES
================================================================================

- Credentials stored encrypted in config.json
- Encryption key tied to computer name + username
- Password cannot be read in plain text
- Config file is machine-specific
- Copying config.json to another PC won't work (re-encryption needed)

================================================================================

**Just double-click SFTP_Monitor.exe and minimize the window!**

For detailed feature documentation, see ABOUT.txt

================================================================================
