"""
Description Panel Widget
Displays scrollable test step description text
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DescriptionPanel(QWidget):
    """
    Scrollable description text area.
    
    Displays:
    - Test step description (read-only)
    - Automatic scrolling for long text
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Description text area (read-only, scrollable)
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet(f"""
            QTextEdit {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: 1px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 10px;
                font-size: {config.FONT_SIZE_DESCRIPTION}pt;
                line-height: 1.5;
            }}
        """)
        
        layout.addWidget(self.text_area)
        self.setLayout(layout)
        
        logger.debug("DescriptionPanel initialized")
    
    def set_text(self, text: str):
        """
        Set description text.
        
        Args:
            text: Description text to display
        """
        self.text_area.setPlainText(text)
        logger.debug(f"Description updated ({len(text)} chars)")# -*- coding: utf-8 -*-

