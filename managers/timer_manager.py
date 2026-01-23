"""
Timer Manager
Handles timing for individual test steps
"""
import time
from typing import Dict, Optional
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

import config
from models.enums import TimerStatus
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TimerManager(QObject):
    """
    Manages timers for test steps.
    
    Features:
    - Independent timer per step
    - Pause/resume support
    - Elapsed time tracking
    - Timer status calculation
    
    Signals:
        timer_tick: Emitted every second (step_index, remaining_seconds, status)
    """
    
    timer_tick = pyqtSignal(int, int, str)  # step_index, remaining, status
    
    def __init__(self):
        super().__init__()
        
        # Timer data: step_index -> {start_time, elapsed, paused, limit}
        self.step_timers: Dict[int, dict] = {}
        
        # Active timer
        self.active_step_index: Optional[int] = None
        
        # QTimer for updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._on_timer_tick)
        self.update_timer.setInterval(config.TIMER_UPDATE_INTERVAL)
        
        logger.info("TimerManager initialized")
    
    def start_timer(self, step_index: int, time_limit: int):
        """
        Start timer for a specific step.
        
        Args:
            step_index: Step to start timer for
            time_limit: Time limit in seconds
        """
        # Initialize timer data if new
        if step_index not in self.step_timers:
            self.step_timers[step_index] = {
                'start_time': time.time(),
                'elapsed': 0,
                'paused': False,
                'limit': time_limit
            }
        else:
            # Resume paused timer
            timer_data = self.step_timers[step_index]
            timer_data['start_time'] = time.time()
            timer_data['paused'] = False
            timer_data['limit'] = time_limit
        
        # Set as active
        self.active_step_index = step_index
        
        # Start update timer
        if not self.update_timer.isActive():
            self.update_timer.start()
        
        logger.info(f"Timer started for step {step_index} (limit: {time_limit}s)")
    
    def stop_timer(self, step_index: int) -> int:
        """
        Stop timer for a specific step.
        
        Args:
            step_index: Step to stop timer for
            
        Returns:
            Total elapsed seconds
        """
        if step_index not in self.step_timers:
            return 0
        
        timer_data = self.step_timers[step_index]
        
        if not timer_data['paused']:
            # Calculate elapsed time since last start
            elapsed_now = int(time.time() - timer_data['start_time'])
            timer_data['elapsed'] += elapsed_now
            timer_data['paused'] = True
        
        # Stop update timer if this was active
        if self.active_step_index == step_index:
            self.active_step_index = None
            self.update_timer.stop()
        
        total_elapsed = timer_data['elapsed']
        logger.info(f"Timer stopped for step {step_index} (elapsed: {total_elapsed}s)")
        
        return total_elapsed
    
    def pause_timer(self, step_index: int):
        """
        Pause timer for a specific step.
        
        Args:
            step_index: Step to pause timer for
        """
        if step_index not in self.step_timers:
            return
        
        timer_data = self.step_timers[step_index]
        
        if not timer_data['paused']:
            elapsed_now = int(time.time() - timer_data['start_time'])
            timer_data['elapsed'] += elapsed_now
            timer_data['paused'] = True
            
            logger.info(f"Timer paused for step {step_index}")
    
    def get_elapsed_time(self, step_index: int) -> int:
        """
        Get elapsed time for a specific step.
        
        Args:
            step_index: Step to get time for
            
        Returns:
            Elapsed seconds (0 if timer never started)
        """
        if step_index not in self.step_timers:
            return 0
        
        timer_data = self.step_timers[step_index]
        
        if timer_data['paused']:
            return timer_data['elapsed']
        else:
            elapsed_now = int(time.time() - timer_data['start_time'])
            return timer_data['elapsed'] + elapsed_now
    
    def get_remaining_time(self, step_index: int) -> int:
        """
        Get remaining time for a specific step.
        
        Args:
            step_index: Step to get remaining time for
            
        Returns:
            Remaining seconds (negative if overtime)
        """
        if step_index not in self.step_timers:
            return 0
        
        timer_data = self.step_timers[step_index]
        elapsed = self.get_elapsed_time(step_index)
        
        return timer_data['limit'] - elapsed
    
    def get_timer_status(self, step_index: int) -> TimerStatus:
        """
        Calculate timer status based on remaining time.
        
        Args:
            step_index: Step to get status for
            
        Returns:
            TimerStatus enum value
        """
        if step_index not in self.step_timers:
            return TimerStatus.NORMAL
        
        timer_data = self.step_timers[step_index]
        remaining = self.get_remaining_time(step_index)
        limit = timer_data['limit']
        
        if remaining < 0:
            return TimerStatus.OVERTIME
        
        percentage = (remaining / limit * 100) if limit > 0 else 100
        
        if percentage > config.TIMER_WARNING_THRESHOLD:
            return TimerStatus.NORMAL
        elif percentage > config.TIMER_CRITICAL_THRESHOLD:
            return TimerStatus.WARNING
        else:
            return TimerStatus.CRITICAL
    
    def _on_timer_tick(self):
        """Called every second to update active timer"""
        if self.active_step_index is None:
            return
        
        remaining = self.get_remaining_time(self.active_step_index)
        status = self.get_timer_status(self.active_step_index)
        
        # Emit signal
        self.timer_tick.emit(self.active_step_index, remaining, status.value)
    
    def clear_timer(self, step_index: int):
        """
        Clear timer data for a specific step.
        
        Args:
            step_index: Step to clear timer for
        """
        if step_index in self.step_timers:
            del self.step_timers[step_index]
            logger.debug(f"Timer cleared for step {step_index}")
    
    def reset_all_timers(self):
        """Reset all timers (for new test session)"""
        self.step_timers.clear()
        self.active_step_index = None
        self.update_timer.stop()
        logger.info("All timers reset")