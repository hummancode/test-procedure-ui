"""
Pass/Fail Input Widget
Handles GEÇTİ/KALDI checkbox input
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox, QPushButton
from PyQt5.QtCore import Qt
import config
from ui.widgets.content.input_widgets.base_input_widget import BaseInputWidget
from utils.logger import setup_logger

logger = setup_logger(__name__)


class PassFailInputWidget(BaseInputWidget):
    """
    PASS_FAIL input type: [GEÇTİ] [KALDI] [YAZ] Sonuç: [Result]
    
    Features:
    - Mutually exclusive checkboxes
    - YAZ button to confirm selection
    - Result display (green=pass, red=fail)
    """
    
    def __init__(self, validation: dict = None, parent=None):
        super().__init__(validation, parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
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
        self.pass_checkbox.stateChanged.connect(
            lambda state: self._on_checkbox_changed(state, 'pass')
        )
        
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
        self.fail_checkbox.stateChanged.connect(
            lambda state: self._on_checkbox_changed(state, 'fail')
        )
        
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
        layout.addWidget(self.pass_checkbox)
        layout.addWidget(self.fail_checkbox)
        layout.addWidget(self.write_button)
        layout.addWidget(QLabel(config.Labels.RESULT_LABEL))
        layout.addWidget(self.result_display)
        layout.addStretch()
        
        self.setLayout(layout)
        
        logger.debug("PassFailInputWidget initialized")
    
    def _on_checkbox_changed(self, state, checkbox_type):
        """Handle checkbox state change (mutually exclusive)"""
        if state == Qt.Checked:
            if checkbox_type == 'pass':
                self.fail_checkbox.setChecked(False)
            else:
                self.pass_checkbox.setChecked(False)
    
    def _on_write_clicked(self):
        """Handle YAZ button click for checkboxes"""
        # Check if at least one checkbox is selected
        if not (self.pass_checkbox.isChecked() or self.fail_checkbox.isChecked()):
            # Don't write if nothing selected
            return
        
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
        self.result_display.setText(result_text)
        self.result_display.setStyleSheet(f"""
            QLabel {{
                color: {result_color};
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
        """)
        
        # Update emoji immediately
        self.emoji_update_requested.emit(is_happy)
        
        # Mark as written
        self.result_written = True
        
        logger.info(f"Checkbox result written: {result_text}")
    
    def get_result(self) -> tuple:
        """
        Get current result value and validity.
        
        Returns:
            (checkbox_value, is_valid) tuple
            - "PASS" or "FAIL" or None
            - True if PASS, False if FAIL
        """
        result_text = self.result_display.text()
        
        if result_text == config.Labels.PASS:
            return ("PASS", True)
        elif result_text == config.Labels.FAIL:
            return ("FAIL", False)
        else:
            return (None, False)
    
    def is_result_written(self) -> bool:
        """Check if YAZ button has been clicked"""
        return self.result_written
    
    def clear(self):
        """Reset widget to initial state"""
        self.pass_checkbox.setChecked(False)
        self.fail_checkbox.setChecked(False)
        self.result_display.clear()
        self.result_written = False# -*- coding: utf-8 -*-

