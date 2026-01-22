"""
Header Widget - Row 1
Displays session metadata (stock number, serial, station, SIP, timestamp)
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt
from datetime import datetime
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class HeaderWidget(QWidget):
    """
    Row 1: Header Information Bar
    
    Displays:
    - STOK NO: xxx | SERİ: xxx | İSTASYON: xxx | SİP: xxx | DD/MM/YYYY HH:MM:SS
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.test_info = {}
        self._init_ui()
        self._setup_timer()
        
    def _init_ui(self):
        """Initialize the UI components"""
        # Set fixed height
        self.setFixedHeight(config.ROW_1_HEIGHT)
        
        # Set background color
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.Colors.BACKGROUND_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
        """)
        
        # Create layout
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(15)
        
        # Create labels
        self.stock_label = QLabel(f"{config.Labels.STOCK_NO}: ---")
        self.serial_label = QLabel(f"{config.Labels.SERIAL}: ---")
        self.station_label = QLabel(f"{config.Labels.STATION}: ---")
        self.sip_label = QLabel(f"{config.Labels.SIP}: ---")
        self.datetime_label = QLabel(self._format_datetime())
        
        # Make label text bold for identifiers
        font_style = f"font-size: {config.FONT_SIZE}pt;"
        for label in [self.stock_label, self.serial_label, self.station_label, self.sip_label]:
            label.setStyleSheet(font_style)
        
        # Add separator style
        separator_style = f"color: {config.Colors.TEXT_SECONDARY};"
        
        # Add to layout with separators
        layout.addWidget(self.stock_label)
        layout.addWidget(self._create_separator(), 0)
        layout.addWidget(self.serial_label)
        layout.addWidget(self._create_separator(), 0)
        layout.addWidget(self.station_label)
        layout.addWidget(self._create_separator(), 0)
        layout.addWidget(self.sip_label)
        layout.addWidget(self._create_separator(), 0)
        layout.addWidget(self.datetime_label)
        layout.addStretch()
        
        self.setLayout(layout)
        
        logger.debug("HeaderWidget initialized")
    
    def _create_separator(self) -> QLabel:
        """Create a separator label |"""
        sep = QLabel("|")
        sep.setStyleSheet(f"color: {config.Colors.TEXT_SECONDARY};")
        return sep
    
    def _setup_timer(self):
        """Setup timer to update datetime every second"""
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_datetime)
        self.timer.start(1000)  # Update every second
    
    def _update_datetime(self):
        """Update the datetime label"""
        self.datetime_label.setText(self._format_datetime())
    
    def _format_datetime(self) -> str:
        """Format current datetime in Turkish format"""
        return datetime.now().strftime(config.DATETIME_FORMAT)
    
    def set_test_info(self, test_info: dict):
        """
        Update header with test information.
        
        Args:
            test_info: Dictionary with keys: stock_number, serial_number, 
                      station_number, sip_code
        """
        self.test_info = test_info
        
        stock = test_info.get('stock_number', '---')
        serial = test_info.get('serial_number', '---')
        station = test_info.get('station_number', '---')
        sip = test_info.get('sip_code', '---')
        
        self.stock_label.setText(f"{config.Labels.STOCK_NO}: {stock}")
        self.serial_label.setText(f"{config.Labels.SERIAL}: {serial}")
        self.station_label.setText(f"{config.Labels.STATION}: {station}")
        self.sip_label.setText(f"{config.Labels.SIP}: {sip}")
        
        logger.info(f"Header updated with test info: {stock}, {serial}")