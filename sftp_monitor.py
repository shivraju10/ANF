#!/usr/bin/env python3
"""
SFTP File Monitor and Downloader
Monitors remote SFTP folders and downloads files to local directories at regular intervals.

Version: 2.0
Features:
- Automatic file versioning with old version archival
- Encrypted credential storage
- Connection keep-alive and timeout management
- Disk space monitoring
- Automatic cleanup of old files (30 days)
- Daily summary reports
- Log rotation (10MB per file, 5 backups)
"""

import os
import sys
import time
import stat
import logging
import re
import shutil
import json
from datetime import datetime, timedelta
from pathlib import Path
from logging.handlers import RotatingFileHandler
import paramiko
import schedule
from cryptography.fernet import Fernet
import base64
import hashlib

# Configuration Files
CONFIG_FILE = 'config.json'
KEY_FILE = '.key'

# Default Configuration
DEFAULT_CONFIG = {
    'sftp': {
        'host': 'sftp.natcoglobal.com',
        'port': 222,
        'username': 'AbercrombieLAX',
        'password': r'<9\u\XxF16fq',
        'connection_timeout': 30,
        'keepalive_interval': 30
    },
    'folders': {
        'ScriptTest/XML FILES': r'C:\A&F\XML FILES',
        'ScriptTest/EXCEL FILES': r'C:\A&F\EXCEL FILES'
    },
    'monitoring': {
        'interval_minutes': 1,
        'min_disk_space_gb': 5
    },
    'maintenance': {
        'old_version_retention_days': 30,
        'cleanup_enabled': True,
        'daily_summary_enabled': True
    },
    'logging': {
        'max_log_size_mb': 10,
        'backup_count': 5
    }
}

# Setup logging with rotation
LOG_FILE = 'sftp_monitor.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Rotating file handler (10MB per file, 5 backups)
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


class ConfigManager:
    """Manages encrypted configuration"""
    
    @staticmethod
    def generate_key():
        """Generate encryption key from machine-specific data"""
        # Use machine name + user as seed for consistent key generation
        seed = f"{os.environ.get('COMPUTERNAME', 'default')}_{os.environ.get('USERNAME', 'user')}"
        key = hashlib.sha256(seed.encode()).digest()
        return base64.urlsafe_b64encode(key)
    
    @staticmethod
    def encrypt_password(password, key):
        """Encrypt password using Fernet"""
        f = Fernet(key)
        return f.encrypt(password.encode()).decode()
    
    @staticmethod
    def decrypt_password(encrypted_password, key):
        """Decrypt password using Fernet"""
        f = Fernet(key)
        return f.decrypt(encrypted_password.encode()).decode()
    
    @staticmethod
    def save_config(config):
        """Save configuration with encrypted password"""
        key = ConfigManager.generate_key()
        config_to_save = config.copy()
        
        # Encrypt password
        if 'sftp' in config_to_save and 'password' in config_to_save['sftp']:
            config_to_save['sftp']['password_encrypted'] = ConfigManager.encrypt_password(
                config_to_save['sftp']['password'], key
            )
            del config_to_save['sftp']['password']
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_to_save, f, indent=4)
        
        logger.info(f"Configuration saved to {CONFIG_FILE}")
    
    @staticmethod
    def load_config():
        """Load configuration and decrypt password"""
        if not os.path.exists(CONFIG_FILE):
            logger.info("No config file found, creating default configuration...")
            ConfigManager.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            
            # Decrypt password
            key = ConfigManager.generate_key()
            if 'sftp' in config and 'password_encrypted' in config['sftp']:
                config['sftp']['password'] = ConfigManager.decrypt_password(
                    config['sftp']['password_encrypted'], key
                )
                del config['sftp']['password_encrypted']
            
            logger.info("Configuration loaded successfully")
            return config
            
        except Exception as e:
            logger.error(f"Failed to load config: {e}. Using defaults.")
            return DEFAULT_CONFIG


