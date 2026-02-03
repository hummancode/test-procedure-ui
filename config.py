import sys
from pathlib import Path
def _resolve_path(relative_path: str) -> str:
    """Resolve relative path for both development and PyInstaller"""
    if getattr(sys, 'frozen', False):
        # PyInstaller bundled path
        base = Path(sys._MEIPASS)
        if (base / relative_path).exists():
            return str(base / relative_path)
        # Fallback to executable directory
        return str(Path(sys.executable).parent / relative_path)
    else:
        # Development mode - __file__ is config.py in project root
        return str(Path(__file__).parent / relative_path)
def _get_writable_path(relative_path: str) -> str:
    """Get writable path (always in executable/project directory, never in _MEIPASS)"""
    if getattr(sys, 'frozen', False):
        return str(Path(sys.executable).parent / relative_path)
    else:
        return str(Path(__file__).parent / relative_path)
    
SETTINGS_FILE = _get_writable_path("app_settings.json")
DEFAULT_UPDATE_FOLDER = _get_writable_path("data/updates")
DEFAULT_EXPORT_FOLDER = _get_writable_path("data/exports")
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
    BORDER = "#455a64" 
    BORDER_COLOR = "#455a64"            # Subtle borders
    INPUT_BACKGROUND = "#37474f"        # Input fields, image containers
    BUTTON_PRIMARY = "#2196f3"          # Action buttons
    BUTTON_HOVER = "#42a5f5"            # Button hover state
    BUTTON_SECONDARY = "#757575"        # Secondary buttons (like comment)


# ============================================================================
# TURKISH UI LABELS
# ============================================================================

class Labels:
        # Test Step Editor (NEW)
    MENU_DEVELOPER = "Geliştirici"
    MENU_EDIT_STEPS = "Test Adımlarını Düzenle..."
    STEP_EDITOR_TITLE = "Test Adımları Editörü"
    STEP_EDITOR_STEP_LIST = "Adım Listesi"
    STEP_EDITOR_STEP_DETAILS = "Adım Detayları"
    STEP_EDITOR_ADD_STEP = "Yeni Adım Ekle"
    STEP_EDITOR_DELETE_STEP = "Adımı Sil"
    STEP_EDITOR_BASIC_INFO = "Temel Bilgiler"
    STEP_EDITOR_INPUT_SETTINGS = "Giriş Ayarları"
    STEP_EDITOR_NUMBER_SETTINGS = "Sayısal Giriş Ayarları"
    # Input types (Turkish)
    INPUT_TYPE_NONE = "Yok (Giriş Yok)"
    INPUT_TYPE_PASS_FAIL = "Geçti-Kaldı"
    INPUT_TYPE_NUMBER = "Sayı"
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
    ADD_COMMENT = "YORUM"
    HIDE_COMMENT = "GİZLE"
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
    
    
    MENU_VIEW = "Görünüm"
    TOGGLE_SIDEBAR = "İlerleme Paneli"
    PROGRESS_NAVIGATOR = "İlerleme Paneli"
    # Export Button
    REPORT = "Raporla"
    
    # Export Messages (NEW)
    SELECT_EXPORT_FOLDER = "Excel Raporu Kaydetme Konumunu Seçin"
    EXPORT_SUCCESS_TITLE = "Rapor Kaydedildi"
    EXPORT_SUCCESS_MESSAGE = "Excel raporu başarıyla kaydedildi:"
    EXPORT_ERROR_TITLE = "Hata"
    EXPORT_ERROR_MESSAGE = "Excel raporu kaydedilemedi. Lütfen tekrar deneyin."
# ============================================================================
# WINDOW SETTINGS
# ============================================================================

WINDOW_MIN_WIDTH = 1920
WINDOW_MIN_HEIGHT = 1080
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
FONT_SIZE_TITLE = 38        # Row 2 step title (was 14pt, now bigger!)
FONT_SIZE_RESULT = 14       # Sonuç: result display (NEW - bold!)
FONT_SIZE_DIALOG = 13      

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
ROW_2_HEIGHT = 70  # Step title (increased from 45 for padding)
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
DIALOG_BUTTON_WIDTH = 120
DIALOG_BUTTON_HEIGHT = 40
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

