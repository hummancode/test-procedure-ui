"""
Configuration and Constants for Test Procedure UI
Phase 1 - Simplified Configuration
"""

# ============================================================================
# COLOR PALETTE (Dark Blue Theme)
# ============================================================================

class Colors:
    """Color definitions for the UI theme"""
    # Primary Colors
    BACKGROUND_PRIMARY = "#1a237e"      # Deep dark blue
    BACKGROUND_SECONDARY = "#283593"    # Medium blue
    BACKGROUND_TERTIARY = "#3949ab"     # Lighter blue
    
    # Text Colors
    TEXT_PRIMARY = "#ffffff"            # White
    TEXT_SECONDARY = "#b0bec5"          # Light gray
    TEXT_DISABLED = "#757575"           # Medium gray
    
    # Accent Colors
    ACCENT_BLUE = "#2196f3"             # Bright blue (primary actions)
    ACCENT_LIGHT = "#64b5f6"            # Light blue (hover states)
    
    # Status Colors
    SUCCESS = "#4caf50"                 # Green (passed, on-time)
    WARNING = "#ff9800"                 # Orange (approaching limit)
    ERROR = "#f44336"                   # Red (failed, overtime)
    INFO = "#2196f3"                    # Blue (informational)
    
    # UI Element Colors
    BORDER_COLOR = "#455a64"            # Subtle borders
    INPUT_BACKGROUND = "#37474f"        # Input fields, image containers
    BUTTON_PRIMARY = "#2196f3"          # Action buttons
    BUTTON_HOVER = "#42a5f5"            # Button hover state


# ============================================================================
# TURKISH UI LABELS
# ============================================================================

class Labels:
    """Turkish language labels for UI elements"""
    # Header Row
    STOCK_NO = "STOK NO"
    SERIAL = "SERİ"
    STATION = "İSTASYON"
    SIP = "SİP"
    
    # Input Labels
    TEST_RESULT = "Test Sonucu"
    COMMENT = "Yorum"
    COMMENT_PLACEHOLDER = "Adım hakkında yorum ekleyin..."
    
    # Buttons
    SUBMIT = "KAYDET VE DEVAM"
    PASS = "BAŞARILI"
    FAIL = "BAŞARISIZ"
    
    # Status Bar
    STEP = "Adım"
    RESERVED = "Ayrılmış"
    
    # Messages
    INVALID_INPUT = "Geçersiz giriş. Lütfen kontrol edin."
    TEST_COMPLETE = "Test tamamlandı!"


# ============================================================================
# WINDOW SETTINGS
# ============================================================================

WINDOW_MIN_WIDTH = 1024
WINDOW_MIN_HEIGHT = 768
WINDOW_TITLE = "Test Prosedürü Uygulaması"

# Font Settings
FONT_SIZE = 10
FONT_SIZE_LARGE = 14
FONT_SIZE_TIMER = 24


# ============================================================================
# TIMER SETTINGS
# ============================================================================

TIMER_UPDATE_INTERVAL = 1000  # milliseconds (1 second)

# Timer color thresholds (percentage of time remaining)
TIMER_WARNING_THRESHOLD = 20  # Yellow when < 20% time left
TIMER_CRITICAL_THRESHOLD = 10  # Red when < 10% time left


# ============================================================================
# ROW HEIGHTS (pixels)
# ============================================================================

ROW_1_HEIGHT = 35  # Header info bar
ROW_2_HEIGHT = 45  # Step title
ROW_4_HEIGHT = 70  # Status bar
# ROW_3 is flexible (fills remaining space)


# ============================================================================
# IMAGE SETTINGS
# ============================================================================

IMAGE_MAX_SIZE_MB = 10
SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg', '.bmp']
PLACEHOLDER_IMAGE_PATH = "resources/images/placeholder.png"


# ============================================================================
# DATE/TIME FORMATS
# ============================================================================

DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"  # DD/MM/YYYY HH:MM:SS (Turkish format)
TIME_FORMAT = "%H:%M:%S"


# ============================================================================
# PATHS
# ============================================================================

DATA_DIR = "data"
RESOURCES_DIR = "resources"
IMAGES_DIR = "resources/images"


# ============================================================================
# LOGGING
# ============================================================================

LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


# ============================================================================
# STATUS EMOJIS
# ============================================================================

EMOJI_HAPPY = "😊"
EMOJI_SAD = "☹️"
EMOJI_NEUTRAL = "😐"