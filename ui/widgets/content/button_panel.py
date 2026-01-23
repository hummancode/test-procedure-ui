"""
Button Panel Widget
Contains comment field and İlerle button
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import pyqtSignal
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ButtonPanel(QWidget):
    """
    Button panel for test step actions.
    
    Contains:
    - YORUM EKLE button (toggles comment field)
    - Comment text field (hidden by default)
    - İlerle > button (proceed to next step)
    
    Signals:
        proceed_clicked: Emitted when İlerle clicked
    """
    
    proceed_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Comment text area (hidden by default)
        self.comment_text = QTextEdit()
        self.comment_text.setPlaceholderText(config.Labels.COMMENT_PLACEHOLDER)
        self.comment_text.setMaximumHeight(config.COMMENT_FIELD_HEIGHT)
        self.comment_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
            }}
        """)
        self.comment_text.hide()
        
        # Button container
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        
        # YORUM EKLE button
        self.comment_button = QPushButton(config.Labels.ADD_COMMENT)
        self.comment_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_SECONDARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
                min-width: {config.BUTTON_COMMENT_WIDTH}px;
                min-height: {config.BUTTON_COMMENT_HEIGHT}px;
            }}
            QPushButton:hover {{
                background-color: #9e9e9e;
            }}
        """)
        self.comment_button.clicked.connect(self._toggle_comment)
        
        # İlerle button
        self.proceed_button = QPushButton(config.Labels.PROCEED)
        self.proceed_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                padding: 12px 24px;
                font-size: {config.FONT_SIZE_BUTTON}pt;
                font-weight: bold;
                min-width: {config.BUTTON_PROCEED_WIDTH}px;
                min-height: {config.BUTTON_PROCEED_HEIGHT}px;
            }}
            QPushButton:hover {{
                background-color: {config.Colors.BUTTON_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {config.Colors.ACCENT_BLUE};
            }}
        """)
        self.proceed_button.clicked.connect(self._on_proceed_clicked)
        
        # Add to button layout
        button_layout.addWidget(self.comment_button)
        button_layout.addStretch()
        button_layout.addWidget(self.proceed_button)
        button_container.setLayout(button_layout)
        
        # Add to main layout
        layout.addWidget(self.comment_text)
        layout.addWidget(button_container)
        
        self.setLayout(layout)
        
        logger.debug("ButtonPanel initialized")
    
    def _toggle_comment(self):
        """Toggle comment field visibility"""
        if self.comment_text.isVisible():
            self.comment_text.hide()
            self.comment_button.setText(config.Labels.ADD_COMMENT)
        else:
            self.comment_text.show()
            self.comment_text.setFocus()
            self.comment_button.setText(config.Labels.HIDE_COMMENT)
    
    def _on_proceed_clicked(self):
        """Handle İlerle button click"""
        self.proceed_clicked.emit()
    
    def get_comment(self) -> str:
        """
        Get comment text.
        
        Returns:
            Comment text (empty string if none)
        """
        return self.comment_text.toPlainText().strip()
    
    def clear_comment(self):
        """Clear comment field and hide it"""
        self.comment_text.clear()
        self.comment_text.hide()
        self.comment_button.setText(config.Labels.ADD_COMMENT)# -*- coding: utf-8 -*-

