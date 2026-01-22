"""
Logging Configuration
Simple logging setup for the application
"""
import logging
import sys
from config import LOG_LEVEL, LOG_FORMAT


def setup_logger(name: str, level: str = LOG_LEVEL) -> logging.Logger:
    """
    Setup and configure a logger.
    
    Args:
        name: Logger name (usually __name__ of the module)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    
    Example:
        >>> logger = setup_logger(__name__)
        >>> logger.info("Application started")
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Set level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger


# Create default application logger
app_logger = setup_logger('test_procedure_app')