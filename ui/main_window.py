"""
Main Window
Main application window that orchestrates all widgets and managers
"""
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.widgets import HeaderWidget, TitleWidget, ContentWidget, StatusBarWidget
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
        
        # Set dark blue background
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {config.Colors.BACKGROUND_PRIMARY};
            }}
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
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
        
        # Content widget signals
        self.content_widget.result_submitted.connect(self._on_user_submit_result)
        
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
                "Hata",
                f"Test dosyası yüklenemedi: {filepath}"
            )
            logger.error(f"Failed to load test procedure: {filepath}")
        
        return success
    
    def start_test(self):
        """Start the test procedure"""
        if not self.test_manager.steps:
            QMessageBox.warning(
                self,
                "Uyarı",
                "Test prosedürü yüklenmedi!"
            )
            return
        
        success = self.test_manager.start_test()
        if success:
            logger.info("Test started")
        else:
            QMessageBox.critical(
                self,
                "Hata",
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
    
    def _on_user_submit_result(self, result_value):
        """
        Handle user submitting a result.
        
        Args:
            result_value: The result value entered by user
        """
        success = self.test_manager.submit_result(result_value)
        
        if not success:
            QMessageBox.warning(
                self,
                "Uyarı",
                config.Labels.INVALID_INPUT
            )
            logger.warning("Invalid input rejected")
    
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
            "Tamamlandı",
            config.Labels.TEST_COMPLETE
        )
        logger.info("Test procedure completed")
        
        # Could add export functionality here in future