"""
Test Procedure UI - Main Entry Point
Phase 1: Simple 2-step demo with Modern UI
"""
import sys
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet
from ui.main_window import MainWindow
from utils.logger import setup_logger
import config
import qdarkstyle


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
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    # Create main window
    window = MainWindow()
    
    # Test info - in real application, this would come from user input or database
    test_info = {
        'stock_number': 'ABC123',
        'serial_number': '456789',
        'station_number': 'ST-01',
        'sip_code': 'X99'
    }
    
    # Load test procedure
    test_file = 'data/sample_test.json'
    if window.load_test_procedure(test_file, test_info):
        logger.info(f"Loaded test procedure: {test_file}")
        
        # Start the test
        window.start_test()
        
        # Show window
        window.show()
        
        logger.info("Application window displayed")
        logger.info("Use 'Dosya > Güncelleme Dosyası Seç...' to enable continuous data writing")
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