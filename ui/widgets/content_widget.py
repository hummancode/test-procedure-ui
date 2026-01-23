"""
Content Widget - Row 3 (PHASE 1 UPDATED - İLERLE BUTTON FIX)
Main content area: Image + Description + Input + Buttons

FIX: İlerle button now ALWAYS visible, even for InputType.NONE steps
"""
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                             QTextEdit, QLineEdit, QPushButton, QCheckBox,
                             QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
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
    Right side (60%): Description + Input (conditional) + Buttons (ALWAYS visible)
    
    Signals:
        result_submitted: Emitted when user clicks İlerle and validation passes
                         (result_value, checkbox_value, comment, is_valid)
        emoji_update_requested: Emitted to update emoji immediately (is_happy)
    """
    
    result_submitted = pyqtSignal(object, object, str, object)  # result, checkbox, comment, is_valid
    emoji_update_requested = pyqtSignal(bool)  # is_happy - NEW signal for immediate emoji updates
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_input_type = InputType.NONE
        self.current_validation = {}
        self.result_written = False  # Track if YAZ button has been clicked
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the UI components"""
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
        """Create the description + input + button area"""
        container = QWidget()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(
            config.ROW_3_DESCRIPTION_PADDING,
            config.ROW_3_DESCRIPTION_PADDING,
            config.ROW_3_DESCRIPTION_PADDING,
            config.ROW_3_DESCRIPTION_PADDING
        )
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
                font-size: {config.FONT_SIZE_DESCRIPTION}pt;
                line-height: 1.5;
            }}
        """)
        
        layout.addWidget(self.description_area, 50)  # 50% of space
        
        # Input section (conditional, will be hidden for NONE type)
        self.input_container = self._create_input_container()
        layout.addWidget(self.input_container, 35)  # 35% of space
        
        # ════════════════════════════════════════════════════════
        # FIX: Button section separate from input (ALWAYS VISIBLE)
        # ════════════════════════════════════════════════════════
        self.button_section = self._create_button_section()
        layout.addWidget(self.button_section, 15)  # 15% of space
        
        container.setLayout(layout)
        return container
    
    def _create_input_container(self) -> QWidget:
        """Create the input section (hidden by default, shown only for NUMBER/PASS_FAIL)"""
        container = QWidget()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # Input widget placeholder (will be replaced based on type)
        self.input_widget_container = QWidget()
        self.input_widget_layout = QVBoxLayout()
        self.input_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.input_widget_layout.setSpacing(10)
        self.input_widget_container.setLayout(self.input_widget_layout)
        
        # Error message label (for inline validation errors)
        self.error_label = QLabel()
        self.error_label.setStyleSheet(f"""
            color: {config.Colors.ERROR};
            font-size: {config.FONT_SIZE_ERROR}pt;
        """)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        
        # Add to layout
        layout.addWidget(self.input_widget_container)
        layout.addWidget(self.error_label)
        
        container.setLayout(layout)
        container.hide()  # Hidden by default
        
        return container
    
    def _create_button_section(self) -> QWidget:
        """
        Create button section (ALWAYS VISIBLE, separate from input_container).
        Contains: YORUM EKLE button, Comment field (toggled), İlerle button
        """
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Comment text area (hidden by default, toggled by YORUM EKLE)
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
        
        # Button container (YORUM EKLE + İlerle)
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        
        # YORUM EKLE button (left)
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
        
        # Spacer
        button_layout.addWidget(self.comment_button)
        button_layout.addStretch()
        
        # İlerle button (right) - ALWAYS VISIBLE
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
        
        button_layout.addWidget(self.proceed_button)
        button_container.setLayout(button_layout)
        
        # Add to main layout
        layout.addWidget(self.comment_text)
        layout.addWidget(button_container)
        
        container.setLayout(layout)
        return container
    
    def _toggle_comment(self):
        """Toggle comment field visibility"""
        if self.comment_text.isVisible():
            self.comment_text.hide()
            self.comment_button.setText(config.Labels.ADD_COMMENT)
        else:
            self.comment_text.show()
            self.comment_text.setFocus()
            self.comment_button.setText(config.Labels.HIDE_COMMENT)
    
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
        
        # Store current validation rules
        self.current_input_type = input_type
        self.current_validation = input_validation or {}
        
        # Update input section
        if input_type != InputType.NONE:
            self._setup_input_widget(input_type, self.current_validation)
            self.input_container.show()
        else:
            self.input_container.hide()  # Hide input widgets for NONE type
        
        # Button section is ALWAYS visible (now separate from input_container)
        self.button_section.show()
        
        # Reset comment
        self.comment_text.clear()
        self.comment_text.hide()
        self.comment_button.setText(config.Labels.ADD_COMMENT)
        
        # Clear error
        self.error_label.hide()
        
        # Reset result_written flag for new step
        self.result_written = False
        
        logger.info(f"Content updated for step: {step_name}")
    
    def _setup_input_widget(self, input_type: InputType, validation: dict):
        """Setup input widget based on type"""
        # Clear existing widgets
        for i in reversed(range(self.input_widget_layout.count())): 
            widget = self.input_widget_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        if input_type == InputType.NUMBER:
            self._create_number_input(validation)
        elif input_type == InputType.PASS_FAIL:
            self._create_pass_fail_input()
    
    def _create_number_input(self, validation: dict):
        """Create NUMBER input: [Input] [YAZ] Sonuç: [Result]"""
        # Container for horizontal layout
        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Input field
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText(config.Labels.ENTER_VALUE)
        self.number_input.setFixedWidth(config.INPUT_FIELD_WIDTH)
        self.number_input.setFixedHeight(config.INPUT_FIELD_HEIGHT)
        self.number_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
            }}
            QLineEdit:focus {{
                border: 2px solid {config.Colors.ACCENT_BLUE};
            }}
        """)
        
        # YAZ button
        self.write_button = QPushButton(config.Labels.WRITE)
        self.write_button.setFixedWidth(config.BUTTON_WRITE_WIDTH)
        self.write_button.setFixedHeight(config.BUTTON_WRITE_HEIGHT)
        self.write_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {config.Colors.BUTTON_HOVER};
            }}
        """)
        self.write_button.clicked.connect(self._on_write_clicked)
        
        # Result display
        self.result_display = QLabel("")
        self.result_display.setMinimumWidth(config.RESULT_DISPLAY_MIN_WIDTH)
        self.result_display.setStyleSheet(f"""
            QLabel {{
                color: {config.Colors.SUCCESS};
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
        """)
        
        # Add to layout
        layout.addWidget(self.number_input)
        layout.addWidget(self.write_button)
        layout.addWidget(QLabel(config.Labels.RESULT_LABEL))
        layout.addWidget(self.result_display)
        layout.addStretch()
        
        container.setLayout(layout)
        self.input_widget_layout.addWidget(container)
    
    def _create_pass_fail_input(self):
        """Create PASS_FAIL checkboxes with YAZ button: [GEÇTİ] [KALDI] [YAZ] Sonuç: [Result]"""
        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(config.CHECKBOX_SPACING)
        
        # GEÇTİ checkbox
        self.pass_checkbox = QCheckBox(config.Labels.PASS)
        self.pass_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {config.Colors.TEXT_PRIMARY};
                font-size: {config.FONT_SIZE}pt;
                spacing: 10px;
            }}
            QCheckBox::indicator {{
                width: 25px;
                height: 25px;
            }}
        """)
        self.pass_checkbox.stateChanged.connect(lambda state: self._on_checkbox_changed(state, 'pass'))
        
        # KALDI checkbox
        self.fail_checkbox = QCheckBox(config.Labels.FAIL)
        self.fail_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {config.Colors.TEXT_PRIMARY};
                font-size: {config.FONT_SIZE}pt;
                spacing: 10px;
            }}
            QCheckBox::indicator {{
                width: 25px;
                height: 25px;
            }}
        """)
        self.fail_checkbox.stateChanged.connect(lambda state: self._on_checkbox_changed(state, 'fail'))
        
        # YAZ button for checkboxes
        self.checkbox_write_button = QPushButton(config.Labels.WRITE)
        self.checkbox_write_button.setFixedWidth(config.BUTTON_WRITE_WIDTH)
        self.checkbox_write_button.setFixedHeight(config.BUTTON_WRITE_HEIGHT)
        self.checkbox_write_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {config.Colors.BUTTON_HOVER};
            }}
        """)
        self.checkbox_write_button.clicked.connect(self._on_checkbox_write_clicked)
        
        # Result display for checkbox
        self.checkbox_result_display = QLabel("")
        self.checkbox_result_display.setMinimumWidth(config.RESULT_DISPLAY_MIN_WIDTH)
        self.checkbox_result_display.setStyleSheet(f"""
            QLabel {{
                color: {config.Colors.SUCCESS};
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
        """)
        
        # Add to layout
        layout.addWidget(self.pass_checkbox)
        layout.addWidget(self.fail_checkbox)
        layout.addWidget(self.checkbox_write_button)
        layout.addWidget(QLabel(config.Labels.RESULT_LABEL))
        layout.addWidget(self.checkbox_result_display)
        layout.addStretch()
        
        container.setLayout(layout)
        self.input_widget_layout.addWidget(container)
    
    def _on_checkbox_changed(self, state, checkbox_type):
        """Handle checkbox state change (mutually exclusive)"""
        if state == Qt.Checked:
            if checkbox_type == 'pass':
                self.fail_checkbox.setChecked(False)
            else:
                self.pass_checkbox.setChecked(False)
    
    def _on_checkbox_write_clicked(self):
        """Handle YAZ button click for checkboxes"""
        # Check if at least one checkbox is selected
        if not (self.pass_checkbox.isChecked() or self.fail_checkbox.isChecked()):
            self.error_label.setText(config.Labels.NO_CHECKBOX_SELECTED)
            self.error_label.show()
            return
        
        # Clear error
        self.error_label.hide()
        
        # Determine which checkbox is selected
        if self.pass_checkbox.isChecked():
            result_text = config.Labels.PASS  # "GEÇTİ"
            result_color = config.Colors.SUCCESS  # Green
            is_happy = True
        else:  # fail_checkbox is checked
            result_text = config.Labels.FAIL  # "KALDI"
            result_color = config.Colors.ERROR  # Red
            is_happy = False
        
        # Write to result display
        self.checkbox_result_display.setText(result_text)
        self.checkbox_result_display.setStyleSheet(f"""
            QLabel {{
                color: {result_color};
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
        """)
        
        # UPDATE EMOJI immediately when checkbox result is written
        self._update_parent_emoji(is_happy)
        
        # Set flag to prevent timer from overriding
        self.result_written = True
        
        logger.info(f"Checkbox result written: {result_text}")
    
    def _on_write_clicked(self):
        """Handle YAZ button click - ALLOWS INVALID VALUES"""
        input_text = self.number_input.text().strip()
        
        if not input_text:
            self.error_label.setText(config.Labels.ENTER_VALUE_FIRST)
            self.error_label.show()
            return
        
        # Try to parse as number
        try:
            value = float(input_text)
        except ValueError:
            self.error_label.setText(config.Labels.INVALID_NUMBER)
            self.error_label.show()
            return
        
        # Check if value is in valid range
        is_valid, error_msg = self._check_number_range(value)
        
        if not is_valid:
            # CHANGED: Show warning but ALLOW writing the value
            self.error_label.setText(f"⚠️ {error_msg} (Değer kaydedilecek ama TEST BAŞARISIZ)")
            self.error_label.setStyleSheet(f"""
                color: {config.Colors.WARNING};
                font-size: {config.FONT_SIZE_ERROR}pt;
                font-weight: bold;
            """)
            self.error_label.show()
            
            # Write to result display but in ORANGE (warning color)
            self.result_display.setText(input_text)
            self.result_display.setStyleSheet(f"""
                QLabel {{
                    color: {config.Colors.WARNING};
                    font-size: {config.FONT_SIZE}pt;
                    font-weight: bold;
                }}
            """)
            
            # UPDATE EMOJI to sad (invalid = failed)
            self._update_parent_emoji(is_happy=False)
            
            # Set flag to prevent timer from overriding
            self.result_written = True
        else:
            # Valid value - clear error
            self.error_label.hide()
            
            # Write to result display in GREEN
            self.result_display.setText(input_text)
            self.result_display.setStyleSheet(f"""
                QLabel {{
                    color: {config.Colors.SUCCESS};
                    font-size: {config.FONT_SIZE}pt;
                    font-weight: bold;
                }}
            """)
            
            # UPDATE EMOJI to happy (valid = passed)
            self._update_parent_emoji(is_happy=True)
            
            # Set flag to prevent timer from overriding
            self.result_written = True
        
        logger.info(f"Value written to result: {input_text} (valid={is_valid})")
    
    def _update_parent_emoji(self, is_happy: bool):
        """
        Request parent window to update emoji.
        Called when YAZ button writes a result.
        
        Args:
            is_happy: True for happy face, False for sad face
        """
        self.emoji_update_requested.emit(is_happy)
    
    def _check_number_range(self, value: float) -> tuple:
        """
        Check if number is in valid range.
        Returns: (is_valid, error_message)
        Does NOT prevent invalid values, just checks them.
        """
        min_val = self.current_validation.get('min')
        max_val = self.current_validation.get('max')
        
        if min_val is not None and value < min_val:
            return (False, config.Labels.VALUE_TOO_LOW.format(min_val))
        
        if max_val is not None and value > max_val:
            return (False, config.Labels.VALUE_TOO_HIGH.format(max_val))
        
        return (True, "")
    
    def _on_proceed_clicked(self):
        """Handle İlerle button click with validation"""
        # ════════════════════════════════════════════════════════
        # FIX: Handle InputType.NONE - proceed without validation
        # ════════════════════════════════════════════════════════
        if self.current_input_type == InputType.NONE:
            # No input required - proceed directly
            result_value = None
            checkbox_value = None
            comment = self.comment_text.toPlainText().strip()
            is_value_valid = None  # None means N/A
            
            self.result_submitted.emit(result_value, checkbox_value, comment, is_value_valid)
            logger.info("Intermediate step (NONE) - proceeding without input validation")
            return
        
        # Validate based on input type (only checks if required fields are filled)
        is_valid, error_msg = self._validate_before_proceed()
        
        if not is_valid:
            # Show popup warning
            QMessageBox.warning(
                self,
                config.Labels.WARNING_TITLE,
                error_msg
            )
            return
        
        # Get values and determine if they pass validation criteria
        result_value = None
        checkbox_value = None
        is_value_valid = True  # Track if value meets criteria
        
        if self.current_input_type == InputType.NUMBER:
            result_value = self.result_display.text()
            
            # Check if the value is within valid range
            try:
                value = float(result_value)
                is_value_valid, _ = self._check_number_range(value)
            except ValueError:
                is_value_valid = False
                
        elif self.current_input_type == InputType.PASS_FAIL:
            # Get result from display, not directly from checkboxes
            result_text = self.checkbox_result_display.text()
            
            if result_text == config.Labels.PASS:  # "GEÇTİ"
                checkbox_value = "PASS"
                is_value_valid = True
            elif result_text == config.Labels.FAIL:  # "KALDI"
                checkbox_value = "FAIL"
                is_value_valid = False
        
        # Get comment
        comment = self.comment_text.toPlainText().strip()
        
        # Emit signal with validation status
        self.result_submitted.emit(result_value, checkbox_value, comment, is_value_valid)
        logger.info(f"Result submitted - Value: {result_value}, Checkbox: {checkbox_value}, "
                   f"Comment: {comment}, Valid: {is_value_valid}")
    
    def _validate_before_proceed(self) -> tuple:
        """
        Validate required inputs before proceeding.
        Returns: (is_valid, error_message)
        """
        if self.current_input_type == InputType.NUMBER:
            if not self.result_display.text().strip():
                return (False, config.Labels.NO_VALUE_WRITTEN)
        
        elif self.current_input_type == InputType.PASS_FAIL:
            # Check result display, not checkboxes
            if not self.checkbox_result_display.text().strip():
                return (False, config.Labels.NO_CHECKBOX_SELECTED)
        
        # No input required or validation passed
        return (True, "")
    
    def has_result_written(self) -> bool:
        """Check if YAZ button has been clicked and result written"""
        return self.result_written
    
    def _load_image(self, image_path: Optional[str]):
        """Load and display image"""
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                logger.debug(f"Image loaded: {image_path}")
                return
        
        self._load_placeholder_image()
    
    def _load_placeholder_image(self):
        """Load placeholder image or show text"""
        self.image_label.setText("Görsel Yok")
        self.image_label.setStyleSheet(f"""
            color: {config.Colors.TEXT_SECONDARY};
            font-size: 18pt;
            border: none;
        """)
        logger.debug("Placeholder image displayed")