"""
Enums and Constants for Test Procedure Application
"""
from enum import Enum


class TestStatus(Enum):
    """Status of a test step"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class InputType(Enum):
    """Type of input required for a test step"""
    NONE = "none"           # No input required
    NUMBER = "number"       # Numeric input
    PASS_FAIL = "pass_fail" # Pass/Fail buttons
    COMMENT = "comment"     # Text comment (optional)


class TimerStatus(Enum):
    """Timer status based on remaining time"""
    NORMAL = "normal"       # > 20% time remaining
    WARNING = "warning"     # 10-20% time remaining
    CRITICAL = "critical"   # < 10% time remaining
    OVERTIME = "overtime"   # Timer has expired