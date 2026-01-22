"""
Test Manager (UPDATED for flexible workflow)
Manages test flow, timing, and state with flexible pass/fail handling
"""
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from typing import List, Optional, Dict, Any
import time
import json

from models.test_step import TestStep
from models.enums import TestStatus, TimerStatus
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)


class TestManager(QObject):
    """
    Manages the test procedure workflow.
    
    Handles:
    - Loading test procedures
    - Step navigation (sequential for now, with infrastructure for random access)
    - Timer management
    - Result submission with flexible pass/fail
    - Status tracking
    
    Signals:
        step_changed: Emitted when moving to new step (step_index, total_steps)
        timer_updated: Emitted every second (remaining_seconds, timer_status)
        result_submitted: Emitted when result accepted (step_index, result_value, status)
        test_completed: Emitted when all steps done
    """
    
    step_changed = pyqtSignal(int, int)  # step_index, total_steps
    timer_updated = pyqtSignal(int, str)  # remaining_seconds, timer_status
    result_submitted = pyqtSignal(int, object, str)  # step_index, result_value, status
    test_completed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.steps: List[TestStep] = []
        self.current_step_index: int = -1
        self.test_info: Dict[str, Any] = {}
        
        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_timer_tick)
        self.step_start_time: Optional[float] = None
        self.time_limit: int = 0
        
        logger.info("TestManager initialized")
    
    def load_test_from_file(self, filepath: str) -> bool:
        """
        Load test procedure from JSON file.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            True if loaded successfully
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load test info
            self.test_info = data.get('test_info', {})
            
            # Load steps
            self.steps = [TestStep.from_dict(step_data) for step_data in data.get('steps', [])]
            
            logger.info(f"Loaded {len(self.steps)} test steps from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load test file: {e}")
            return False
    
    def start_test(self) -> bool:
        """Start the test procedure from first step"""
        if not self.steps:
            logger.warning("Cannot start test - no steps loaded")
            return False
        
        self.current_step_index = 0
        self._start_current_step()
        
        logger.info("Test started")
        return True
    
    def get_current_step(self) -> Optional[TestStep]:
        """Get the current step object"""
        if 0 <= self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None
    
    def submit_result(self, result_value: Any, status: str = "passed") -> bool:
        """
        Submit result for current step and move to next.
        
        Args:
            result_value: The submitted result
            status: "passed", "failed", or "not_applicable"
            
        Returns:
            True if submitted successfully
        """
        current_step = self.get_current_step()
        if not current_step:
            logger.warning("No current step to submit result")
            return False
        
        # Stop timer
        self.timer.stop()
        
        # Calculate actual duration
        if self.step_start_time:
            actual_duration = int(time.time() - self.step_start_time)
            current_step.actual_duration = actual_duration
        
        # Save result and status
        current_step.result_value = result_value
        
        # Set status based on provided status string
        if status == "passed":
            current_step.status = TestStatus.PASSED
        elif status == "failed":
            current_step.status = TestStatus.FAILED
        elif status == "not_applicable":
            current_step.status = TestStatus.NOT_APPLICABLE
        else:
            current_step.status = TestStatus.PASSED  # Default
        
        logger.info(f"Step {self.current_step_index + 1} completed: "
                   f"result={result_value}, status={current_step.status.value}, "
                   f"duration={current_step.actual_duration}s")
        
        # Emit result submitted signal
        self.result_submitted.emit(
            self.current_step_index,
            result_value,
            current_step.status.value
        )
        
        # Move to next step
        self._move_to_next_step()
        
        return True
    
    def _start_current_step(self):
        """Start the current step (timer + emit signal)"""
        current_step = self.get_current_step()
        if not current_step:
            return
        
        # Update step status
        current_step.status = TestStatus.IN_PROGRESS
        
        # Start timer
        self.time_limit = current_step.time_limit
        self.step_start_time = time.time()
        self.timer.start(config.TIMER_UPDATE_INTERVAL)
        
        # Emit step changed signal
        self.step_changed.emit(self.current_step_index, len(self.steps))
        
        logger.info(f"Started step {self.current_step_index + 1}/{len(self.steps)}: "
                   f"{current_step.name} (time_limit={self.time_limit}s)")
    
    def _move_to_next_step(self):
        """Move to next step or complete test"""
        self.current_step_index += 1
        
        if self.current_step_index < len(self.steps):
            # Start next step
            self._start_current_step()
        else:
            # Test completed
            logger.info("All steps completed")
            self.test_completed.emit()
    
    def _on_timer_tick(self):
        """Handle timer tick (every second)"""
        if not self.step_start_time:
            return
        
        elapsed = int(time.time() - self.step_start_time)
        remaining = self.time_limit - elapsed
        
        # Determine timer status
        if remaining > 0:
            percentage = (remaining / self.time_limit) * 100
            if percentage > config.TIMER_WARNING_THRESHOLD:
                timer_status = TimerStatus.NORMAL.value
            elif percentage > config.TIMER_CRITICAL_THRESHOLD:
                timer_status = TimerStatus.WARNING.value
            else:
                timer_status = TimerStatus.CRITICAL.value
        else:
            timer_status = TimerStatus.OVERTIME.value
        
        # Emit timer update
        self.timer_updated.emit(remaining, timer_status)
    
    # ========================================================================
    # Future: Random Step Access (infrastructure ready, not enabled yet)
    # ========================================================================
    
    def jump_to_step(self, step_index: int) -> bool:
        """
        Jump to specific step (for future sidebar navigation).
        Currently disabled in sequential mode.
        
        Args:
            step_index: Target step index (0-based)
            
        Returns:
            True if jumped successfully
        """
        # TODO: Enable this when sidebar click navigation is implemented
        if not (0 <= step_index < len(self.steps)):
            logger.warning(f"Invalid step index: {step_index}")
            return False
        
        # Stop current timer
        self.timer.stop()
        
        # Jump to step
        self.current_step_index = step_index
        self._start_current_step()
        
        logger.info(f"Jumped to step {step_index + 1}")
        return True
    
    def can_go_back(self) -> bool:
        """Check if can go to previous step"""
        return self.current_step_index > 0
    
    def go_back(self) -> bool:
        """Go to previous step (for future back button)"""
        if not self.can_go_back():
            return False
        
        return self.jump_to_step(self.current_step_index - 1)
    
    # ========================================================================
    # Export / Summary
    # ========================================================================
    
    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary of test results"""
        total = len(self.steps)
        passed = sum(1 for s in self.steps if s.status == TestStatus.PASSED)
        failed = sum(1 for s in self.steps if s.status == TestStatus.FAILED)
        not_applicable = sum(1 for s in self.steps if s.status == TestStatus.NOT_APPLICABLE)
        not_started = sum(1 for s in self.steps if s.status == TestStatus.NOT_STARTED)
        
        return {
            'total_steps': total,
            'passed': passed,
            'failed': failed,
            'not_applicable': not_applicable,
            'not_started': not_started,
            'completion_rate': ((total - not_started) / total * 100) if total > 0 else 0
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Export current test state to dictionary"""
        return {
            'test_info': self.test_info,
            'steps': [step.to_dict() for step in self.steps],
            'current_step_index': self.current_step_index,
            'summary': self.get_test_summary()
        }