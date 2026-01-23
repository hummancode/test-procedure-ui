"""
Configuration and Constants for Test Procedure UI
Phase 2 - Updated with larger fonts, new UI elements, and continuous writing
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
    BUTTON_SECONDARY = "#757575"        # Secondary buttons (like comment)


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
    RESULT_LABEL = "Sonuç:"
    ENTER_VALUE = "Değer girin..."
    COMMENT = "Yorum"
    COMMENT_PLACEHOLDER = "Adım hakkında yorum ekleyin..."
    
    # Buttons
    PROCEED = "İlerle >"
    WRITE = "YAZ"
    ADD_COMMENT = "YORUM EKLE"
    HIDE_COMMENT = "YORUM GİZLE"
    PASS = "GEÇTİ"
    FAIL = "KALDI"
    OK = "Tamam"
    
    # Status Bar
    STEP = "Adım"
    RESERVED = "Rezerve Alan"
    
    # Menu Items
    MENU_FILE = "Dosya"
    MENU_UPDATE_SETTINGS = "Güncelleme Ayarları..."
    MENU_EXIT = "Çıkış"
    
    # Messages
    VALIDATION_REQUIRED = "Lütfen gerekli değerleri girin!"
    NO_VALUE_WRITTEN = "Lütfen değer girin ve YAZ butonuna basın!"
    NO_CHECKBOX_SELECTED = "Lütfen GEÇTİ veya KALDI seçin ve YAZ butonuna basın!"
    INVALID_NUMBER = "Geçersiz sayı formatı!"
    VALUE_TOO_LOW = "Değer {} değerinden küçük olamaz!"
    VALUE_TOO_HIGH = "Değer {} değerinden büyük olamaz!"
    ENTER_VALUE_FIRST = "Lütfen bir değer girin!"
    INVALID_INPUT = "Geçersiz giriş. Lütfen kontrol edin."
    TEST_COMPLETE = "Test tamamlandı!"
    UPDATE_FILE_SELECTED = "Güncelleme klasörü seçildi"
    UPDATE_FILE_ERROR = "Güncelleme klasörü ayarlanamadı"
    UPDATE_DISABLED = "Sürekli güncelleme durduruldu"
    
    # Dialog Titles
    ERROR_TITLE = "Hata"
    WARNING_TITLE = "Uyarı"
    SUCCESS_TITLE = "Başarılı"


# ============================================================================
# WINDOW SETTINGS
# ============================================================================

WINDOW_MIN_WIDTH = 1024
WINDOW_MIN_HEIGHT = 768
WINDOW_TITLE = "Test Prosedürü Uygulaması"

# Font Settings (60% increase from original)
FONT_SIZE = 16              # Base font (was 10pt)
FONT_SIZE_LARGE = 22        # Large text like titles (was 14pt)
FONT_SIZE_TIMER = 38        # Timer display (was 24pt)
FONT_SIZE_PROGRESS = 19     # Progress text (was 12pt)
FONT_SIZE_EMOJI = 58        # Emoji size (was 36pt)
FONT_SIZE_DESCRIPTION = 17  # Description text (was 11pt)
FONT_SIZE_BUTTON = 18       # Button text
FONT_SIZE_ERROR = 14        # Error messages


# ============================================================================
# TIMER SETTINGS
# ============================================================================

TIMER_UPDATE_INTERVAL = 1000  # milliseconds (1 second)

# Timer color thresholds (percentage of time remaining)
TIMER_WARNING_THRESHOLD = 20  # Yellow when < 20% time left
TIMER_CRITICAL_THRESHOLD = 10  # Red when < 10% time left


# ============================================================================
# ROW HEIGHTS (pixels) - Updated with better spacing
# ============================================================================

ROW_1_HEIGHT = 35  # Header info bar
ROW_2_HEIGHT = 50  # Step title (increased from 45 for padding)
ROW_4_HEIGHT = 180  # Status bar (2.5x increase from original 70, was 90)
# ROW_3 is flexible (fills remaining space)


# ============================================================================
# PADDING & MARGINS (pixels)
# ============================================================================

# Row 1
ROW_1_PADDING_H = 8  # Horizontal padding

# Row 2
ROW_2_PADDING_TOP = 10
ROW_2_PADDING_BOTTOM = 10
ROW_2_PADDING_LEFT = 15
ROW_2_PADDING_RIGHT = 15

# Row 3
ROW_3_DESCRIPTION_PADDING = 20  # All sides

# Row 4
ROW_4_PADDING_TOP = 15
ROW_4_PADDING_BOTTOM = 15
ROW_4_PADDING_LEFT = 15
ROW_4_PADDING_RIGHT = 15
ROW_4_BOTTOM_MARGIN = 20  # Margin from window edge
ROW_4_SECTION_SPACING = 10  # Spacing between sections


# ============================================================================
# WIDGET SIZES
# ============================================================================

# Buttons
BUTTON_PROCEED_WIDTH = 200
BUTTON_PROCEED_HEIGHT = 50
BUTTON_WRITE_WIDTH = 80
BUTTON_WRITE_HEIGHT = 40
BUTTON_COMMENT_WIDTH = 150
BUTTON_COMMENT_HEIGHT = 40

# Input fields
INPUT_FIELD_WIDTH = 150
INPUT_FIELD_HEIGHT = 40

# Result display
RESULT_DISPLAY_MIN_WIDTH = 150

# Comment field
COMMENT_FIELD_HEIGHT = 100

# Progress bar
PROGRESS_BAR_HEIGHT = 25

# Emoji
EMOJI_BACKGROUND_SIZE = 80  # Circular background size

# Checkboxes
CHECKBOX_SPACING = 30  # Space between checkboxes


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
UPDATE_FILES_DIR = "data/updates"  # Directory for continuous update files


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


# ============================================================================
# ANIMATION SETTINGS
# ============================================================================

ANIMATION_DURATION = 200  # milliseconds for smooth transitions