"""
Base Input Widget
Common interface for all input types
"""
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal


class BaseInputWidget(QWidget):
    """
    Base class for input widgets.
    
    All input widgets should implement:
    - get_result() -> Returns entered value
    - is_result_written() -> Returns True if YAZ clicked
    - clear() -> Resets widget state
    
    Signals:
        emoji_update_requested(bool): Request emoji update (happy/sad)
    """
    
    emoji_update_requested = pyqtSignal(bool)  # is_happy
    
    def __init__(self, validation: dict = None, parent=None):
        super().__init__(parent)
        self.validation = validation or {}
        self.result_written = False
    
    def get_result(self) -> tuple:
        """
        Get current result value and validity.
        
        Returns:
            (result_value, is_valid) tuple
            - result_value: The entered value
            - is_valid: True if valid, False if invalid
            
        Note: Subclasses should override this method
        """
        raise NotImplementedError("Subclass must implement get_result()")
    
    def is_result_written(self) -> bool:
        """
        Check if result has been written (YAZ clicked).
        
        Returns:
            True if YAZ button clicked
            
        Note: Subclasses should override this method
        """
        raise NotImplementedError("Subclass must implement is_result_written()")
    
    def clear(self):
        """
        Reset widget to initial state.
        
        Note: Subclasses should override this method
        """
        raise NotImplementedError("Subclass must implement clear()")