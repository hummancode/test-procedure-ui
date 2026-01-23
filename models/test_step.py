"""
TestStep Data Model
Represents a single step in the test procedure
"""
from typing import Optional, Dict, Any
from datetime import datetime
from models.enums import TestStatus, InputType
import config


class TestStep:
    """
    Represents a single test step in the procedure.
    
    Attributes:
        step_id: Unique identifier for the step
        name: Step name/title
        description: Detailed description of the test step
        time_limit: Time limit in seconds
        image_path: Optional path to test step image
        input_type: Type of input required (InputType enum)
        input_label: Label for the input field
        input_validation: Validation rules (e.g., {"min": 0, "max": 100})
        status: Current status of the step (TestStatus enum)
        result_value: User-entered result value
        actual_duration: Actual time taken to complete (seconds)
        start_time: Unix timestamp when step started
        comment: Optional comment from user
    """
    
    def __init__(
        self,
        step_id: int,
        name: str,
        description: str,
        time_limit: int,
        image_path: Optional[str] = None,
        input_type: InputType = InputType.NONE,
        input_label: str = "Test Sonucu",
        input_validation: Optional[Dict[str, Any]] = None
    ):
        self.step_id = step_id
        self.name = name
        self.description = description
        self.time_limit = time_limit  # seconds
        self.image_path = image_path
        self.input_type = input_type
        self.input_label = input_label
        self.input_validation = input_validation or {}
        
        # Runtime state
        self.status = TestStatus.NOT_STARTED
        self.result_value: Optional[Any] = None
        self.actual_duration: Optional[int] = None
        self.start_time: Optional[float] = None  # Unix timestamp
        self.comment: Optional[str] = None
        
    @property
    def requires_input(self) -> bool:
        """Check if this step requires user input"""
        return self.input_type != InputType.NONE
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'step_id': self.step_id,
            'name': self.name,
            'description': self.description,
            'time_limit': self.time_limit,
            'image_path': self.image_path,
            'input_type': self.input_type.value,
            'input_label': self.input_label,
            'input_validation': self.input_validation,
            'status': self.status.value,
            'result_value': self.result_value,
            'actual_duration': self.actual_duration,
            'start_time': self._format_timestamp(self.start_time),
            'comment': self.comment
        }
    
    def _format_timestamp(self, timestamp: Optional[float]) -> Optional[str]:
        """
        Format Unix timestamp to readable string.
        
        Args:
            timestamp: Unix timestamp (seconds since epoch)
            
        Returns:
            Formatted datetime string or None
        """
        if timestamp is None:
            return None
        
        try:
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime(config.DATETIME_FORMAT)
        except:
            return None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestStep':
        """Create TestStep from dictionary"""
        step = cls(
            step_id=data['step_id'],
            name=data['name'],
            description=data['description'],
            time_limit=data['time_limit'],
            image_path=data.get('image_path'),
            input_type=InputType(data.get('input_type', 'none')),
            input_label=data.get('input_label', 'Test Sonucu'),
            input_validation=data.get('input_validation', {})
        )
        
        # Restore runtime state if present
        if 'status' in data:
            step.status = TestStatus(data['status'])
        if 'result_value' in data:
            step.result_value = data['result_value']
        if 'actual_duration' in data:
            step.actual_duration = data['actual_duration']
        if 'comment' in data:
            step.comment = data['comment']
            
        return step
    
    def __repr__(self) -> str:
        return f"TestStep(id={self.step_id}, name='{self.name}', status={self.status.value})"