"""
Enums for Test Procedure Application (PHASE 1 UPDATED)
"""
from enum import Enum


class TestStatus(Enum):
    """Status of a test step"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    NOT_APPLICABLE = "not_applicable"  # For intermediate steps with no validation


class InputType(Enum):
    """Type of input required for a test step"""
    NONE = "none"           # No input required (intermediate step)
    NUMBER = "number"       # Numeric input with validation
    PASS_FAIL = "pass_fail" # Pass/Fail checkboxes
    TEXT = "text"           # Free text input (future)


class TimerStatus(Enum):
    """Status of the timer"""
    NORMAL = "normal"       # > 20% time remaining
    WARNING = "warning"     # 10-20% time remaining
    CRITICAL = "critical"   # < 10% time remaining
    OVERTIME = "overtime"   # Time expired (negative)