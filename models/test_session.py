"""
TestSession Data Model
Represents a complete test session with all steps and metadata

Updated to include extended SessionMetadata for:
- Product information
- Software versions
- Device calibrations
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from models.test_step import TestStep
from models.enums import TestStatus
from models.session_metadata import SessionMetadata


class TestSession:
    """
    Represents a complete test execution session.
    
    Tracks all test steps, metadata, timing, and results for a single test run.
    
    Attributes:
        session_id: Unique identifier for this session
        stock_number: Product stock number (from metadata.stok_no)
        serial_number: Product serial number (from metadata.seri_no)
        station_number: Test station identifier (from metadata.istasyon)
        sip_code: SIP code (from metadata.sip_code)
        start_time: Session start timestamp
        end_time: Session end timestamp (None if in progress)
        steps: List of TestStep objects
        metadata: Extended session metadata (NEW)
    """
    
    def __init__(
        self,
        stock_number: str = "",
        serial_number: str = "",
        station_number: str = "",
        sip_code: str = "",
        metadata: Optional[SessionMetadata] = None
    ):
        self.session_id = self._generate_session_id()
        
        # If metadata provided, use it; otherwise use direct parameters
        if metadata:
            self.metadata = metadata
            self.stock_number = metadata.stok_no
            self.serial_number = metadata.seri_no
            self.station_number = metadata.istasyon
            self.sip_code = metadata.sip_code
        else:
            self.metadata = None
            self.stock_number = stock_number
            self.serial_number = serial_number
            self.station_number = station_number
            self.sip_code = sip_code
        
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        
        self.steps: List[TestStep] = []
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID based on timestamp"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def start_session(self):
        """Mark session as started"""
        self.start_time = datetime.now()
    
    def end_session(self):
        """Mark session as ended"""
        self.end_time = datetime.now()
    
    @property
    def is_active(self) -> bool:
        """Check if session is currently active"""
        return self.start_time is not None and self.end_time is None
    
    @property
    def duration_seconds(self) -> Optional[int]:
        """Get total session duration in seconds"""
        if self.start_time is None:
            return None
        
        end = self.end_time or datetime.now()
        return int((end - self.start_time).total_seconds())
    
    def get_completion_percentage(self) -> float:
        """Calculate completion percentage"""
        if not self.steps:
            return 0.0
        
        completed = sum(
            1 for step in self.steps 
            if step.status in [TestStatus.PASSED, TestStatus.FAILED]
        )
        return (completed / len(self.steps)) * 100
    
    def get_passed_count(self) -> int:
        """Count passed steps"""
        return sum(1 for step in self.steps if step.status == TestStatus.PASSED)
    
    def get_failed_count(self) -> int:
        """Count failed steps"""
        return sum(1 for step in self.steps if step.status == TestStatus.FAILED)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert session to dictionary for serialization.
        
        Returns:
            Dictionary representation of session
        """
        data = {
            'session_id': self.session_id,
            'stock_number': self.stock_number,
            'serial_number': self.serial_number,
            'station_number': self.station_number,
            'sip_code': self.sip_code,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'completion_percentage': self.get_completion_percentage(),
            'passed_count': self.get_passed_count(),
            'failed_count': self.get_failed_count(),
            'steps': [step.to_dict() for step in self.steps]
        }
        
        # Include metadata if available
        if self.metadata:
            data['metadata'] = self.metadata.to_dict()
        
        return data
    
    def to_dict_for_excel(self) -> Dict[str, Any]:
        """
        Convert session to dictionary for Excel export.
        Excludes UI-only fields (istasyon, sip_code).
        
        Returns:
            Dictionary with Excel-exportable fields
        """
        data = {
            'session_id': self.session_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'completion_percentage': self.get_completion_percentage(),
            'passed_count': self.get_passed_count(),
            'failed_count': self.get_failed_count(),
            'steps': [step.to_dict() for step in self.steps]
        }
        
        # Include metadata for Excel (without UI-only fields)
        if self.metadata:
            data['metadata'] = self.metadata.get_excel_data()
        else:
            # Fallback to basic stock/serial if no metadata
            data['metadata'] = {
                'stok_no': self.stock_number,
                'seri_no': self.serial_number
            }
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestSession':
        """
        Create TestSession from dictionary.
        
        Args:
            data: Dictionary with session data
            
        Returns:
            TestSession instance
        """
        # Check for metadata
        metadata = None
        if 'metadata' in data and data['metadata']:
            metadata = SessionMetadata.from_dict(data['metadata'])
        
        session = cls(
            stock_number=data.get('stock_number', ''),
            serial_number=data.get('serial_number', ''),
            station_number=data.get('station_number', ''),
            sip_code=data.get('sip_code', ''),
            metadata=metadata
        )
        
        session.session_id = data.get('session_id', session.session_id)
        
        if data.get('start_time'):
            session.start_time = datetime.fromisoformat(data['start_time'])
        if data.get('end_time'):
            session.end_time = datetime.fromisoformat(data['end_time'])
        
        # Load steps
        session.steps = [
            TestStep.from_dict(step_data) 
            for step_data in data.get('steps', [])
        ]
        
        return session
    
    def __repr__(self) -> str:
        status = "Active" if self.is_active else "Completed"
        return (f"TestSession(id={self.session_id}, "
                f"status={status}, "
                f"steps={len(self.steps)}, "
                f"completion={self.get_completion_percentage():.1f}%)")