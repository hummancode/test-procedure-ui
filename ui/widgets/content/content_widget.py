"""
Content Widget - Row 3 (STEP 1: BOTTOM SECTION REORGANIZED)
Main orchestrator with all controls in single horizontal row

CHANGES FROM ORIGINAL:
1. Description panel gets 80% vertical space (was 50%)
2. All controls moved to single horizontal row (15% space)
3. Image padding reduced from 10px to 5px
4. Button heights standardized to 45px
5. Logical left-to-right flow for controls
"""
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                             QMessageBox, QPushButton, QTextEdit)
from PyQt5.QtCore import pyqtSignal
from typing import Optional

import config
from models.enums import InputType
from ui.widgets.content.image_viewer import ImageViewer
from ui.widgets.content.description_panel import DescriptionPanel
from ui.widgets.content.input_widgets import NumberInputWidget, PassFailInputWidget
from ui.widgets.content.export_button import ExportButton
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ContentWidget(QWidget):
    """
    Row 3: Main Content Area (REORGANIZED - Step 1)
    
    Layout:
    - Left (40%): ImageViewer (reduced padding for larger image)
    - Right (60%): 
        - DescriptionPanel (80% - MORE SPACE)
        - Single horizontal control row (15%)
        - Comment field (5%, hidden by default)
    
    NEW: All controls in ONE horizontal row:
    [Input widgets] [YAZ] Sonuç:__ [Raporla] [YORUM EKLE] [İlerle >]
    
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
        self.comment_visible = False
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
        # CHANGE: Reduce padding in ImageViewer for larger image display
        main_layout.addWidget(self.image_viewer, 40)
        
        # Right: Content area (60%)
        right_container = self._create_right_container()
        main_layout.addWidget(right_container, 60)
        
        self.setLayout(main_layout)
        
        logger.debug("ContentWidget initialized (Step 1: Reorganized)")
    
    def _create_right_container(self) -> QWidget:
        """Create right side with NEW single-row controls layout"""
        container = QWidget()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(
            config.ROW_3_DESCRIPTION_PADDING,
            config.ROW_3_DESCRIPTION_PADDING,
            config.ROW_3_DESCRIPTION_PADDING,
            config.ROW_3_DESCRIPTION_PADDING
        )
        layout.setSpacing(15)
        
        # CHANGE 1: Description panel - NOW GETS 80% of vertical space (was 50%)
        self.description_panel = DescriptionPanel()
        layout.addWidget(self.description_panel, 80)
        
        # CHANGE 2: NEW single horizontal row for ALL controls (15% of space)
        self.controls_row = self._create_controls_row()
        layout.addWidget(self.controls_row, 15)
        
        # CHANGE 3: Comment field (5% of space, shown below controls when toggled)
        self.comment_field = QTextEdit()
        self.comment_field.setPlaceholderText(config.Labels.COMMENT_PLACEHOLDER)
        self.comment_field.setMaximumHeight(80)
        self.comment_field.setStyleSheet(f"""
            QTextEdit {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
            }}
        """)
        self.comment_field.hide()
        layout.addWidget(self.comment_field, 5)
        
        # Error label
        self.error_label = QLabel()
        self.error_label.setStyleSheet(f"""
            color: {config.Colors.ERROR};
            font-size: {config.FONT_SIZE_ERROR}pt;
        """)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        container.setLayout(layout)
        return container
    
    def _create_controls_row(self) -> QWidget:
        """
        NEW METHOD: Create single horizontal row with all controls:
        [Input widgets] [YAZ] Sonuç:__ [Raporla] [YORUM EKLE] [İlerle >]
        
        Layout flow (left to right):
        1. Input section (NUMBER or PASS/FAIL widgets dynamically inserted)
        2. Stretch (pushes action buttons to the right)
        3. Raporla (Export) button
        4. YORUM EKLE (Comment toggle) button
        5. İlerle > (Proceed) button
        """
        container = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        
        # Section 1: Input widgets container (left side, dynamic content)
        self.input_container = QWidget()
        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(0, 0, 0, 0)
        self.input_layout.setSpacing(10)
        self.input_container.setLayout(self.input_layout)
        main_layout.addWidget(self.input_container)
        
        # Add stretch to push action buttons to the right
        main_layout.addStretch(1)
        
        # Section 2: Export button (Raporla)
        self.export_button = ExportButton()
        # CHANGE: Standardized height
        self.export_button.setFixedHeight(45)
        main_layout.addWidget(self.export_button)
        
        # Section 3: Comment toggle button (YORUM EKLE)
        self.comment_button = QPushButton(config.Labels.ADD_COMMENT)
        self.comment_button.setFixedHeight(45)  # CHANGE: Standardized height
        self.comment_button.setMinimumWidth(120)
        self.comment_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 10px 20px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                border-color: {config.Colors.ACCENT_BLUE};
            }}
            QPushButton:checked {{
                background-color: {config.Colors.ACCENT_BLUE};
                border-color: {config.Colors.ACCENT_BLUE};
            }}
        """)
        self.comment_button.setCheckable(True)
        self.comment_button.clicked.connect(self._on_comment_toggle)
        main_layout.addWidget(self.comment_button)
        
        # Section 4: Proceed button (İlerle >)
        self.proceed_button = QPushButton(config.Labels.PROCEED)
        self.proceed_button.setFixedHeight(45)  # CHANGE: Standardized height
        self.proceed_button.setMinimumWidth(100)
        self.proceed_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {config.Colors.BUTTON_HOVER};
            }}
        """)
        self.proceed_button.clicked.connect(self._on_proceed_clicked)
        main_layout.addWidget(self.proceed_button)
        
        container.setLayout(main_layout)
        return container
    
    def _on_comment_toggle(self):
        """Toggle comment field visibility"""
        self.comment_visible = not self.comment_visible
        if self.comment_visible:
            self.comment_field.show()
            self.comment_button.setText(config.Labels.HIDE_COMMENT)
        else:
            self.comment_field.hide()
            self.comment_button.setText(config.Labels.ADD_COMMENT)
    
    def get_comment(self) -> str:
        """Get comment text"""
        return self.comment_field.toPlainText().strip()
    
    def clear_comment(self):
        """Clear comment field and reset state"""
        self.comment_field.clear()
        self.comment_field.hide()
        self.comment_visible = False
        self.comment_button.setChecked(False)
        self.comment_button.setText(config.Labels.ADD_COMMENT)
    
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
            input_label: Input field label (unused)
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
        self.clear_comment()
        
        logger.info(f"Content updated for step: {step_name} (type: {input_type.value})")
    
    def set_session(self, session):
        """
        Update the export button with current test session.
        
        Args:
            session: TestSession object containing test data and results
        """
        if hasattr(self, 'export_button'):
            self.export_button.set_session(session)
            logger.debug(f"Export button updated with session: {session.session_id if session else None}")
    
    def _on_proceed_clicked(self):
        """Handle İlerle button click"""
        # Handle InputType.NONE - no validation needed
        if self.current_input_type == InputType.NONE:
            comment = self.get_comment()
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
        comment = self.get_comment()
        
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
        return False