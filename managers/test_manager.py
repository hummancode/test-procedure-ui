"""
Test Manager
Handles test flow, timer, and state management with continuous data writing
"""
from typing import List, Optional, Dict, Any
import json
import time
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

from models import TestStep, TestStatus, InputType, TimerStatus, TestSession
from models.enums import TimerStatus
from persistence import ContinuousWriter
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)


class TestManager(QObject):
    """
    Manages test procedure execution, timing, and state.
    
    Signals:
        step_changed: Emitted when moving to a new step (step_index, total_steps)
        timer_updated: Emitted every second (remaining_seconds, timer_status)
        test_completed: Emitted when all steps are finished
        result_submitted: Emitted when a step result is saved (step_index, result_value, status)
        data_updated: Emitted when session data is written to file
    """
    
    # Signals
    step_changed = pyqtSignal(int, int)  # current_index, total_steps
    timer_updated = pyqtSignal(int, str)  # remaining_seconds, timer_status
    test_completed = pyqtSignal()
    result_submitted = pyqtSignal(int, object, str)  # step_index, result_value, status
    data_updated = pyqtSignal()  # Emitted after successful write
    
    def __init__(self):
        super().__init__()
        
        # Test session
        self.session: Optional[TestSession] = None
        self.current_step_index: int = -1
        
        # Continuous writer
        self.continuous_writer = ContinuousWriter()
        
        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_timer_tick)
        self.timer.setInterval(config.TIMER_UPDATE_INTERVAL)
        
        self.step_start_time: Optional[float] = None
        self.elapsed_seconds: int = 0
        
        logger.info("TestManager initialized")
    
    def load_test_from_file(self, filepath: str, test_info: Dict[str, str]) -> bool:
        """
        Load test procedure from JSON file and create session.
        
        Args:
            filepath: Path to JSON file
            test_info: Dict with stock_number, serial_number, station_number, sip_code
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Create new session
            self.session = TestSession(
                stock_number=test_info.get('stock_number', ''),
                serial_number=test_info.get('serial_number', ''),
                station_number=test_info.get('station_number', ''),
                sip_code=test_info.get('sip_code', '')
            )
            
            # Load steps into session
            for step_data in data.get('steps', []):
                step = TestStep.from_dict(step_data)
                self.session.steps.append(step)
            
            # Set session in continuous writer
            self.continuous_writer.set_session(self.session)
            
            logger.info(f"Loaded {len(self.session.steps)} test steps from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load test file {filepath}: {e}")
            return False
    
    def set_continuous_output_directory(self, directory: str) -> bool:
        """
        Set output directory for continuous data writing.
        Filename will be auto-generated.
        
        Args:
            directory: Path to directory where files will be saved
            
        Returns:
            True if successful
        """
        success = self.continuous_writer.set_output_directory(directory)
        if success:
            # Write initial state
            self._write_update()
        return success
    
    def disable_continuous_writing(self):
        """Disable continuous data writing"""
        self.continuous_writer.disable()
        logger.info("Continuous writing disabled")
    
    def start_test(self) -> bool:
        """
        Start the test procedure from the first step.
        
        Returns:
            True if started successfully
        """
        if self.session is None or not self.session.steps:
            logger.error("Cannot start test: No session or steps loaded")
            return False
        
        self.session.start_session()
        self.current_step_index = 0
        self._start_current_step()
        
        # Write initial state
        self._write_update()
        
        logger.info("Test procedure started")
        return True
    
    def _start_current_step(self):
        """Start the current step and begin timer"""
        if not self._is_valid_step_index(self.current_step_index):
            return
        
        current_step = self.session.steps[self.current_step_index]
        current_step.status = TestStatus.IN_PROGRESS
        current_step.start_time = time.time()
        
        self.step_start_time = time.time()
        self.elapsed_seconds = 0
        
        # Start timer
        self.timer.start()
        
        # Emit signal
        self.step_changed.emit(self.current_step_index, len(self.session.steps))
        
        # Write update
        self._write_update()
        
        logger.info(f"Started step {self.current_step_index + 1}/{len(self.session.steps)}: {current_step.name}")
    
    def _on_timer_tick(self):
        """Called every second to update timer"""
        if self.step_start_time is None:
            return
        
        self.elapsed_seconds = int(time.time() - self.step_start_time)
        
        current_step = self.get_current_step()
        if current_step is None:
            return
        
        remaining_seconds = current_step.time_limit - self.elapsed_seconds
        timer_status = self._calculate_timer_status(remaining_seconds, current_step.time_limit)
        
        # Emit timer update
        self.timer_updated.emit(remaining_seconds, timer_status.value)
        
        # Write update every X seconds during active step (from settings)
        update_interval = self.continuous_writer.settings.get_update_interval()
        if self.elapsed_seconds % update_interval == 0:
            self._write_update()
    
    def _calculate_timer_status(self, remaining: int, limit: int) -> TimerStatus:
        """Calculate timer status based on remaining time"""
        if remaining < 0:
            return TimerStatus.OVERTIME
        
        percentage = (remaining / limit) * 100 if limit > 0 else 100
        
        if percentage > config.TIMER_WARNING_THRESHOLD:
            return TimerStatus.NORMAL
        elif percentage > config.TIMER_CRITICAL_THRESHOLD:
            return TimerStatus.WARNING
        else:
            return TimerStatus.CRITICAL
    
    def submit_result(self, result_value: Any) -> bool:
        """
        Submit result for current step and move to next.
        
        Args:
            result_value: The result value entered by user
            
        Returns:
            True if submitted successfully
        """
        current_step = self.get_current_step()
        if current_step is None:
            logger.error("Cannot submit result: No current step")
            return False
        
        # Validate input
        if not self._validate_input(current_step, result_value):
            logger.warning(f"Invalid input for step {self.current_step_index + 1}")
            return False
        
        # Save result
        current_step.result_value = result_value
        current_step.actual_duration = self.elapsed_seconds
        
        # Determine status based on input type
        if current_step.input_type == InputType.PASS_FAIL:
            # Handle both Turkish and English values
            passed = result_value in ["PASS", "GEÇTİ"]
            current_step.status = TestStatus.PASSED if passed else TestStatus.FAILED
        elif current_step.input_type == InputType.NUMBER:
            # Check if number is in valid range
            validation = current_step.input_validation
            min_val = validation.get('min', float('-inf'))
            max_val = validation.get('max', float('inf'))
            
            try:
                num_value = float(result_value)
                if min_val <= num_value <= max_val:
                    current_step.status = TestStatus.PASSED
                else:
                    current_step.status = TestStatus.FAILED
            except ValueError:
                current_step.status = TestStatus.FAILED
        else:
            current_step.status = TestStatus.PASSED
        
        # Stop timer
        self.timer.stop()
        
        # Emit result submitted signal
        self.result_submitted.emit(
            self.current_step_index,
            result_value,
            current_step.status.value
        )
        
        # Write update after result submission
        self._write_update()
        
        logger.info(f"Step {self.current_step_index + 1} completed: {current_step.status.value}")
        
        # Move to next step or complete test
        if self.current_step_index < len(self.session.steps) - 1:
            self.current_step_index += 1
            self._start_current_step()
        else:
            self._complete_test()
        
        return True
    
    def _validate_input(self, step: TestStep, value: Any) -> bool:
        """Validate user input based on step requirements"""
        if step.input_type == InputType.NONE:
            return True
        
        if value is None or value == "":
            return False
        
        if step.input_type == InputType.PASS_FAIL:
            # Accept both Turkish and English values
            return value in ["PASS", "FAIL", "GEÇTİ", "KALDI"]
        
        if step.input_type == InputType.NUMBER:
            try:
                float(value)
                return True
            except ValueError:
                return False
        
        return True
    
    def _complete_test(self):
        """Complete the test procedure"""
        self.timer.stop()
        
        if self.session:
            self.session.end_session()
            
        # Final write
        self._write_update()
        
        logger.info("Test procedure completed")
        self.test_completed.emit()
    
    def _write_update(self):
        """Write current session state to file"""
        if self.continuous_writer.write_update():
            self.data_updated.emit()
    
    def get_current_step(self) -> Optional[TestStep]:
        """Get the current test step"""
        if self.session and self._is_valid_step_index(self.current_step_index):
            return self.session.steps[self.current_step_index]
        return None
    
    def get_step(self, index: int) -> Optional[TestStep]:
        """Get a specific step by index"""
        if self.session and self._is_valid_step_index(index):
            return self.session.steps[index]
        return None
    
    def _is_valid_step_index(self, index: int) -> bool:
        """Check if step index is valid"""
        if self.session:
            return 0 <= index < len(self.session.steps)
        return False
    
    def get_progress_percentage(self) -> float:
        """Calculate completion percentage"""
        if self.session:
            return self.session.get_completion_percentage()
        return 0.0
    
    def get_elapsed_time(self) -> int:
        """Get elapsed time for current step in seconds"""
        return self.elapsed_seconds
    
    def get_remaining_time(self) -> int:
        """Get remaining time for current step in seconds"""
        current_step = self.get_current_step()
        if current_step:
            return current_step.time_limit - self.elapsed_seconds
        return 0
    
    def get_test_info(self) -> Dict[str, str]:
        """Get test session info"""
        if self.session:
            return {
                'stock_number': self.session.stock_number,
                'serial_number': self.session.serial_number,
                'station_number': self.session.station_number,
                'sip_code': self.session.sip_code
            }
        return {}