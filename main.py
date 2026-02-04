# -*- coding: utf-8 -*-

"""
Test Procedure UI - Main Entry Point

Flow:
1. LoginDialog - User authentication (operator/admin selection)
2. TestSessionSetupDialog - Collect test session metadata (NEW)
3. MainWindow - Test execution

Features:
- User authentication (3-role system)
- Extended session metadata entry with memory
- Dark theme UI
"""
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from ui.main_window import MainWindow
from utils.logger import setup_logger
from utils.auth_manager import AuthManager
from utils.settings_manager import SettingsManager
from ui.dialogs.login_dialog import LoginDialog
from ui.dialogs.test_session_setup_dialog import TestSessionSetupDialog
import config
import qdarkstyle
import atexit
import signal

# Setup logger
logger = setup_logger('main')

# Global reference for cleanup
_main_window = None

def cleanup():
    """Cleanup function called on exit"""
    global _main_window
    logger.info("Application cleanup - stopping all timers")
    if _main_window is not None:
        try:
            if hasattr(_main_window, 'test_manager') and _main_window.test_manager:
                if hasattr(_main_window.test_manager, 'timer'):
                    _main_window.test_manager.timer.stop()
                    logger.info("Timer stopped")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

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
def get_bundled_path(relative_path: str) -> Path:
    """Get path to BUNDLED files (read-only, inside _internal for PyInstaller)"""
    if getattr(sys, 'frozen', False):
        # PyInstaller extracts bundled files to _MEIPASS
        base = Path(sys._MEIPASS)
    else:
        # Development mode - same as project root
        base = Path(__file__).parent
    return base / relative_path

def main():
    """Main application entry point"""
    global _main_window
    
    logger.info("=" * 60)
    logger.info("Test Procedure Application Starting")
    logger.info("=" * 60)
    
    # ========================================================================
    # Register cleanup handlers FIRST (before anything else)
    # ========================================================================
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
    
    # Get application base path
    app_path = get_application_path()
    logger.info(f"Application path: {app_path}")
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(config.WINDOW_TITLE)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    
    # Initialize managers
    auth_manager = AuthManager()
    settings_manager = SettingsManager()
    
    # ========================================================================
    # STEP 1: User Authentication
    # ========================================================================
    logger.info("Step 1: Showing login dialog...")
    login_dialog = LoginDialog(auth_manager)
    
    if login_dialog.exec_() != QDialog.Accepted:
        logger.info("Login cancelled by user - exiting application")
        sys.exit(0)
    
    # Log successful authentication
    user_role = auth_manager.get_role()
    user_name = auth_manager.get_display_name()
    logger.info(f"User authenticated: {user_name} (Role: {user_role})")
    
    # ========================================================================
    # STEP 2: Test Session Setup (NEW - Collect Metadata)
    # ========================================================================
    logger.info("Step 2: Showing test session setup dialog...")
    setup_dialog = TestSessionSetupDialog(settings_manager)
    
    if setup_dialog.exec_() != QDialog.Accepted:
        logger.info("Session setup cancelled by user - exiting application")
        sys.exit(0)
    
    # Get the metadata from the dialog
    session_metadata = setup_dialog.get_metadata()
    logger.info(f"Session metadata collected: {session_metadata}")
    
    # Create test_info dict for backwards compatibility with MainWindow
    test_info = {
        'stock_number': session_metadata.stok_no,
        'serial_number': session_metadata.seri_no,
        'station_number': session_metadata.istasyon,
        'sip_code': session_metadata.sip_code
    }
    
    # ========================================================================
    # STEP 3: Create Main Window
    # ========================================================================
    logger.info("Step 3: Creating main window...")
    window = MainWindow(auth_manager=auth_manager)
    _main_window = window  # Store global reference for cleanup
    
    # Pass the full metadata to the window (for Excel export)
    if hasattr(window, 'test_manager') and window.test_manager:
        # Store metadata in test_manager for later use
        window.test_manager.session_metadata = session_metadata
    
    # Update window title based on user role
    if auth_manager.is_admin():
        window.setWindowTitle(f"{config.WINDOW_TITLE} - YÖNETİCİ MODU")
        logger.info("Admin mode enabled - backward navigation allowed")
    else:
        window.setWindowTitle(config.WINDOW_TITLE)
        logger.info("Operator mode - sequential navigation only")
    
    # ========================================================================
    # STEP 4: Load Test Procedure
    # ========================================================================
    test_file = get_bundled_path('data/sample_test.json')

    logger.info(f"Loading test file: {test_file}")
    
    if not test_file.exists():
        logger.error(f"Test file not found: {test_file}")
        QMessageBox.critical(
            None, 
            "Hata", 
            f"Test dosyası bulunamadı:\n{test_file}"
        )
        sys.exit(1)
    
    if window.load_test_procedure(str(test_file), test_info):
        logger.info(f"Loaded test procedure: {test_file}")
        
        # Attach metadata to the session after loading
        if window.test_manager and window.test_manager.session:
            window.test_manager.session.metadata = session_metadata
            logger.info("Session metadata attached to test session")
        
        # Start the test
        window.start_test()
        
        # Show window
        window.show()
        
        logger.info("Application window displayed")
        logger.info("Use 'Dosya > Güncelleme Ayarları...' to configure data output")
    else:
        logger.error("Failed to load test procedure. Exiting.")
        QMessageBox.critical(
            None,
            "Hata",
            "Test prosedürü yüklenemedi. Uygulama kapatılıyor."
        )
        sys.exit(1)
    
    # ========================================================================
    # Run application event loop
    # ========================================================================
    exit_code = app.exec_()
    
    logger.info("=" * 60)
    logger.info(f"Application Exited with code {exit_code}")
    logger.info(f"User: {user_name} logged out")
    logger.info("=" * 60)
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()