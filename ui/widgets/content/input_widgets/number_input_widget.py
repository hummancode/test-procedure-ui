"""
Number Input Widget
Handles numeric input with validation
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import config
from ui.widgets.content.input_widgets.base_input_widget import BaseInputWidget
from utils.logger import setup_logger

logger = setup_logger(__name__)


class NumberInputWidget(BaseInputWidget):
    """
    NUMBER input type: [Input] [YAZ] [Result]
    
    UPDATED: Removed "Sonuç:" label, result displays directly with larger font
    
    Features:
    - Numeric input field
    - YAZ button to confirm entry
    - Result display (green=valid, orange=invalid)
    - Range validation (allows invalid but marks as failed)
    """
    
    def __init__(self, validation: dict = None, parent=None):
        super().__init__(validation, parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
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
        
        # Result display - BIGGER FONT, NO LABEL
        self.result_display = QLabel("")
        self.result_display.setMinimumWidth(config.RESULT_DISPLAY_MIN_WIDTH)
        self.result_display.setStyleSheet(f"""
            QLabel {{
                color: {config.Colors.SUCCESS};
                font-size: 20pt;
                font-weight: bold;
            }}
        """)
        
        # Add to layout - NO "Sonuç:" LABEL ANYMORE
        layout.addWidget(self.number_input)
        layout.addWidget(self.write_button)
        layout.addWidget(self.result_display)  # Just the value!
        layout.addStretch()
        
        self.setLayout(layout)
        
        logger.debug("NumberInputWidget initialized (no Sonuç label, bigger font)")
    
    def _on_write_clicked(self):
        """Handle YAZ button click - ALLOWS INVALID VALUES"""
        input_text = self.number_input.text().strip()
        
        if not input_text:
            # Don't write empty values
            return
        
        # Try to parse as number
        try:
            value = float(input_text)
        except ValueError:
            # Invalid number format - don't write
            return
        
        # Check if value is in valid range
        is_valid = self._check_number_range(value)
        
        if not is_valid:
            # Write in ORANGE (warning color) - BIGGER FONT
            self.result_display.setText(input_text)
            self.result_display.setStyleSheet(f"""
                QLabel {{
                    color: {config.Colors.WARNING};
                    font-size: 20pt;
                    font-weight: bold;
                }}
            """)
            
            # Update emoji to sad (invalid = failed)
            self.emoji_update_requested.emit(False)
        else:
            # Write in GREEN (valid) - BIGGER FONT
            self.result_display.setText(input_text)
            self.result_display.setStyleSheet(f"""
                QLabel {{
                    color: {config.Colors.SUCCESS};
                    font-size: 20pt;
                    font-weight: bold;
                }}
            """)
            
            # Update emoji to happy (valid = passed)
            self.emoji_update_requested.emit(True)
        
        # Mark as written
        self.result_written = True
        
        logger.info(f"Value written: {input_text} (valid={is_valid})")
    
    def _check_number_range(self, value: float) -> bool:
        """
        Check if number is in valid range.
        
        Args:
            value: Number to check
            
        Returns:
            True if valid, False if out of range
        """
        min_val = self.validation.get('min')
        max_val = self.validation.get('max')
        
        if min_val is not None and value < min_val:
            return False
        
        if max_val is not None and value > max_val:
            return False
        
        return True
    
    def get_result(self) -> tuple:
        """
        Get current result value and validity.
        
        Returns:
            (result_value, is_valid) tuple
        """
        result_text = self.result_display.text()
        
        if not result_text:
            return (None, False)
        
        try:
            value = float(result_text)
            is_valid = self._check_number_range(value)
            return (result_text, is_valid)
        except ValueError:
            return (result_text, False)
    
    def is_result_written(self) -> bool:
        """Check if YAZ button has been clicked"""
        return self.result_written
    
    def clear(self):
        """Reset widget to initial state"""
        self.number_input.clear()
        self.result_display.clear()
        self.result_written = False