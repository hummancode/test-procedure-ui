# -*- coding: utf-8 -*-

"""
Test Procedure UI - Main Entry Point
UPDATED: Added user authentication system
Phase 1: Simple 2-step demo with Modern UI
FIXED: Correct path resolution for EXE distribution
"""
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QDialog
from qt_material import apply_stylesheet
from ui.main_window import MainWindow
from utils.logger import setup_logger
from utils.auth_manager import AuthManager
from ui.dialogs.login_dialog import LoginDialog
import config
import qdarkstyle

# Setup logger
logger = setup_logger('main')


def get_application_path():
    """
    Get the base path of the application.
    
    Works both in development and when frozen by PyInstaller.
    
    Returns:
        Path object pointing to the application base directory
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        application_path = Path(sys.executable).parent
    else:
        # Running in development
        application_path = Path(__file__).parent
    
    return application_path


def main():
    """Main application entry point"""
    logger.info("=" * 60)
    logger.info("Test Procedure Application Starting (with Authentication)")
    logger.info("=" * 60)
    
    # Get application base path
    app_path = get_application_path()
    logger.info(f"Application path: {app_path}")
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(config.WINDOW_TITLE)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    
    # ========================================================================
    # NEW: User Authentication
    # ========================================================================
    logger.info("Showing login dialog...")
    auth_manager = AuthManager()
    login_dialog = LoginDialog(auth_manager)
    
    if login_dialog.exec_() != QDialog.Accepted:
        logger.info("Login cancelled by user - exiting application")
        sys.exit(0)
    
    # Log successful authentication
    user_role = auth_manager.get_role()
    user_name = auth_manager.get_display_name()
    logger.info(f"User authenticated: {user_name} (Role: {user_role})")
    
    # ========================================================================
    # Create main window (with auth manager)
    # ========================================================================
    window = MainWindow(auth_manager=auth_manager)
    
    # Update window title based on user role
    if auth_manager.is_admin():
        window.setWindowTitle(f"{config.WINDOW_TITLE} - YÖNETİCİ MODU")
        logger.info("Admin mode enabled - backward navigation allowed")
    else:
        window.setWindowTitle(config.WINDOW_TITLE)
        logger.info("Operator mode - sequential navigation only")
    
    # ========================================================================
    # Load test procedure
    # ========================================================================
    # Test info - in real application, this would come from user input or database
    test_info = {
        'stock_number': 'ABC123',
        'serial_number': '456789',
        'station_number': 'ST-01',
        'sip_code': 'X99'
    }
    
    # Load test procedure - USE ABSOLUTE PATH
    test_file = app_path / 'data' / 'sample_test.json'
    logger.info(f"Loading test file: {test_file}")
    
    if not test_file.exists():
        logger.error(f"Test file not found: {test_file}")
        logger.error(f"Current working directory: {os.getcwd()}")
        logger.error(f"Application path: {app_path}")
        logger.error(f"Contents of app path: {list(app_path.iterdir())}")
        sys.exit(1)
    
    if window.load_test_procedure(str(test_file), test_info):
        logger.info(f"Loaded test procedure: {test_file}")
        
        # Start the test
        window.start_test()
        
        # Show window
        window.show()
        
        logger.info("Application window displayed")
        logger.info("Use 'Dosya > Güncelleme Ayarları...' to configure data output")
    else:
        logger.error("Failed to load test procedure. Exiting.")
        sys.exit(1)
    
    # Run application event loop
    exit_code = app.exec_()
    
    logger.info("=" * 60)
    logger.info(f"Application Exited with code {exit_code}")
    logger.info(f"User: {user_name} logged out")
    logger.info("=" * 60)
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()