# Sidebar Settings (NEW)
SIDEBAR_WIDTH = 250  # pixels
SIDEBAR_ANIMATION_DURATION = 200  # milliseconds
# ============================================================================
# IMAGE SETTINGS
# ============================================================================

IMAGE_MAX_SIZE_MB = 10
SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg', '.bmp']
PLACEHOLDER_IMAGE_PATH = _resolve_path("resources/images/placeholder.png")



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
EXPORT_DIR = "data/exports"  # NEW: Default export directory

# ============================================================================
# LOGGING
# ============================================================================

LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


# ============================================================================
# STATUS EMOJIS
# ============================================================================

ICON_HAPPY = _resolve_path("resources/icons/happy.png")
ICON_SAD = _resolve_path("resources/icons/sad.png")


# ============================================================================
# ANIMATION SETTINGS
# ============================================================================

ANIMATION_DURATION = 200  # milliseconds for smooth transitions
DEFAULT_UPDATE_INTERVAL = 10  # seconds
# ============================================================================
# USER ROLES & AUTHENTICATION
# ============================================================================

class UserRole:
    """
    3 User role types:
    
    1. DEVELOPER - All admin rights + can edit test steps (future)
    2. ADMIN - Can navigate back, edit results, export reports  
    3. OPERATOR - Basic test execution only (no password)
    
    Hierarchy: DEVELOPER > ADMIN > OPERATOR
    """
    # Role identifiers
    ADMIN = "admin"
    OPERATOR = "operator"
    DEVELOPER = "developer"
    
    # Display names (Turkish)
    DISPLAY_NAMES = {
        ADMIN: "Yönetici",
        OPERATOR: "Operatör",
        DEVELOPER: "Geliştirici"
    }
    
    # Roles that can navigate backward
    BACKWARD_NAV_ROLES = [ADMIN, DEVELOPER]
    
    # Roles that can edit submitted results
    EDIT_ROLES = [ADMIN, DEVELOPER]
    
    # Roles that can export reports
    EXPORT_ROLES = [ADMIN, DEVELOPER]
    
    # Roles that can edit test steps (Developer mode - future feature)
    EDIT_STEPS_ROLES = [DEVELOPER]
    
    # Roles that require password login
    PASSWORD_REQUIRED_ROLES = [ADMIN, DEVELOPER]
    # NEW: Roles that can edit time limits only (Admin + Developer)
    EDIT_TIME_LIMIT_ROLES = [ADMIN, DEVELOPER]
    @classmethod
    def get_display_name(cls, role: str) -> str:
        """Get Turkish display name for a role."""
        return cls.DISPLAY_NAMES.get(role, role)
    
    @classmethod
    def can_navigate_back(cls, role: str) -> bool:
        """Check if role can navigate to previous steps."""
        return role in cls.BACKWARD_NAV_ROLES
    
    @classmethod
    def can_edit_results(cls, role: str) -> bool:
        """Check if role can edit submitted results."""
        return role in cls.EDIT_ROLES
    
    @classmethod
    def can_export(cls, role: str) -> bool:
        """Check if role can export reports."""
        return role in cls.EXPORT_ROLES

    # Roles that can edit test steps (Developer mode)
    
    

    
    @classmethod
    def can_edit_test_steps(cls, role: str) -> bool:
        '''Check if role can fully edit test steps (Developer mode).'''
        return role in cls.EDIT_STEPS_ROLES
    
    @classmethod
    def can_edit_time_limits(cls, role: str) -> bool:
        '''Check if role can edit time limits (Admin and Developer).'''
        return role in cls.EDIT_TIME_LIMIT_ROLES

# Default admin credentials (used as fallback if users.json not found)
DEFAULT_ADMIN_PASSWORD = "admin123"  # Change in production!

# Path to users file
USERS_FILE_PATH = _resolve_path("data/users.json")
