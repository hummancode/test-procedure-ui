"""
Navigation Manager
Handles test step navigation logic and validation
"""
from typing import Optional, Tuple
from PyQt5.QtCore import QObject, pyqtSignal

from models.enums import NavigationMode, TestStatus
from utils.logger import setup_logger
import config
logger = setup_logger(__name__)


class NavigationManager(QObject):
    """
    Manages navigation between test steps.
    
    Features:
    - Navigation validation
    - Business rules enforcement
    - Navigation history tracking
    
    Signals:
        navigation_requested: (target_index, mode)
        navigation_blocked: (reason)
    """
    
    navigation_requested = pyqtSignal(int, str)  # target_index, mode
    navigation_blocked = pyqtSignal(str)         # reason
    
    def __init__(self):
        super().__init__()
        
        # Navigation history
        self.navigation_history = []  # [(from_index, to_index, timestamp), ...]
        
        logger.info("NavigationManager initialized")
    
    def can_navigate_to(self, current_index: int, target_index: int, 
                       total_steps: int, steps_data: list, 
                       user_role: str = None) -> Tuple[bool, str]:
        """
        Validate if navigation to target step is allowed.
        
        Args:
            current_index: Current step index
            target_index: Target step index
            total_steps: Total number of steps
            steps_data: List of TestStep objects
            user_role: Current user role (from AuthManager)
            
        Returns:
            (allowed: bool, reason: str)
        """
        # Basic validation
        if target_index < 0 or target_index >= total_steps:
            return (False, "Geçersiz adım numarası")
        
        if target_index == current_index:
            return (False, "Zaten bu adımdasınız")
        
        # ========================================================================
        # ROLE-BASED NAVIGATION RULES
        # ========================================================================
        
        # Going backward (to previous steps)
        if target_index < current_index:
            # Only admins can go backward
            if user_role == config.UserRole.ADMIN:
                logger.info(f"Admin navigating backward: {current_index} → {target_index}")
                return (True, "")
            else:
                return (False, "Geri gitme yetkisi yok. Sadece yönetici geri gidebilir.")
        
        # Going forward (to next steps)
        elif target_index > current_index:
            # Everyone can go forward (sequential)
            # In the future, might add: "can only skip 1 step" rule
            return (True, "")
        
        return (True, "")
    
    def determine_navigation_mode(self, current_index: int, target_index: int,
                                  target_step_status: TestStatus) -> NavigationMode:
        """
        Determine appropriate navigation mode based on context.
        
        Args:
            current_index: Current step index
            target_index: Target step index
            target_step_status: Status of target step
            
        Returns:
            NavigationMode enum value
        """
        # Going backward to completed step
        if target_index < current_index:
            if target_step_status in [TestStatus.PASSED, TestStatus.FAILED]:
                return NavigationMode.VIEW_ONLY
            else:
                return NavigationMode.NORMAL
        
        # Going forward to not-started step
        elif target_index > current_index:
            return NavigationMode.NORMAL
        
        # Same step (shouldn't happen)
        else:
            return NavigationMode.VIEW_ONLY
    
    def record_navigation(self, from_index: int, to_index: int):
        """
        Record navigation event in history.
        
        Args:
            from_index: Starting step index
            to_index: Target step index
        """
        import time
        
        self.navigation_history.append({
            'from': from_index,
            'to': to_index,
            'timestamp': time.time()
        })
        
        logger.debug(f"Navigation recorded: {from_index} → {to_index}")
    
    def get_navigation_history(self) -> list:
        """Get navigation history"""
        return self.navigation_history.copy()