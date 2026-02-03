"""
Continuous Data Writer
Writes test session data continuously to a JSON file with overwriting
Folder selection persists between sessions
"""
import json
import os
from typing import Optional
from datetime import datetime
from pathlib import Path

from models.test_session import TestSession
from utils.logger import setup_logger
from utils.settings_manager import SettingsManager
import config

logger = setup_logger(__name__)


class ContinuousWriter:
    """
    Handles continuous writing of test session data to file.
    
    Overwrites the file with updated data after each significant event.
    File name includes station, date, and other key identifiers.
    Folder is selected once and persists between sessions.
    """
    
    def __init__(self):
        self.settings = SettingsManager()
        self.output_directory: str = self.settings.get_update_folder()  # Always has default
        self.output_filepath: Optional[str] = None   # Auto-generated filepath
        self.session: Optional[TestSession] = None
        self.write_enabled = True  # Enabled by default with default folder
        
        logger.info(f"ContinuousWriter initialized with folder: {self.output_directory}")
        
    def set_output_directory(self, directory: str) -> bool:
        """
        Set the output directory for continuous writing.
        Filename will be auto-generated based on session info.
        This setting is saved and persists between app sessions.
        
        Args:
            directory: Path to directory where files will be saved
            
        Returns:
            True if directory is valid and writable
        """
        try:
            # Ensure directory exists
            os.makedirs(directory, exist_ok=True)
            
            # Test write access
            test_file = os.path.join(directory, 'test_write_check.tmp')
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write('test')
            os.remove(test_file)
            
            # Save to persistent settings
            self.settings.set_update_folder(directory)
            
            self.output_directory = directory
            self.write_enabled = True
            
            # Generate filepath if we have session info
            if self.session:
                self._generate_filepath()
            
            logger.info(f"Continuous writer directory set to: {directory}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set output directory {directory}: {e}")
            self.write_enabled = False
            return False
    
    def _generate_filepath(self):
        """Generate the output filepath based on current session info"""
        if not self.output_directory or not self.session:
            return
        
        filename = self.generate_filename(
            self.session.station_number,
            self.session.stock_number
        )
        self.output_filepath = os.path.join(self.output_directory, filename)
        logger.info(f"Generated filepath: {self.output_filepath}")
    
    def set_session(self, session: TestSession):
        """
        Set the test session to track.
        
        Args:
            session: TestSession instance to write
        """
        self.session = session
        
        # Generate new filepath based on session info
        if self.output_directory:
            self._generate_filepath()
        
        logger.debug(f"Session set: {session.session_id}")
    
    def write_update(self) -> bool:
        """
        Write current session state to file (overwriting).
        
        Returns:
            True if write successful
        """
        if not self.write_enabled:
            logger.warning("Continuous writer not enabled (no output file set)")
            return False
        
        if self.session is None:
            logger.warning("No session to write")
            return False
        
        try:
            data = self._prepare_data()
            
            # Write to file (overwrite)
            with open(self.output_filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Session data written to {self.output_filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write session data: {e}")
            return False
    
    def _prepare_data(self) -> dict:
        """
        Prepare session data for writing.
        
        Returns:
            Dictionary with formatted session data
        """
        data = self.session.to_dict()
        
        # Add metadata
        data['last_updated'] = datetime.now().isoformat()
        data['file_version'] = '1.0'
        
        # Format step data for readability
        formatted_steps = []
        for step_dict in data['steps']:
            formatted_step = {
                'step_id': step_dict['step_id'],
                'name': step_dict['name'],
                'status': step_dict['status'],
                'start_time': self._format_timestamp(step_dict.get('start_time')),
                'actual_duration': step_dict.get('actual_duration'),
                'result_value': step_dict.get('result_value'),
                'comment': step_dict.get('comment'),  # User comment
                'time_limit': step_dict['time_limit'],
                'completed_by': step_dict['completed_by'],
                'input_validation': step_dict.get('input_validation')  # Min/max values
                
            }
            formatted_steps.append(formatted_step)
        
        data['steps'] = formatted_steps
        
        return data
    
    def _format_timestamp(self, timestamp) -> Optional[str]:
        """Format timestamp for display"""
        if timestamp is None:
            return None
        
        # If it's already a string, return as-is
        if isinstance(timestamp, str):
            return timestamp
        
        # If it's a datetime object, format it
        if isinstance(timestamp, datetime):
            return timestamp.strftime(config.DATETIME_FORMAT)
        
        # If it's a Unix timestamp (float), convert to datetime first
        if isinstance(timestamp, (int, float)):
            try:
                dt = datetime.fromtimestamp(timestamp)
                return dt.strftime(config.DATETIME_FORMAT)
            except:
                return str(timestamp)
        
        return str(timestamp)
    
    def disable(self):
        """Disable continuous writing"""
        self.write_enabled = False
        logger.info("Continuous writer disabled")
    
    def is_enabled(self) -> bool:
        """
        Check if continuous writing is enabled.
        
        Returns True if we have a valid directory and filepath.
        Note: Always enabled by default with default folder.
        """
        return (self.write_enabled and 
                self.output_directory is not None and 
                self.output_filepath is not None)
    
    def get_current_directory(self) -> str:
        """Get the current output directory"""
        return self.output_directory
    
    def get_current_filepath(self) -> Optional[str]:
        """Get the current output filepath (if generated)"""
        return self.output_filepath
    
    @staticmethod
    def generate_filename(station_number: str, stock_number: str = "") -> str:
        """
        Generate filename with station, date, and identifiers.
        
        Format: GuncellemeRaporu_<STATION>_<DATE>_<STOCK>.json
        Example: GuncellemeRaporu_ST-01_20260123_ABC123.json
        
        Args:
            station_number: Station identifier
            stock_number: Optional stock number
            
        Returns:
            Suggested filename
        """
        date_str = datetime.now().strftime("%Y%m%d")
        
        parts = ["GuncellemeRaporu", station_number, date_str]
        
        if stock_number:
            # Clean stock number (remove special chars)
            clean_stock = "".join(c for c in stock_number if c.isalnum() or c in "-_")
            parts.append(clean_stock)
        
        filename = "_".join(parts) + ".json"
        
        return filename