# Load configuration
CONFIG = ConfigManager.load_config()
SFTP_CONFIG = CONFIG['sftp']
FOLDER_MAPPINGS = CONFIG['folders']
CHECK_INTERVAL = CONFIG['monitoring']['interval_minutes']
MIN_DISK_SPACE_GB = CONFIG['monitoring']['min_disk_space_gb']
OLD_VERSION_RETENTION_DAYS = CONFIG['maintenance']['old_version_retention_days']
CLEANUP_ENABLED = CONFIG['maintenance']['cleanup_enabled']
DAILY_SUMMARY_ENABLED = CONFIG['maintenance']['daily_summary_enabled']


class SFTPMonitor:
    """SFTP monitoring and file download handler"""

    def __init__(self):
        self.sftp = None
        self.transport = None
        self.daily_stats = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'files_downloaded': 0,
            'files_failed': 0,
            'errors': [],
            'folders_checked': 0
        }

    def connect(self):
        """Establish SFTP connection with timeout and keep-alive"""
        try:
            logger.info(f"Connecting to {SFTP_CONFIG['host']}:{SFTP_CONFIG['port']}...")

            # Create SSH transport with timeout
            self.transport = paramiko.Transport(
                (SFTP_CONFIG['host'], SFTP_CONFIG['port'])
            )
            
            # Set connection timeout
            self.transport.banner_timeout = SFTP_CONFIG.get('connection_timeout', 30)
            
            # Connect with credentials
            self.transport.connect(
                username=SFTP_CONFIG['username'],
                password=SFTP_CONFIG['password']
            )
            
            # Enable keep-alive to prevent connection drops
            self.transport.set_keepalive(SFTP_CONFIG.get('keepalive_interval', 30))

            # Create SFTP client
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            logger.info("Successfully connected to SFTP server (with keep-alive enabled)")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to SFTP server: {e}")
            self.daily_stats['errors'].append(f"Connection failed: {e}")
            return False

    def disconnect(self):
        """Close SFTP connection"""
        try:
            if self.sftp:
                self.sftp.close()
            if self.transport:
                self.transport.close()
            logger.info("Disconnected from SFTP server")
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")

    def ensure_local_directory(self, local_path):
        """Create local directory if it doesn't exist"""
        try:
            Path(local_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {local_path}: {e}")
            return False

    def check_disk_space(self, path):
        """Check if sufficient disk space is available"""
        try:
            stat_info = shutil.disk_usage(path)
            free_gb = stat_info.free / (1024**3)
            
            if free_gb < MIN_DISK_SPACE_GB:
                logger.warning(f"Low disk space: {free_gb:.2f}GB free (minimum: {MIN_DISK_SPACE_GB}GB)")
                self.daily_stats['errors'].append(f"Low disk space: {free_gb:.2f}GB")
                return False
            
            logger.info(f"Disk space OK: {free_gb:.2f}GB free")
            return True
            
        except Exception as e:
            logger.error(f"Failed to check disk space for {path}: {e}")
            return True  # Don't block on error, just log it

    def parse_filename(self, filename):
        """Parse filename to extract base name and timestamp.
        
        Example: China_Hang_Tag_131260041_04-18-2026_04-36-13.xls
        Returns: ('China_Hang_Tag_131260041', '04-18-2026_04-36-13', '.xls')
        """
        # Pattern: base_name + underscore + timestamp (MM-DD-YYYY_HH-MM-SS) + extension
        pattern = r'^(.+?)_(\d{2}-\d{2}-\d{4}_\d{2}-\d{2}-\d{2})(\.[^.]+)$'
        match = re.match(pattern, filename)
        
        if match:
            base_name = match.group(1)
            timestamp = match.group(2)
            extension = match.group(3)
            return (base_name, timestamp, extension)
        return (None, None, None)

    def find_existing_versions(self, local_dir, base_name, extension):
        """Find all existing versions of a file in the local directory.
        
        Args:
            local_dir: Directory to search
            base_name: Base name without timestamp (e.g., 'China_Hang_Tag_131260041')
            extension: File extension (e.g., '.xls')
            
        Returns:
            List of tuples: [(full_filename, timestamp), ...]
        """
        if not os.path.exists(local_dir):
            return []
        
        existing_versions = []
        pattern = re.compile(rf'^{re.escape(base_name)}_(\d{{2}}-\d{{2}}-\d{{4}}_\d{{2}}-\d{{2}}-\d{{2}}){re.escape(extension)}$')
        
        try:
            for filename in os.listdir(local_dir):
                match = pattern.match(filename)
                if match:
                    timestamp = match.group(1)
                    existing_versions.append((filename, timestamp))
        except Exception as e:
            logger.error(f"Error scanning directory {local_dir}: {e}")
        
        return existing_versions

    def move_to_old_versions(self, local_dir, filename):
        """Move old version file to OldVer subdirectory.
        
        Args:
            local_dir: Current directory of the file
            filename: Name of the file to move
        """
        try:
            old_ver_dir = os.path.join(local_dir, 'OldVer')
            self.ensure_local_directory(old_ver_dir)
            
            source_path = os.path.join(local_dir, filename)
            dest_path = os.path.join(old_ver_dir, filename)
            
            # If file already exists in OldVer, add timestamp to avoid collision
            if os.path.exists(dest_path):
                name, ext = os.path.splitext(filename)
                timestamp_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
                dest_filename = f"{name}_moved_{timestamp_suffix}{ext}"
                dest_path = os.path.join(old_ver_dir, dest_filename)
            
            shutil.move(source_path, dest_path)
            logger.info(f"Moved old version: {filename} -> OldVer/{os.path.basename(dest_path)}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to move {filename} to OldVer: {e}")
            return False

    def cleanup_old_versions(self, local_dir):
        """Remove files older than retention period from OldVer subdirectory.
        
        Args:
            local_dir: Directory containing OldVer subdirectory
        """
        if not CLEANUP_ENABLED:
            return 0
            
        try:
            old_ver_dir = os.path.join(local_dir, 'OldVer')
            if not os.path.exists(old_ver_dir):
                return 0
            
            cutoff_date = datetime.now() - timedelta(days=OLD_VERSION_RETENTION_DAYS)
            files_deleted = 0
            
            for filename in os.listdir(old_ver_dir):
                file_path = os.path.join(old_ver_dir, filename)
                
                if os.path.isfile(file_path):
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    if file_mtime < cutoff_date:
                        os.remove(file_path)
                        logger.info(f"Cleaned up old file: {filename} (age: {(datetime.now() - file_mtime).days} days)")
                        files_deleted += 1
            
            if files_deleted > 0:
                logger.info(f"Cleanup complete: {files_deleted} file(s) deleted from {old_ver_dir}")
            
            return files_deleted
            
        except Exception as e:
            logger.error(f"Failed to cleanup old versions in {local_dir}: {e}")
            return 0

    def get_unique_filename(self, filepath):
        """Generate unique filename by adding timestamp if file exists"""
        if not os.path.exists(filepath):
            return filepath

        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        new_filename = f"{name}_{timestamp}{ext}"
        new_filepath = os.path.join(directory, new_filename)

        logger.info(f"File exists, renaming to: {new_filename}")
        return new_filepath

    def download_file(self, remote_path, local_path):
        """Download a single file from remote to local"""
        try:
            local_dir = os.path.dirname(local_path)
            filename = os.path.basename(local_path)
            
            # Parse filename to check for versioning pattern
            base_name, timestamp, extension = self.parse_filename(filename)
            
            if base_name and timestamp and extension:
                # This is a versioned file - check for older versions
                existing_versions = self.find_existing_versions(local_dir, base_name, extension)
                
                if existing_versions:
                    logger.info(f"Found {len(existing_versions)} existing version(s) of {base_name}{extension}")
                    
                    # Move all old versions to OldVer subdirectory
                    for old_filename, old_timestamp in existing_versions:
                        if old_timestamp != timestamp:  # Don't move if same timestamp (unlikely but safe)
                            logger.info(f"Newer version detected: {timestamp} > {old_timestamp}")
                            self.move_to_old_versions(local_dir, old_filename)
            else:
                # Not a versioned file - use unique filename if exists
                local_path = self.get_unique_filename(local_path)

            # Download file
            self.sftp.get(remote_path, local_path)
            logger.info(f"Downloaded: {remote_path} -> {local_path}")

            # Delete from remote after successful download
            self.sftp.remove(remote_path)
            logger.info(f"Deleted from remote: {remote_path}")

            # Track stats
            self.daily_stats['files_downloaded'] += 1
            
            return True

        except Exception as e:
            logger.error(f"Failed to download {remote_path}: {e}")
            self.daily_stats['files_failed'] += 1
            self.daily_stats['errors'].append(f"Download failed: {remote_path} - {e}")
            return False

    def list_files(self, remote_dir):
        """List all files in remote directory (non-recursive)"""
        try:
            files = []
            for entry in self.sftp.listdir_attr(remote_dir):
                # Check if it's a file (not a directory)
                if not stat.S_ISDIR(entry.st_mode):
                    files.append(entry.filename)
            return files
        except Exception as e:
            logger.error(f"Failed to list files in {remote_dir}: {e}")
            return []

    def monitor_and_download(self):
        """Check remote folders and download any files found"""
        logger.info("=" * 60)
        logger.info(f"Starting monitoring cycle at {datetime.now()}")

        # Check if we need to reset daily stats (new day)
        current_date = datetime.now().strftime('%Y-%m-%d')
        if self.daily_stats['date'] != current_date:
            # Generate summary for previous day before reset
            if DAILY_SUMMARY_ENABLED:
                self.generate_daily_summary()
            
            # Reset stats for new day
            self.daily_stats = {
                'date': current_date,
                'files_downloaded': 0,
                'files_failed': 0,
                'errors': [],
                'folders_checked': 0
            }

        # Reconnect if not connected (connection keep-alive should prevent this)
        if not self.sftp or not self.transport or not self.transport.is_active():
            logger.info("Connection lost, reconnecting...")
            if not self.connect():
                logger.error("Cannot proceed without SFTP connection")
                return

        total_files_downloaded = 0

        for remote_folder, local_folder in FOLDER_MAPPINGS.items():
            try:
                logger.info(f"Checking folder: {remote_folder}")
                self.daily_stats['folders_checked'] += 1

                # Check disk space before processing
                if not self.check_disk_space(local_folder):
                    logger.warning(f"Skipping {remote_folder} due to low disk space")
                    continue

                # Ensure local directory exists
                if not self.ensure_local_directory(local_folder):
                    continue

                # List files in remote folder
                files = self.list_files(remote_folder)

                if not files:
                    logger.info(f"No files found in {remote_folder}")
                    continue

                logger.info(f"Found {len(files)} file(s) in {remote_folder}")

                # Download each file
                for filename in files:
                    remote_path = f"{remote_folder}/{filename}"
                    local_path = os.path.join(local_folder, filename)

                    if self.download_file(remote_path, local_path):
                        total_files_downloaded += 1
                
                # Cleanup old versions after processing folder
                if CLEANUP_ENABLED:
                    deleted = self.cleanup_old_versions(local_folder)
                    if deleted > 0:
                        logger.info(f"Cleaned up {deleted} old version(s) from {local_folder}")

            except Exception as e:
                logger.error(f"Error processing folder {remote_folder}: {e}")
                self.daily_stats['errors'].append(f"Folder error: {remote_folder} - {e}")

        logger.info(f"Monitoring cycle complete. Total files downloaded: {total_files_downloaded}")
        logger.info("=" * 60)

    def generate_daily_summary(self):
        """Generate daily summary report"""
        try:
            summary_dir = 'reports'
            os.makedirs(summary_dir, exist_ok=True)
            
            summary_file = os.path.join(summary_dir, f"{self.daily_stats['date']}_summary.txt")
            
            with open(summary_file, 'w') as f:
                f.write("=" * 70 + "\n")
                f.write(f"SFTP Monitor Daily Summary - {self.daily_stats['date']}\n")
                f.write("=" * 70 + "\n\n")
                
                f.write(f"Files Downloaded: {self.daily_stats['files_downloaded']}\n")
                f.write(f"Files Failed: {self.daily_stats['files_failed']}\n")
                f.write(f"Folders Checked: {self.daily_stats['folders_checked']}\n")
                f.write(f"Success Rate: {self.calculate_success_rate()}%\n\n")
                
                if self.daily_stats['errors']:
                    f.write(f"Errors ({len(self.daily_stats['errors'])}): \n")
                    f.write("=" * 70 + "\n")
                    for i, error in enumerate(self.daily_stats['errors'], 1):
                        f.write(f"{i}. {error}\n")
                    f.write("\n")
                else:
                    f.write("No errors reported.\n\n")
                
                # Disk space info for all monitored folders
                f.write("Disk Space Status:\n")
                f.write("=" * 70 + "\n")
                for local_folder in set(FOLDER_MAPPINGS.values()):
                    try:
                        stat_info = shutil.disk_usage(local_folder)
                        free_gb = stat_info.free / (1024**3)
                        total_gb = stat_info.total / (1024**3)
                        used_percent = (stat_info.used / stat_info.total) * 100
                        f.write(f"{local_folder}:\n")
                        f.write(f"  Free: {free_gb:.2f}GB / {total_gb:.2f}GB ({100-used_percent:.1f}% free)\n")
                    except:
                        f.write(f"{local_folder}: Unable to check\n")
                
                f.write("\n" + "=" * 70 + "\n")
                f.write(f"Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            logger.info(f"Daily summary saved to {summary_file}")
            
        except Exception as e:
            logger.error(f"Failed to generate daily summary: {e}")
    
    def calculate_success_rate(self):
        """Calculate success rate for daily stats"""
        total = self.daily_stats['files_downloaded'] + self.daily_stats['files_failed']
        if total == 0:
            return 100.0
        return round((self.daily_stats['files_downloaded'] / total) * 100, 2)


def main():
    """Main execution function"""
    logger.info("=" * 70)
    logger.info("SFTP Monitor Service v2.0 Starting...")
    logger.info("=" * 70)
    logger.info(f"Monitoring interval: {CHECK_INTERVAL} minutes")
    logger.info(f"Connection timeout: {SFTP_CONFIG.get('connection_timeout', 30)} seconds")
    logger.info(f"Keep-alive interval: {SFTP_CONFIG.get('keepalive_interval', 30)} seconds")
    logger.info(f"Min disk space: {MIN_DISK_SPACE_GB}GB")
    logger.info(f"Old version retention: {OLD_VERSION_RETENTION_DAYS} days")
    logger.info(f"Daily summary: {'Enabled' if DAILY_SUMMARY_ENABLED else 'Disabled'}")
    logger.info(f"Folder mappings:")
    for remote, local in FOLDER_MAPPINGS.items():
        logger.info(f"  {remote} -> {local}")
    logger.info("=" * 70)

    monitor = SFTPMonitor()

    # Initial connection test
    if not monitor.connect():
        logger.error("Initial connection failed. Exiting.")
        return

    # Schedule the monitoring job
    schedule.every(CHECK_INTERVAL).minutes.do(monitor.monitor_and_download)
    
    # Schedule daily summary generation (at midnight)
    if DAILY_SUMMARY_ENABLED:
        schedule.every().day.at("00:01").do(monitor.generate_daily_summary)

    # Run first check immediately
    monitor.monitor_and_download()

    # Keep running and check schedule
    logger.info(f"Monitoring started. Will check every {CHECK_INTERVAL} minutes. Press Ctrl+C to stop.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds if a scheduled task is due
    except KeyboardInterrupt:
        logger.info("Received stop signal. Shutting down...")
        
        # Generate final summary before exit
        if DAILY_SUMMARY_ENABLED:
            logger.info("Generating final daily summary...")
            monitor.generate_daily_summary()
    finally:
        monitor.disconnect()
        logger.info("SFTP Monitor Service Stopped")


if __name__ == "__main__":
    main()
