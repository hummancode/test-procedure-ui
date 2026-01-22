"""
Main Window (PHASE 1 UPDATED)
Main application window that orchestrates all widgets and managers
"""
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.widgets.header_widget import HeaderWidget
from ui.widgets.title_widget import TitleWidget
from ui.widgets.content_widget import ContentWidget
from ui.widgets.status_bar_widget import StatusBarWidget
from managers import TestManager
from models.enums import InputType, TimerStatus
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window.
    
    Layout:
    - Row 1: Header (test info + timestamp)
    - Row 2: Step title
    - Row 3: Content (image + description + input)
    - Row 4: Status bar (timer + progress + emoji)
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize test manager
        self.test_manager = TestManager()
        
        # Setup UI
        self._init_ui()
        self._connect_signals()
        
        logger.info("MainWindow initialized")
    
    def _init_ui(self):
        """Initialize the user interface"""
        # Window settings
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setMinimumSize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        
        # Set dark blue background and theme
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {config.Colors.BACKGROUND_PRIMARY};
            }}
            
            /* Style QMessageBox for dark theme */
            QMessageBox {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
            QMessageBox QLabel {{
                color: {config.Colors.TEXT_PRIMARY};
                font-size: {config.FONT_SIZE}pt;
            }}
            QMessageBox QPushButton {{
                background-color: {config.Colors.BUTTON_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: {config.FONT_SIZE}pt;
                min-width: 80px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {config.Colors.BUTTON_HOVER};
            }}
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, config.ROW_4_BOTTOM_MARGIN)
        main_layout.setSpacing(0)
        
        # Create all row widgets
        self.header_widget = HeaderWidget()
        self.title_widget = TitleWidget()
        self.content_widget = ContentWidget()
        self.status_bar_widget = StatusBarWidget()
        
        # Add widgets to layout
        main_layout.addWidget(self.header_widget)
        main_layout.addWidget(self.title_widget)
        main_layout.addWidget(self.content_widget, 1)  # Stretch factor 1 (fills space)
        main_layout.addWidget(self.status_bar_widget)
        
        central_widget.setLayout(main_layout)
        
        logger.debug("UI layout created")
    
    def _connect_signals(self):
        """Connect signals between components"""
        # Test manager signals
        self.test_manager.step_changed.connect(self._on_step_changed)
        self.test_manager.timer_updated.connect(self._on_timer_updated)
        self.test_manager.test_completed.connect(self._on_test_completed)
        self.test_manager.result_submitted.connect(self._on_result_submitted)
        
        # Content widget signals - UPDATED for flexible workflow
        # New signature: (result_value, checkbox_value, comment, is_valid)
        self.content_widget.result_submitted.connect(self._on_user_submit_result)
        
        # Emoji update signal - NEW: Update emoji when YAZ button is clicked
        self.content_widget.emoji_update_requested.connect(self._on_emoji_update_requested)
        
        logger.debug("Signals connected")
    
    def load_test_procedure(self, filepath: str) -> bool:
        """
        Load test procedure from JSON file.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            True if loaded successfully
        """
        success = self.test_manager.load_test_from_file(filepath)
        
        if success:
            # Update header with test info
            self.header_widget.set_test_info(self.test_manager.test_info)
            logger.info(f"Test procedure loaded: {filepath}")
        else:
            QMessageBox.critical(
                self,
                config.Labels.ERROR_TITLE,
                f"Test dosyası yüklenemedi: {filepath}"
            )
            logger.error(f"Failed to load test procedure: {filepath}")
        
        return success
    
    def start_test(self):
        """Start the test procedure"""
        if not self.test_manager.steps:
            QMessageBox.warning(
                self,
                config.Labels.WARNING_TITLE,
                "Test prosedürü yüklenmedi!"
            )
            return
        
        success = self.test_manager.start_test()
        if success:
            logger.info("Test started")
        else:
            QMessageBox.critical(
                self,
                config.Labels.ERROR_TITLE,
                "Test başlatılamadı!"
            )
    
    def _on_step_changed(self, step_index: int, total_steps: int):
        """
        Handle step change event.
        
        Args:
            step_index: Current step index (0-based)
            total_steps: Total number of steps
        """
        current_step = self.test_manager.get_current_step()
        if current_step is None:
            return
        
        # Update title
        self.title_widget.set_title(current_step.name)
        
        # Update content
        self.content_widget.set_step_content(
            step_name=current_step.name,
            description=current_step.description,
            image_path=current_step.image_path,
            input_type=current_step.input_type,
            input_label=current_step.input_label,
            input_validation=current_step.input_validation
        )
        
        # Update progress (1-based for display)
        self.status_bar_widget.update_progress(step_index + 1, total_steps)
        
        # Reset emoji to happy
        self.status_bar_widget.update_emoji(is_happy=True)
        
        logger.info(f"UI updated for step {step_index + 1}/{total_steps}: {current_step.name}")
    
    def _on_timer_updated(self, remaining_seconds: int, timer_status: str):
        """
        Handle timer update event.
        
        Args:
            remaining_seconds: Remaining time (negative if overtime)
            timer_status: Timer status string
        """
        # Update timer display
        self.status_bar_widget.update_timer(remaining_seconds, timer_status)
        
        # Only update emoji if no result has been written yet
        # (YAZ button sets the emoji and shouldn't be overridden by timer)
        if self.content_widget.has_result_written():
            # Result already written - don't override emoji
            return
        
        # Update emoji based on timer
        if remaining_seconds <= 0:
            self.status_bar_widget.update_emoji(is_happy=False)
        else:
            # Check if there's a failed result
            current_step = self.test_manager.get_current_step()
            if current_step and current_step.result_value == "FAIL":
                self.status_bar_widget.update_emoji(is_happy=False)
            else:
                self.status_bar_widget.update_emoji(is_happy=True)
    
    def _on_user_submit_result(self, result_value, checkbox_value, comment, is_valid):
        """
        Handle user submitting a result (UPDATED for flexible workflow).
        
        Args:
            result_value: Numeric result value (or None)
            checkbox_value: "PASS" or "FAIL" (or None)
            comment: Comment text (may be empty string)
            is_valid: True if valid, False if failed, None if N/A
        """
        # Determine the actual result to submit
        # Priority: checkbox_value > result_value
        final_result = checkbox_value if checkbox_value is not None else result_value
        
        # Get current step
        current_step = self.test_manager.get_current_step()
        if not current_step:
            return
        
        # Save comment if provided
        if comment:
            current_step.comment = comment
            logger.info(f"Comment saved: {comment}")
        
        # Determine test status based on is_valid
        if is_valid is None:
            # No input required - intermediate step
            test_status = "not_applicable"
        elif is_valid is True:
            # Valid input - passed
            test_status = "passed"
        else:
            # Invalid input or FAIL checkbox - failed
            test_status = "failed"
        
        # Submit result to test manager with status
        success = self.test_manager.submit_result(final_result, test_status)
        
        if success:
            logger.info(f"Step completed with status: {test_status}")
        else:
            QMessageBox.warning(
                self,
                config.Labels.WARNING_TITLE,
                config.Labels.INVALID_INPUT
            )
            logger.warning("Failed to submit result")
    
    def _on_emoji_update_requested(self, is_happy: bool):
        """
        Handle emoji update request from content widget.
        Called when YAZ button writes a result.
        
        Args:
            is_happy: True for happy, False for sad
        """
        self.status_bar_widget.update_emoji(is_happy)
        logger.debug(f"Emoji updated: {'happy' if is_happy else 'sad'}")
    
    def _on_result_submitted(self, step_index: int, result_value, status: str):
        """
        Handle result submission confirmation from manager.
        
        Args:
            step_index: Step index that was completed
            result_value: The submitted result
            status: Step status (passed/failed)
        """
        logger.info(f"Step {step_index + 1} result: {result_value} ({status})")
        
        # Update emoji based on result
        if status == "passed":
            self.status_bar_widget.update_emoji(is_happy=True)
        else:
            self.status_bar_widget.update_emoji(is_happy=False)
    
    def _on_test_completed(self):
        """Handle test completion"""
        QMessageBox.information(
            self,
            config.Labels.SUCCESS_TITLE,
            config.Labels.TEST_COMPLETE
        )
        logger.info("Test procedure completed")
        
        # Could add export functionality here in future