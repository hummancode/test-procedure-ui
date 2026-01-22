"""
Test Procedure UI - Main Entry Point
Phase 1: Simple 2-step demo
"""
import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.logger import setup_logger
import config

# Setup logger
logger = setup_logger('main')


def main():
    """Main application entry point"""
    logger.info("=" * 60)
    logger.info("Test Procedure Application Starting")
    logger.info("=" * 60)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(config.WINDOW_TITLE)
    
    # Create main window
    window = MainWindow()

    # Load test procedure
    test_file = 'data/sample_test.json'
    if window.load_test_procedure(test_file):
        logger.info(f"Loaded test procedure: {test_file}")
        
        # Start the test
        window.start_test()
        
        # Show window
        window.show()
        
        logger.info("Application window displayed")
    else:
        logger.error("Failed to load test procedure. Exiting.")
        sys.exit(1)
    
    # Run application event loop
    exit_code = app.exec_()
    
    logger.info("=" * 60)
    logger.info(f"Application Exited with code {exit_code}")
    logger.info("=" * 60)
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()