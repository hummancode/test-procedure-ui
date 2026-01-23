"""
Content Widget - Row 3 (REFACTORED)
Main orchestrator for content area components
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal
from typing import Optional

import config
from models.enums import InputType
from ui.widgets.content.image_viewer import ImageViewer
from ui.widgets.content.description_panel import DescriptionPanel
from ui.widgets.content.input_widgets import NumberInputWidget, PassFailInputWidget
from ui.widgets.content.button_panel import ButtonPanel
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ContentWidget(QWidget):
    """
    Row 3: Main Content Area (Refactored Orchestrator)
    
    Layout:
    - Left (40%): ImageViewer
    - Right (60%): DescriptionPanel + Input widgets + ButtonPanel
    
    Signals:
        result_submitted: (result_value, checkbox_value, comment, is_valid)
        emoji_update_requested: (is_happy)
    """
    
    result_submitted = pyqtSignal(object, object, str, object)
    emoji_update_requested = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_input_type = InputType.NONE
        self.current_input_widget = None
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.Colors.BACKGROUND_PRIMARY};
            }}
        """)
        
        # Main horizontal layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Left: Image viewer (40%)
        self.image_viewer = ImageViewer()
        main_layout.addWidget(self.image_viewer, 40)
        
        # Right: Content area (60%)
        right_container = self._create_right_container()
        main_layout.addWidget(right_container, 60)
        
        self.setLayout(main_layout)
        
        logger.debug("ContentWidget initialized (refactored)")
    
    def _create_right_container(self) -> QWidget:
        """Create right side container with description + input + buttons"""
        container = QWidget()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(
            config.ROW_3_DESCRIPTION_PADDING,
            config.ROW_3_DESCRIPTION_PADDING,
            config.ROW_3_DESCRIPTION_PADDING,
            config.ROW_3_DESCRIPTION_PADDING
        )
        layout.setSpacing(15)
        
        # Description panel (50%)
        self.description_panel = DescriptionPanel()
        layout.addWidget(self.description_panel, 50)
        
        # Input container (35%)
        self.input_container = QWidget()
        self.input_layout = QVBoxLayout()
        self.input_layout.setContentsMargins(0, 0, 0, 0)
        self.input_container.setLayout(self.input_layout)
        layout.addWidget(self.input_container, 35)
        
        # Error label
        self.error_label = QLabel()
        self.error_label.setStyleSheet(f"""
            color: {config.Colors.ERROR};
            font-size: {config.FONT_SIZE_ERROR}pt;
        """)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        # Button panel (15%)
        self.button_panel = ButtonPanel()
        self.button_panel.proceed_clicked.connect(self._on_proceed_clicked)
        layout.addWidget(self.button_panel, 15)
        
        container.setLayout(layout)
        return container
    
    def set_step_content(self, step_name: str, description: str, image_path: Optional[str],
                        input_type: InputType, input_label: str = "Test Sonucu",
                        input_validation: dict = None):
        """
        Update content for current step.
        
        Args:
            step_name: Step name
            description: Step description
            image_path: Image file path
            input_type: InputType enum
            input_label: Input field label (unused in refactored version)
            input_validation: Validation rules
        """
        # Update image
        self.image_viewer.load_image(image_path)
        
        # Update description
        self.description_panel.set_text(description)
        
        # Clear previous input widget
        if self.current_input_widget:
            self.input_layout.removeWidget(self.current_input_widget)
            self.current_input_widget.deleteLater()
            self.current_input_widget = None
        
        # Create new input widget based on type
        self.current_input_type = input_type
        
        if input_type == InputType.NUMBER:
            self.current_input_widget = NumberInputWidget(input_validation)
            self.current_input_widget.emoji_update_requested.connect(
                self.emoji_update_requested.emit
            )
            self.input_layout.addWidget(self.current_input_widget)
        
        elif input_type == InputType.PASS_FAIL:
            self.current_input_widget = PassFailInputWidget(input_validation)
            self.current_input_widget.emoji_update_requested.connect(
                self.emoji_update_requested.emit
            )
            self.input_layout.addWidget(self.current_input_widget)
        
        # Clear error and comment
        self.error_label.hide()
        self.button_panel.clear_comment()
        
        logger.info(f"Content updated for step: {step_name} (type: {input_type.value})")
    
    def _on_proceed_clicked(self):
        """Handle İlerle button click"""
        # Handle InputType.NONE - no validation needed
        if self.current_input_type == InputType.NONE:
            comment = self.button_panel.get_comment()
            self.result_submitted.emit(None, None, comment, None)
            logger.info("NONE type step - proceeding without validation")
            return
        
        # Validate that result has been written
        if not self.current_input_widget or not self.current_input_widget.is_result_written():
            QMessageBox.warning(
                self,
                config.Labels.WARNING_TITLE,
                config.Labels.NO_VALUE_WRITTEN
            )
            return
        
        # Get result and validity
        result_value, checkbox_value, is_valid = self._get_result_values()
        comment = self.button_panel.get_comment()
        
        # Emit result
        self.result_submitted.emit(result_value, checkbox_value, comment, is_valid)
        logger.info(f"Result submitted: {result_value}/{checkbox_value}, valid={is_valid}")
    
    def _get_result_values(self) -> tuple:
        """
        Get result values from current input widget.
        
        Returns:
            (result_value, checkbox_value, is_valid) tuple
        """
        if self.current_input_type == InputType.NUMBER:
            result_value, is_valid = self.current_input_widget.get_result()
            return (result_value, None, is_valid)
        
        elif self.current_input_type == InputType.PASS_FAIL:
            checkbox_value, is_valid = self.current_input_widget.get_result()
            return (None, checkbox_value, is_valid)
        
        return (None, None, False)
    
    def has_result_written(self) -> bool:
        """Check if result has been written"""
        if self.current_input_widget:
            return self.current_input_widget.is_result_written()
        return False# -*- coding: utf-8 -*-

