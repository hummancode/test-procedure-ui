"""
Settings Manager
Handles persistent application settings (saves to disk)

Extended with session metadata memory feature:
- Remembers last entered session metadata values
- Pre-populates fields for faster entry
"""
import json
import os
from typing import Optional, Dict, Any
from pathlib import Path
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)


class SettingsManager:
    """
    Manages application settings that persist between sessions.
    Settings are saved to a JSON file in the application directory.
    
    Extended Features:
    - Session metadata memory (remembers last entered values)
    """
    
    # Default settings file location
    #SETTINGS_FILE = "app_settings.json"
    
    # Default values
    DEFAULT_UPDATE_FOLDER = config.DEFAULT_UPDATE_FOLDER
    DEFAULT_UPDATE_INTERVAL = 10  # seconds
    
    def __init__(self):
        self.settings_path = config.SETTINGS_FILE
        self.settings: Dict[str, Any] = {}
        self._load_settings()
        
    def _load_settings(self):
        """Load settings from disk, create defaults if not exists"""
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
                logger.info(f"Settings loaded from {self.settings_path}")
            else:
                # Create default settings
                self._create_default_settings()
                logger.info("Created default settings")
                
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            self._create_default_settings()
    
    def _create_default_settings(self):
        """Create default settings"""
        self.settings = {
            'update_folder': self.DEFAULT_UPDATE_FOLDER,
            'update_interval': self.DEFAULT_UPDATE_INTERVAL,
            'last_station': '',
            'window_geometry': None,
            'version': '1.0',
            # NEW: Session metadata memory
            'last_session_metadata': {}
        }
        self._save_settings()
    
    def _save_settings(self):
        """Save current settings to disk"""
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            logger.debug(f"Settings saved to {self.settings_path}")
            
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
    
    def get_update_folder(self) -> str:
        """
        Get the update folder path.
        
        Returns:
            Path to update folder (always returns a value, never None)
        """
        folder = self.settings.get('update_folder', self.DEFAULT_UPDATE_FOLDER)
        
        # Ensure the folder exists
        try:
            os.makedirs(folder, exist_ok=True)
        except Exception as e:
            logger.warning(f"Could not create update folder {folder}: {e}")
            # Fall back to default if current folder fails
            folder = self.DEFAULT_UPDATE_FOLDER
            os.makedirs(folder, exist_ok=True)
        
        return folder
    
    def set_update_folder(self, folder: str):
        """
        Set and save the update folder path.
        
        Args:
            folder: Path to update folder
        """
        self.settings['update_folder'] = folder
        self._save_settings()
        logger.info(f"Update folder saved: {folder}")
    
    def get_last_station(self) -> str:
        """Get last used station number"""
        return self.settings.get('last_station', '')
    
    def set_last_station(self, station: str):
        """Save last used station number"""
        self.settings['last_station'] = station
        self._save_settings()
    
    def get_update_interval(self) -> int:
        """
        Get update interval in seconds.
        
        Returns:
            Update interval in seconds (default 10)
        """
        return self.settings.get('update_interval', self.DEFAULT_UPDATE_INTERVAL)
    
    def set_update_interval(self, interval: int):
        """
        Set and save the update interval.
        
        Args:
            interval: Update interval in seconds (minimum 5)
        """
        # Ensure minimum 5 seconds
        interval = max(5, interval)
        self.settings['update_interval'] = interval
        self._save_settings()
        logger.info(f"Update interval saved: {interval} seconds")
    
    # =========================================================================
    # NEW: Session Metadata Memory
    # =========================================================================
    
    def get_last_session_metadata(self) -> Dict[str, Any]:
        """
        Get last entered session metadata values.
        
        Used to pre-populate the TestSessionSetupDialog for faster entry.
        
        Returns:
            Dictionary with last session metadata, or empty dict if none
        """
        return self.settings.get('last_session_metadata', {})
    
    def set_last_session_metadata(self, metadata: Dict[str, Any]):
        """
        Save session metadata for next session.
        
        Args:
            metadata: Dictionary with session metadata values
        """
        self.settings['last_session_metadata'] = metadata
        self._save_settings()
        logger.info("Last session metadata saved for quick entry")
    
    def clear_last_session_metadata(self):
        """Clear saved session metadata"""
        self.settings['last_session_metadata'] = {}
        self._save_settings()
        logger.info("Last session metadata cleared")
    
    # =========================================================================
    # General Methods
    # =========================================================================
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self._create_default_settings()
        logger.info("Settings reset to defaults")
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings as dictionary"""
        return self.settings.copy()