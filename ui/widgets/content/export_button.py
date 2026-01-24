"""
Export Button Widget
Handles Excel export functionality with folder selection
"""
from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from typing import Optional

from exporters.excel_exporter import ExcelExporter
from models.test_session import TestSession
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ExportButton(QPushButton):
    """
    Export button widget for generating Excel reports.
    
    Features:
    - Opens folder selection dialog
    - Exports test results to Excel
    - Shows success/error messages
    - Styled to match app theme
    
    Signals:
        export_completed: Emitted when export succeeds (filepath)
        export_failed: Emitted when export fails (error_message)
    """
    
    export_completed = pyqtSignal(str)  # filepath
    export_failed = pyqtSignal(str)     # error_message
    
    def __init__(self, parent=None):
        super().__init__(config.Labels.REPORT, parent)
        
        self.session: Optional[TestSession] = None
        self.exporter = ExcelExporter()
        self.last_export_folder = config.EXPORT_DIR
        
        self._init_ui()
        self._connect_signals()
        
        logger.debug("ExportButton initialized")
    
    def _init_ui(self):
        """Initialize button styling"""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.SUCCESS};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                padding: 12px 24px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: #66bb6a;
            }}
            QPushButton:pressed {{
                background-color: {config.Colors.SUCCESS};
            }}
            QPushButton:disabled {{
                background-color: {config.Colors.TEXT_DISABLED};
            }}
        """)
        
        # Disabled by default (no session loaded)
        self.setEnabled(False)
    
    def _connect_signals(self):
        """Connect button click signal"""
        self.clicked.connect(self._on_export_clicked)
    
    def set_session(self, session: Optional[TestSession]):
        """
        Set the test session to export.
        
        Args:
            session: TestSession object or None
        """
        self.session = session
        self.setEnabled(session is not None)
        
        if session:
            logger.debug(f"Export button enabled for session: {session.session_id}")
        else:
            logger.debug("Export button disabled (no session)")
    
    def _on_export_clicked(self):
        """Handle export button click"""
        if not self.session:
            logger.warning("Export clicked but no session available")
            return
        
        # Open folder selection dialog
        folder = QFileDialog.getExistingDirectory(
            self,
            config.Labels.SELECT_EXPORT_FOLDER,
            self.last_export_folder,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if not folder:
            logger.debug("Export cancelled by user")
            return
        
        # Save selected folder for next time
        self.last_export_folder = folder
        
        # Generate filename
        filepath = self.exporter.generate_filename(self.session, folder)
        
        # Export to Excel
        success = self.exporter.export_session(self.session, filepath)
        
        if success:
            # Show success message
            QMessageBox.information(
                self,
                config.Labels.EXPORT_SUCCESS_TITLE,
                f"{config.Labels.EXPORT_SUCCESS_MESSAGE}\n\n{filepath}"
            )
            self.export_completed.emit(filepath)
            logger.info(f"Excel export successful: {filepath}")
        else:
            # Show error message
            QMessageBox.critical(
                self,
                config.Labels.EXPORT_ERROR_TITLE,
                config.Labels.EXPORT_ERROR_MESSAGE
            )
            self.export_failed.emit("Export failed")
            logger.error("Excel export failed")