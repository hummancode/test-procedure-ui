"""
Result Manager
Handles test result saving and validation
"""
from typing import Any, Optional
from PyQt5.QtCore import QObject, pyqtSignal

from models.enums import TestStatus, InputType
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ResultManager(QObject):
    """
    Manages test result saving and validation.
    
    Features:
    - Result validation
    - Status determination
    - Change tracking
    
    Signals:
        result_saved: (step_index, result_value, status)
        result_changed: (step_index, old_value, new_value)
    """
    
    result_saved = pyqtSignal(int, object, str)      # step_index, value, status
    result_changed = pyqtSignal(int, object, object)  # step_index, old, new
    
    def __init__(self):
        super().__init__()
        logger.info("ResultManager initialized")
    
    def save_result(self, step, step_index: int, result_value: Any, 
                   checkbox_value: Optional[str], comment: str, 
                   is_valid: Optional[bool], actual_duration: int):
        """
        Save result to test step.
        
        Args:
            step: TestStep object
            step_index: Step index
            result_value: Result value (number or None)
            checkbox_value: Checkbox value ("PASS"/"FAIL" or None)
            comment: Comment text
            is_valid: Whether value is valid (True/False/None)
            actual_duration: Time taken in seconds
            
        Returns:
            TestStatus enum value
        """
        # Track old value for change detection
        old_value = step.result_value
        
        # Determine which value to save
        if checkbox_value:
            final_value = checkbox_value
        elif result_value:
            final_value = result_value
        else:
            final_value = None
        
        # Save to step
        step.result_value = final_value
        step.comment = comment
        step.actual_duration = actual_duration
        
        # Determine status
        status = self._determine_status(step.input_type, is_valid)
        step.status = status
        
        # Emit signals
        if old_value != final_value:
            self.result_changed.emit(step_index, old_value, final_value)
        
        self.result_saved.emit(step_index, final_value, status.value)
        
        logger.info(f"Result saved for step {step_index}: {final_value} ({status.value})")
        
        return status
    
    def _determine_status(self, input_type: InputType, is_valid: Optional[bool]) -> TestStatus:
        """
        Determine test status based on input type and validity.
        
        Args:
            input_type: Type of input
            is_valid: Whether input is valid (True/False/None)
            
        Returns:
            TestStatus enum value
        """
        if is_valid is None:
            # No validation (InputType.NONE)
            return TestStatus.PASSED  # Or NOT_APPLICABLE if you prefer
        
        elif is_valid is True:
            return TestStatus.PASSED
        
        else:  # is_valid is False
            return TestStatus.FAILED
    
    def validate_result(self, input_type: InputType, result_value: Any,
                       validation_rules: dict) -> bool:
        """
        Validate result value against rules.
        
        Args:
            input_type: Type of input
            result_value: Value to validate
            validation_rules: Validation rules dict
            
        Returns:
            True if valid, False otherwise
        """
        if input_type == InputType.NUMBER:
            try:
                value = float(result_value)
                min_val = validation_rules.get('min')
                max_val = validation_rules.get('max')
                
                if min_val is not None and value < min_val:
                    return False
                if max_val is not None and value > max_val:
                    return False
                
                return True
            except (ValueError, TypeError):
                return False
        
        elif input_type == InputType.PASS_FAIL:
            return result_value in ["PASS", "FAIL", "GEÇTİ", "KALDI"]
        
        else:
            return True