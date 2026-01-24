"""
Main Window
Main application window with menu bar, sidebar, continuous data writing, and Excel export
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, 
                             QFileDialog, QMenuBar, QMenu, QAction, QStatusBar, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os

from ui.widgets import HeaderWidget, TitleWidget, ContentWidget, StatusBarWidget, ProgressNavigator
from ui.dialogs import UpdateSettingsDialog
from managers import TestManager
from models.enums import InputType, TimerStatus
from persistence import ContinuousWriter
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window with menu bar, sidebar, continuous data writing, and Excel export.
    
    Layout:
    - Menu Bar: File and View menus
    - Row 1: Header (test info + timestamp)
    - Row 2: Step title
    - Row 3: Content (image + description + input + export button)
    - Row 4: Status bar (timer + progress + emoji)
    - Sidebar: Progress navigator (toggleable)
    - Status Bar: Show continuous writer status
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize test manager
        self.test_manager = TestManager()
        
        # Sidebar state
        self.sidebar_visible = False
        
        # Setup UI
        self._init_ui()
        self._create_menu_bar()
        self._create_status_bar()
        self._connect_signals()
        
        logger.info("MainWindow initialized with Excel export support")
    
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
        
        # Horizontal layout for main content + sidebar
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.setSpacing(0)
        
        # Main content area (left side)
        main_content = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create all row widgets
        self.header_widget = HeaderWidget()
        self.title_widget = TitleWidget()
        self.content_widget = ContentWidget()
        self.status_bar_widget = StatusBarWidget()
        
        # Add widgets to main layout
        main_layout.addWidget(self.header_widget)
        main_layout.addWidget(self.title_widget)
        main_layout.addWidget(self.content_widget, 1)  # Stretch factor 1 (fills space)
        main_layout.addWidget(self.status_bar_widget)
        
        main_content.setLayout(main_layout)
        
        # Add main content to horizontal layout
        horizontal_layout.addWidget(main_content, 1)
        
        # Create sidebar (hidden initially)
        self.sidebar = ProgressNavigator()
        self.sidebar.hide()
        horizontal_layout.addWidget(self.sidebar)
        
        central_widget.setLayout(horizontal_layout)
        
        logger.debug("UI layout created with sidebar support")
    
    def _create_menu_bar(self):
        """Create menu bar with File and View menus"""
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
        
        # View menu
        view_menu = menubar.addMenu(config.Labels.MENU_VIEW)
        
        # Toggle sidebar action
        self.toggle_sidebar_action = QAction(config.Labels.TOGGLE_SIDEBAR, self)
        self.toggle_sidebar_action.setCheckable(True)
        self.toggle_sidebar_action.setChecked(False)
        self.toggle_sidebar_action.setShortcut("F2")
        self.toggle_sidebar_action.triggered.connect(self.toggle_sidebar)
        view_menu.addAction(self.toggle_sidebar_action)
        
        logger.debug("Menu bar created with View menu")
    
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
    
    def toggle_sidebar(self):
        """Toggle sidebar visibility"""
        self.sidebar_visible = not self.sidebar_visible
        
        if self.sidebar_visible:
            self.sidebar.show()
            logger.info("Sidebar shown")
        else:
            self.sidebar.hide()
            logger.info("Sidebar hidden")
        
        # Update menu action state
        self.toggle_sidebar_action.setChecked(self.sidebar_visible)
    
    def _connect_signals(self):
        """Connect signals between components"""
        # Test manager signals
        self.test_manager.step_changed.connect(self._on_step_changed)
        self.test_manager.timer_updated.connect(self._on_timer_updated)
        self.test_manager.test_completed.connect(self._on_test_completed)
        self.test_manager.result_submitted.connect(self._on_result_submitted)
        
        # Content widget signals
        self.content_widget.result_submitted.connect(self._on_user_submit_result)
        self.content_widget.emoji_update_requested.connect(
            lambda is_happy: self.status_bar_widget.update_emoji(is_happy)
        )
        
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
            
            # Initialize sidebar with steps
            if self.sidebar:
                self.sidebar.set_steps(self.test_manager.steps)
            
            # >>> NEW: Update export button with session <<<
            if hasattr(self.test_manager, 'session') and self.test_manager.session:
                self.content_widget.set_session(self.test_manager.session)
                logger.debug("Export button enabled with loaded session")
            
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
            # >>> NEW: Update export button with started session <<<
            if hasattr(self.test_manager, 'session') and self.test_manager.session:
                self.content_widget.set_session(self.test_manager.session)
                logger.debug("Export button updated after test start")
            
            self.status_bar.showMessage("Test başladı")
            logger.info("Test started")
        else:
            QMessageBox.critical(
                self,
                "Hata",
                "Test başlatılamadı!"
            )
    
    def _on_step_changed(self, step_index: int, total_steps: int, mode: str = 'normal'):
        """
        Handle step change event.
        
        Args:
            step_index: Current step index (0-based)
            total_steps: Total number of steps
            mode: Navigation mode (normal, view_only, edit)
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
        
        # >>> NEW: Update export button with latest session state <<<
        if hasattr(self.test_manager, 'session') and self.test_manager.session:
            self.content_widget.set_session(self.test_manager.session)
        
        # Update progress (1-based for display)
        self.status_bar_widget.update_progress(step_index + 1, total_steps)
        
        # Reset emoji to happy
        self.status_bar_widget.update_emoji(is_happy=True)
        
        # Update sidebar
        if self.sidebar:
            self.sidebar.update_current_step(step_index)
        
        logger.info(f"UI updated for step {step_index + 1}/{total_steps}: {current_step.name} (mode: {mode})")    
    
    def _on_timer_updated(self, remaining_seconds: int, timer_status: str):
        """
        Handle timer update event.
        
        Args:
            remaining_seconds: Remaining time (negative if overtime)
            timer_status: Timer status string
        """
        # Update timer display
        self.status_bar_widget.update_timer(remaining_seconds, timer_status)
        
        # Only update emoji from timer if result hasn't been written yet
        if self.content_widget.has_result_written():
            return  # Don't override emoji after result written
        
        # Update emoji based on timer
        if remaining_seconds <= 0:
            self.status_bar_widget.update_emoji(is_happy=False)
        else:
            # Check if there's a failed result
            current_step = self.test_manager.get_current_step()
            if current_step and current_step.result_value in ["FAIL", "KALDI"]:
                self.status_bar_widget.update_emoji(is_happy=False)
            else:
                self.status_bar_widget.update_emoji(is_happy=True)
    
    def _on_user_submit_result(self, result_value, checkbox_value, comment, is_valid):
        """
        Handle user submitting a result from ContentWidget.
        
        Args:
            result_value: Numeric result or None
            checkbox_value: "PASS"/"FAIL"/"GEÇTİ"/"KALDI" or None  
            comment: Comment text
            is_valid: Whether value is valid (True/False/None)
        """
        # Save comment to current step
        current_step = self.test_manager.get_current_step()
        if current_step and comment:
            current_step.comment = comment
        
        # Determine final value to submit based on input type
        if current_step.input_type == InputType.PASS_FAIL:
            # Use checkbox value for PASS/FAIL steps
            final_value = checkbox_value
        elif current_step.input_type == InputType.NUMBER:
            # Use numeric value for NUMBER steps
            final_value = result_value
        else:
            # No input required
            final_value = None
        
        # Submit to TestManager with ALL 4 parameters
        self.test_manager.submit_result(result_value, checkbox_value, comment, is_valid)
        
        logger.info(f"Result submitted: value={result_value}, checkbox={checkbox_value}, valid={is_valid}")
        
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
        
        # Update sidebar step status
        if self.sidebar:
            self.sidebar.update_step_status(step_index)
    
    def _on_test_completed(self):
        """Handle test completion"""
        self.status_bar.showMessage("Test tamamlandı!")
        
        # >>> NEW: Final update to export button with completed session <<<
        if hasattr(self.test_manager, 'session') and self.test_manager.session:
            self.content_widget.set_session(self.test_manager.session)
            logger.debug("Export button updated with completed session")
        
        # >>> OPTIONAL: Prompt for export <<<
        result = QMessageBox.question(
            self,
            "Tamamlandı",
            "Test tamamlandı!\n\nŞimdi Excel raporu oluşturmak ister misiniz?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if result == QMessageBox.Yes:
            # Trigger export button click
            if hasattr(self.content_widget, 'export_button'):
                self.content_widget.export_button.click()
        
        logger.info("Test procedure completed")