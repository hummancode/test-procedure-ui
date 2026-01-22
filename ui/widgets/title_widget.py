"""
Title Widget - Row 2 (PHASE 1 UPDATED)
Displays current test step title with proper padding
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TitleWidget(QWidget):
    """
    Row 2: Test Step Title
    
    Displays the name/title of the current test step.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the UI components"""
        # Set fixed height
        self.setFixedHeight(config.ROW_2_HEIGHT)
        
        # Set background color
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
        """)
        
        # Create layout with padding
        layout = QHBoxLayout()
        layout.setContentsMargins(
            config.ROW_2_PADDING_LEFT,
            config.ROW_2_PADDING_TOP,
            config.ROW_2_PADDING_RIGHT,
            config.ROW_2_PADDING_BOTTOM
        )
        
        # Create title label
        self.title_label = QLabel("---")
        self.title_label.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_LARGE}pt;
            font-weight: bold;
            color: {config.Colors.TEXT_PRIMARY};
        """)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title_label.setWordWrap(False)
        
        layout.addWidget(self.title_label)
        
        self.setLayout(layout)
        
        logger.debug("TitleWidget initialized")
    
    def set_title(self, title: str):
        """
        Set the step title.
        
        Args:
            title: The step title/name to display
        """
        self.title_label.setText(title)
        logger.debug(f"Title updated: {title}")