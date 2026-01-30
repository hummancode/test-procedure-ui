"""
Image Viewer Widget (STEP 1 UPDATE: Reduced padding)
Displays test step images with fallback placeholder
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from typing import Optional
import os
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ImageViewer(QWidget):
    """
    Image display widget for test steps.
    
    STEP 1 CHANGE: Reduced padding from 10px to 5px for larger image display
    
    Displays:
    - Test step image (scaled to fit)
    - Placeholder text if no image
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                border: 1px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
            }}
        """)
        
        layout = QVBoxLayout()
        # CHANGE: Reduced padding from 10 to 5 for larger image display
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(False)
        self.image_label.setStyleSheet("border: none;")
        
        # Load placeholder by default
        self.show_placeholder()
        
        layout.addWidget(self.image_label)
        self.setLayout(layout)
        
        logger.debug("ImageViewer initialized (Step 1: Reduced padding)")
    
    def load_image(self, image_path: Optional[str]):
        """
        Load and display image.
        
        Args:
            image_path: Path to image file (or None for placeholder)
        """
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Scale to fit while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                logger.debug(f"Image loaded: {image_path}")
                return
        
        # Fallback to placeholder
        self.show_placeholder()
    
    def show_placeholder(self):
        """Display placeholder text when no image available"""
        self.image_label.clear()
        self.image_label.setText("Görsel Yok")
        self.image_label.setStyleSheet(f"""
            color: {config.Colors.TEXT_SECONDARY};
            font-size: 18pt;
            border: none;
        """)
        logger.debug("Placeholder image displayed")