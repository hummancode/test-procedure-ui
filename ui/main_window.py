"""
Main Window
Main application window with menu bar for continuous data writing
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QMessageBox, 
                             QFileDialog, QMenuBar, QMenu, QAction, QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os

from ui.widgets import HeaderWidget, TitleWidget, ContentWidget, StatusBarWidget
from ui.dialogs import UpdateSettingsDialog
from managers import TestManager
from models.enums import InputType, TimerStatus
from persistence import ContinuousWriter
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window with menu bar and continuous data writing.
    
    Layout:
    - Menu Bar: File menu with continuous update file selection
    - Row 1: Header (test info + timestamp)
    - Row 2: Step title
    - Row 3: Content (image + description + input)
    - Row 4: Status bar (timer + progress + emoji)
    - Status Bar: Show continuous writer status
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize test manager
        self.test_manager = TestManager()
        
        # Setup UI
        self._init_ui()
        self._create_menu_bar()
        self._create_status_bar()
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
    
    def _create_menu_bar(self):
        """Create menu bar with File menu"""
        menubar = self.menuBar()
        menubar.setStyleSheet(f"""
            QMenuBar {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                color: {config.Colors.TEXT_PRIMARY};
                padding: 4px;
            }}
            QMenuBar::item:selected {{
                background-color: {config.Colors.ACCENT_BLUE};
            }}
            QMenu {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: 1px solid {config.Colors.BORDER_COLOR};
            }}
            QMenu::item:selected {{
                background-color: {config.Colors.ACCENT_BLUE};
            }}
        """)
        
        # File menu
        file_menu = menubar.addMenu(config.Labels.MENU_FILE)
        
        # Update settings action
        self.update_settings_action = QAction(config.Labels.MENU_UPDATE_SETTINGS, self)
        self.update_settings_action.triggered.connect(self._on_open_update_settings)
        file_menu.addAction(self.update_settings_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction(config.Labels.MENU_EXIT, self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        logger.debug("Menu bar created")
    
    def _create_status_bar(self):
        """Create status bar to show continuous writer status"""
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {config.Colors.BACKGROUND_TERTIARY};
                color: {config.Colors.TEXT_SECONDARY};
                padding: 2px;
            }}
        """)
        self.setStatusBar(self.status_bar)
        
        # Show current update folder on startup
        current_folder = self.test_manager.continuous_writer.get_current_directory()
        self.status_bar.showMessage(f"Güncelleme klasörü: {current_folder}")
        
        logger.debug("Status bar created")
    
    def _connect_signals(self):
        """Connect signals between components"""
        # Test manager signals
        self.test_manager.step_changed.connect(self._on_step_changed)
        self.test_manager.timer_updated.connect(self._on_timer_updated)
        self.test_manager.test_completed.connect(self._on_test_completed)
        self.test_manager.result_submitted.connect(self._on_result_submitted)
        self.test_manager.data_updated.connect(self._on_data_updated)
        
        # Content widget signals
        self.content_widget.result_submitted.connect(self._on_user_submit_result)
        
        logger.debug("Signals connected")
    
    def _on_open_update_settings(self):
        """Open update settings dialog"""
        dialog = UpdateSettingsDialog(
            self.test_manager.continuous_writer.settings,
            self
        )
        dialog.settings_changed.connect(self._on_settings_changed)
        dialog.exec_()
    
    def _on_settings_changed(self):
        """Handle settings changed - update the continuous writer"""
        # Reload folder from settings
        new_folder = self.test_manager.continuous_writer.settings.get_update_folder()
        self.test_manager.set_continuous_output_directory(new_folder)
        
        # Update interval (will be used on next timer tick)
        new_interval = self.test_manager.continuous_writer.settings.get_update_interval()
        
        # Update status bar
        self.status_bar.showMessage(
            f"Güncelleme klasörü: {new_folder} | Her {new_interval}s"
        )
        
        logger.info(f"Settings updated: folder={new_folder}, interval={new_interval}s")
    
    def _on_data_updated(self):
        """Handle data update event"""
        # Could add visual feedback here (e.g., flash icon in status bar)
        logger.debug("Session data written to file")
    
    def load_test_procedure(self, filepath: str, test_info: dict) -> bool:
        """
        Load test procedure from JSON file.
        
        Args:
            filepath: Path to JSON file
            test_info: Dict with test metadata (stock_number, etc.)
            
        Returns:
            True if loaded successfully
        """
        success = self.test_manager.load_test_from_file(filepath, test_info)
        
        if success:
            # Update header with test info
            self.header_widget.set_test_info(test_info)
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
        if self.test_manager.session is None or not self.test_manager.session.steps:
            QMessageBox.warning(
                self,
                "Uyarı",
                "Test prosedürü yüklenmedi!"
            )
            return
        
        success = self.test_manager.start_test()
        if success:
            self.status_bar.showMessage("Test başladı")
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
        
        # Update status bar
        self.status_bar.showMessage(f"Adım {step_index + 1}/{total_steps}: {current_step.name}")
        
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
    
    def _on_user_submit_result(self, result_value, checkbox_value, comment, is_valid):
        """
        Handle user submitting a result.
        
        Args:
            result_value: Value from NUMBER input (or None)
            checkbox_value: Value from PASS/FAIL checkbox (or None)  
            comment: Optional comment text
            is_valid: True/False/None validation result
        """
        # Save comment to current step
        current_step = self.test_manager.get_current_step()
        if current_step and comment:
            current_step.comment = comment
        
        # Determine which value to use based on input type
        if current_step and current_step.input_type == InputType.PASS_FAIL:
            # For checkboxes, use checkbox_value ("PASS" or "FAIL")
            final_value = checkbox_value
        elif current_step and current_step.input_type == InputType.NUMBER:
            # For numbers, use result_value
            final_value = result_value
        else:
            # For NONE type
            final_value = None
        
        # Submit to TestManager
        success = self.test_manager.submit_result(final_value)
        
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
        self.status_bar.showMessage("Test tamamlandı!")
        
        QMessageBox.information(
            self,
            "Tamamlandı",
            config.Labels.TEST_COMPLETE
        )
        logger.info("Test procedure completed")
        
        # Could add export functionality here in future