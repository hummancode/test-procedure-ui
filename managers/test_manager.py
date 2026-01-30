"""
Test Manager (REFACTORED)
Orchestrates test flow using specialized managers
"""
from typing import List, Optional, Dict, Any
import json
import time
from PyQt5.QtCore import QObject, pyqtSignal

from models import TestStep, TestStatus
from models.test_session import TestSession
from models.enums import NavigationMode
from managers.timer_manager import TimerManager
from managers.navigation_manager import NavigationManager
from managers.result_manager import ResultManager
from persistence.continuous_writer import ContinuousWriter
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)


class TestManager(QObject):
    """
    Test Manager - Main Orchestrator (Refactored)
    
    Delegates to specialized managers:
    - TimerManager: Timing logic
    - NavigationManager: Navigation validation
    - ResultManager: Result saving
    
    Signals:
        step_changed: (step_index, total_steps, mode)
        timer_updated: (remaining_seconds, timer_status)
        test_completed: ()
        result_submitted: (step_index, result_value, status)
    """
    
    # Signals
    step_changed = pyqtSignal(int, int, str)  # index, total, mode
    timer_updated = pyqtSignal(int, str)      # remaining, status
    test_completed = pyqtSignal()
    result_submitted = pyqtSignal(int, object, str)  # index, value, status
    
    def __init__(self, auth_manager=None):
        super().__init__()
        
        # Specialized managers
        self.timer_manager = TimerManager()
        self.navigation_manager = NavigationManager()
        self.result_manager = ResultManager()
        
        # Connect manager signals
        self.timer_manager.timer_tick.connect(self._on_timer_tick)
        
        # Test data
        self.session: Optional[TestSession] = None
        self.steps: List[TestStep] = []
        self.test_info: Dict[str, str] = {}
        self.current_step_index: int = -1
        
        # Continuous writer
        self.continuous_writer = ContinuousWriter()
        self.auth_manager = auth_manager
        logger.info("TestManager initialized (refactored)")
    
    # ════════════════════════════════════════════════════════
    # LOADING
    # ════════════════════════════════════════════════════════
    
    def load_test_from_file(self, filepath: str, test_info: dict = None) -> bool:
        """Load test procedure from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load test info from file
            self.test_info = data.get('test_info', {})
            
            # Override with provided test_info if given
            if test_info:
                self.test_info.update(test_info)
            
            # Load steps
            self.steps = []
            for step_data in data.get('steps', []):
                step = TestStep.from_dict(step_data)
                self.steps.append(step)
            
            # Create session (don't pass steps in constructor)
            self.session = TestSession(
                stock_number=self.test_info.get('stock_number', ''),
                serial_number=self.test_info.get('serial_number', ''),
                station_number=self.test_info.get('station_number', ''),
                sip_code=self.test_info.get('sip_code', '')
            )
            
            # Assign steps to session after creation
            self.session.steps = self.steps
            
            # Set session in continuous writer
            self.continuous_writer.set_session(self.session)
            
            logger.info(f"Loaded {len(self.steps)} test steps from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load test file {filepath}: {e}")
            return False    
    # ════════════════════════════════════════════════════════
    # TEST FLOW
    # ════════════════════════════════════════════════════════
    
    def start_test(self) -> bool:
        """Start test from first step"""
        if not self.steps:
            logger.error("Cannot start test: No steps loaded")
            return False
        
        # Start session (manually set start time)
        if self.session:
            from datetime import datetime
            self.session.start_time = datetime.now()
        
        # Navigate to first step
        self.navigate_to_step(0, NavigationMode.NORMAL)
        
        # Write initial state
        self._write_update()
        
        logger.info("Test procedure started")
        return True
    # ════════════════════════════════════════════════════════
    # NAVIGATION (Delegated to NavigationManager)
    # ════════════════════════════════════════════════════════
    
    def navigate_to_step(self, target_index: int, mode: NavigationMode = NavigationMode.NORMAL):
        """
        Navigate to specific step.
        
        Args:
            target_index: Step to navigate to
            mode: Navigation mode (NORMAL, VIEW_ONLY, etc.)
        """
        user_role = None
        if self.auth_manager:
            user_role = self.auth_manager.get_role()
        # Validate navigation
        allowed, reason = self.navigation_manager.can_navigate_to(
            self.current_step_index,
            target_index,
            len(self.steps),
            self.steps, user_role=user_role 
        )
        
        if not allowed:
            logger.warning(f"Navigation blocked: {reason}")
            self.navigation_manager.navigation_blocked.emit(reason)
            return
        
        # Stop current timer
        if self.current_step_index >= 0:
            self.timer_manager.stop_timer(self.current_step_index)
        
        # Record navigation
        if self.current_step_index >= 0:
            self.navigation_manager.record_navigation(self.current_step_index, target_index)
        
        # Update index
        old_index = self.current_step_index
        self.current_step_index = target_index
        
        # Update step status
        target_step = self.steps[target_index]
        if target_step.status == TestStatus.NOT_STARTED:
            target_step.status = TestStatus.IN_PROGRESS
            target_step.start_time = time.time()
        
        # Emit signal
        self.step_changed.emit(target_index, len(self.steps), mode.value)
        
        # Start timer based on mode
        if mode == NavigationMode.NORMAL:
            self.timer_manager.start_timer(target_index, target_step.time_limit)
        # For VIEW_ONLY, EDIT modes: no timer
        
        # Write update
        self._write_update()
        
        logger.info(f"Navigated: {old_index} → {target_index} (mode: {mode.value})")
    
    def navigate_next(self):
        """Navigate to next step"""
        if self.current_step_index < len(self.steps) - 1:
            self.navigate_to_step(self.current_step_index + 1, NavigationMode.NORMAL)
        else:
            self._complete_test()
    
    def navigate_previous(self):
        """Navigate to previous step (view mode)"""
        if self.current_step_index > 0:
            self.navigate_to_step(self.current_step_index - 1, NavigationMode.VIEW_ONLY)
    
    # ════════════════════════════════════════════════════════
    # RESULT HANDLING (Delegated to ResultManager)
    # ════════════════════════════════════════════════════════
    
    def submit_result(self, result_value: Any, checkbox_value: Optional[str],
                     comment: str, is_valid: Optional[bool]):
        """
        Submit result for current step.
        
        Args:
            result_value: Numeric result or None
            checkbox_value: "PASS"/"FAIL" or None
            comment: Comment text
            is_valid: Whether value is valid (True/False/None)
        """
        current_step = self.get_current_step()
        if current_step is None:
            logger.error("Cannot submit result: No current step")
            return
        
        # Get elapsed time
        actual_duration = self.timer_manager.get_elapsed_time(self.current_step_index)
        
        # Save result
        status = self.result_manager.save_result(
            current_step,
            self.current_step_index,
            result_value,
            checkbox_value,
            comment,
            is_valid,
            actual_duration
        )
        
        # Stop timer
        self.timer_manager.stop_timer(self.current_step_index)
        
        # Emit signal
        final_value = checkbox_value if checkbox_value else result_value
        self.result_submitted.emit(self.current_step_index, final_value, status.value)
        
        # Write update
        self._write_update()
        
        logger.info(f"Result submitted for step {self.current_step_index + 1}")
        
        # Auto-navigate to next step
        self.navigate_next()
    
    # ════════════════════════════════════════════════════════
    # TIMER (Delegated to TimerManager)
    # ════════════════════════════════════════════════════════
    
    def _on_timer_tick(self, step_index: int, remaining: int, status: str):
        """Handle timer tick from TimerManager"""
        # Only emit if it's for current step
        if step_index == self.current_step_index:
            self.timer_updated.emit(remaining, status)
            
            # Auto-save every N seconds
            elapsed = self.timer_manager.get_elapsed_time(step_index)
            if elapsed > 0 and elapsed % config.DEFAULT_UPDATE_INTERVAL == 0:
                self._write_update()
    
    def get_elapsed_time(self) -> int:
        """Get elapsed time for current step"""
        if self.current_step_index >= 0:
            return self.timer_manager.get_elapsed_time(self.current_step_index)
        return 0
    
    def get_remaining_time(self) -> int:
        """Get remaining time for current step"""
        if self.current_step_index >= 0:
            return self.timer_manager.get_remaining_time(self.current_step_index)
        return 0
    
    # ════════════════════════════════════════════════════════
    # COMPLETION
    # ════════════════════════════════════════════════════════
    def _complete_test(self):
        """Complete the test procedure"""
        self.timer_manager.stop_timer(self.current_step_index)
        
        if self.session:
            # Set end time (duration_seconds is auto-calculated as a property)
            from datetime import datetime
            self.session.end_time = datetime.now()
            
            # DON'T set duration_seconds - it's a read-only property!
            # The TestSession class calculates it automatically from start_time and end_time
        
        # Write final state
        self._write_update()
        
        logger.info("Test procedure completed")
        self.test_completed.emit()
        
    # ════════════════════════════════════════════════════════
    # QUERIES
    # ════════════════════════════════════════════════════════
    
    def get_current_step(self) -> Optional[TestStep]:
        """Get current test step"""
        if 0 <= self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None
    
    def get_step(self, index: int) -> Optional[TestStep]:
        """Get specific step by index"""
        if 0 <= index < len(self.steps):
            return self.steps[index]
        return None
    
    def get_progress_percentage(self) -> float:
        """Calculate completion percentage"""
        if not self.steps:
            return 0.0
        completed = sum(1 for s in self.steps if s.status in [TestStatus.PASSED, TestStatus.FAILED])
        return (completed / len(self.steps)) * 100
    
    def get_test_info(self) -> Dict[str, str]:
        """Get test metadata"""
        return self.test_info.copy()
    
    # ════════════════════════════════════════════════════════
    # PERSISTENCE
    # ════════════════════════════════════════════════════════
    
    def set_continuous_output_directory(self, folder: str) -> bool:
        """Set output directory for continuous updates"""
        return self.continuous_writer.set_output_directory(folder)
    
    def _write_update(self):
        """Write continuous update to JSON"""
        if self.session and self.continuous_writer:
            try:
                # Change write_data() to write_update()
                self.continuous_writer.write_update()
            except Exception as e:
                logger.error(f"Failed to write update: {e}")