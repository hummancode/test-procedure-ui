"""
Content Widget - Row 3
Main content area: Image + Description + Input
"""
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                             QTextEdit, QLineEdit, QPushButton, QScrollArea,
                             QMessageBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
from typing import Optional
import os
import config
from models.enums import InputType
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ContentWidget(QWidget):
    """
    Row 3: Main Content Area
    
    Left side (40%): Test step image
    Right side (60%): Description + Input + Submit button
    
    Signals:
        result_submitted: Emitted when user submits result (result_value)
    """
    
    result_submitted = pyqtSignal(object)  # result_value
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_input_type = InputType.NONE
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the UI components"""
        # Set background
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.Colors.BACKGROUND_PRIMARY};
            }}
        """)
        
        # Main horizontal layout (40% image | 60% content)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Left: Image container (40%)
        self.image_container = self._create_image_container()
        main_layout.addWidget(self.image_container, 40)
        
        # Right: Description + Input container (60%)
        self.content_container = self._create_content_container()
        main_layout.addWidget(self.content_container, 60)
        
        self.setLayout(main_layout)
        
        logger.debug("ContentWidget initialized")
    
    def _create_image_container(self) -> QWidget:
        """Create the image display area"""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                border: 1px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(False)
        self.image_label.setStyleSheet("border: none;")
        
        # Load placeholder by default
        self._load_placeholder_image()
        
        layout.addWidget(self.image_label)
        container.setLayout(layout)
        
        return container
    
    def _create_content_container(self) -> QWidget:
        """Create the description + input area"""
        container = QWidget()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Description area (scrollable)
        self.description_area = QTextEdit()
        self.description_area.setReadOnly(True)
        self.description_area.setStyleSheet(f"""
            QTextEdit {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: 1px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 10px;
                font-size: {config.FONT_SIZE}pt;
                line-height: 1.5;
            }}
        """)
        
        layout.addWidget(self.description_area, 70)  # 70% of space
        
        # Input section (conditional, will be shown/hidden)
        self.input_container = self._create_input_container()
        layout.addWidget(self.input_container, 30)  # 30% of space
        
        container.setLayout(layout)
        return container
    
    def _create_input_container(self) -> QWidget:
        """Create the input section (hidden by default)"""
        container = QWidget()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Input label
        self.input_label = QLabel(config.Labels.TEST_RESULT)
        self.input_label.setStyleSheet(f"""
            color: {config.Colors.TEXT_PRIMARY};
            font-size: {config.FONT_SIZE}pt;
            font-weight: bold;
        """)
        
        # Input widget placeholder (will be replaced based on type)
        self.input_widget_container = QWidget()
        self.input_widget_layout = QVBoxLayout()
        self.input_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.input_widget_container.setLayout(self.input_widget_layout)
        
        # Error message label
        self.error_label = QLabel()
        self.error_label.setStyleSheet(f"color: {config.Colors.ERROR}; font-size: 9pt;")
        self.error_label.hide()
        
        # Submit button
        self.submit_button = QPushButton(config.Labels.SUBMIT)
        self.submit_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                padding: 12px 24px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
                min-width: 200px;
            }}
            QPushButton:hover {{
                background-color: {config.Colors.BUTTON_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {config.Colors.ACCENT_BLUE};
            }}
        """)
        self.submit_button.clicked.connect(self._on_submit_clicked)
        
        # Add to layout
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_widget_container)
        layout.addWidget(self.error_label)
        
        # Right-align submit button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        layout.addLayout(button_layout)
        
        container.setLayout(layout)
        container.hide()  # Hidden by default
        
        return container
    
    def set_step_content(self, step_name: str, description: str, image_path: Optional[str],
                        input_type: InputType, input_label: str = "Test Sonucu",
                        input_validation: dict = None):
        """
        Update content for current step.
        
        Args:
            step_name: Step name/title
            description: Step description text
            image_path: Path to image file (or None)
            input_type: Type of input required
            input_label: Label for input field
            input_validation: Validation rules dict
        """
        # Update description
        self.description_area.setPlainText(description)
        
        # Update image
        self._load_image(image_path)
        
        # Update input section
        self.current_input_type = input_type
        self.input_label.setText(input_label)
        
        if input_type != InputType.NONE:
            self._setup_input_widget(input_type, input_validation or {})
            self.input_container.show()
        else:
            self.input_container.hide()
        
        # Clear error
        self.error_label.hide()
        
        logger.info(f"Content updated for step: {step_name}")
    
    def _setup_input_widget(self, input_type: InputType, validation: dict):
        """Setup input widget based on type"""
        # Clear existing widget
        for i in reversed(range(self.input_widget_layout.count())): 
            self.input_widget_layout.itemAt(i).widget().setParent(None)
        
        if input_type == InputType.NUMBER:
            self._create_number_input(validation)
        elif input_type == InputType.PASS_FAIL:
            self._create_pass_fail_input()
        elif input_type == InputType.COMMENT:
            self._create_comment_input()
    
    def _create_number_input(self, validation: dict):
        """Create numeric input field"""
        self.number_input = QDoubleSpinBox()
        self.number_input.setDecimals(2)
        self.number_input.setMinimum(validation.get('min', -999999))
        self.number_input.setMaximum(validation.get('max', 999999))
        self.number_input.setValue(validation.get('min', 0))
        self.number_input.setStyleSheet(f"""
            QDoubleSpinBox {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
            }}
        """)
        
        self.input_widget_layout.addWidget(self.number_input)
    
    def _create_pass_fail_input(self):
        """Create PASS/FAIL buttons"""
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # PASS button
        self.pass_button = QPushButton(config.Labels.PASS)
        self.pass_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.SUCCESS};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 15px 30px;
                font-size: {config.FONT_SIZE_LARGE}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #66bb6a;
            }}
        """)
        self.pass_button.clicked.connect(lambda: self._on_pass_fail_clicked("PASS"))
        
        # FAIL button
        self.fail_button = QPushButton(config.Labels.FAIL)
        self.fail_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.ERROR};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 15px 30px;
                font-size: {config.FONT_SIZE_LARGE}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #ef5350;
            }}
        """)
        self.fail_button.clicked.connect(lambda: self._on_pass_fail_clicked("FAIL"))
        
        button_layout.addWidget(self.pass_button)
        button_layout.addWidget(self.fail_button)
        button_container.setLayout(button_layout)
        
        self.input_widget_layout.addWidget(button_container)
        
        # Hide submit button for PASS/FAIL (buttons submit directly)
        self.submit_button.hide()
    
    def _create_comment_input(self):
        """Create comment text area"""
        self.comment_input = QTextEdit()
        self.comment_input.setPlaceholderText(config.Labels.COMMENT_PLACEHOLDER)
        self.comment_input.setMaximumHeight(80)
        self.comment_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
            }}
        """)
        
        self.input_widget_layout.addWidget(self.comment_input)
    
    def _on_pass_fail_clicked(self, result: str):
        """Handle PASS/FAIL button click"""
        self.result_submitted.emit(result)
        logger.info(f"PASS/FAIL result: {result}")
    
    def _on_submit_clicked(self):
        """Handle submit button click"""
        result = self._get_input_value()
        
        if result is None:
            self.error_label.setText(config.Labels.INVALID_INPUT)
            self.error_label.show()
            return
        
        self.error_label.hide()
        self.result_submitted.emit(result)
        logger.info(f"Result submitted: {result}")
    
    def _get_input_value(self) -> Optional[object]:
        """Get current input value based on type"""
        if self.current_input_type == InputType.NUMBER:
            return self.number_input.value()
        elif self.current_input_type == InputType.COMMENT:
            text = self.comment_input.toPlainText().strip()
            return text if text else None
        elif self.current_input_type == InputType.PASS_FAIL:
            return None  # Handled by buttons
        
        return None
    
    def _load_image(self, image_path: Optional[str]):
        """Load and display image"""
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
        
        # Load placeholder if image not found
        self._load_placeholder_image()
    
    def _load_placeholder_image(self):
        """Load placeholder image or show text"""
        # For now, just show text placeholder
        self.image_label.setText("Görsel Yok")
        self.image_label.setStyleSheet(f"""
            color: {config.Colors.TEXT_SECONDARY};
            font-size: 18pt;
            border: none;
        """)
        logger.debug("Placeholder image displayed")