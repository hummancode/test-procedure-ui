# .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
*.egg

# PyInstaller build artifacts
build/
dist/
*.spec

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Spyder
.spyproject/
.spyderproject

# Data files (don't commit autosaves/exports)
data/autosave/*
data/exports/*
!data/autosave/.gitkeep
!data/exports/.gitkeep

# Logs
logs/*.log
*.log

# OS files
.DS_Store
Thumbs.db
Desktop.ini

# Runtime/settings files (auto-generated)
app_settings.json

# Large files
*.exe
codebase.md

# Conda
*.conda
```

# app_settings.json

```json
{
  "update_folder": "C:/Users/ABDULLAH/Desktop/Kiosk-test_yazılımı/test_procedure_ui/data/updates",
  "last_station": "",
  "window_geometry": null,
  "version": "1.0",
  "update_interval": 10,
  "last_session_metadata": {
    "stok_no": "1",
    "opsiyonel_stok_no": "2312",
    "tanim": "21",
    "teu_udk": "2",
    "seri_no": "2",
    "revizyon_261": "assafgggg",
    "test_donanimi_revizyon": "as",
    "test_yazilimi_revizyon": "21",
    "is_tipi_no": "12",
    "kay_yazilimi_versiyon": "AS",
    "sky_yazilimi_versiyon": "12",
    "istasyon": "",
    "sip_code": "",
    "fluke_esa620_kalibrasyon": "2027-01-01",
    "italsea_7proglcd_kalibrasyon": "2027-01-01",
    "geratech_kalibrasyon": "2027-01-01",
    "iba_magicmax_kalibrasyon": "2027-01-01",
    "iba_primus_a_kalibrasyon": "2027-01-01"
  }
}
```

# build_exe_anaconda.bat

```bat
@echo off
REM ============================================================================
REM Build Script for Test Procedure Application (ANACONDA VERSION)
REM Creates a standalone executable with PyInstaller using Anaconda environment
REM ============================================================================

echo ========================================
echo Building Test Procedure Application
echo Publisher: X
echo Version: 1.0
echo Using: Anaconda Environment
echo ========================================
echo.

REM ============================================================================
REM CONFIGURATION - CHANGE THIS TO YOUR ENVIRONMENT NAME
REM ============================================================================
set CONDA_ENV_NAME=test_station_kiosk
REM Replace 'your_env_name' with your actual Anaconda environment name
REM Example: set CONDA_ENV_NAME=testproc
REM ============================================================================

echo Activating Anaconda environment: %CONDA_ENV_NAME%
echo.

REM Try to activate Anaconda environment
call conda activate %CONDA_ENV_NAME%
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Failed to activate Anaconda environment '%CONDA_ENV_NAME%'
    echo ========================================
    echo.
    echo Please check:
    echo 1. Anaconda/Miniconda is installed
    echo 2. Environment name is correct
    echo 3. Run this from Anaconda Prompt OR
    echo 4. Run 'conda init' first
    echo.
    echo Current environments:
    call conda env list
    echo.
    pause
    exit /b 1
)

echo Environment activated successfully!
echo.

REM Verify Python version
echo Python version:
python --version
echo.

REM Verify PyInstaller is installed in this environment
python -c "import PyInstaller; print('PyInstaller version:', PyInstaller.__version__)" 2>NUL
if errorlevel 1 (
    echo.
    echo PyInstaller not found in environment '%CONDA_ENV_NAME%'!
    echo Installing PyInstaller...
    echo.
    conda install -c conda-forge pyinstaller -y
    if errorlevel 1 (
        pip install pyinstaller
        if errorlevel 1 (
            echo Failed to install PyInstaller!
            pause
            exit /b 1
        )
    )
)

echo PyInstaller found!
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

REM Create icon if it doesn't exist (optional)
if not exist resources\icons mkdir resources\icons
if not exist resources\icons\app_icon.ico (
    echo WARNING: app_icon.ico not found in resources\icons\
    echo The executable will be built without a custom icon.
    echo.
)

REM Build the executable using the spec file
echo.
echo Building executable...
echo.
pyinstaller TestProcedure.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo.
    echo Please check the error messages above.
    echo Common issues:
    echo - Missing dependencies: pip install -r requirements.txt
    echo - Wrong environment activated
    echo - Missing spec file
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo.
echo Executable location: dist\TestProcedure\TestProcedure.exe
echo.
echo You can now distribute the entire 'dist\TestProcedure' folder
echo.

REM Optional: Create a simple README in the dist folder
echo Creating distribution README...
(
echo Test Prosedürü Uygulaması v1.0
echo.
echo KURULUM:
echo --------
echo 1. Tüm "TestProcedure" klasörünü istediğiniz konuma kopyalayın
echo 2. TestProcedure.exe dosyasını çalıştırın
echo.
echo NOTLAR:
echo -------
echo - İlk çalıştırmada "data" klasörü otomatik oluşturulacaktır
echo - Güncelleme ayarları için: Dosya ^> Güncelleme Ayarları
echo - Excel raporları için: Test sırasında "Raporla" butonuna tıklayın
echo.
echo Publisher: X
echo Copyright (c) 2026 X
echo.
echo Built with Python from Anaconda environment: %CONDA_ENV_NAME%
) > dist\TestProcedure\README.txt

echo Distribution README created.
echo.

REM Optional: Copy data folder if needed
if exist data (
    echo Copying data folder to distribution...
    xcopy data dist\TestProcedure\data\ /E /I /Y
)

REM Optional: Copy resources folder if needed
if exist resources (
    echo Copying resources folder to distribution...
    xcopy resources dist\TestProcedure\resources\ /E /I /Y
)

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Environment used: %CONDA_ENV_NAME%
echo Python location: 
python -c "import sys; print(sys.executable)"
echo.
echo Next steps:
echo 1. Test the executable: dist\TestProcedure\TestProcedure.exe
echo 2. If it works, compress "dist\TestProcedure" folder to ZIP
echo 3. Distribute to users
echo.
echo Note: The executable is STANDALONE - users don't need Python/Anaconda!
echo.

pause

```

# config.py

```py
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
EXPORT_DIR = "data/exports"  # NEW: Default export directory

# ============================================================================
# LOGGING
# ============================================================================

LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


# ============================================================================
# STATUS EMOJIS
# ============================================================================

ICON_HAPPY = "resources/icons/happy.png"
ICON_SAD = "resources/icons/sad.png"


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
USERS_FILE_PATH = "data/users.json"
```

# data\sample_test.json

```json
{
  "test_info": {
    "stock_number": "ABC123",
    "serial_number": "456789",
    "station_number": "ST-01",
    "sip_code": "X99"
  },
  "steps": [
    {
      "step_id": 1,
      "name": "Görsel Kontrol - Ön Panel1",
      "description": "Ön paneldeki tüm göstergelerin çalıştığını doğrulayın.\n\nKontrol edilecekler:\n• LED'lerin yanıp yanmadığını kontrol edin\n• Ekran parlaklığının uygun seviyede olduğunu doğrulayın\n• Fiziksel hasarlar için dış kasayı inceleyin\n\nBeklenen sonuç: Tüm göstergeler normal çalışıyor olmalı.",
      "time_limit": 15,
      "image_path": "resources/images/step_001.png",
      "input_type": "pass_fail",
      "input_label": "Sonuç",
      "input_validation": {}
    },
    {
      "step_id": 2,
      "name": "Ara Adım - Bilgilendirme",
      "description": "Ara adım - devam etmek için İlerle butonuna basın.",
      "time_limit": 10,
      "image_path": "resources/images/step_001.png",
      "input_type": "none",
      "input_label": "",
      "input_validation": {}
    },
    {
      "step_id": 3,
      "name": "Voltaj Ölçümü",
      "description": "Multimetre kullanarak çıkış voltajını ölçün.\n\nAdımlar:\n1. Multimetreyi DC voltaj moduna ayarlayın\n2. Kırmızı probu (+) terminale bağlayın\n3. Siyah probu (-) terminale bağlayın\n4. Okunan değeri kaydedin\n\nBeklenen aralık: 11.5V - 12.5V",
      "time_limit": 120,
      "image_path": "resources/images/step_002.png",
      "input_type": "number",
      "input_label": "Voltaj (V)",
      "input_validation": {
        "max": 12.5,
        "min": 11.5
      }
    },
    {
      "step_id": 4,
      "name": "Yeni Adım 4",
      "description": "",
      "time_limit": 60,
      "image_path": "none",
      "input_type": "number",
      "input_label": "Test Sonucu",
      "input_validation": {
        "max": 100.0,
        "min": 0.0
      }
    }
  ]
}
```

# data\updates\GuncellemeRaporu__20260203_1.json

```json
{
  "session_id": "20260203_142509",
  "stock_number": "1",
  "serial_number": "2",
  "station_number": "",
  "sip_code": "",
  "start_time": "2026-02-03T14:25:09.275300",
  "end_time": null,
  "duration_seconds": 20,
  "completion_percentage": 0.0,
  "passed_count": 0,
  "failed_count": 0,
  "steps": [
    {
      "step_id": 1,
      "name": "Görsel Kontrol - Ön Panel1",
      "status": "in_progress",
      "start_time": "03/02/2026 14:25:09",
      "actual_duration": null,
      "result_value": null,
      "comment": null,
      "time_limit": 15,
      "completed_by": null,
      "input_validation": {}
    },
    {
      "step_id": 2,
      "name": "Ara Adım - Bilgilendirme",
      "status": "not_started",
      "start_time": null,
      "actual_duration": null,
      "result_value": null,
      "comment": null,
      "time_limit": 10,
      "completed_by": null,
      "input_validation": {}
    },
    {
      "step_id": 3,
      "name": "Voltaj Ölçümü",
      "status": "not_started",
      "start_time": null,
      "actual_duration": null,
      "result_value": null,
      "comment": null,
      "time_limit": 120,
      "completed_by": null,
      "input_validation": {
        "max": 12.5,
        "min": 11.5
      }
    },
    {
      "step_id": 4,
      "name": "Yeni Adım 4",
      "status": "not_started",
      "start_time": null,
      "actual_duration": null,
      "result_value": null,
      "comment": null,
      "time_limit": 60,
      "completed_by": null,
      "input_validation": {
        "max": 100.0,
        "min": 0.0
      }
    }
  ],
  "metadata": {
    "stok_no": "1",
    "opsiyonel_stok_no": "2312",
    "tanim": "21",
    "teu_udk": "2",
    "seri_no": "2",
    "revizyon_261": "assafgggg",
    "test_donanimi_revizyon": "as",
    "test_yazilimi_revizyon": "21",
    "is_tipi_no": "12",
    "kay_yazilimi_versiyon": "AS",
    "sky_yazilimi_versiyon": "12",
    "fluke_esa620_kalibrasyon": "2027-01-01",
    "italsea_7proglcd_kalibrasyon": "2027-01-01",
    "geratech_kalibrasyon": "2027-01-01",
    "iba_magicmax_kalibrasyon": "2027-01-01",
    "iba_primus_a_kalibrasyon": "2027-01-01",
    "istasyon": "",
    "sip_code": ""
  },
  "last_updated": "2026-02-03T14:25:29.293021",
  "file_version": "1.0"
}
```

# data\updates\GuncellemeRaporu_ST-01_20260123_ABC123.json

```json
{
  "session_id": "20260123_191343",
  "stock_number": "ABC123",
  "serial_number": "456789",
  "station_number": "ST-01",
  "sip_code": "X99",
  "start_time": "2026-01-23T19:13:43.954392",
  "end_time": "2026-01-23T19:14:01.963114",
  "duration_seconds": 18,
  "completion_percentage": 100.0,
  "passed_count": 1,
  "failed_count": 2,
  "steps": [
    {
      "step_id": 1,
      "name": "Görsel Kontrol - Ön Panel",
      "status": "failed",
      "start_time": "23/01/2026 19:13:43",
      "actual_duration": 7,
      "result_value": "FAIL",
      "comment": "",
      "time_limit": 5,
      "input_validation": {}
    },
    {
      "step_id": 2,
      "name": "Ara Adım - Bilgilendirme",
      "status": "passed",
      "start_time": "23/01/2026 19:13:51",
      "actual_duration": 6,
      "result_value": null,
      "comment": "AS",
      "time_limit": 10,
      "input_validation": {}
    },
    {
      "step_id": 3,
      "name": "Voltaj Ölçümü",
      "status": "failed",
      "start_time": "23/01/2026 19:13:57",
      "actual_duration": 4,
      "result_value": "2",
      "comment": "",
      "time_limit": 120,
      "input_validation": {
        "min": 11.5,
        "max": 12.5
      }
    }
  ],
  "last_updated": "2026-01-23T19:14:01.963248",
  "file_version": "1.0"
}
```

# data\updates\GuncellemeRaporu_ST-01_20260124_ABC123.json

```json
{
  "session_id": "20260124_190228",
  "stock_number": "ABC123",
  "serial_number": "456789",
  "station_number": "ST-01",
  "sip_code": "X99",
  "start_time": "2026-01-24T19:02:28.297637",
  "end_time": null,
  "duration_seconds": 0,
  "completion_percentage": 0.0,
  "passed_count": 0,
  "failed_count": 0,
  "steps": [
    {
      "step_id": 1,
      "name": "Görsel Kontrol - Ön Panel",
      "status": "in_progress",
      "start_time": "24/01/2026 19:02:28",
      "actual_duration": null,
      "result_value": null,
      "comment": null,
      "time_limit": 5,
      "input_validation": {}
    },
    {
      "step_id": 2,
      "name": "Ara Adım - Bilgilendirme",
      "status": "not_started",
      "start_time": null,
      "actual_duration": null,
      "result_value": null,
      "comment": null,
      "time_limit": 10,
      "input_validation": {}
    },
    {
      "step_id": 3,
      "name": "Voltaj Ölçümü",
      "status": "not_started",
      "start_time": null,
      "actual_duration": null,
      "result_value": null,
      "comment": null,
      "time_limit": 120,
      "input_validation": {
        "min": 11.5,
        "max": 12.5
      }
    }
  ],
  "last_updated": "2026-01-24T19:02:28.313712",
  "file_version": "1.0"
}
```

# data\updates\GuncellemeRaporu_ST-01_20260129_ABC123.json

```json
{
  "session_id": "20260129_112934",
  "stock_number": "ABC123",
  "serial_number": "456789",
  "station_number": "ST-01",
  "sip_code": "X99",
  "start_time": "2026-01-29T11:29:34.361548",
  "end_time": null,
  "duration_seconds": 83271,
  "completion_percentage": 66.66666666666666,
  "passed_count": 1,
  "failed_count": 1,
  "steps": [
    {
      "step_id": 1,
      "name": "Görsel Kontrol - Ön Panel",
      "status": "failed",
      "start_time": "29/01/2026 11:29:34",
      "actual_duration": 9,
      "result_value": "FAIL",
      "comment": "",
      "time_limit": 5,
      "input_validation": {}
    },
    {
      "step_id": 2,
      "name": "Ara Adım - Bilgilendirme",
      "status": "passed",
      "start_time": "29/01/2026 11:29:43",
      "actual_duration": 1,
      "result_value": null,
      "comment": "",
      "time_limit": 10,
      "input_validation": {}
    },
    {
      "step_id": 3,
      "name": "Voltaj Ölçümü",
      "status": "in_progress",
      "start_time": "29/01/2026 11:29:44",
      "actual_duration": null,
      "result_value": null,
      "comment": null,
      "time_limit": 120,
      "input_validation": {
        "min": 11.5,
        "max": 12.5
      }
    }
  ],
  "last_updated": "2026-01-30T10:37:25.481911",
  "file_version": "1.0"
}
```

# data\updates\GuncellemeRaporu_ST-01_20260130_ABC123.json

```json
{
  "session_id": "20260130_155516",
  "stock_number": "ABC123",
  "serial_number": "456789",
  "station_number": "ST-01",
  "sip_code": "X99",
  "start_time": "2026-01-30T15:55:16.193155",
  "end_time": "2026-01-30T15:55:30.734977",
  "duration_seconds": 14,
  "completion_percentage": 100.0,
  "passed_count": 2,
  "failed_count": 1,
  "steps": [
    {
      "step_id": 1,
      "name": "Görsel Kontrol - Ön Panel",
      "status": "passed",
      "start_time": "30/01/2026 15:55:16",
      "actual_duration": 4,
      "result_value": "PASS",
      "comment": "",
      "time_limit": 5,
      "completed_by": "Sistem Yöneticisi",
      "input_validation": {}
    },
    {
      "step_id": 2,
      "name": "Ara Adım - Bilgilendirme",
      "status": "passed",
      "start_time": "30/01/2026 15:55:20",
      "actual_duration": 5,
      "result_value": null,
      "comment": "",
      "time_limit": 10,
      "completed_by": "Fatma Öztürk",
      "input_validation": {}
    },
    {
      "step_id": 3,
      "name": "Voltaj Ölçümü",
      "status": "failed",
      "start_time": "30/01/2026 15:55:26",
      "actual_duration": 4,
      "result_value": "5",
      "comment": "",
      "time_limit": 120,
      "completed_by": "Fatma Öztürk",
      "input_validation": {
        "min": 11.5,
        "max": 12.5
      }
    }
  ],
  "last_updated": "2026-01-30T15:55:52.126579",
  "file_version": "1.0"
}
```

# data\updates\GuncellemeRaporu_ST-01_20260202_ABC123.json

```json
{
  "session_id": "20260202_161223",
  "stock_number": "ABC123",
  "serial_number": "456789",
  "station_number": "ST-01",
  "sip_code": "X99",
  "start_time": "2026-02-02T16:12:23.796337",
  "end_time": null,
  "duration_seconds": 79890,
  "completion_percentage": 0.0,
  "passed_count": 0,
  "failed_count": 0,
  "steps": [
    {
      "step_id": 1,
      "name": "Görsel Kontrol - Ön Panel",
      "status": "in_progress",
      "start_time": "02/02/2026 16:12:23",
      "actual_duration": null,
      "result_value": null,
      "comment": null,
      "time_limit": 5,
      "completed_by": null,
      "input_validation": {}
    },
    {
      "step_id": 2,
      "name": "Ara Adım - Bilgilendirme",
      "status": "not_started",
      "start_time": null,
      "actual_duration": null,
      "result_value": null,
      "comment": null,
      "time_limit": 10,
      "completed_by": null,
      "input_validation": {}
    },
    {
      "step_id": 3,
      "name": "Voltaj Ölçümü",
      "status": "not_started",
      "start_time": null,
      "actual_duration": null,
      "result_value": null,
      "comment": null,
      "time_limit": 120,
      "completed_by": null,
      "input_validation": {
        "min": 11.5,
        "max": 12.5
      }
    }
  ],
  "last_updated": "2026-02-03T14:23:54.464522",
  "file_version": "1.0"
}
```

# data\updates\GuncellemeRaporu_ST-01_20260203_ABC123.json

```json
{
  "session_id": "20260203_092543",
  "stock_number": "ABC123",
  "serial_number": "456789",
  "station_number": "ST-01",
  "sip_code": "X99",
  "start_time": "2026-02-03T09:25:43.451264",
  "end_time": null,
  "duration_seconds": 50,
  "completion_percentage": 33.33333333333333,
  "passed_count": 1,
  "failed_count": 0,
  "steps": [
    {
      "step_id": 1,
      "name": "Görsel Kontrol - Ön Panel",
      "status": "passed",
      "start_time": "03/02/2026 09:25:43",
      "actual_duration": 14,
      "result_value": "PASS",
      "comment": "",
      "time_limit": 5,
      "completed_by": "Sistem Yöneticisi",
      "input_validation": {}
    },
    {
      "step_id": 2,
      "name": "Ara Adım - Bilgilendirme",
      "status": "in_progress",
      "start_time": "03/02/2026 09:25:58",
      "actual_duration": null,
      "result_value": null,
      "comment": null,
      "time_limit": 10,
      "completed_by": null,
      "input_validation": {}
    },
    {
      "step_id": 3,
      "name": "Voltaj Ölçümü",
      "status": "not_started",
      "start_time": null,
      "actual_duration": null,
      "result_value": null,
      "comment": null,
      "time_limit": 120,
      "completed_by": null,
      "input_validation": {
        "min": 11.5,
        "max": 12.5
      }
    }
  ],
  "last_updated": "2026-02-03T09:26:33.659225",
  "file_version": "1.0"
}
```

# data\users.json

```json
{
    "version": "1.0",
    "description": "Kullanıcı tanımları - 3 Rol Tipi: Admin, Operator, Developer",
    "users": {
        "admins": [
            {
                "username": "admin",
                "password_hash": "0192023a7bbd73250516f069df18b500",
                "display_name": "Sistem Yöneticisi",
                "employee_id": "ADM001",
                "department": "IT",
                "active": true
            },
            {
                "username": "admin2",
                "password_hash": "0192023a7bbd73250516f069df18b500",
                "display_name": "Yedek Yönetici",
                "employee_id": "ADM002",
                "department": "IT",
                "active": true
            }
        ],
        "operators": [
            {
                "username": "op1",
                "password_hash": "",
                "display_name": "Ali Yılmaz",
                "employee_id": "OP001",
                "department": "Üretim Hattı A",
                "active": true
            },
            {
                "username": "op2",
                "password_hash": "",
                "display_name": "Ayşe Kaya",
                "employee_id": "OP002",
                "department": "Üretim Hattı A",
                "active": true
            },
            {
                "username": "op3",
                "password_hash": "",
                "display_name": "Mehmet Demir",
                "employee_id": "OP003",
                "department": "Üretim Hattı B",
                "active": true
            },
            {
                "username": "op4",
                "password_hash": "",
                "display_name": "Fatma Öztürk",
                "employee_id": "OP004",
                "department": "Üretim Hattı B",
                "active": true
            },
            {
                "username": "op5",
                "password_hash": "",
                "display_name": "Mustafa Çelik",
                "employee_id": "OP005",
                "department": "Üretim Hattı C",
                "active": true
            }
        ],
        "developers": [
            {
                "username": "dev1",
                "password_hash": "e99a18c428cb38d5f260853678922e03",
                "display_name": "Zeynep Aksoy (Dev)",
                "employee_id": "DEV001",
                "department": "Yazılım",
                "active": true
            },
            {
                "username": "dev2",
                "password_hash": "e99a18c428cb38d5f260853678922e03",
                "display_name": "Can Yıldırım (Dev)",
                "employee_id": "DEV002",
                "department": "Yazılım",
                "active": true
            }
        ]
    },
    "roles": {
        "admin": {
            "display_name": "Yönetici",
            "can_navigate_back": true,
            "can_edit_results": true,
            "can_export": true,
            "can_manage_users": true,
            "can_edit_test_steps": false,
            "requires_password": true
        },
        "operator": {
            "display_name": "Operatör",
            "can_navigate_back": false,
            "can_edit_results": false,
            "can_export": true,
            "can_manage_users": false,
            "can_edit_test_steps": false,
            "requires_password": true
        },
        "developer": {
            "display_name": "Geliştirici",
            "can_navigate_back": true,
            "can_edit_results": true,
            "can_export": true,
            "can_manage_users": true,
            "can_edit_test_steps": true,
            "requires_password": true
        }
    },
    "_passwords_for_testing": {
        "admin": "admin123",
        "admin2": "admin123",
        "dev1": "abc123",
        "dev2": "abc123"
    }
}
```

# exporters\__init__.py

```py
"""
Exporters Package
Excel and JSON export functionality
"""
from exporters.excel_exporter import ExcelExporter

__all__ = ['ExcelExporter']
```

# exporters\excel_exporter.py

```py
# -*- coding: utf-8 -*-

"""
Excel Exporter
Exports test session data to formatted Excel files.

Updated to include extended session metadata:
- Ürün Bilgileri (Product Info)
- Yazılım Bilgileri (Software Info)
- Cihaz Kalibrasyonları (Device Calibrations)
- Oturum Bilgileri (Session Info)

NOTE: İstasyon and SİP are NOT included in Excel (UI-only fields)
"""
from datetime import datetime
from pathlib import Path
from typing import Optional

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

from models.test_session import TestSession
from models.enums import TestStatus
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ExcelExporter:
    """
    Exports test session data to formatted Excel files.
    
    Features:
    - Extended session metadata (product, software, calibrations)
    - Step-by-step results with status, duration, and comments
    - Color-coded pass/fail status
    - Professional formatting
    - Auto-column sizing
    
    NOTE: İstasyon and SİP are UI-only fields and NOT included in Excel export.
    """
    
    # Excel styling constants
    HEADER_FILL = PatternFill(start_color="1a237e", end_color="1a237e", fill_type="solid")
    HEADER_FONT = Font(color="FFFFFF", bold=True, size=12)
    
    SECTION_FILL = PatternFill(start_color="3949ab", end_color="3949ab", fill_type="solid")
    SECTION_FONT = Font(color="FFFFFF", bold=True, size=11)
    
    PASS_FILL = PatternFill(start_color="C8E6C9", end_color="C8E6C9", fill_type="solid")
    FAIL_FILL = PatternFill(start_color="FFCDD2", end_color="FFCDD2", fill_type="solid")
    NA_FILL = PatternFill(start_color="E0E0E0", end_color="E0E0E0", fill_type="solid")
    WARNING_FILL = PatternFill(start_color="FFF3E0", end_color="FFF3E0", fill_type="solid")
    EXPIRED_FILL = PatternFill(start_color="FFCDD2", end_color="FFCDD2", fill_type="solid")
    
    BORDER_THIN = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    def __init__(self):
        """Initialize the Excel exporter"""
        logger.info("ExcelExporter initialized (with extended metadata support)")
    
    def export_session(self, session: TestSession, output_path: str) -> bool:
        """
        Export test session to Excel file.
        
        Args:
            session: TestSession to export
            output_path: Full path where Excel file should be saved
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            # Create workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "Test Sonuçları"
            
            # Write content
            current_row = 1
            current_row = self._write_header_section(ws, session, current_row)
            current_row += 2  # Add spacing
            current_row = self._write_results_table(ws, session, current_row)
            
            # Auto-adjust column widths
            self._auto_size_columns(ws)
            
            # Save file
            wb.save(output_path)
            
            logger.info(f"Excel file exported successfully to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export Excel file: {e}")
            return False
    
    def _write_header_section(self, ws, session: TestSession, start_row: int) -> int:
        """
        Write session metadata header section with extended information.
        
        Includes:
        - Report Title
        - Ürün Bilgileri (Product Info)
        - Yazılım Bilgileri (Software Info)
        - Cihaz Kalibrasyonları (Device Calibrations)
        - Oturum Bilgileri (Session Timing)
        
        NOTE: İstasyon and SİP are NOT included (UI-only fields)
        
        Returns:
            Next available row number
        """
        row = start_row
        
        # =====================================================================
        # Report Title
        # =====================================================================
        ws.merge_cells(f'A{row}:G{row}')
        cell = ws[f'A{row}']
        cell.value = "TEST PROSEDÜRÜ RAPORU"
        cell.font = Font(size=16, bold=True, color="1a237e")
        cell.alignment = Alignment(horizontal='center', vertical='center')
        row += 2
        
        # Check if extended metadata is available
        metadata = session.metadata if hasattr(session, 'metadata') and session.metadata else None
        
        # =====================================================================
        # ÜRÜN BİLGİLERİ (Product Information)
        # =====================================================================
        row = self._write_section_header(ws, row, "ÜRÜN BİLGİLERİ")
        
        if metadata:
            product_data = [
                ("Stok No:", metadata.stok_no or session.stock_number),
                ("Opsiyonel Stok No:", metadata.opsiyonel_stok_no),
                ("Tanım:", metadata.tanim),
                ("TEU UDK:", metadata.teu_udk),
                ("Seri No:", metadata.seri_no or session.serial_number),
                ("261 Revizyonu:", metadata.revizyon_261),
                ("Test Donanımı Revizyon:", metadata.test_donanimi_revizyon),
                ("Test Yazılımı Revizyon:", metadata.test_yazilimi_revizyon),
                ("İş Tipi No:", metadata.is_tipi_no),
            ]
        else:
            # Fallback to basic session info
            product_data = [
                ("Stok No:", session.stock_number),
                ("Seri No:", session.serial_number),
            ]
        
        for label, value in product_data:
            if value:  # Only write non-empty values
                row = self._write_info_row(ws, row, label, value)
        
        row += 1  # Spacing
        
        # =====================================================================
        # YAZILIM BİLGİLERİ (Software Information)
        # =====================================================================
        if metadata and (metadata.kay_yazilimi_versiyon or metadata.sky_yazilimi_versiyon):
            row = self._write_section_header(ws, row, "YAZILIM BİLGİLERİ")
            
            software_data = [
                ("KAY Yazılımı Versiyon:", metadata.kay_yazilimi_versiyon),
                ("SKY Yazılımı Versiyon:", metadata.sky_yazilimi_versiyon),
            ]
            
            for label, value in software_data:
                if value:
                    row = self._write_info_row(ws, row, label, value)
            
            row += 1  # Spacing
        
        # =====================================================================
        # CİHAZ KALİBRASYONLARI (Device Calibrations)
        # =====================================================================
        if metadata:
            calibration_data = [
                ("FLUKE ESA620:", metadata.fluke_esa620_kalibrasyon, 'fluke_esa620_kalibrasyon'),
                ("ITALSEA 7PROGLCD:", metadata.italsea_7proglcd_kalibrasyon, 'italsea_7proglcd_kalibrasyon'),
                ("Geratech:", metadata.geratech_kalibrasyon, 'geratech_kalibrasyon'),
                ("IBA MagicMax:", metadata.iba_magicmax_kalibrasyon, 'iba_magicmax_kalibrasyon'),
                ("IBA Primus A:", metadata.iba_primus_a_kalibrasyon, 'iba_primus_a_kalibrasyon'),
            ]
            
            # Check if any calibration data exists
            has_calibrations = any(date_val for _, date_val, _ in calibration_data)
            
            if has_calibrations:
                row = self._write_section_header(ws, row, "CİHAZ KALİBRASYONLARI")
                
                for label, date_val, field_name in calibration_data:
                    if date_val:
                        # Format date for display
                        formatted_date = metadata.format_date_for_display(field_name)
                        status = metadata.get_calibration_status(field_name)
                        row = self._write_calibration_row(ws, row, label, formatted_date, status)
                
                row += 1  # Spacing
        
        # =====================================================================
        # OTURUM BİLGİLERİ (Session Timing) - Generic timing, NO İstasyon/SİP
        # =====================================================================
        row = self._write_section_header(ws, row, "OTURUM BİLGİLERİ")
        
        # Calculate duration text
        if session.duration_seconds:
            minutes = session.duration_seconds // 60
            seconds = session.duration_seconds % 60
            duration_text = f"{minutes} dakika {seconds} saniye"
        else:
            duration_text = "---"
        
        session_data = [
            ("Başlangıç:", session.start_time.strftime(config.DATETIME_FORMAT) if session.start_time else "---"),
            ("Bitiş:", session.end_time.strftime(config.DATETIME_FORMAT) if session.end_time else "Devam Ediyor"),
            ("Süre:", duration_text),
            ("Tamamlanma:", f"%{session.get_completion_percentage():.0f}"),
            ("Başarılı:", str(session.get_passed_count())),
            ("Başarısız:", str(session.get_failed_count())),
        ]
        
        for label, value in session_data:
            row = self._write_info_row(ws, row, label, value)
        
        return row
    
    def _write_section_header(self, ws, row: int, title: str) -> int:
        """Write a section header row"""
        ws.merge_cells(f'A{row}:G{row}')
        cell = ws[f'A{row}']
        cell.value = title
        cell.font = self.SECTION_FONT
        cell.fill = self.SECTION_FILL
        cell.alignment = Alignment(horizontal='left', vertical='center')
        cell.border = self.BORDER_THIN
        return row + 1
    
    def _write_info_row(self, ws, row: int, label: str, value: str) -> int:
        """Write a label-value info row"""
        ws[f'A{row}'] = label
        ws[f'A{row}'].font = Font(bold=True)
        ws[f'A{row}'].border = self.BORDER_THIN
        
        ws.merge_cells(f'B{row}:G{row}')
        ws[f'B{row}'] = value
        ws[f'B{row}'].border = self.BORDER_THIN
        
        return row + 1
    
    def _write_calibration_row(self, ws, row: int, label: str, date_value: str, status: str) -> int:
        """Write a calibration row with status-based coloring"""
        ws[f'A{row}'] = label
        ws[f'A{row}'].font = Font(bold=True)
        ws[f'A{row}'].border = self.BORDER_THIN
        
        ws.merge_cells(f'B{row}:F{row}')
        ws[f'B{row}'] = date_value
        ws[f'B{row}'].border = self.BORDER_THIN
        
        # Status indicator with color
        status_cell = ws[f'G{row}']
        if status == 'expired':
            status_cell.value = "SÜRESİ DOLMUŞ"
            status_cell.fill = self.EXPIRED_FILL
            status_cell.font = Font(color="B71C1C", bold=True)
        elif status == 'warning':
            status_cell.value = "YAKINDA DOLACAK"
            status_cell.fill = self.WARNING_FILL
            status_cell.font = Font(color="E65100", bold=True)
        else:
            status_cell.value = "GEÇERLİ"
            status_cell.fill = self.PASS_FILL
            status_cell.font = Font(color="1B5E20", bold=True)
        
        status_cell.border = self.BORDER_THIN
        status_cell.alignment = Alignment(horizontal='center')
        
        return row + 1
    
    def _write_results_table(self, ws, session: TestSession, start_row: int) -> int:
        """
        Write test results table with step details.
        
        Returns:
            Next available row number
        """
        row = start_row
        
        # Table header
        row = self._write_section_header(ws, row, "TEST SONUÇLARI")
        
        # Table column headers
        headers = [
            "Adım No",
            "Adım Adı",
            "Durum",
            "Başlangıç",
            "Süre (sn)",
            "Sonuç",
            "Yorum"
        ]
        
        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=row, column=col_idx)
            cell.value = header
            cell.font = self.HEADER_FONT
            cell.fill = self.HEADER_FILL
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = self.BORDER_THIN
        
        row += 1
        
        # Table data
        for step in session.steps:
            col_idx = 1
            
            # Step ID
            cell = ws.cell(row=row, column=col_idx)
            cell.value = step.step_id
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            # Step Name
            cell = ws.cell(row=row, column=col_idx)
            cell.value = step.name
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            # Status (with color coding)
            cell = ws.cell(row=row, column=col_idx)
            status_text, status_fill = self._get_status_display(step.status)
            cell.value = status_text
            cell.fill = status_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            # Start Time
            cell = ws.cell(row=row, column=col_idx)
            if step.start_time:
                cell.value = datetime.fromtimestamp(step.start_time).strftime(config.DATETIME_FORMAT)
            else:
                cell.value = "---"
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            # Duration
            cell = ws.cell(row=row, column=col_idx)
            cell.value = step.actual_duration if step.actual_duration is not None else "---"
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            # Result Value
            cell = ws.cell(row=row, column=col_idx)
            cell.value = self._format_result_value(step.result_value)
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            # Comment
            cell = ws.cell(row=row, column=col_idx)
            cell.value = step.comment if step.comment else ""
            cell.border = self.BORDER_THIN
            col_idx += 1
            
            row += 1
        
        return row
    
    def _get_status_display(self, status: TestStatus) -> tuple:
        """
        Get display text and fill color for status.
        
        Returns:
            Tuple of (status_text, fill_color)
        """
        if status == TestStatus.PASSED:
            return ("BAŞARILI", self.PASS_FILL)
        elif status == TestStatus.FAILED:
            return ("BAŞARISIZ", self.FAIL_FILL)
        elif status == TestStatus.IN_PROGRESS:
            return ("DEVAM EDİYOR", PatternFill(start_color="FFF9C4", end_color="FFF9C4", fill_type="solid"))
        elif status == TestStatus.SKIPPED:
            return ("ATLANDI", self.NA_FILL)
        else:
            return ("BAŞLANMAMIŞ", self.NA_FILL)
    
    def _format_result_value(self, value) -> str:
        """Format result value for display"""
        if value is None:
            return "---"
        elif value in ["PASS", "GEÇTİ"]:
            return "GEÇTİ"
        elif value in ["FAIL", "KALDI"]:
            return "KALDI"
        else:
            return str(value)
    
    def _auto_size_columns(self, ws):
        """Auto-adjust column widths based on content"""
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            
            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            
            # Set width with some padding
            adjusted_width = min(max_length + 2, 50)  # Max 50 characters
            ws.column_dimensions[column_letter].width = adjusted_width
    
    def generate_filename(self, session: TestSession, output_dir: str) -> str:
        """
        Generate Excel filename based on session data.
        
        Format: TestRaporu_<DATE>_<STOCK>_<SERIAL>.xlsx
        
        Args:
            session: TestSession object
            output_dir: Directory where file will be saved
            
        Returns:
            Full path to output file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stock = self._sanitize_filename(session.stock_number)
        serial = self._sanitize_filename(session.serial_number)
        
        filename = f"TestRaporu_{timestamp}_{stock}_{serial}.xlsx"
        
        return str(Path(output_dir) / filename)
    
    def _sanitize_filename(self, name: str) -> str:
        """Remove invalid characters from filename"""
        if not name:
            return "unknown"
        # Keep only alphanumeric, hyphens, and underscores
        return ''.join(c if c.isalnum() or c in '-_' else '_' for c in name)
```

# exporters\TestRaporu_ST-01_20260130_142719_ABC123.xlsx

This is a binary file of the type: Excel Spreadsheet

# exporters\TestRaporu_ST-01_20260130_142730_ABC123.xlsx

This is a binary file of the type: Excel Spreadsheet

# exporters\TestRaporu_ST-01_20260130_145028_ABC123.xlsx

This is a binary file of the type: Excel Spreadsheet

# exporters\TestRaporu_ST-01_20260130_154956_ABC123.xlsx

This is a binary file of the type: Excel Spreadsheet

# generate_codebase.bat

```bat
@echo off
echo ================================================
echo AI Digest - Codebase Documentation Generator
echo ================================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    echo.
    pause
    exit /b 1
)

REM Check if npx is available
where npx >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npx is not available!
    echo Please make sure Node.js is properly installed.
    echo.
    pause
    exit /b 1
)

echo Node.js found: 
node --version
echo.

echo Running ai-digest to generate codebase.md...
echo.

REM Run ai-digest
npx ai-digest

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo SUCCESS! codebase.md has been generated.
    echo ================================================
    echo.
    echo You can now find the codebase.md file in your project directory.
    echo.
) else (
    echo.
    echo ================================================
    echo ERROR: Failed to generate codebase.md
    echo ================================================
    echo.
    echo Please check the error messages above.
    echo.
)

pause

```

# main.py

```py
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
    logger.info("Test Procedure Application Starting")
    logger.info("=" * 60)
    
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
    test_file = app_path / 'data' / 'sample_test.json'
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
    
    # Run application event loop
    exit_code = app.exec_()
    
    logger.info("=" * 60)
    logger.info(f"Application Exited with code {exit_code}")
    logger.info(f"User: {user_name} logged out")
    logger.info("=" * 60)
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
```

# managers\__init__.py

```py
"""
Managers Package
Business logic and flow control
"""
from managers.test_manager import TestManager
from managers.timer_manager import TimerManager
from managers.navigation_manager import NavigationManager
from managers.result_manager import ResultManager

__all__ = [
    'TestManager',
    'TimerManager',
    'NavigationManager',
    'ResultManager'
]
```

# managers\navigation_manager.py

```py
"""
Navigation Manager
Handles test step navigation logic and validation
"""
from typing import Optional, Tuple
from PyQt5.QtCore import QObject, pyqtSignal

from models.enums import NavigationMode, TestStatus
from utils.logger import setup_logger
import config
logger = setup_logger(__name__)


class NavigationManager(QObject):
    """
    Manages navigation between test steps.
    
    Features:
    - Navigation validation
    - Business rules enforcement
    - Navigation history tracking
    
    Signals:
        navigation_requested: (target_index, mode)
        navigation_blocked: (reason)
    """
    
    navigation_requested = pyqtSignal(int, str)  # target_index, mode
    navigation_blocked = pyqtSignal(str)         # reason
    
    def __init__(self):
        super().__init__()
        
        # Navigation history
        self.navigation_history = []  # [(from_index, to_index, timestamp), ...]
        
        logger.info("NavigationManager initialized")
    
    def can_navigate_to(self, current_index: int, target_index: int, 
                       total_steps: int, steps_data: list, 
                       user_role: str = None) -> Tuple[bool, str]:
        """
        Validate if navigation to target step is allowed.
        
        Args:
            current_index: Current step index
            target_index: Target step index
            total_steps: Total number of steps
            steps_data: List of TestStep objects
            user_role: Current user role (from AuthManager)
            
        Returns:
            (allowed: bool, reason: str)
        """
        # Basic validation
        if target_index < 0 or target_index >= total_steps:
            return (False, "Geçersiz adım numarası")
        
        if target_index == current_index:
            return (False, "Zaten bu adımdasınız")
        
        # ========================================================================
        # ROLE-BASED NAVIGATION RULES
        # ========================================================================
        
        # Going backward (to previous steps)
        if target_index < current_index:
            # Only admins can go backward
            if user_role == config.UserRole.ADMIN:
                logger.info(f"Admin navigating backward: {current_index} → {target_index}")
                return (True, "")
            else:
                return (False, "Geri gitme yetkisi yok. Sadece yönetici geri gidebilir.")
        
        # Going forward (to next steps)
        elif target_index > current_index:
            # Everyone can go forward (sequential)
            # In the future, might add: "can only skip 1 step" rule
            return (True, "")
        
        return (True, "")
    
    def determine_navigation_mode(self, current_index: int, target_index: int,
                                  target_step_status: TestStatus) -> NavigationMode:
        """
        Determine appropriate navigation mode based on context.
        
        Args:
            current_index: Current step index
            target_index: Target step index
            target_step_status: Status of target step
            
        Returns:
            NavigationMode enum value
        """
        # Going backward to completed step
        if target_index < current_index:
            if target_step_status in [TestStatus.PASSED, TestStatus.FAILED]:
                return NavigationMode.VIEW_ONLY
            else:
                return NavigationMode.NORMAL
        
        # Going forward to not-started step
        elif target_index > current_index:
            return NavigationMode.NORMAL
        
        # Same step (shouldn't happen)
        else:
            return NavigationMode.VIEW_ONLY
    
    def record_navigation(self, from_index: int, to_index: int):
        """
        Record navigation event in history.
        
        Args:
            from_index: Starting step index
            to_index: Target step index
        """
        import time
        
        self.navigation_history.append({
            'from': from_index,
            'to': to_index,
            'timestamp': time.time()
        })
        
        logger.debug(f"Navigation recorded: {from_index} → {to_index}")
    
    def get_navigation_history(self) -> list:
        """Get navigation history"""
        return self.navigation_history.copy()
```

# managers\result_manager.py

```py
"""
Result Manager
Handles test result saving and validation
"""
from typing import Any, Optional
from PyQt5.QtCore import QObject, pyqtSignal

from models.enums import TestStatus, InputType
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ResultManager(QObject):
    """
    Manages test result saving and validation.
    
    Features:
    - Result validation
    - Status determination
    - Change tracking
    
    Signals:
        result_saved: (step_index, result_value, status)
        result_changed: (step_index, old_value, new_value)
    """
    
    result_saved = pyqtSignal(int, object, str)      # step_index, value, status
    result_changed = pyqtSignal(int, object, object)  # step_index, old, new
    
    def __init__(self, auth_manager=None):
        self.auth_manager = auth_manager
        super().__init__()
        logger.info("ResultManager initialized")
    
    def save_result(self, step, step_index: int, result_value: Any, 
                   checkbox_value: Optional[str], comment: str, 
                   is_valid: Optional[bool], actual_duration: int):
        """
        Save result to test step.
        
        Args:
            step: TestStep object
            step_index: Step index
            result_value: Result value (number or None)
            checkbox_value: Checkbox value ("PASS"/"FAIL" or None)
            comment: Comment text
            is_valid: Whether value is valid (True/False/None)
            actual_duration: Time taken in seconds
            
        Returns:
            TestStatus enum value
        """
        # Track old value for change detection
        old_value = step.result_value
        
        # Determine which value to save
        if checkbox_value:
            final_value = checkbox_value
        elif result_value:
            final_value = result_value
        else:
            final_value = None
        
        # Save to step
        step.result_value = final_value
        step.comment = comment
        step.actual_duration = actual_duration
        step.completed_by = self.auth_manager.get_display_name()
        # Determine status
        status = self._determine_status(step.input_type, is_valid)
        step.status = status
        
        # Emit signals
        if old_value != final_value:
            self.result_changed.emit(step_index, old_value, final_value)
        
        self.result_saved.emit(step_index, final_value, status.value)
        
        logger.info(f"Result saved for step {step_index}: {final_value} ({status.value})")
        
        return status
    
    def _determine_status(self, input_type: InputType, is_valid: Optional[bool]) -> TestStatus:
        """
        Determine test status based on input type and validity.
        
        Args:
            input_type: Type of input
            is_valid: Whether input is valid (True/False/None)
            
        Returns:
            TestStatus enum value
        """
        if is_valid is None:
            # No validation (InputType.NONE)
            return TestStatus.PASSED  # Or NOT_APPLICABLE if you prefer
        
        elif is_valid is True:
            return TestStatus.PASSED
        
        else:  # is_valid is False
            return TestStatus.FAILED
    
    def validate_result(self, input_type: InputType, result_value: Any,
                       validation_rules: dict) -> bool:
        """
        Validate result value against rules.
        
        Args:
            input_type: Type of input
            result_value: Value to validate
            validation_rules: Validation rules dict
            
        Returns:
            True if valid, False otherwise
        """
        if input_type == InputType.NUMBER:
            try:
                value = float(result_value)
                min_val = validation_rules.get('min')
                max_val = validation_rules.get('max')
                
                if min_val is not None and value < min_val:
                    return False
                if max_val is not None and value > max_val:
                    return False
                
                return True
            except (ValueError, TypeError):
                return False
        
        elif input_type == InputType.PASS_FAIL:
            return result_value in ["PASS", "FAIL", "GEÇTİ", "KALDI"]
        
        else:
            return True
```

# managers\test_manager.py

```py
"""
Test Manager (REFACTORED)
Orchestrates test flow using specialized managers
"""
from typing import List, Optional, Dict, Any
import json
import time
from PyQt5.QtCore import QObject, pyqtSignal

from models import TestStep, TestStatus
from models.test_session import TestSession
from models.enums import NavigationMode
from managers.timer_manager import TimerManager
from managers.navigation_manager import NavigationManager
from managers.result_manager import ResultManager
from persistence.continuous_writer import ContinuousWriter
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)


class TestManager(QObject):
    """
    Test Manager - Main Orchestrator (Refactored)
    
    Delegates to specialized managers:
    - TimerManager: Timing logic
    - NavigationManager: Navigation validation
    - ResultManager: Result saving
    
    Signals:
        step_changed: (step_index, total_steps, mode)
        timer_updated: (remaining_seconds, timer_status)
        test_completed: ()
        result_submitted: (step_index, result_value, status)
    """
    
    # Signals
    step_changed = pyqtSignal(int, int, str)  # index, total, mode
    timer_updated = pyqtSignal(int, str)      # remaining, status
    test_completed = pyqtSignal()
    result_submitted = pyqtSignal(int, object, str)  # index, value, status
    
    def __init__(self, auth_manager=None):
        super().__init__()
        self.auth_manager = auth_manager
        # Specialized managers
        self.timer_manager = TimerManager()
        self.navigation_manager = NavigationManager()
        self.result_manager = ResultManager(auth_manager)
        
        # Connect manager signals
        self.timer_manager.timer_tick.connect(self._on_timer_tick)
        
        # Test data
        self.session: Optional[TestSession] = None
        self.steps: List[TestStep] = []
        self.test_info: Dict[str, str] = {}
        self.current_step_index: int = -1
        
        # Continuous writer
        self.continuous_writer = ContinuousWriter()
        
        logger.info("TestManager initialized (refactored)")
    
    # ════════════════════════════════════════════════════════
    # LOADING
    # ════════════════════════════════════════════════════════
    
    def load_test_from_file(self, filepath: str, test_info: dict = None) -> bool:
        """Load test procedure from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load test info from file
            self.test_info = data.get('test_info', {})
            
            # Override with provided test_info if given
            if test_info:
                self.test_info.update(test_info)
            
            # Load steps
            self.steps = []
            for step_data in data.get('steps', []):
                step = TestStep.from_dict(step_data)
                self.steps.append(step)
            
            # Create session (don't pass steps in constructor)
            self.session = TestSession(
                stock_number=self.test_info.get('stock_number', ''),
                serial_number=self.test_info.get('serial_number', ''),
                station_number=self.test_info.get('station_number', ''),
                sip_code=self.test_info.get('sip_code', '')
            )
            
            # Assign steps to session after creation
            self.session.steps = self.steps
            
            # Set session in continuous writer
            self.continuous_writer.set_session(self.session)
            
            logger.info(f"Loaded {len(self.steps)} test steps from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load test file {filepath}: {e}")
            return False    
    # ════════════════════════════════════════════════════════
    # TEST FLOW
    # ════════════════════════════════════════════════════════
    
    def start_test(self) -> bool:
        """Start test from first step"""
        if not self.steps:
            logger.error("Cannot start test: No steps loaded")
            return False
        
        # Start session (manually set start time)
        if self.session:
            from datetime import datetime
            self.session.start_time = datetime.now()
        
        # Navigate to first step
        self.navigate_to_step(0, NavigationMode.NORMAL)
        
        # Write initial state
        self._write_update()
        
        logger.info("Test procedure started")
        return True
    # ════════════════════════════════════════════════════════
    # NAVIGATION (Delegated to NavigationManager)
    # ════════════════════════════════════════════════════════
    
    def navigate_to_step(self, target_index: int, mode: NavigationMode = NavigationMode.NORMAL):
        """
        Navigate to specific step.
        
        Args:
            target_index: Step to navigate to
            mode: Navigation mode (NORMAL, VIEW_ONLY, etc.)
        """
        user_role = None
        if self.auth_manager:
            user_role = self.auth_manager.get_role()
        # Validate navigation
        allowed, reason = self.navigation_manager.can_navigate_to(
            self.current_step_index,
            target_index,
            len(self.steps),
            self.steps, user_role=user_role 
        )
        
        if not allowed:
            logger.warning(f"Navigation blocked: {reason}")
            self.navigation_manager.navigation_blocked.emit(reason)
            return
        
        # Stop current timer
        if self.current_step_index >= 0:
            self.timer_manager.stop_timer(self.current_step_index)
        
        # Record navigation
        if self.current_step_index >= 0:
            self.navigation_manager.record_navigation(self.current_step_index, target_index)
        
        # Update index
        old_index = self.current_step_index
        self.current_step_index = target_index
        
        # Update step status
        target_step = self.steps[target_index]
        if target_step.status == TestStatus.NOT_STARTED:
            target_step.status = TestStatus.IN_PROGRESS
            target_step.start_time = time.time()
        
        # Emit signal
        self.step_changed.emit(target_index, len(self.steps), mode.value)
        
        # Start timer based on mode
        if mode == NavigationMode.NORMAL:
            self.timer_manager.start_timer(target_index, target_step.time_limit)
        # For VIEW_ONLY, EDIT modes: no timer
        
        # Write update
        self._write_update()
        
        logger.info(f"Navigated: {old_index} → {target_index} (mode: {mode.value})")
    
    def navigate_next(self):
        """Navigate to next step"""
        if self.current_step_index < len(self.steps) - 1:
            self.navigate_to_step(self.current_step_index + 1, NavigationMode.NORMAL)
        else:
            self._complete_test()
    
    def navigate_previous(self):
        """Navigate to previous step (view mode)"""
        if self.current_step_index > 0:
            self.navigate_to_step(self.current_step_index - 1, NavigationMode.VIEW_ONLY)
    
    # ════════════════════════════════════════════════════════
    # RESULT HANDLING (Delegated to ResultManager)
    # ════════════════════════════════════════════════════════
    
    def submit_result(self, result_value: Any, checkbox_value: Optional[str],
                     comment: str, is_valid: Optional[bool]):
        """
        Submit result for current step.
        
        Args:
            result_value: Numeric result or None
            checkbox_value: "PASS"/"FAIL" or None
            comment: Comment text
            is_valid: Whether value is valid (True/False/None)
        """
        current_step = self.get_current_step()
        if current_step is None:
            logger.error("Cannot submit result: No current step")
            return
        
        # Get elapsed time
        actual_duration = self.timer_manager.get_elapsed_time(self.current_step_index)
        
        # Save result
        status = self.result_manager.save_result(
            current_step,
            self.current_step_index,
            result_value,
            checkbox_value,
            comment,
            is_valid,
            actual_duration
        )
        
        # Stop timer
        self.timer_manager.stop_timer(self.current_step_index)
        
        # Emit signal
        final_value = checkbox_value if checkbox_value else result_value
        self.result_submitted.emit(self.current_step_index, final_value, status.value)
        
        # Write update
        self._write_update()
        
        logger.info(f"Result submitted for step {self.current_step_index + 1}")
        
        # Auto-navigate to next step
        self.navigate_next()
    
    # ════════════════════════════════════════════════════════
    # TIMER (Delegated to TimerManager)
    # ════════════════════════════════════════════════════════
    
    def _on_timer_tick(self, step_index: int, remaining: int, status: str):
        """Handle timer tick from TimerManager"""
        # Only emit if it's for current step
        if step_index == self.current_step_index:
            self.timer_updated.emit(remaining, status)
            
            # Auto-save every N seconds
            elapsed = self.timer_manager.get_elapsed_time(step_index)
            if elapsed > 0 and elapsed % config.DEFAULT_UPDATE_INTERVAL == 0:
                self._write_update()
    
    def get_elapsed_time(self) -> int:
        """Get elapsed time for current step"""
        if self.current_step_index >= 0:
            return self.timer_manager.get_elapsed_time(self.current_step_index)
        return 0
    
    def get_remaining_time(self) -> int:
        """Get remaining time for current step"""
        if self.current_step_index >= 0:
            return self.timer_manager.get_remaining_time(self.current_step_index)
        return 0
    
    # ════════════════════════════════════════════════════════
    # COMPLETION
    # ════════════════════════════════════════════════════════
    def _complete_test(self):
        """Complete the test procedure"""
        self.timer_manager.stop_timer(self.current_step_index)
        
        if self.session:
            # Set end time (duration_seconds is auto-calculated as a property)
            from datetime import datetime
            self.session.end_time = datetime.now()
            
            # DON'T set duration_seconds - it's a read-only property!
            # The TestSession class calculates it automatically from start_time and end_time
        
        # Write final state
        self._write_update()
        
        logger.info("Test procedure completed")
        self.test_completed.emit()
        
    # ════════════════════════════════════════════════════════
    # QUERIES
    # ════════════════════════════════════════════════════════
    
    def get_current_step(self) -> Optional[TestStep]:
        """Get current test step"""
        if 0 <= self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None
    
    def get_step(self, index: int) -> Optional[TestStep]:
        """Get specific step by index"""
        if 0 <= index < len(self.steps):
            return self.steps[index]
        return None
    
    def get_progress_percentage(self) -> float:
        """Calculate completion percentage"""
        if not self.steps:
            return 0.0
        completed = sum(1 for s in self.steps if s.status in [TestStatus.PASSED, TestStatus.FAILED])
        return (completed / len(self.steps)) * 100
    
    def get_test_info(self) -> Dict[str, str]:
        """Get test metadata"""
        return self.test_info.copy()
    
    # ════════════════════════════════════════════════════════
    # PERSISTENCE
    # ════════════════════════════════════════════════════════
    
    def set_continuous_output_directory(self, folder: str) -> bool:
        """Set output directory for continuous updates"""
        return self.continuous_writer.set_output_directory(folder)
    
    def _write_update(self):
        """Write continuous update to JSON"""
        if self.session and self.continuous_writer:
            try:
                # Change write_data() to write_update()
                self.continuous_writer.write_update()
            except Exception as e:
                logger.error(f"Failed to write update: {e}")
```

# managers\timer_manager.py

```py
"""
Timer Manager
Handles timing for individual test steps
"""
import time
from typing import Dict, Optional
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

import config
from models.enums import TimerStatus
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TimerManager(QObject):
    """
    Manages timers for test steps.
    
    Features:
    - Independent timer per step
    - Pause/resume support
    - Elapsed time tracking
    - Timer status calculation
    
    Signals:
        timer_tick: Emitted every second (step_index, remaining_seconds, status)
    """
    
    timer_tick = pyqtSignal(int, int, str)  # step_index, remaining, status
    
    def __init__(self):
        super().__init__()
        
        # Timer data: step_index -> {start_time, elapsed, paused, limit}
        self.step_timers: Dict[int, dict] = {}
        
        # Active timer
        self.active_step_index: Optional[int] = None
        
        # QTimer for updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._on_timer_tick)
        self.update_timer.setInterval(config.TIMER_UPDATE_INTERVAL)
        
        logger.info("TimerManager initialized")
    
    def start_timer(self, step_index: int, time_limit: int):
        """
        Start timer for a specific step.
        
        Args:
            step_index: Step to start timer for
            time_limit: Time limit in seconds
        """
        # Initialize timer data if new
        if step_index not in self.step_timers:
            self.step_timers[step_index] = {
                'start_time': time.time(),
                'elapsed': 0,
                'paused': False,
                'limit': time_limit
            }
        else:
            # Resume paused timer
            timer_data = self.step_timers[step_index]
            timer_data['start_time'] = time.time()
            timer_data['paused'] = False
            timer_data['limit'] = time_limit
        
        # Set as active
        self.active_step_index = step_index
        
        # Start update timer
        if not self.update_timer.isActive():
            self.update_timer.start()
        
        logger.info(f"Timer started for step {step_index} (limit: {time_limit}s)")
    
    def stop_timer(self, step_index: int) -> int:
        """
        Stop timer for a specific step.
        
        Args:
            step_index: Step to stop timer for
            
        Returns:
            Total elapsed seconds
        """
        if step_index not in self.step_timers:
            return 0
        
        timer_data = self.step_timers[step_index]
        
        if not timer_data['paused']:
            # Calculate elapsed time since last start
            elapsed_now = int(time.time() - timer_data['start_time'])
            timer_data['elapsed'] += elapsed_now
            timer_data['paused'] = True
        
        # Stop update timer if this was active
        if self.active_step_index == step_index:
            self.active_step_index = None
            self.update_timer.stop()
        
        total_elapsed = timer_data['elapsed']
        logger.info(f"Timer stopped for step {step_index} (elapsed: {total_elapsed}s)")
        
        return total_elapsed
    
    def pause_timer(self, step_index: int):
        """
        Pause timer for a specific step.
        
        Args:
            step_index: Step to pause timer for
        """
        if step_index not in self.step_timers:
            return
        
        timer_data = self.step_timers[step_index]
        
        if not timer_data['paused']:
            elapsed_now = int(time.time() - timer_data['start_time'])
            timer_data['elapsed'] += elapsed_now
            timer_data['paused'] = True
            
            logger.info(f"Timer paused for step {step_index}")
    
    def get_elapsed_time(self, step_index: int) -> int:
        """
        Get elapsed time for a specific step.
        
        Args:
            step_index: Step to get time for
            
        Returns:
            Elapsed seconds (0 if timer never started)
        """
        if step_index not in self.step_timers:
            return 0
        
        timer_data = self.step_timers[step_index]
        
        if timer_data['paused']:
            return timer_data['elapsed']
        else:
            elapsed_now = int(time.time() - timer_data['start_time'])
            return timer_data['elapsed'] + elapsed_now
    
    def get_remaining_time(self, step_index: int) -> int:
        """
        Get remaining time for a specific step.
        
        Args:
            step_index: Step to get remaining time for
            
        Returns:
            Remaining seconds (negative if overtime)
        """
        if step_index not in self.step_timers:
            return 0
        
        timer_data = self.step_timers[step_index]
        elapsed = self.get_elapsed_time(step_index)
        
        return timer_data['limit'] - elapsed
    
    def get_timer_status(self, step_index: int) -> TimerStatus:
        """
        Calculate timer status based on remaining time.
        
        Args:
            step_index: Step to get status for
            
        Returns:
            TimerStatus enum value
        """
        if step_index not in self.step_timers:
            return TimerStatus.NORMAL
        
        timer_data = self.step_timers[step_index]
        remaining = self.get_remaining_time(step_index)
        limit = timer_data['limit']
        
        if remaining < 0:
            return TimerStatus.OVERTIME
        
        percentage = (remaining / limit * 100) if limit > 0 else 100
        
        if percentage > config.TIMER_WARNING_THRESHOLD:
            return TimerStatus.NORMAL
        elif percentage > config.TIMER_CRITICAL_THRESHOLD:
            return TimerStatus.WARNING
        else:
            return TimerStatus.CRITICAL
    
    def _on_timer_tick(self):
        """Called every second to update active timer"""
        if self.active_step_index is None:
            return
        
        remaining = self.get_remaining_time(self.active_step_index)
        status = self.get_timer_status(self.active_step_index)
        
        # Emit signal
        self.timer_tick.emit(self.active_step_index, remaining, status.value)
    
    def clear_timer(self, step_index: int):
        """
        Clear timer data for a specific step.
        
        Args:
            step_index: Step to clear timer for
        """
        if step_index in self.step_timers:
            del self.step_timers[step_index]
            logger.debug(f"Timer cleared for step {step_index}")
    
    def reset_all_timers(self):
        """Reset all timers (for new test session)"""
        self.step_timers.clear()
        self.active_step_index = None
        self.update_timer.stop()
        logger.info("All timers reset")
```

# models\__init__.py

```py
"""
Models Package
Data structures for test procedure application
"""
from models.enums import TestStatus, InputType, TimerStatus, NavigationMode
from models.test_step import TestStep
from models.test_session import TestSession
from models.session_metadata import SessionMetadata

__all__ = [
    'TestStatus', 
    'InputType', 
    'TimerStatus', 
    'NavigationMode',
    'TestStep', 
    'TestSession',
    'SessionMetadata'
]
```

# models\enums.py

```py
"""
Enums and Constants for Test Procedure Application
"""
from enum import Enum


class TestStatus(Enum):
    """Status of a test step"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class InputType(Enum):
    """Type of input required for a test step"""
    NONE = "none"           # No input required
    NUMBER = "number"       # Numeric input
    PASS_FAIL = "pass_fail" # Pass/Fail buttons
    COMMENT = "comment"     # Text comment (optional)


class TimerStatus(Enum):
    """Timer status based on remaining time"""
    NORMAL = "normal"       # > 20% time remaining
    WARNING = "warning"     # 10-20% time remaining
    CRITICAL = "critical"   # < 10% time remaining
    OVERTIME = "overtime"   # Timer has expired


# ════════════════════════════════════════════════════════
# NEW: Navigation mode
# ════════════════════════════════════════════════════════
class NavigationMode(Enum):
    """Navigation mode for step transitions"""
    NORMAL = "normal"          # Fresh start (reset timer)
    VIEW_ONLY = "view_only"    # Just viewing (no timer)
    EDIT = "edit"              # Editing completed step
    RESUME = "resume"          # Resume paused step (future)
```

# models\session_metadata.py

```py
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

"""
Session Metadata Data Model
Contains all test session setup information entered at login

Fields are organized into 3 categories:
1. Ürün Bilgileri (Product Information) - goes to Excel report
2. Yazılım Bilgileri (Software Information) - goes to Excel report
3. Cihaz Kalibrasyonları (Device Calibrations) - goes to Excel report
4. Oturum Bilgileri (Session Info) - İstasyon and SİP for UI only, NOT in Excel
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
from datetime import date, datetime


@dataclass
class SessionMetadata:
    """
    Complete test session metadata.
    
    All fields have defaults for easy initialization.
    Calibration dates are stored as date objects for easy comparison.
    """
    
    # =========================================================================
    # ÜRÜN BİLGİLERİ (Product Information) - Goes to Excel Report
    # =========================================================================
    stok_no: str = ""
    opsiyonel_stok_no: str = ""
    tanim: str = ""  # Tanım (Description)
    teu_udk: str = ""
    seri_no: str = ""
    revizyon_261: str = ""  # 261 revizyonu
    test_donanimi_revizyon: str = ""  # Test Donanımı Revizyon
    test_yazilimi_revizyon: str = ""  # Test Yazılımı Revizyonu
    is_tipi_no: str = ""  # İş Tipi No
    
    # =========================================================================
    # YAZILIM BİLGİLERİ (Software Information) - Goes to Excel Report
    # =========================================================================
    kay_yazilimi_versiyon: str = ""  # KAY Yazılımı Versiyon No
    sky_yazilimi_versiyon: str = ""  # SKY Yazılımı Versiyon No
    
    # =========================================================================
    # CİHAZ KALİBRASYONLARI (Device Calibrations) - Goes to Excel Report
    # Stored as ISO date strings (YYYY-MM-DD) for JSON serialization
    # =========================================================================
    fluke_esa620_kalibrasyon: str = ""  # FLUKE ESA620 kalibrasyon bitiş tarihi
    italsea_7proglcd_kalibrasyon: str = ""  # ITALSEA 7PROGLCD kalibrasyon bitiş tarihi
    geratech_kalibrasyon: str = ""  # Geratech kalibrasyon bitiş tarihi
    iba_magicmax_kalibrasyon: str = ""  # IBA MagicMax kalibrasyon bitiş tarihi
    iba_primus_a_kalibrasyon: str = ""  # IBA Primus A kalibrasyon bitiş tarihi
    
    # =========================================================================
    # OTURUM BİLGİLERİ (Session Info) - UI Header ONLY, NOT in Excel Report
    # =========================================================================
    istasyon: str = ""  # İstasyon (Station) - for UI header only
    sip_code: str = ""  # SİP Kodu - for UI header only
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for JSON serialization.
        
        Returns:
            Dictionary with all fields
        """
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionMetadata':
        """
        Create SessionMetadata from dictionary.
        
        Args:
            data: Dictionary with metadata fields
            
        Returns:
            SessionMetadata instance
        """
        # Filter only known fields to avoid TypeError
        known_fields = {
            'stok_no', 'opsiyonel_stok_no', 'tanim', 'teu_udk', 'seri_no',
            'revizyon_261', 'test_donanimi_revizyon', 'test_yazilimi_revizyon',
            'is_tipi_no', 'kay_yazilimi_versiyon', 'sky_yazilimi_versiyon',
            'fluke_esa620_kalibrasyon', 'italsea_7proglcd_kalibrasyon',
            'geratech_kalibrasyon', 'iba_magicmax_kalibrasyon',
            'iba_primus_a_kalibrasyon', 'istasyon', 'sip_code'
        }
        filtered_data = {k: v for k, v in data.items() if k in known_fields}
        return cls(**filtered_data)
    
    def get_excel_data(self) -> Dict[str, Any]:
        """
        Get only the fields that should appear in Excel report.
        Excludes İstasyon and SİP (UI-only fields).
        
        Returns:
            Dictionary with Excel-exportable fields
        """
        data = self.to_dict()
        # Remove UI-only fields
        data.pop('istasyon', None)
        data.pop('sip_code', None)
        return data
    
    def get_calibration_status(self, field_name: str) -> str:
        """
        Check calibration date status.
        
        Args:
            field_name: Name of calibration field
            
        Returns:
            'valid' (>30 days), 'warning' (<=30 days), 'expired', or 'empty'
        """
        date_str = getattr(self, field_name, "")
        if not date_str:
            return 'empty'
        
        try:
            cal_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            today = date.today()
            days_remaining = (cal_date - today).days
            
            if days_remaining < 0:
                return 'expired'
            elif days_remaining <= 30:
                return 'warning'
            else:
                return 'valid'
        except ValueError:
            return 'empty'
    
    def get_all_calibration_statuses(self) -> Dict[str, str]:
        """
        Get status of all calibration dates.
        
        Returns:
            Dictionary mapping field name to status
        """
        calibration_fields = [
            'fluke_esa620_kalibrasyon',
            'italsea_7proglcd_kalibrasyon',
            'geratech_kalibrasyon',
            'iba_magicmax_kalibrasyon',
            'iba_primus_a_kalibrasyon'
        ]
        return {field: self.get_calibration_status(field) for field in calibration_fields}
    
    def has_expired_calibrations(self) -> bool:
        """
        Check if any calibration is expired.
        
        Returns:
            True if any calibration is expired
        """
        statuses = self.get_all_calibration_statuses()
        return 'expired' in statuses.values()
    
    def format_date_for_display(self, field_name: str) -> str:
        """
        Format a date field for display (DD/MM/YYYY).
        
        Args:
            field_name: Name of date field
            
        Returns:
            Formatted date string or empty string
        """
        date_str = getattr(self, field_name, "")
        if not date_str:
            return ""
        
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except ValueError:
            return date_str
    
    def __repr__(self) -> str:
        return (f"SessionMetadata(stok_no={self.stok_no}, "
                f"seri_no={self.seri_no}, "
                f"istasyon={self.istasyon})")
```

# models\test_session.py

```py
"""
TestSession Data Model
Represents a complete test session with all steps and metadata

Updated to include extended SessionMetadata for:
- Product information
- Software versions
- Device calibrations
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from models.test_step import TestStep
from models.enums import TestStatus
from models.session_metadata import SessionMetadata


class TestSession:
    """
    Represents a complete test execution session.
    
    Tracks all test steps, metadata, timing, and results for a single test run.
    
    Attributes:
        session_id: Unique identifier for this session
        stock_number: Product stock number (from metadata.stok_no)
        serial_number: Product serial number (from metadata.seri_no)
        station_number: Test station identifier (from metadata.istasyon)
        sip_code: SIP code (from metadata.sip_code)
        start_time: Session start timestamp
        end_time: Session end timestamp (None if in progress)
        steps: List of TestStep objects
        metadata: Extended session metadata (NEW)
    """
    
    def __init__(
        self,
        stock_number: str = "",
        serial_number: str = "",
        station_number: str = "",
        sip_code: str = "",
        metadata: Optional[SessionMetadata] = None
    ):
        self.session_id = self._generate_session_id()
        
        # If metadata provided, use it; otherwise use direct parameters
        if metadata:
            self.metadata = metadata
            self.stock_number = metadata.stok_no
            self.serial_number = metadata.seri_no
            self.station_number = metadata.istasyon
            self.sip_code = metadata.sip_code
        else:
            self.metadata = None
            self.stock_number = stock_number
            self.serial_number = serial_number
            self.station_number = station_number
            self.sip_code = sip_code
        
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        
        self.steps: List[TestStep] = []
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID based on timestamp"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def start_session(self):
        """Mark session as started"""
        self.start_time = datetime.now()
    
    def end_session(self):
        """Mark session as ended"""
        self.end_time = datetime.now()
    
    @property
    def is_active(self) -> bool:
        """Check if session is currently active"""
        return self.start_time is not None and self.end_time is None
    
    @property
    def duration_seconds(self) -> Optional[int]:
        """Get total session duration in seconds"""
        if self.start_time is None:
            return None
        
        end = self.end_time or datetime.now()
        return int((end - self.start_time).total_seconds())
    
    def get_completion_percentage(self) -> float:
        """Calculate completion percentage"""
        if not self.steps:
            return 0.0
        
        completed = sum(
            1 for step in self.steps 
            if step.status in [TestStatus.PASSED, TestStatus.FAILED]
        )
        return (completed / len(self.steps)) * 100
    
    def get_passed_count(self) -> int:
        """Count passed steps"""
        return sum(1 for step in self.steps if step.status == TestStatus.PASSED)
    
    def get_failed_count(self) -> int:
        """Count failed steps"""
        return sum(1 for step in self.steps if step.status == TestStatus.FAILED)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert session to dictionary for serialization.
        
        Returns:
            Dictionary representation of session
        """
        data = {
            'session_id': self.session_id,
            'stock_number': self.stock_number,
            'serial_number': self.serial_number,
            'station_number': self.station_number,
            'sip_code': self.sip_code,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'completion_percentage': self.get_completion_percentage(),
            'passed_count': self.get_passed_count(),
            'failed_count': self.get_failed_count(),
            'steps': [step.to_dict() for step in self.steps]
        }
        
        # Include metadata if available
        if self.metadata:
            data['metadata'] = self.metadata.to_dict()
        
        return data
    
    def to_dict_for_excel(self) -> Dict[str, Any]:
        """
        Convert session to dictionary for Excel export.
        Excludes UI-only fields (istasyon, sip_code).
        
        Returns:
            Dictionary with Excel-exportable fields
        """
        data = {
            'session_id': self.session_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'completion_percentage': self.get_completion_percentage(),
            'passed_count': self.get_passed_count(),
            'failed_count': self.get_failed_count(),
            'steps': [step.to_dict() for step in self.steps]
        }
        
        # Include metadata for Excel (without UI-only fields)
        if self.metadata:
            data['metadata'] = self.metadata.get_excel_data()
        else:
            # Fallback to basic stock/serial if no metadata
            data['metadata'] = {
                'stok_no': self.stock_number,
                'seri_no': self.serial_number
            }
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestSession':
        """
        Create TestSession from dictionary.
        
        Args:
            data: Dictionary with session data
            
        Returns:
            TestSession instance
        """
        # Check for metadata
        metadata = None
        if 'metadata' in data and data['metadata']:
            metadata = SessionMetadata.from_dict(data['metadata'])
        
        session = cls(
            stock_number=data.get('stock_number', ''),
            serial_number=data.get('serial_number', ''),
            station_number=data.get('station_number', ''),
            sip_code=data.get('sip_code', ''),
            metadata=metadata
        )
        
        session.session_id = data.get('session_id', session.session_id)
        
        if data.get('start_time'):
            session.start_time = datetime.fromisoformat(data['start_time'])
        if data.get('end_time'):
            session.end_time = datetime.fromisoformat(data['end_time'])
        
        # Load steps
        session.steps = [
            TestStep.from_dict(step_data) 
            for step_data in data.get('steps', [])
        ]
        
        return session
    
    def __repr__(self) -> str:
        status = "Active" if self.is_active else "Completed"
        return (f"TestSession(id={self.session_id}, "
                f"status={status}, "
                f"steps={len(self.steps)}, "
                f"completion={self.get_completion_percentage():.1f}%)")
```

# models\test_step.py

```py
"""
TestStep Data Model
Represents a single step in the test procedure
UPDATED: Added completed_by and completed_at fields to track who/when completed the step
"""
from typing import Optional, Dict, Any
from datetime import datetime
import time
from models.enums import TestStatus, InputType
import config


class TestStep:
    """
    Represents a single test step in the procedure.
    
    Attributes:
        step_id: Unique identifier for the step
        name: Step name/title
        description: Detailed description of the test step
        time_limit: Time limit in seconds
        image_path: Optional path to test step image
        input_type: Type of input required (InputType enum)
        input_label: Label for the input field
        input_validation: Validation rules (e.g., {"min": 0, "max": 100})
        status: Current status of the step (TestStatus enum)
        result_value: User-entered result value
        actual_duration: Actual time taken to complete (seconds)
        comment: Optional comment for the step
        start_time: When the step was started (Unix timestamp)
        completed_by: Display name of user who completed the step
        completed_at: Timestamp when step was completed (overwrites on re-do)
    """
    
    def __init__(
        self,
        step_id: int,
        name: str,
        description: str,
        time_limit: int,
        image_path: Optional[str] = None,
        input_type: InputType = InputType.NONE,
        input_label: str = "Test Sonucu",
        input_validation: Optional[Dict[str, Any]] = None
    ):
        self.step_id = step_id
        self.name = name
        self.description = description
        self.time_limit = time_limit  # seconds
        self.image_path = image_path
        self.input_type = input_type
        self.input_label = input_label
        self.input_validation = input_validation or {}
        
        # Runtime state
        self.status = TestStatus.NOT_STARTED
        self.result_value: Optional[Any] = None
        self.actual_duration: Optional[int] = None
        self.start_time: Optional[float] = None
        self.comment: Optional[str] = None
        
        # User tracking (OVERWRITES on re-submission)
        self.completed_by: Optional[str] = None   # e.g., "Ali Yılmaz", "Sistem Yöneticisi"
        self.completed_at: Optional[float] = None  # Unix timestamp when completed
        
    @property
    def requires_input(self) -> bool:
        """Check if this step requires user input"""
        return self.input_type != InputType.NONE
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for JSON serialization.
        
        Output order is organized for readability:
        1. Step definition (id, name, time_limit, validation)
        2. Execution state (status, result, duration)
        3. User tracking (completed_by, completed_at)
        4. Comments
        """
        return {
            # Step definition
            'step_id': self.step_id,
            'name': self.name,
            'time_limit': self.time_limit,
            'input_validation': self.input_validation,
            
            # Execution state
            'status': self.status.value,
            'result_value': self.result_value,
            'actual_duration': self.actual_duration,
            'start_time': self._format_timestamp(self.start_time),
            
            # User tracking (OVERWRITES on re-submission)
            'completed_by': self.completed_by,
            'completed_at': self._format_timestamp(self.completed_at),
            
            # Comments
            'comment': self.comment
        }
    
    def _format_timestamp(self, timestamp: Optional[float]) -> Optional[str]:
        """
        Format Unix timestamp to human-readable string.
        
        Args:
            timestamp: Unix timestamp (seconds since epoch)
            
        Returns:
            Formatted datetime string or None
        """
        if timestamp is None:
            return None
        
        try:
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime(config.DATETIME_FORMAT)
        except:
            return None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestStep':
        """Create TestStep from dictionary"""
        step = cls(
            step_id=data['step_id'],
            name=data['name'],
            description=data['description'],
            time_limit=data['time_limit'],
            image_path=data.get('image_path'),
            input_type=InputType(data.get('input_type', 'none')),
            input_label=data.get('input_label', 'Test Sonucu'),
            input_validation=data.get('input_validation', {})
        )
        
        # Restore runtime state if present
        if 'status' in data:
            step.status = TestStatus(data['status'])
        if 'result_value' in data:
            step.result_value = data['result_value']
        if 'actual_duration' in data:
            step.actual_duration = data['actual_duration']
        if 'comment' in data:
            step.comment = data['comment']
        if 'completed_by' in data:
            step.completed_by = data['completed_by']
        if 'completed_at' in data:
            step.completed_at = data['completed_at']
            
        return step
    
    def __repr__(self) -> str:
        return f"TestStep(id={self.step_id}, name='{self.name}', status={self.status.value})"
```

# persistence\__init__.py

```py
# -*- coding: utf-8 -*-

from persistence.continuous_writer import ContinuousWriter

__all__ = ['ContinuousWriter']
```

# persistence\continuous_writer.py

```py
"""
Continuous Data Writer
Writes test session data continuously to a JSON file with overwriting
Folder selection persists between sessions
"""
import json
import os
from typing import Optional
from datetime import datetime
from pathlib import Path

from models.test_session import TestSession
from utils.logger import setup_logger
from utils.settings_manager import SettingsManager
import config

logger = setup_logger(__name__)


class ContinuousWriter:
    """
    Handles continuous writing of test session data to file.
    
    Overwrites the file with updated data after each significant event.
    File name includes station, date, and other key identifiers.
    Folder is selected once and persists between sessions.
    """
    
    def __init__(self):
        self.settings = SettingsManager()
        self.output_directory: str = self.settings.get_update_folder()  # Always has default
        self.output_filepath: Optional[str] = None   # Auto-generated filepath
        self.session: Optional[TestSession] = None
        self.write_enabled = True  # Enabled by default with default folder
        
        logger.info(f"ContinuousWriter initialized with folder: {self.output_directory}")
        
    def set_output_directory(self, directory: str) -> bool:
        """
        Set the output directory for continuous writing.
        Filename will be auto-generated based on session info.
        This setting is saved and persists between app sessions.
        
        Args:
            directory: Path to directory where files will be saved
            
        Returns:
            True if directory is valid and writable
        """
        try:
            # Ensure directory exists
            os.makedirs(directory, exist_ok=True)
            
            # Test write access
            test_file = os.path.join(directory, 'test_write_check.tmp')
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write('test')
            os.remove(test_file)
            
            # Save to persistent settings
            self.settings.set_update_folder(directory)
            
            self.output_directory = directory
            self.write_enabled = True
            
            # Generate filepath if we have session info
            if self.session:
                self._generate_filepath()
            
            logger.info(f"Continuous writer directory set to: {directory}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set output directory {directory}: {e}")
            self.write_enabled = False
            return False
    
    def _generate_filepath(self):
        """Generate the output filepath based on current session info"""
        if not self.output_directory or not self.session:
            return
        
        filename = self.generate_filename(
            self.session.station_number,
            self.session.stock_number
        )
        self.output_filepath = os.path.join(self.output_directory, filename)
        logger.info(f"Generated filepath: {self.output_filepath}")
    
    def set_session(self, session: TestSession):
        """
        Set the test session to track.
        
        Args:
            session: TestSession instance to write
        """
        self.session = session
        
        # Generate new filepath based on session info
        if self.output_directory:
            self._generate_filepath()
        
        logger.debug(f"Session set: {session.session_id}")
    
    def write_update(self) -> bool:
        """
        Write current session state to file (overwriting).
        
        Returns:
            True if write successful
        """
        if not self.write_enabled:
            logger.warning("Continuous writer not enabled (no output file set)")
            return False
        
        if self.session is None:
            logger.warning("No session to write")
            return False
        
        try:
            data = self._prepare_data()
            
            # Write to file (overwrite)
            with open(self.output_filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Session data written to {self.output_filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write session data: {e}")
            return False
    
    def _prepare_data(self) -> dict:
        """
        Prepare session data for writing.
        
        Returns:
            Dictionary with formatted session data
        """
        data = self.session.to_dict()
        
        # Add metadata
        data['last_updated'] = datetime.now().isoformat()
        data['file_version'] = '1.0'
        
        # Format step data for readability
        formatted_steps = []
        for step_dict in data['steps']:
            formatted_step = {
                'step_id': step_dict['step_id'],
                'name': step_dict['name'],
                'status': step_dict['status'],
                'start_time': self._format_timestamp(step_dict.get('start_time')),
                'actual_duration': step_dict.get('actual_duration'),
                'result_value': step_dict.get('result_value'),
                'comment': step_dict.get('comment'),  # User comment
                'time_limit': step_dict['time_limit'],
                'completed_by': step_dict['completed_by'],
                'input_validation': step_dict.get('input_validation')  # Min/max values
                
            }
            formatted_steps.append(formatted_step)
        
        data['steps'] = formatted_steps
        
        return data
    
    def _format_timestamp(self, timestamp) -> Optional[str]:
        """Format timestamp for display"""
        if timestamp is None:
            return None
        
        # If it's already a string, return as-is
        if isinstance(timestamp, str):
            return timestamp
        
        # If it's a datetime object, format it
        if isinstance(timestamp, datetime):
            return timestamp.strftime(config.DATETIME_FORMAT)
        
        # If it's a Unix timestamp (float), convert to datetime first
        if isinstance(timestamp, (int, float)):
            try:
                dt = datetime.fromtimestamp(timestamp)
                return dt.strftime(config.DATETIME_FORMAT)
            except:
                return str(timestamp)
        
        return str(timestamp)
    
    def disable(self):
        """Disable continuous writing"""
        self.write_enabled = False
        logger.info("Continuous writer disabled")
    
    def is_enabled(self) -> bool:
        """
        Check if continuous writing is enabled.
        
        Returns True if we have a valid directory and filepath.
        Note: Always enabled by default with default folder.
        """
        return (self.write_enabled and 
                self.output_directory is not None and 
                self.output_filepath is not None)
    
    def get_current_directory(self) -> str:
        """Get the current output directory"""
        return self.output_directory
    
    def get_current_filepath(self) -> Optional[str]:
        """Get the current output filepath (if generated)"""
        return self.output_filepath
    
    @staticmethod
    def generate_filename(station_number: str, stock_number: str = "") -> str:
        """
        Generate filename with station, date, and identifiers.
        
        Format: GuncellemeRaporu_<STATION>_<DATE>_<STOCK>.json
        Example: GuncellemeRaporu_ST-01_20260123_ABC123.json
        
        Args:
            station_number: Station identifier
            stock_number: Optional stock number
            
        Returns:
            Suggested filename
        """
        date_str = datetime.now().strftime("%Y%m%d")
        
        parts = ["GuncellemeRaporu", station_number, date_str]
        
        if stock_number:
            # Clean stock number (remove special chars)
            clean_stock = "".join(c for c in stock_number if c.isalnum() or c in "-_")
            parts.append(clean_stock)
        
        filename = "_".join(parts) + ".json"
        
        return filename
```

# readme.txt

```txt
npx ai-digest to codebase.md
```

# requirements.txt

```txt
# Test Procedure Application - Python Dependencies
# For PyInstaller builds

# GUI Framework
PyQt5==5.15.10
PyQt5-Qt5==5.15.2
PyQt5-sip==12.13.0

# Excel Export
openpyxl==3.1.2
et-xmlfile==1.1.0

# UI Themes
qt-material==2.14
qdarkstyle==3.2.1

# Required for Excel/JSON
Jinja2==3.1.2

# Build Tool (for creating executable)
pyinstaller==6.3.0

# Optional but recommended
# Pillow==10.1.0  # If you need to create/convert icons

```

# resources\icons\happy.png

This is a binary file of the type: Image

# resources\icons\sad.png

This is a binary file of the type: Image

# resources\images\step_001.png

This is a binary file of the type: Image

# resources\images\step_002.png

This is a binary file of the type: Image

# TestProcedure.spec

```spec
# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File for Test Procedure Application
Publisher: X
Version: 1.0
FIXED: Excludes pandas/numpy to reduce size and prevent errors
FIXED: Removed problematic empty list causing icon error
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Application metadata
APP_NAME = 'TestProcedure'
APP_VERSION = '1.0'
APP_PUBLISHER = 'X'  # Change this to your actual publisher name
APP_COPYRIGHT = 'Copyright (c) 2026 X'
APP_DESCRIPTION = 'Test Prosedürü Uygulaması - Manufacturing Quality Control System'

# Collect all data files
datas = []
datas += collect_data_files('qt_material')
datas += collect_data_files('qdarkstyle')

# Add your data folders
datas += [('data', 'data')]
datas += [('resources', 'resources')]

# Collect only necessary submodules
hiddenimports = [
    'openpyxl.cell._writer',
]

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude heavy packages not needed
        'tkinter',
        'matplotlib',
        'numpy',           # NOT NEEDED - pandas is imported but not used
        'scipy',
        'pandas',          # NOT NEEDED - imported but not actually used
        'IPython',         # NOT NEEDED - Spyder/Jupyter stuff
        'jedi',            # NOT NEEDED - Code completion
        'parso',           # NOT NEEDED - Parser
        'black',           # NOT NEEDED - Code formatter
        'sphinx',          # NOT NEEDED - Documentation
        'docutils',        # NOT NEEDED
        'pygments',        # NOT NEEDED - Syntax highlighting
        'astroid',         # NOT NEEDED - Code analysis
        'wcwidth',         # NOT NEEDED
        'zmq',             # NOT NEEDED - Messaging
        'nbformat',        # NOT NEEDED - Jupyter notebooks
        'jsonschema',      # NOT NEEDED
        'cryptography',    # NOT NEEDED - unless you use encryption
        'bcrypt',          # NOT NEEDED
        'certifi',         # NOT NEEDED
        'urllib3',         # NOT NEEDED
        'charset_normalizer', # NOT NEEDED
        'psutil',          # NOT NEEDED
        'cloudpickle',     # NOT NEEDED
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to False for GUI-only app (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Windows-specific metadata
    version='version_info.txt',
    # icon='resources/icons/app_icon.ico',  # Add icon later if needed
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)

```

# ui\__init__.py

```py
"""
UI Package
User interface components
"""
```

# ui\dialogs\__init__.py

```py
# -*- coding: utf-8 -*-

"""
Dialogs Package
Dialog windows for the application
"""
from ui.dialogs.update_settings_dialog import UpdateSettingsDialog
from ui.dialogs.switch_user_dialog import SwitchUserDialog
from ui.dialogs.test_session_setup_dialog import TestSessionSetupDialog
from ui.dialogs.test_step_editor_dialog import TestStepEditorDialog

__all__ = [
    'UpdateSettingsDialog', 
    'SwitchUserDialog',
    'TestSessionSetupDialog',
    'TestStepEditorDialog'
]
```

# ui\dialogs\login_dialog.py

```py
# -*- coding: utf-8 -*-

"""
Login Dialog - 3 Role System
Supports: Admin, Operator, Developer

Features:
- Dropdown to select operator (no password needed)
- Password field for admin/developer login
- Shows user's department and employee ID
- Developer mode indicator
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QMessageBox, QFrame, QComboBox,
                             QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LoginDialog(QDialog):
    """
    3-Role login dialog:
    
    1. Operator Selection (dropdown, no password)
    2. Admin/Developer Login (username + password)
    
    Developer has all admin rights + can_edit_test_steps (future)
    """
    
    def __init__(self, auth_manager, parent=None):
        """
        Initialize the login dialog.
        
        Args:
            auth_manager: AuthManager instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.user_authenticated = False
        
        self.setWindowTitle("Giriş Yap")
        self.setFixedSize(950,720)
        self.setModal(True)
        
        self._init_ui()
        
        logger.debug("LoginDialog initialized (3-Role System)")
    
    def _init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(30, 20, 30, 20)
        
        # ====================================================================
        # Header
        # ====================================================================
        header_label = QLabel("Test Prosedür Uygulaması")
        header_label.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_LARGE + 2}pt;
            color: {config.Colors.TEXT_PRIMARY};
            font-weight: bold;
            padding-bottom: 5px;
        """)
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)
        
        # ====================================================================
        # SECTION 1: Operator Selection (Dropdown - No Password)
        # ====================================================================
        operator_group = QGroupBox("👷 Operatör Girişi")
        operator_group.setStyleSheet(f"""
            QGroupBox {{
                font-size: {config.FONT_SIZE + 1}pt;
                font-weight: bold;
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.ACCENT_BLUE};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        
        operator_layout = QVBoxLayout()
        operator_layout.setSpacing(8)
        
        # Operator dropdown
        operator_label = QLabel("Operatör Seçin:")
        operator_label.setStyleSheet(f"font-size: {config.FONT_SIZE}pt; color: {config.Colors.TEXT_PRIMARY};")
        operator_layout.addWidget(operator_label)
        
        self.operator_combo = QComboBox()
        self.operator_combo.setMinimumHeight(42)
        self.operator_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 8px;
                font-size: {config.FONT_SIZE + 1}pt;
                border: 2px solid {config.Colors.BORDER};
                border-radius: 6px;
                background-color: {config.Colors.BACKGROUND_TERTIARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
            QComboBox:hover {{ border: 2px solid {config.Colors.ACCENT_BLUE}; }}
            QComboBox::drop-down {{ border: none; width: 30px; }}
            QComboBox QAbstractItemView {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                color: {config.Colors.TEXT_PRIMARY};
                selection-background-color: {config.Colors.ACCENT_BLUE};
            }}
        """)
        
        self._populate_operators()
        self.operator_combo.currentIndexChanged.connect(self._on_operator_changed)
        operator_layout.addWidget(self.operator_combo)
        
        # Operator info display
        self.operator_info_label = QLabel("")
        self.operator_info_label.setStyleSheet(f"font-size: {config.FONT_SIZE - 1}pt; color: {config.Colors.TEXT_SECONDARY}; padding: 3px;")
        operator_layout.addWidget(self.operator_info_label)
        self._on_operator_changed(0)
        
        # Operator login button
        operator_btn = QPushButton("Operatör Olarak Giriş Yap")
        operator_btn.setMinimumHeight(50)
        operator_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.ACCENT_BLUE};
                color: white;
                padding: 12px;
                font-size: {config.FONT_SIZE_BUTTON + 1}pt;
                font-weight: bold;
                border-radius: 6px;
                border: none;
            }}
            QPushButton:hover {{ background-color: {config.Colors.ACCENT_LIGHT}; }}
            QPushButton:pressed {{ background-color: #1976d2; }}
        """)
        operator_btn.clicked.connect(self._login_as_operator)
        operator_layout.addWidget(operator_btn)
        
        operator_group.setLayout(operator_layout)
        layout.addWidget(operator_group)
        
        # ====================================================================
        # Separator
        # ====================================================================
        separator_layout = QHBoxLayout()
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFixedHeight(2)
        line1.setStyleSheet(f"background-color: {config.Colors.BORDER};")
        
        separator_label = QLabel("VEYA")
        separator_label.setStyleSheet(f"color: {config.Colors.TEXT_SECONDARY}; font-size: {config.FONT_SIZE}pt; padding: 0 15px;")
        
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFixedHeight(2)
        line2.setStyleSheet(f"background-color: {config.Colors.BORDER};")
        
        separator_layout.addWidget(line1)
        separator_layout.addWidget(separator_label)
        separator_layout.addWidget(line2)
        layout.addLayout(separator_layout)
        
        # ====================================================================
        # SECTION 2: Admin/Developer Login (Username + Password)
        # ====================================================================
        admin_group = QGroupBox("🔐 Yetkili Girişi (Admin / Geliştirici)")
        admin_group.setStyleSheet(f"""
            QGroupBox {{
                font-size: {config.FONT_SIZE + 1}pt;
                font-weight: bold;
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.WARNING};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        
        admin_layout = QVBoxLayout()
        admin_layout.setSpacing(6)
        
        # Username input
        username_label = QLabel("Kullanıcı Adı:")
        username_label.setStyleSheet(f"font-size: {config.FONT_SIZE}pt; color: {config.Colors.TEXT_PRIMARY};")
        admin_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adı girin...")
        self.username_input.setMinimumHeight(38)
        self.username_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
                border: 2px solid {config.Colors.BORDER};
                border-radius: 6px;
                background-color: {config.Colors.BACKGROUND_TERTIARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
            QLineEdit:focus {{ border: 2px solid {config.Colors.WARNING}; }}
        """)
        admin_layout.addWidget(self.username_input)
        
        # Password input
        password_label = QLabel("Şifre:")
        password_label.setStyleSheet(f"font-size: {config.FONT_SIZE}pt; color: {config.Colors.TEXT_PRIMARY};")
        admin_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Şifre girin...")
        self.password_input.setMinimumHeight(38)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
                border: 2px solid {config.Colors.BORDER};
                border-radius: 6px;
                background-color: {config.Colors.BACKGROUND_TERTIARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
            QLineEdit:focus {{ border: 2px solid {config.Colors.WARNING}; }}
        """)
        self.password_input.returnPressed.connect(self._login_as_admin)
        admin_layout.addWidget(self.password_input)
        
        # Admin login button
        admin_btn = QPushButton("Yetkili Olarak Giriş Yap")
        admin_btn.setMinimumHeight(50)
        admin_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.WARNING};
                color: white;
                padding: 12px;
                font-size: {config.FONT_SIZE_BUTTON + 1}pt;
                font-weight: bold;
                border-radius: 6px;
                border: none;
            }}
            QPushButton:hover {{ background-color: #f57c00; }}
            QPushButton:pressed {{ background-color: #e65100; }}
        """)
        admin_btn.clicked.connect(self._login_as_admin)
        admin_layout.addWidget(admin_btn)
        
        admin_group.setLayout(admin_layout)
        layout.addWidget(admin_group)
        
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Set dark background
        self.setStyleSheet(f"QDialog {{ background-color: {config.Colors.BACKGROUND_PRIMARY}; }}")
    
    def _populate_operators(self):
        """Populate the operator dropdown with users from auth_manager."""
        self.operator_combo.clear()
        
        operators = self.auth_manager.get_operators() if hasattr(self.auth_manager, 'get_operators') else []
        
        if operators:
            for op in operators:
                display_text = op.get('display_name', op.get('username', 'Operatör'))
                self.operator_combo.addItem(display_text, op)
        else:
            self.operator_combo.addItem("Operatör", {
                'username': 'operator',
                'display_name': 'Operatör',
                'role': 'operator',
                'department': '',
                'employee_id': ''
            })
        
        logger.debug(f"Populated {self.operator_combo.count()} operators")
    
    def _on_operator_changed(self, index):
        """Update operator info display when selection changes."""
        if index < 0:
            return
            
        user_data = self.operator_combo.itemData(index)
        if user_data:
            dept = user_data.get('department', '')
            emp_id = user_data.get('employee_id', '')
            
            info_parts = []
            if emp_id:
                info_parts.append(f"Sicil: {emp_id}")
            if dept:
                info_parts.append(f"Departman: {dept}")
            
            self.operator_info_label.setText(" | ".join(info_parts) if info_parts else "")
    
    def _login_as_operator(self):
        """Login as selected operator."""
        user_data = self.operator_combo.currentData()
        
        if user_data:
            username = user_data.get('username', 'operator')
            self.auth_manager.login_as_operator(username)
            self.user_authenticated = True
            logger.info(f"User logged in as operator: {user_data.get('display_name')}")
            self.accept()
    
    def _login_as_admin(self):
        """Login as admin or developer with username and password."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username:
            QMessageBox.warning(self, "Uyarı", "Lütfen kullanıcı adı girin!", QMessageBox.Ok)
            self.username_input.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, "Uyarı", "Lütfen şifre girin!", QMessageBox.Ok)
            self.password_input.setFocus()
            return
        
        if self.auth_manager.authenticate(username, password):
            self.user_authenticated = True
            
            role = self.auth_manager.get_role()
            display_name = self.auth_manager.get_display_name()
            
            # Role-specific messages
            if role == 'developer':
                permissions = (
                    "✓ Tüm yönetici yetkileri\n"
                    "✓ Geri gitme özelliği aktif\n"
                    "✓ Test adımları düzenleme (yakında)"
                )
                title_suffix = "GELİŞTİRİCİ MODU"
            elif role == 'admin':
                permissions = (
                    "✓ Geri gitme özelliği aktif\n"
                    "✓ Sonuç düzenleme yetkisi\n"
                    "✓ Raporlama yetkisi"
                )
                title_suffix = "YÖNETİCİ MODU"
            else:
                permissions = "Standart yetkiler"
                title_suffix = ""
            
            QMessageBox.information(
                self,
                "Giriş Başarılı",
                f"Hoş geldiniz, {display_name}!\n\n{permissions}",
                QMessageBox.Ok
            )
            
            logger.info(f"User logged in: {display_name} ({role})")
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "Giriş Hatası",
                "Kullanıcı adı veya şifre hatalı!\n\nLütfen tekrar deneyin.",
                QMessageBox.Ok
            )
            self.password_input.clear()
            self.password_input.setFocus()
```

# ui\dialogs\switch_user_dialog.py

```py
# -*- coding: utf-8 -*-

"""
Switch User Dialog - 3 Role System
Allows switching between Operator, Admin, and Developer roles during test execution.

Use case: 
- Operator is running a test and needs to go to a previous step
- Admin/Developer comes over, enters password to switch mode
- Navigate back to the needed step
- Switch back to operator mode when done

Roles:
- Operator: No password, basic test execution
- Admin: Password required, can navigate back
- Developer: Password required, all admin rights + edit test steps (future)

Location: ui/dialogs/switch_user_dialog.py
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QMessageBox, QFrame, QComboBox,
                             QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SwitchUserDialog(QDialog):
    """
    Dialog for switching user roles during test execution.
    
    3 Role System:
    - Operator: Select from dropdown (no password)
    - Admin/Developer: Username + password required
    
    Signals:
        user_switched(str): Emitted when user role changes, sends new role
    """
    
    # Signal emitted when user successfully switches role
    user_switched = pyqtSignal(str)  # Emits new role
    
    def __init__(self, auth_manager, parent=None):
        """
        Initialize the switch user dialog.
        
        Args:
            auth_manager: AuthManager instance for authentication
            parent: Parent widget (usually MainWindow)
        """
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.setWindowTitle("Kullanıcı Değiştir")
        self.setFixedSize(950, 780)
        self.setModal(True)
        self._init_ui()
        
        logger.debug("SwitchUserDialog initialized (3-Role System)")
    
    def _init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(25, 20, 25, 20)
        
        # ====================================================================
        # Current User Info
        # ====================================================================
        current_role = self.auth_manager.get_role()
        current_name = self.auth_manager.get_display_name()
        
        # Determine role display
        if current_role == 'developer':
            role_text = "Geliştirici"
            role_color = config.Colors.SUCCESS
        elif current_role == 'admin':
            role_text = "Yönetici"
            role_color = config.Colors.WARNING
        else:
            role_text = "Operatör"
            role_color = config.Colors.ACCENT_BLUE
        
        is_privileged = current_role in ['admin', 'developer']
        
        # Header
        header_label = QLabel("Kullanıcı Değiştir")
        header_label.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_LARGE}pt;
            color: {config.Colors.TEXT_PRIMARY};
            font-weight: bold;
        """)
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)
        
        # Current user box
        current_user_label = QLabel(f"Mevcut: {current_name} ({role_text})")
        current_user_label.setStyleSheet(f"""
            font-size: {config.FONT_SIZE + 1}pt;
            color: {config.Colors.TEXT_PRIMARY};
            padding: 10px;
            background-color: {config.Colors.BACKGROUND_TERTIARY};
            border-radius: 5px;
            border-left: 4px solid {role_color};
        """)
        current_user_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(current_user_label)
        
        layout.addSpacing(8)
        
        # ====================================================================
        # OPTION 1: Switch to Operator (show if currently admin/developer)
        # ====================================================================
        if is_privileged:
            operator_group = QGroupBox("👷 Operatör Moduna Geç")
            operator_group.setStyleSheet(f"""
                QGroupBox {{
                    font-size: {config.FONT_SIZE + 1}pt;
                    font-weight: bold;
                    color: {config.Colors.TEXT_PRIMARY};
                    border: 2px solid {config.Colors.ACCENT_BLUE};
                    border-radius: 8px;
                    margin-top: 8px;
                    padding-top: 8px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 15px;
                    padding: 0 8px;
                }}
            """)
            
            operator_layout = QVBoxLayout()
            operator_layout.setSpacing(8)
            
            # Operator dropdown
            op_label = QLabel("Operatör Seçin:")
            op_label.setStyleSheet(f"font-size: {config.FONT_SIZE}pt; color: {config.Colors.TEXT_PRIMARY};")
            operator_layout.addWidget(op_label)
            
            self.operator_combo = QComboBox()
            self.operator_combo.setMinimumHeight(40)
            self.operator_combo.setStyleSheet(f"""
                QComboBox {{
                    padding: 8px;
                    font-size: {config.FONT_SIZE}pt;
                    border: 2px solid {config.Colors.BORDER};
                    border-radius: 6px;
                    background-color: {config.Colors.BACKGROUND_TERTIARY};
                    color: {config.Colors.TEXT_PRIMARY};
                }}
                QComboBox:hover {{ border: 2px solid {config.Colors.ACCENT_BLUE}; }}
                QComboBox QAbstractItemView {{
                    background-color: {config.Colors.BACKGROUND_SECONDARY};
                    color: {config.Colors.TEXT_PRIMARY};
                    selection-background-color: {config.Colors.ACCENT_BLUE};
                }}
            """)
            self._populate_operators()
            operator_layout.addWidget(self.operator_combo)
            
            # Switch to operator button
            operator_btn = QPushButton("Operatör Olarak Devam Et")
            operator_btn.setMinimumHeight(45)
            operator_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {config.Colors.ACCENT_BLUE};
                    color: white;
                    padding: 10px;
                    font-size: {config.FONT_SIZE_BUTTON}pt;
                    font-weight: bold;
                    border-radius: 6px;
                    border: none;
                }}
                QPushButton:hover {{ background-color: {config.Colors.ACCENT_LIGHT}; }}
                QPushButton:pressed {{ background-color: #1976d2; }}
            """)
            operator_btn.clicked.connect(self._switch_to_operator)
            operator_layout.addWidget(operator_btn)
            
            # Info text
            info_label = QLabel("⚠ Operatör modunda geri gitme özelliği devre dışıdır")
            info_label.setStyleSheet(f"font-size: {config.FONT_SIZE - 1}pt; color: {config.Colors.TEXT_SECONDARY};")
            info_label.setAlignment(Qt.AlignCenter)
            operator_layout.addWidget(info_label)
            
            operator_group.setLayout(operator_layout)
            layout.addWidget(operator_group)
        
        # ====================================================================
        # Separator
        # ====================================================================
        separator_layout = QHBoxLayout()
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFixedHeight(2)
        line1.setStyleSheet(f"background-color: {config.Colors.BORDER};")
        
        separator_label = QLabel("VEYA")
        separator_label.setStyleSheet(f"color: {config.Colors.TEXT_SECONDARY}; font-size: {config.FONT_SIZE}pt; padding: 0 15px;")
        
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFixedHeight(2)
        line2.setStyleSheet(f"background-color: {config.Colors.BORDER};")
        
        separator_layout.addWidget(line1)
        separator_layout.addWidget(separator_label)
        separator_layout.addWidget(line2)
        layout.addLayout(separator_layout)
        
        # ====================================================================
        # OPTION 2: Switch to Admin/Developer (always show)
        # ====================================================================
        admin_group = QGroupBox("🔐 Yetkili Girişi (Admin / Geliştirici)")
        admin_group.setStyleSheet(f"""
            QGroupBox {{
                font-size: {config.FONT_SIZE + 1}pt;
                font-weight: bold;
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.WARNING};
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
            }}
        """)
        
        admin_layout = QVBoxLayout()
        admin_layout.setSpacing(6)
        
        # Username input
        username_label = QLabel("Kullanıcı Adı:")
        username_label.setStyleSheet(f"font-size: {config.FONT_SIZE}pt; color: {config.Colors.TEXT_PRIMARY};")
        admin_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adı girin...")
        self.username_input.setMinimumHeight(38)
        self.username_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
                border: 2px solid {config.Colors.BORDER};
                border-radius: 6px;
                background-color: {config.Colors.BACKGROUND_TERTIARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
            QLineEdit:focus {{ border: 2px solid {config.Colors.WARNING}; }}
        """)
        admin_layout.addWidget(self.username_input)
        
        # Password input
        password_label = QLabel("Şifre:")
        password_label.setStyleSheet(f"font-size: {config.FONT_SIZE}pt; color: {config.Colors.TEXT_PRIMARY};")
        admin_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Şifre girin...")
        self.password_input.setMinimumHeight(38)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
                border: 2px solid {config.Colors.BORDER};
                border-radius: 6px;
                background-color: {config.Colors.BACKGROUND_TERTIARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
            QLineEdit:focus {{ border: 2px solid {config.Colors.WARNING}; }}
        """)
        self.password_input.returnPressed.connect(self._switch_to_admin)
        admin_layout.addWidget(self.password_input)
        
        # Admin login button
        admin_btn = QPushButton("Yetkili Olarak Giriş Yap")
        admin_btn.setMinimumHeight(45)
        admin_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.WARNING};
                color: white;
                padding: 10px;
                font-size: {config.FONT_SIZE_BUTTON}pt;
                font-weight: bold;
                border-radius: 6px;
                border: none;
            }}
            QPushButton:hover {{ background-color: #f57c00; }}
            QPushButton:pressed {{ background-color: #e65100; }}
        """)
        admin_btn.clicked.connect(self._switch_to_admin)
        admin_layout.addWidget(admin_btn)
        
        # Info text
        info_label = QLabel("✓ Yetkili modunda önceki adımlara geri dönebilirsiniz")
        info_label.setStyleSheet(f"font-size: {config.FONT_SIZE - 1}pt; color: {config.Colors.TEXT_SECONDARY};")
        info_label.setAlignment(Qt.AlignCenter)
        admin_layout.addWidget(info_label)
        
        admin_group.setLayout(admin_layout)
        layout.addWidget(admin_group)
        
        # ====================================================================
        # Cancel Button
        # ====================================================================
        layout.addStretch()
        
        cancel_btn = QPushButton("İptal")
        cancel_btn.setMinimumHeight(38)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BACKGROUND_TERTIARY};
                color: {config.Colors.TEXT_PRIMARY};
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
                border-radius: 5px;
                border: 1px solid {config.Colors.BORDER};
            }}
            QPushButton:hover {{ background-color: {config.Colors.BACKGROUND_SECONDARY}; }}
        """)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        
        self.setLayout(layout)
        
        # Set dark background
        self.setStyleSheet(f"QDialog {{ background-color: {config.Colors.BACKGROUND_PRIMARY}; }}")
        
        # Focus appropriate input
        if not is_privileged:
            self.username_input.setFocus()
    
    def _populate_operators(self):
        """Populate the operator dropdown with users from auth_manager."""
        if not hasattr(self, 'operator_combo'):
            return
            
        self.operator_combo.clear()
        
        operators = self.auth_manager.get_operators() if hasattr(self.auth_manager, 'get_operators') else []
        
        if operators:
            for op in operators:
                display_text = op.get('display_name', op.get('username', 'Operatör'))
                dept = op.get('department', '')
                if dept:
                    display_text += f" ({dept})"
                self.operator_combo.addItem(display_text, op)
        else:
            self.operator_combo.addItem("Operatör", {
                'username': 'operator',
                'display_name': 'Operatör',
                'role': 'operator'
            })
    
    def _switch_to_operator(self):
        """Switch to selected operator (no password needed)"""
        user_data = self.operator_combo.currentData()
        
        if user_data:
            username = user_data.get('username', 'operator')
            self.auth_manager.login_as_operator(username)
            
            display_name = user_data.get('display_name', 'Operatör')
            logger.info(f"User switched to operator: {display_name}")
            
            QMessageBox.information(
                self,
                "Başarılı",
                f"Operatör moduna geçildi: {display_name}\n\n"
                "✗ Geri gitme özelliği devre dışı\n"
                "✓ Sadece ileri gidilebilir",
                QMessageBox.Ok
            )
            
            self.user_switched.emit('operator')
            self.accept()
    
    def _switch_to_admin(self):
        """Switch to admin or developer role (requires password)"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username:
            QMessageBox.warning(self, "Uyarı", "Lütfen kullanıcı adı girin!", QMessageBox.Ok)
            self.username_input.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, "Uyarı", "Lütfen şifre girin!", QMessageBox.Ok)
            self.password_input.setFocus()
            return
        
        if self.auth_manager.authenticate(username, password):
            role = self.auth_manager.get_role()
            display_name = self.auth_manager.get_display_name()
            
            logger.info(f"User switched to {role}: {display_name}")
            
            # Role-specific message
            if role == 'developer':
                permissions = (
                    "✓ Tüm yönetici yetkileri\n"
                    "✓ Geri gitme özelliği aktif\n"
                    "✓ Test adımları düzenleme (yakında)"
                )
                mode_text = "GELİŞTİRİCİ"
            else:
                permissions = (
                    "✓ Geri gitme özelliği aktif\n"
                    "✓ Tamamlanan adımlara tıklayarak gidebilirsiniz"
                )
                mode_text = "YÖNETİCİ"
            
            QMessageBox.information(
                self,
                "Başarılı",
                f"{mode_text} moduna geçildi!\n\n{permissions}",
                QMessageBox.Ok
            )
            
            self.user_switched.emit(role)
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "Hata",
                "Kullanıcı adı veya şifre hatalı!\n\nLütfen tekrar deneyin.",
                QMessageBox.Ok
            )
            self.password_input.clear()
            self.password_input.setFocus()
```

# ui\dialogs\test_session_setup_dialog.py

```py
# -*- coding: utf-8 -*-

"""
Test Session Setup Dialog
Collects all test session metadata before starting a test.

Features:
- 4 sections: Product Info, Software Info, Device Calibrations, Session Info
- Memory: Remembers last entered values from previous session
- Validation: Required fields (Stok No, Seri No) and calibration date warnings
- Calibration status indicators (green/yellow/red)
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QLineEdit, QDateEdit, QMessageBox,
    QGroupBox, QScrollArea, QWidget, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from typing import Optional, Dict, Any
from datetime import datetime, date

import config
from models.session_metadata import SessionMetadata
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TestSessionSetupDialog(QDialog):
    """
    Dialog for collecting test session metadata.
    
    Shows 4 sections:
    1. Ürün Bilgileri (Product Info)
    2. Yazılım Bilgileri (Software Info)
    3. Cihaz Kalibrasyonları (Device Calibrations)
    4. Oturum Bilgileri (Session Info - İstasyon, SİP)
    
    All values are pre-populated from last session (memory feature).
    """
    
    def __init__(self, settings_manager, parent=None):
        """
        Initialize the dialog.
        
        Args:
            settings_manager: SettingsManager instance for saving/loading defaults
            parent: Parent widget
        """
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.metadata: Optional[SessionMetadata] = None
        
        # Input widgets storage
        self.inputs: Dict[str, QWidget] = {}
        
        self.setWindowTitle("Test Oturumu Başlat")
        self.setMinimumSize(1100, 900)
        self.setModal(True)
        
        self._init_ui()
        self._load_defaults()
        
        logger.info("TestSessionSetupDialog initialized")
    
    def _init_ui(self):
        """Initialize the UI components"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("🔧 Test Oturumu Bilgileri")
        header.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_LARGE + 4}pt;
            font-weight: bold;
            color: {config.Colors.TEXT_PRIMARY};
            padding: 10px;
        """)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {config.Colors.BACKGROUND_PRIMARY};
            }}
        """)
        
        # Content widget
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)
        
        # Section 1: Ürün Bilgileri
        content_layout.addWidget(self._create_product_section())
        
        # Section 2: Yazılım Bilgileri
        content_layout.addWidget(self._create_software_section())
        
        # Section 3: Cihaz Kalibrasyonları
        content_layout.addWidget(self._create_calibration_section())
        
        # Section 4: Oturum Bilgileri (İstasyon, SİP)
        content_layout.addWidget(self._create_session_section())
        
        content_layout.addStretch()
        content.setLayout(content_layout)
        scroll.setWidget(content)
        
        main_layout.addWidget(scroll, 1)
        
        # Bottom buttons
        main_layout.addWidget(self._create_button_section())
        
        self.setLayout(main_layout)
        
        # Set dark background
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {config.Colors.BACKGROUND_PRIMARY};
            }}
        """)
    
    def _create_group_box(self, title: str, icon: str = "") -> QGroupBox:
        """Create a styled group box"""
        group = QGroupBox(f"{icon} {title}" if icon else title)
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: {config.FONT_SIZE + 1}pt;
                font-weight: bold;
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.ACCENT_BLUE};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        return group
    
    def _create_input_row(self, label_text: str, field_name: str, 
                          placeholder: str = "") -> QHBoxLayout:
        """Create a label + input row"""
        row = QHBoxLayout()
        row.setSpacing(10)
        
        # Label
        label = QLabel(f"{label_text}:")
        label.setFixedWidth(200)
        label.setStyleSheet(f"""
            font-size: {config.FONT_SIZE}pt;
            color: {config.Colors.TEXT_PRIMARY};
        """)
        row.addWidget(label)
        
        # Input - Made larger with better padding for clearer text
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder or f"{label_text} girin...")
        input_field.setMinimumHeight(55)
        input_field.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px 12px;
                font-size: {config.FONT_SIZE + 1}pt;
                border: 2px solid {config.Colors.BORDER};
                border-radius: 6px;
                background-color: {config.Colors.BACKGROUND_TERTIARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
            QLineEdit:focus {{
                border: 2px solid {config.Colors.ACCENT_BLUE};
            }}
        """)
        row.addWidget(input_field, 1)
        
        # Store reference
        self.inputs[field_name] = input_field
        
        return row
    
    def _create_date_row(self, label_text: str, field_name: str) -> QHBoxLayout:
        """Create a label + date picker row with status indicator"""
        row = QHBoxLayout()
        row.setSpacing(10)
        
        # Label
        label = QLabel(f"{label_text}:")
        label.setFixedWidth(200)
        label.setStyleSheet(f"""
            font-size: {config.FONT_SIZE}pt;
            color: {config.Colors.TEXT_PRIMARY};
        """)
        row.addWidget(label)
        
        # Date picker - Made larger with better padding
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDisplayFormat("dd/MM/yyyy")
        date_edit.setMinimumHeight(55)
        date_edit.setSpecialValueText("Tarih seçin...")  # Empty state text
        date_edit.setStyleSheet(f"""
            QDateEdit {{
                padding: 10px 12px;
                font-size: {config.FONT_SIZE + 1}pt;
                border: 2px solid {config.Colors.BORDER};
                border-radius: 6px;
                background-color: {config.Colors.BACKGROUND_TERTIARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
            QDateEdit:focus {{
                border: 2px solid {config.Colors.ACCENT_BLUE};
            }}
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: right center;
                width: 30px;
                border-left: 1px solid {config.Colors.BORDER};
            }}
        """)
        
        # Connect to status update
        date_edit.dateChanged.connect(lambda: self._update_date_status(field_name))
        
        row.addWidget(date_edit, 1)
        
        # Status indicator
        status_label = QLabel("📅")
        status_label.setFixedWidth(35)
        status_label.setStyleSheet(f"font-size: 18pt;")
        row.addWidget(status_label)
        
        # Store references
        self.inputs[field_name] = date_edit
        self.inputs[f"{field_name}_status"] = status_label
        
        return row
    
    def _update_date_status(self, field_name: str):
        """Update the status indicator for a date field"""
        date_edit = self.inputs.get(field_name)
        status_label = self.inputs.get(f"{field_name}_status")
        
        if not date_edit or not status_label:
            return
        
        selected_date = date_edit.date().toPyDate()
        today = date.today()
        
        # Check if date is the minimum (empty/unset)
        if date_edit.date() == date_edit.minimumDate():
            status_label.setText("📅")
            status_label.setToolTip("Tarih seçilmedi")
            return
        
        days_remaining = (selected_date - today).days
        
        if days_remaining < 0:
            status_label.setText("🔴")
            status_label.setToolTip(f"SÜRESİ DOLMUŞ ({abs(days_remaining)} gün önce)")
        elif days_remaining <= 30:
            status_label.setText("🟡")
            status_label.setToolTip(f"Yakında dolacak ({days_remaining} gün kaldı)")
        else:
            status_label.setText("🟢")
            status_label.setToolTip(f"Geçerli ({days_remaining} gün kaldı)")
    
    def _create_product_section(self) -> QGroupBox:
        """Create the Product Information section"""
        group = self._create_group_box("ÜRÜN BİLGİLERİ", "📦")
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Fields - no required constraints
        layout.addLayout(self._create_input_row("Stok No", "stok_no"))
        layout.addLayout(self._create_input_row("Opsiyonel Stok No", "opsiyonel_stok_no"))
        layout.addLayout(self._create_input_row("Tanım", "tanim"))
        layout.addLayout(self._create_input_row("TEU UDK", "teu_udk"))
        layout.addLayout(self._create_input_row("Seri No", "seri_no"))
        layout.addLayout(self._create_input_row("261 Revizyonu", "revizyon_261"))
        layout.addLayout(self._create_input_row("Test Donanımı Revizyon", "test_donanimi_revizyon"))
        layout.addLayout(self._create_input_row("Test Yazılımı Revizyon", "test_yazilimi_revizyon"))
        layout.addLayout(self._create_input_row("İş Tipi No", "is_tipi_no"))
        
        group.setLayout(layout)
        return group
    
    def _create_software_section(self) -> QGroupBox:
        """Create the Software Information section"""
        group = self._create_group_box("YAZILIM BİLGİLERİ", "💻")
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        layout.addLayout(self._create_input_row("KAY Yazılımı Versiyon No", "kay_yazilimi_versiyon"))
        layout.addLayout(self._create_input_row("SKY Yazılımı Versiyon No", "sky_yazilimi_versiyon"))
        
        group.setLayout(layout)
        return group
    
    def _create_calibration_section(self) -> QGroupBox:
        """Create the Device Calibration section"""
        group = self._create_group_box("CİHAZ KALİBRASYONLARI", "🔧")
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Info label
        info = QLabel("Kalibrasyon bitiş tarihlerini girin (🟢 Geçerli | 🟡 30 gün kaldı | 🔴 Süresi dolmuş)")
        info.setStyleSheet(f"""
            font-size: {config.FONT_SIZE - 1}pt;
            color: {config.Colors.TEXT_SECONDARY};
            padding: 5px;
        """)
        layout.addWidget(info)
        
        layout.addLayout(self._create_date_row("FLUKE ESA620", "fluke_esa620_kalibrasyon"))
        layout.addLayout(self._create_date_row("ITALSEA 7PROGLCD", "italsea_7proglcd_kalibrasyon"))
        layout.addLayout(self._create_date_row("Geratech", "geratech_kalibrasyon"))
        layout.addLayout(self._create_date_row("IBA MagicMax", "iba_magicmax_kalibrasyon"))
        layout.addLayout(self._create_date_row("IBA Primus A", "iba_primus_a_kalibrasyon"))
        
        group.setLayout(layout)
        return group
    
    def _create_session_section(self) -> QGroupBox:
        """Create the Session Info section (İstasyon, SİP - UI only)"""
        group = self._create_group_box("OTURUM BİLGİLERİ", "🏭")
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Info label
        info = QLabel("Bu bilgiler sadece UI başlığında gösterilir, Excel raporuna yazılmaz.")
        info.setStyleSheet(f"""
            font-size: {config.FONT_SIZE - 1}pt;
            color: {config.Colors.TEXT_SECONDARY};
            font-style: italic;
            padding: 5px;
        """)
        layout.addWidget(info)
        
        layout.addLayout(self._create_input_row("İstasyon", "istasyon"))
        layout.addLayout(self._create_input_row("SİP Kodu", "sip_code"))
        
        group.setLayout(layout)
        return group
    
    def _create_button_section(self) -> QWidget:
        """Create the bottom button section"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 15, 0, 0)
        
        layout.addStretch()
        
        # Clear button - same size as continue button
        clear_btn = QPushButton("Temizle")
        clear_btn.setFixedHeight(50)
        clear_btn.setFixedWidth(200)
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_SECONDARY};
                color: white;
                padding: 12px 25px;
                font-size: {config.FONT_SIZE + 1}pt;
                font-weight: bold;
                border-radius: 6px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #8e8e8e;
            }}
        """)
        clear_btn.clicked.connect(self._clear_fields)
        layout.addWidget(clear_btn)
        
        layout.addSpacing(15)
        
        # Continue button - same size as clear button
        continue_btn = QPushButton("Devam Et →")
        continue_btn.setFixedHeight(50)
        continue_btn.setFixedWidth(200)
        continue_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.SUCCESS};
                color: white;
                padding: 12px 25px;
                font-size: {config.FONT_SIZE + 1}pt;
                font-weight: bold;
                border-radius: 6px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #45a049;
            }}
            QPushButton:pressed {{
                background-color: #3d8b40;
            }}
        """)
        continue_btn.clicked.connect(self._on_continue)
        layout.addWidget(continue_btn)
        
        widget.setLayout(layout)
        return widget
    
    def _load_defaults(self):
        """Load last session values from settings"""
        saved_data = self.settings_manager.get_last_session_metadata()
        
        if not saved_data:
            logger.info("No saved session metadata found, using empty defaults")
            return
        
        logger.info("Loading saved session metadata as defaults")
        
        # Load text fields
        text_fields = [
            'stok_no', 'opsiyonel_stok_no', 'tanim', 'teu_udk', 'seri_no',
            'revizyon_261', 'test_donanimi_revizyon', 'test_yazilimi_revizyon',
            'is_tipi_no', 'kay_yazilimi_versiyon', 'sky_yazilimi_versiyon',
            'istasyon', 'sip_code'
        ]
        
        for field in text_fields:
            if field in self.inputs and field in saved_data:
                self.inputs[field].setText(saved_data.get(field, ""))
        
        # Load date fields
        date_fields = [
            'fluke_esa620_kalibrasyon', 'italsea_7proglcd_kalibrasyon',
            'geratech_kalibrasyon', 'iba_magicmax_kalibrasyon',
            'iba_primus_a_kalibrasyon'
        ]
        
        for field in date_fields:
            if field in self.inputs and field in saved_data:
                date_str = saved_data.get(field, "")
                if date_str:
                    try:
                        dt = datetime.strptime(date_str, "%Y-%m-%d")
                        self.inputs[field].setDate(QDate(dt.year, dt.month, dt.day))
                        self._update_date_status(field)
                    except ValueError:
                        pass
    
    def _save_to_settings(self):
        """Save current values to settings for next session"""
        data = {}
        
        # Save text fields
        text_fields = [
            'stok_no', 'opsiyonel_stok_no', 'tanim', 'teu_udk', 'seri_no',
            'revizyon_261', 'test_donanimi_revizyon', 'test_yazilimi_revizyon',
            'is_tipi_no', 'kay_yazilimi_versiyon', 'sky_yazilimi_versiyon',
            'istasyon', 'sip_code'
        ]
        
        for field in text_fields:
            if field in self.inputs:
                data[field] = self.inputs[field].text().strip()
        
        # Save date fields
        date_fields = [
            'fluke_esa620_kalibrasyon', 'italsea_7proglcd_kalibrasyon',
            'geratech_kalibrasyon', 'iba_magicmax_kalibrasyon',
            'iba_primus_a_kalibrasyon'
        ]
        
        for field in date_fields:
            if field in self.inputs:
                date_edit = self.inputs[field]
                if date_edit.date() != date_edit.minimumDate():
                    data[field] = date_edit.date().toString("yyyy-MM-dd")
                else:
                    data[field] = ""
        
        self.settings_manager.set_last_session_metadata(data)
        logger.info("Session metadata saved to settings")
    
    def _clear_fields(self):
        """Clear all input fields"""
        reply = QMessageBox.question(
            self, 
            "Alanları Temizle",
            "Tüm alanlar temizlenecek. Emin misiniz?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            for name, widget in self.inputs.items():
                if isinstance(widget, QLineEdit):
                    widget.clear()
                elif isinstance(widget, QDateEdit):
                    widget.setDate(widget.minimumDate())
            
            logger.info("All fields cleared")
    
    def _validate_inputs(self) -> bool:
        """
        Validate inputs (optional - only check calibration warnings).
        
        Returns:
            True if valid (or user accepts warnings), False otherwise
        """
        # Check for expired calibrations (warning only, not blocking)
        expired_calibrations = []
        date_fields = {
            'fluke_esa620_kalibrasyon': 'FLUKE ESA620',
            'italsea_7proglcd_kalibrasyon': 'ITALSEA 7PROGLCD',
            'geratech_kalibrasyon': 'Geratech',
            'iba_magicmax_kalibrasyon': 'IBA MagicMax',
            'iba_primus_a_kalibrasyon': 'IBA Primus A'
        }
        
        today = date.today()
        for field, name in date_fields.items():
            date_edit = self.inputs.get(field)
            if date_edit and date_edit.date() != date_edit.minimumDate():
                selected_date = date_edit.date().toPyDate()
                if selected_date < today:
                    expired_calibrations.append(name)
        
        if expired_calibrations:
            reply = QMessageBox.warning(
                self,
                "⚠️ Süresi Dolmuş Kalibrasyon",
                f"Aşağıdaki cihazların kalibrasyon süresi dolmuş:\n\n"
                f"• {chr(10).join(expired_calibrations)}\n\n"
                f"Yine de devam etmek istiyor musunuz?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return False
        
        return True
    
    def _on_continue(self):
        """Handle continue button click"""
        if not self._validate_inputs():
            return
        
        # Create metadata object
        self.metadata = SessionMetadata(
            # Product info
            stok_no=self.inputs['stok_no'].text().strip(),
            opsiyonel_stok_no=self.inputs['opsiyonel_stok_no'].text().strip(),
            tanim=self.inputs['tanim'].text().strip(),
            teu_udk=self.inputs['teu_udk'].text().strip(),
            seri_no=self.inputs['seri_no'].text().strip(),
            revizyon_261=self.inputs['revizyon_261'].text().strip(),
            test_donanimi_revizyon=self.inputs['test_donanimi_revizyon'].text().strip(),
            test_yazilimi_revizyon=self.inputs['test_yazilimi_revizyon'].text().strip(),
            is_tipi_no=self.inputs['is_tipi_no'].text().strip(),
            
            # Software info
            kay_yazilimi_versiyon=self.inputs['kay_yazilimi_versiyon'].text().strip(),
            sky_yazilimi_versiyon=self.inputs['sky_yazilimi_versiyon'].text().strip(),
            
            # Calibrations
            fluke_esa620_kalibrasyon=self._get_date_value('fluke_esa620_kalibrasyon'),
            italsea_7proglcd_kalibrasyon=self._get_date_value('italsea_7proglcd_kalibrasyon'),
            geratech_kalibrasyon=self._get_date_value('geratech_kalibrasyon'),
            iba_magicmax_kalibrasyon=self._get_date_value('iba_magicmax_kalibrasyon'),
            iba_primus_a_kalibrasyon=self._get_date_value('iba_primus_a_kalibrasyon'),
            
            # Session info (UI only)
            istasyon=self.inputs['istasyon'].text().strip(),
            sip_code=self.inputs['sip_code'].text().strip()
        )
        
        # Save to settings for next time
        self._save_to_settings()
        
        logger.info(f"Session metadata created: {self.metadata}")
        self.accept()
    
    def _get_date_value(self, field_name: str) -> str:
        """Get date value as ISO string, or empty string if not set"""
        date_edit = self.inputs.get(field_name)
        if date_edit and date_edit.date() != date_edit.minimumDate():
            return date_edit.date().toString("yyyy-MM-dd")
        return ""
    
    def get_metadata(self) -> Optional[SessionMetadata]:
        """
        Get the entered metadata.
        
        Returns:
            SessionMetadata object or None if dialog was cancelled
        """
        return self.metadata
```

# ui\dialogs\test_step_editor_dialog.py

```py
# -*- coding: utf-8 -*-

"""
Test Step Editor Dialog
Allows developers to add, edit, and manage test steps via UI.

Features:
- Left panel: Scrollable list of test steps (number + name)
- Right panel: Step details editor
- Role-based permissions:
  - DEVELOPER: Full access (add/edit/delete all fields)
  - ADMIN: Can only edit time_limit field

IMPORTANT: This dialog handles a bug in TestStep.to_dict() which doesn't include
description, image_path, input_type, and input_label. We work around this by
accessing the original TestStep objects directly.

Location: ui/dialogs/test_step_editor_dialog.py
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
    QPushButton, QLineEdit, QTextEdit, QSpinBox, QComboBox,
    QListWidget, QListWidgetItem, QGroupBox, QScrollArea,
    QMessageBox, QFileDialog, QFrame, QSplitter, QDoubleSpinBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from typing import Optional, List, Dict, Any
import json
import os

import config
from models.enums import InputType
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TestStepEditorDialog(QDialog):
    """
    Dialog for editing test steps.
    
    Layout:
    ┌────────────────────────────────────────────────────────────────┐
    │                    Test Adımları Editörü                       │
    ├──────────────────┬─────────────────────────────────────────────┤
    │  Step List       │  Step Details                               │
    │  (Scrollable)    │                                             │
    │                  │  Name: [_______________]                    │
    │  1. Step Name    │  Description: [________________]            │
    │  2. Step Name    │  Time Limit: [___] seconds                  │
    │  3. Step Name◄   │  Image Path: [___________] [Browse]         │
    │  4. Step Name    │  Input Type: [Dropdown▼]                    │
    │  ...             │                                             │
    │                  │  [If NUMBER selected:]                      │
    │  [+ Yeni Adım]   │  Input Label: [_______________]             │
    │                  │  Min Value: [___] Max Value: [___]          │
    │                  │                                             │
    │                  │  [If PASS_FAIL selected:]                   │
    │                  │  Input Label: "Sonuç" (fixed)               │
    │                  │                                             │
    ├──────────────────┴─────────────────────────────────────────────┤
    │           [Kaydet]  [İptal]  [Adımı Sil]                       │
    └────────────────────────────────────────────────────────────────┘
    
    Signals:
        steps_updated: Emitted when steps are saved (list of complete step dicts)
    """
    
    steps_updated = pyqtSignal(list)  # Emits list of updated step dictionaries
    
    # Input type display names (Turkish)
    INPUT_TYPE_NAMES = {
        InputType.NONE: "Yok (Giriş Yok)",
        InputType.PASS_FAIL: "Geçti-Kaldı",
        InputType.NUMBER: "Sayı"
    }
    
    def __init__(self, test_steps: list, auth_manager=None, parent=None):
        """
        Initialize the test step editor dialog.
        
        Args:
            test_steps: List of TestStep objects (not dicts!) from test_manager.steps
            auth_manager: AuthManager instance for role-based permissions
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Store original TestStep objects and create editable copies
        self.original_steps = test_steps
        self.steps = self._create_step_dicts(test_steps)
        
        self.auth_manager = auth_manager
        self.current_step_index = -1
        self.unsaved_changes = False
        
        # Determine if user is developer (full access) or admin (limited access)
        self.is_developer = False
        if auth_manager:
            role = auth_manager.get_role()
            self.is_developer = (role == config.UserRole.DEVELOPER)
        
        self._init_ui()
        self._populate_step_list()
        
        # Select first step if available
        if self.steps:
            self.step_list.setCurrentRow(0)
            self._on_step_selected(0)
        
        logger.info(f"TestStepEditorDialog initialized with {len(self.steps)} steps "
                   f"(Developer mode: {self.is_developer})")
    
    def _create_step_dicts(self, test_steps: list) -> List[Dict[str, Any]]:
        """
        Create complete step dictionaries from TestStep objects.
        
        This method creates dictionaries with ALL fields needed for TestStep.from_dict(),
        working around the bug where TestStep.to_dict() doesn't include all fields.
        
        Args:
            test_steps: List of TestStep objects
            
        Returns:
            List of complete step dictionaries
        """
        step_dicts = []
        
        for step in test_steps:
            # Create a complete dictionary with all required fields
            step_dict = {
                # Required fields for from_dict
                'step_id': step.step_id,
                'name': step.name,
                'description': step.description,  # This is missing from to_dict()!
                'time_limit': step.time_limit,
                'image_path': step.image_path,  # This is missing from to_dict()!
                'input_type': step.input_type.value,  # This is missing from to_dict()!
                'input_label': step.input_label,  # This is missing from to_dict()!
                'input_validation': step.input_validation,
                
                # Runtime state (optional)
                'status': step.status.value,
                'result_value': step.result_value,
                'actual_duration': step.actual_duration,
                'comment': step.comment,
                'completed_by': step.completed_by,
                'completed_at': step.completed_at,
            }
            step_dicts.append(step_dict)
        
        return step_dicts
    
    def _init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Test Adımları Editörü")
        self.setMinimumSize(1000, 700)
        self.setModal(True)
        
        # Set dark theme
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {config.Colors.BACKGROUND_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
            QLabel {{
                color: {config.Colors.TEXT_PRIMARY};
                font-size: {config.FONT_SIZE}pt;
            }}
            QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
                background-color: {config.Colors.BACKGROUND_TERTIARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER};
                border-radius: 6px;
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
            }}
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
                border: 2px solid {config.Colors.ACCENT_BLUE};
            }}
            QLineEdit:disabled, QTextEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QComboBox:disabled {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                color: {config.Colors.TEXT_DISABLED};
            }}
            QPushButton {{
                background-color: {config.Colors.ACCENT_BLUE};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {config.Colors.ACCENT_LIGHT};
            }}
            QPushButton:pressed {{
                background-color: #1976d2;
            }}
            QPushButton:disabled {{
                background-color: {config.Colors.TEXT_DISABLED};
            }}
            QListWidget {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER};
                border-radius: 6px;
                font-size: {config.FONT_SIZE}pt;
                outline: none;
            }}
            QListWidget::item {{
                padding: 10px;
                border-bottom: 1px solid {config.Colors.BORDER};
            }}
            QListWidget::item:selected {{
                background-color: {config.Colors.ACCENT_BLUE};
                color: white;
            }}
            QListWidget::item:hover {{
                background-color: {config.Colors.BACKGROUND_TERTIARY};
            }}
            QGroupBox {{
                font-size: {config.FONT_SIZE + 1}pt;
                font-weight: bold;
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.ACCENT_BLUE};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("🔧 Test Adımları Editörü")
        title_label.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_LARGE}pt;
            font-weight: bold;
            color: {config.Colors.TEXT_PRIMARY};
            padding: 10px 0;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Role indicator
        if self.is_developer:
            role_text = "🛠️ Geliştirici Modu - Tüm alanları düzenleyebilirsiniz"
            role_color = config.Colors.SUCCESS
        else:
            role_text = "🔒 Yönetici Modu - Sadece süre limitini düzenleyebilirsiniz"
            role_color = config.Colors.WARNING
        
        role_label = QLabel(role_text)
        role_label.setStyleSheet(f"""
            font-size: {config.FONT_SIZE - 1}pt;
            color: {role_color};
            padding: 5px;
            background-color: {config.Colors.BACKGROUND_SECONDARY};
            border-radius: 4px;
        """)
        role_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(role_label)
        
        # Splitter for list and details
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel: Step list
        left_panel = self._create_step_list_panel()
        splitter.addWidget(left_panel)
        
        # Right panel: Step details
        right_panel = self._create_step_details_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions (30% list, 70% details)
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter, 1)
        
        # Bottom buttons
        main_layout.addWidget(self._create_button_panel())
        
        self.setLayout(main_layout)
    
    def _create_step_list_panel(self) -> QWidget:
        """Create the left panel with step list"""
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 10, 0)
        
        # Header
        header = QLabel("📋 Adım Listesi")
        header.setStyleSheet(f"""
            font-size: {config.FONT_SIZE + 1}pt;
            font-weight: bold;
            padding: 5px;
        """)
        layout.addWidget(header)
        
        # Step list
        self.step_list = QListWidget()
        self.step_list.setMinimumWidth(250)
        self.step_list.currentRowChanged.connect(self._on_step_selected)
        layout.addWidget(self.step_list, 1)
        
        # Add new step button (only for developers)
        if self.is_developer:
            add_btn = QPushButton("➕ Yeni Adım Ekle")
            add_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {config.Colors.SUCCESS};
                    padding: 12px;
                }}
                QPushButton:hover {{
                    background-color: #66bb6a;
                }}
            """)
            add_btn.clicked.connect(self._on_add_step)
            layout.addWidget(add_btn)
        
        panel.setLayout(layout)
        return panel
    
    def _create_step_details_panel(self) -> QWidget:
        """Create the right panel with step details editor"""
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 0, 0, 0)
        
        # Header
        header = QLabel("📝 Adım Detayları")
        header.setStyleSheet(f"""
            font-size: {config.FONT_SIZE + 1}pt;
            font-weight: bold;
            padding: 5px;
        """)
        layout.addWidget(header)
        
        # Scroll area for details
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(15)
        
        # Basic Info Group
        basic_group = self._create_basic_info_group()
        scroll_layout.addWidget(basic_group)
        
        # Input Settings Group
        input_group = self._create_input_settings_group()
        scroll_layout.addWidget(input_group)
        
        # Number Input Settings Group (conditionally visible)
        self.number_settings_group = self._create_number_settings_group()
        self.number_settings_group.setVisible(False)
        scroll_layout.addWidget(self.number_settings_group)
        
        scroll_layout.addStretch()
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        
        layout.addWidget(scroll, 1)
        panel.setLayout(layout)
        return panel
    
    def _create_basic_info_group(self) -> QGroupBox:
        """Create the basic information group"""
        group = QGroupBox("📌 Temel Bilgiler")
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 20, 15, 15)
        
        # Step ID (read-only display)
        id_layout = QHBoxLayout()
        id_label = QLabel("Adım No:")
        id_label.setFixedWidth(120)
        self.step_id_display = QLabel("-")
        self.step_id_display.setStyleSheet(f"""
            font-weight: bold;
            color: {config.Colors.ACCENT_BLUE};
        """)
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.step_id_display, 1)
        layout.addLayout(id_layout)
        
        # Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Adım Adı:")
        name_label.setFixedWidth(120)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Adım adını girin...")
        self.name_input.setEnabled(self.is_developer)
        self.name_input.textChanged.connect(self._on_field_changed)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input, 1)
        layout.addLayout(name_layout)
        
        # Description
        desc_layout = QVBoxLayout()
        desc_label = QLabel("Açıklama:")
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Adım açıklamasını girin...")
        self.description_input.setMinimumHeight(100)
        self.description_input.setMaximumHeight(150)
        self.description_input.setEnabled(self.is_developer)
        self.description_input.textChanged.connect(self._on_field_changed)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.description_input)
        layout.addLayout(desc_layout)
        
        # Time Limit (editable by both admin and developer)
        time_layout = QHBoxLayout()
        time_label = QLabel("Süre Limiti:")
        time_label.setFixedWidth(120)
        self.time_limit_input = QSpinBox()
        self.time_limit_input.setRange(1, 3600)  # 1 second to 1 hour
        self.time_limit_input.setSuffix(" saniye")
        self.time_limit_input.setValue(60)
        self.time_limit_input.setEnabled(True)  # Always enabled for admin/developer
        self.time_limit_input.valueChanged.connect(self._on_field_changed)
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_limit_input)
        time_layout.addStretch()
        layout.addLayout(time_layout)
        
        # Image Path
        image_layout = QHBoxLayout()
        image_label = QLabel("Görsel Yolu:")
        image_label.setFixedWidth(120)
        self.image_path_input = QLineEdit()
        self.image_path_input.setPlaceholderText("resources/images/step_xxx.png")
        self.image_path_input.setEnabled(self.is_developer)
        self.image_path_input.textChanged.connect(self._on_field_changed)
        
        browse_btn = QPushButton("Gözat...")
        browse_btn.setFixedWidth(100)
        browse_btn.setEnabled(self.is_developer)
        browse_btn.clicked.connect(self._on_browse_image)
        
        image_layout.addWidget(image_label)
        image_layout.addWidget(self.image_path_input, 1)
        image_layout.addWidget(browse_btn)
        layout.addLayout(image_layout)
        
        group.setLayout(layout)
        return group
    
    def _create_input_settings_group(self) -> QGroupBox:
        """Create the input settings group"""
        group = QGroupBox("⌨️ Giriş Ayarları")
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 20, 15, 15)
        
        # Input Type
        type_layout = QHBoxLayout()
        type_label = QLabel("Giriş Tipi:")
        type_label.setFixedWidth(120)
        self.input_type_combo = QComboBox()
        for input_type, display_name in self.INPUT_TYPE_NAMES.items():
            self.input_type_combo.addItem(display_name, input_type)
        self.input_type_combo.setEnabled(self.is_developer)
        self.input_type_combo.currentIndexChanged.connect(self._on_input_type_changed)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.input_type_combo, 1)
        layout.addLayout(type_layout)
        
        # Input Label (shown conditionally)
        self.input_label_layout = QHBoxLayout()
        input_label_label = QLabel("Giriş Etiketi:")
        input_label_label.setFixedWidth(120)
        self.input_label_input = QLineEdit()
        self.input_label_input.setPlaceholderText("Test Sonucu")
        self.input_label_input.setEnabled(self.is_developer)
        self.input_label_input.textChanged.connect(self._on_field_changed)
        self.input_label_layout.addWidget(input_label_label)
        self.input_label_layout.addWidget(self.input_label_input, 1)
        
        self.input_label_widget = QWidget()
        self.input_label_widget.setLayout(self.input_label_layout)
        self.input_label_widget.setVisible(False)
        layout.addWidget(self.input_label_widget)
        
        # Fixed label for pass/fail
        self.pass_fail_label = QLabel("ℹ️ Geçti-Kaldı seçildiğinde giriş etiketi otomatik olarak 'Sonuç' olur.")
        self.pass_fail_label.setStyleSheet(f"""
            color: {config.Colors.TEXT_SECONDARY};
            font-size: {config.FONT_SIZE - 1}pt;
            font-style: italic;
            padding: 5px;
        """)
        self.pass_fail_label.setVisible(False)
        layout.addWidget(self.pass_fail_label)
        
        group.setLayout(layout)
        return group
    
    def _create_number_settings_group(self) -> QGroupBox:
        """Create the number-specific settings group"""
        group = QGroupBox("🔢 Sayısal Giriş Ayarları")
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 20, 15, 15)
        
        # Min/Max values
        range_layout = QHBoxLayout()
        
        min_label = QLabel("Minimum:")
        min_label.setFixedWidth(80)
        self.min_value_input = QDoubleSpinBox()
        self.min_value_input.setRange(-999999, 999999)
        self.min_value_input.setDecimals(2)
        self.min_value_input.setValue(0)
        self.min_value_input.setEnabled(self.is_developer)
        self.min_value_input.valueChanged.connect(self._on_field_changed)
        
        max_label = QLabel("Maximum:")
        max_label.setFixedWidth(80)
        self.max_value_input = QDoubleSpinBox()
        self.max_value_input.setRange(-999999, 999999)
        self.max_value_input.setDecimals(2)
        self.max_value_input.setValue(100)
        self.max_value_input.setEnabled(self.is_developer)
        self.max_value_input.valueChanged.connect(self._on_field_changed)
        
        range_layout.addWidget(min_label)
        range_layout.addWidget(self.min_value_input)
        range_layout.addSpacing(20)
        range_layout.addWidget(max_label)
        range_layout.addWidget(self.max_value_input)
        range_layout.addStretch()
        layout.addLayout(range_layout)
        
        # Info label
        info_label = QLabel("ℹ️ Girilen değer bu aralıkta olmalıdır.")
        info_label.setStyleSheet(f"""
            color: {config.Colors.TEXT_SECONDARY};
            font-size: {config.FONT_SIZE - 1}pt;
            font-style: italic;
            padding: 5px;
        """)
        layout.addWidget(info_label)
        
        group.setLayout(layout)
        return group
    
    def _create_button_panel(self) -> QWidget:
        """Create the bottom button panel"""
        panel = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 10, 0, 0)
        
        # Delete button (only for developers)
        if self.is_developer:
            self.delete_btn = QPushButton("🗑️ Adımı Sil")
            self.delete_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {config.Colors.ERROR};
                    padding: 12px 20px;
                }}
                QPushButton:hover {{
                    background-color: #e53935;
                }}
            """)
            self.delete_btn.clicked.connect(self._on_delete_step)
            layout.addWidget(self.delete_btn)
        
        layout.addStretch()
        
        # Cancel button
        cancel_btn = QPushButton("İptal")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_SECONDARY};
                padding: 12px 30px;
            }}
        """)
        cancel_btn.clicked.connect(self._on_cancel)
        layout.addWidget(cancel_btn)
        
        # Save button
        save_btn = QPushButton("💾 Kaydet")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.SUCCESS};
                padding: 12px 30px;
            }}
            QPushButton:hover {{
                background-color: #66bb6a;
            }}
        """)
        save_btn.clicked.connect(self._on_save)
        layout.addWidget(save_btn)
        
        panel.setLayout(layout)
        return panel
    
    def _populate_step_list(self):
        """Populate the step list with current steps"""
        self.step_list.clear()
        
        for i, step in enumerate(self.steps):
            step_id = step.get('step_id', i + 1)
            name = step.get('name', f'Adım {step_id}')
            item = QListWidgetItem(f"{step_id}. {name}")
            item.setData(Qt.UserRole, i)  # Store index
            self.step_list.addItem(item)
    
    def _on_step_selected(self, row: int):
        """Handle step selection from list"""
        if row < 0 or row >= len(self.steps):
            return
        
        # Save current step if there were changes
        if self.current_step_index >= 0 and self.unsaved_changes:
            self._save_current_step_to_memory()
        
        self.current_step_index = row
        step = self.steps[row]
        
        # Populate fields
        self.step_id_display.setText(str(step.get('step_id', row + 1)))
        self.name_input.setText(step.get('name', ''))
        self.description_input.setPlainText(step.get('description', ''))
        self.time_limit_input.setValue(step.get('time_limit', 60))
        self.image_path_input.setText(step.get('image_path') or '')
        
        # Input type
        input_type_str = step.get('input_type', 'none')
        try:
            input_type = InputType(input_type_str)
        except ValueError:
            input_type = InputType.NONE
        
        # Find and set combo box index
        for i in range(self.input_type_combo.count()):
            if self.input_type_combo.itemData(i) == input_type:
                self.input_type_combo.setCurrentIndex(i)
                break
        
        # Input label
        self.input_label_input.setText(step.get('input_label', 'Test Sonucu'))
        
        # Number validation
        validation = step.get('input_validation', {})
        self.min_value_input.setValue(validation.get('min', 0))
        self.max_value_input.setValue(validation.get('max', 100))
        
        # Update visibility based on input type
        self._on_input_type_changed(self.input_type_combo.currentIndex())
        
        self.unsaved_changes = False
        logger.debug(f"Step {row + 1} selected: {step.get('name', 'Unknown')}")
    
    def _on_input_type_changed(self, index: int):
        """Handle input type change"""
        input_type = self.input_type_combo.itemData(index)
        
        if input_type == InputType.NONE:
            # No input - hide all input settings
            self.input_label_widget.setVisible(False)
            self.pass_fail_label.setVisible(False)
            self.number_settings_group.setVisible(False)
        
        elif input_type == InputType.PASS_FAIL:
            # Pass/Fail - show fixed label info
            self.input_label_widget.setVisible(False)
            self.pass_fail_label.setVisible(True)
            self.number_settings_group.setVisible(False)
        
        elif input_type == InputType.NUMBER:
            # Number - show label and range settings
            self.input_label_widget.setVisible(True)
            self.pass_fail_label.setVisible(False)
            self.number_settings_group.setVisible(True)
        
        self._on_field_changed()
    
    def _on_field_changed(self):
        """Mark that there are unsaved changes"""
        self.unsaved_changes = True
    
    def _save_current_step_to_memory(self):
        """Save current step changes to memory (not to file yet)"""
        if self.current_step_index < 0 or self.current_step_index >= len(self.steps):
            return
        
        step = self.steps[self.current_step_index]
        
        # Only update fields the user can edit
        if self.is_developer:
            step['name'] = self.name_input.text().strip()
            step['description'] = self.description_input.toPlainText().strip()
            step['image_path'] = self.image_path_input.text().strip() or None
            
            input_type = self.input_type_combo.currentData()
            step['input_type'] = input_type.value
            
            if input_type == InputType.PASS_FAIL:
                step['input_label'] = 'Sonuç'
            elif input_type == InputType.NUMBER:
                step['input_label'] = self.input_label_input.text().strip() or 'Test Sonucu'
                step['input_validation'] = {
                    'min': self.min_value_input.value(),
                    'max': self.max_value_input.value()
                }
            else:
                step['input_label'] = 'Test Sonucu'
                step['input_validation'] = {}
        
        # Time limit is always editable
        step['time_limit'] = self.time_limit_input.value()
        
        # Update list item text
        item = self.step_list.item(self.current_step_index)
        if item:
            item.setText(f"{step.get('step_id', self.current_step_index + 1)}. {step.get('name', '')}")
        
        logger.debug(f"Step {self.current_step_index + 1} saved to memory")
    
    def _on_browse_image(self):
        """Open file dialog to browse for image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Görsel Seç",
            "resources/images",
            "Görseller (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            # Convert to relative path if possible
            try:
                rel_path = os.path.relpath(file_path)
                self.image_path_input.setText(rel_path)
            except ValueError:
                self.image_path_input.setText(file_path)
    
    def _on_add_step(self):
        """Add a new step"""
        if not self.is_developer:
            return
        
        # Save current step first
        if self.current_step_index >= 0:
            self._save_current_step_to_memory()
        
        # Create new step with next ID
        max_id = max((step.get('step_id', 0) for step in self.steps), default=0)
        new_step = {
            'step_id': max_id + 1,
            'name': f'Yeni Adım {max_id + 1}',
            'description': '',
            'time_limit': 60,
            'image_path': None,
            'input_type': 'none',
            'input_label': 'Test Sonucu',
            'input_validation': {},
            # Runtime state (defaults)
            'status': 'not_started',
            'result_value': None,
            'actual_duration': None,
            'comment': None,
            'completed_by': None,
            'completed_at': None,
        }
        
        self.steps.append(new_step)
        self._populate_step_list()
        
        # Select the new step
        self.step_list.setCurrentRow(len(self.steps) - 1)
        
        self.unsaved_changes = True
        logger.info(f"New step added: {new_step['name']}")
    
    def _on_delete_step(self):
        """Delete the current step"""
        if not self.is_developer:
            return
        
        if self.current_step_index < 0 or len(self.steps) <= 1:
            QMessageBox.warning(
                self,
                "Uyarı",
                "En az bir adım olmalıdır. Silme işlemi yapılamaz.",
                QMessageBox.Ok
            )
            return
        
        step = self.steps[self.current_step_index]
        
        reply = QMessageBox.question(
            self,
            "Adımı Sil",
            f"'{step.get('name', 'Bu adım')}' adımını silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            del self.steps[self.current_step_index]
            
            # Re-number steps
            for i, step in enumerate(self.steps):
                step['step_id'] = i + 1
            
            self._populate_step_list()
            
            # Select previous step or first
            new_index = min(self.current_step_index, len(self.steps) - 1)
            if new_index >= 0:
                self.step_list.setCurrentRow(new_index)
            
            self.unsaved_changes = True
            logger.info(f"Step deleted, {len(self.steps)} steps remaining")
    
    def _on_save(self):
        """Save all changes and close"""
        # Save current step
        if self.current_step_index >= 0:
            self._save_current_step_to_memory()
        
        # Validate all steps
        for i, step in enumerate(self.steps):
            if not step.get('name', '').strip():
                QMessageBox.warning(
                    self,
                    "Doğrulama Hatası",
                    f"Adım {i + 1}: Adım adı boş olamaz.",
                    QMessageBox.Ok
                )
                self.step_list.setCurrentRow(i)
                return
            
            if step.get('time_limit', 0) <= 0:
                QMessageBox.warning(
                    self,
                    "Doğrulama Hatası",
                    f"Adım {i + 1}: Süre limiti 0'dan büyük olmalıdır.",
                    QMessageBox.Ok
                )
                self.step_list.setCurrentRow(i)
                return
            
            # Validate number range
            if step.get('input_type') == 'number':
                validation = step.get('input_validation', {})
                min_val = validation.get('min', 0)
                max_val = validation.get('max', 100)
                if min_val >= max_val:
                    QMessageBox.warning(
                        self,
                        "Doğrulama Hatası",
                        f"Adım {i + 1}: Minimum değer maksimum değerden küçük olmalıdır.",
                        QMessageBox.Ok
                    )
                    self.step_list.setCurrentRow(i)
                    return
        
        # Emit signal with updated steps
        self.steps_updated.emit(self.steps)
        
        logger.info(f"Steps saved: {len(self.steps)} steps")
        QMessageBox.information(
            self,
            "Başarılı",
            f"{len(self.steps)} adım başarıyla kaydedildi.",
            QMessageBox.Ok
        )
        
        self.accept()
    
    def _on_cancel(self):
        """Cancel and close without saving"""
        if self.unsaved_changes:
            reply = QMessageBox.question(
                self,
                "Kaydedilmemiş Değişiklikler",
                "Kaydedilmemiş değişiklikler var. Çıkmak istediğinize emin misiniz?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        self.reject()
    
    def get_steps(self) -> List[Dict[str, Any]]:
        """Get the edited steps"""
        return self.steps
```

# ui\dialogs\update_settings_dialog.py

```py
"""
Update Settings Dialog
Allows user to configure continuous update settings
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QSpinBox, QGroupBox,
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
import os

from utils.settings_manager import SettingsManager
from persistence import ContinuousWriter
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class UpdateSettingsDialog(QDialog):
    """
    Dialog for configuring continuous update settings.
    
    Allows user to:
    - View and change update folder
    - Change update frequency (in seconds)
    
    Signals:
        settings_changed: Emitted when settings are saved
    """
    
    settings_changed = pyqtSignal()
    
    def __init__(self, settings_manager: SettingsManager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self._init_ui()
        self._load_current_settings()
        
    def _init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Güncelleme Ayarları")
        self.setMinimumWidth(500)
        self.setMinimumHeight(250)
        
        # Set style
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {config.Colors.BACKGROUND_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
            QLabel {{
                color: {config.Colors.TEXT_PRIMARY};
                font-size: {config.FONT_SIZE}pt;
            }}
            QLineEdit {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
            }}
            QSpinBox {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
            }}
            QPushButton {{
                background-color: {config.Colors.BUTTON_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {config.Colors.BUTTON_HOVER};
            }}
            QGroupBox {{
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        
        # Folder settings group
        folder_group = QGroupBox("Güncelleme Klasörü")
        folder_layout = QVBoxLayout()
        
        folder_label = QLabel("Güncel klasör:")
        self.folder_display = QLineEdit()
        self.folder_display.setReadOnly(True)
        
        folder_button_layout = QHBoxLayout()
        self.change_folder_button = QPushButton("Klasör Değiştir...")
        self.change_folder_button.clicked.connect(self._on_change_folder)
        folder_button_layout.addStretch()
        folder_button_layout.addWidget(self.change_folder_button)
        
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_display)
        folder_layout.addLayout(folder_button_layout)
        folder_group.setLayout(folder_layout)
        
        # Interval settings group
        interval_group = QGroupBox("Güncelleme Sıklığı")
        interval_layout = QHBoxLayout()
        
        interval_label = QLabel("Dosya her")
        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setMinimum(5)
        self.interval_spinbox.setMaximum(300)
        self.interval_spinbox.setSuffix(" saniye")
        self.interval_spinbox.setValue(10)
        interval_label2 = QLabel("de bir güncellenir")
        
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.interval_spinbox)
        interval_layout.addWidget(interval_label2)
        interval_layout.addStretch()
        interval_group.setLayout(interval_layout)
        
        # Info label
        info_label = QLabel(
            "Not: Ayarlar kaydedildiğinde hemen etkinleşir ve kalıcıdır."
        )
        info_label.setStyleSheet(f"""
            color: {config.Colors.TEXT_SECONDARY};
            font-size: {config.FONT_SIZE - 1}pt;
            font-style: italic;
        """)
        info_label.setWordWrap(True)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Kaydet")
        self.save_button.clicked.connect(self._on_save)
        
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_SECONDARY};
            }}
            QPushButton:hover {{
                background-color: {config.Colors.TEXT_DISABLED};
            }}
        """)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        
        # Add all to main layout
        main_layout.addWidget(folder_group)
        main_layout.addWidget(interval_group)
        main_layout.addWidget(info_label)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        logger.debug("UpdateSettingsDialog initialized")
    
    def _load_current_settings(self):
        """Load and display current settings"""
        # Get current folder
        folder = self.settings_manager.get_update_folder()
        self.folder_display.setText(folder)
        
        # Get current interval
        interval = self.settings_manager.get_update_interval()
        self.interval_spinbox.setValue(interval)
        
        logger.debug(f"Loaded settings: folder={folder}, interval={interval}s")
    
    def _on_change_folder(self):
        """Handle folder change button"""
        current_folder = self.folder_display.text()
        
        # Open folder selection dialog
        folder = QFileDialog.getExistingDirectory(
            self,
            "Güncelleme Klasörü Seç",
            current_folder,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder:
            self.folder_display.setText(folder)
            logger.debug(f"Folder selected: {folder}")
    
    def _on_save(self):
        """Save settings and close dialog"""
        new_folder = self.folder_display.text()
        new_interval = self.interval_spinbox.value()
        
        # Validate folder exists or can be created
        try:
            os.makedirs(new_folder, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Hata",
                f"Klasör oluşturulamadı:\n{str(e)}"
            )
            logger.error(f"Failed to create folder {new_folder}: {e}")
            return
        
        # Save settings
        self.settings_manager.set_update_folder(new_folder)
        self.settings_manager.set_update_interval(new_interval)
        
        # Emit signal
        self.settings_changed.emit()
        
        # Show confirmation
        QMessageBox.information(
            self,
            "Başarılı",
            f"Ayarlar kaydedildi:\n\n"
            f"Klasör: {new_folder}\n"
            f"Güncelleme: Her {new_interval} saniye"
        )
        
        logger.info(f"Settings saved: folder={new_folder}, interval={new_interval}s")
        
        # Close dialog
        self.accept()
```

# ui\main_window.py

```py
"""
Main Window
Main application window with menu bar, sidebar, continuous data writing, and Excel export
UPDATED: Added user switching feature (Kullanıcı menu)
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, 
                             QFileDialog, QMenuBar, QMenu, QAction, QStatusBar, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os

from ui.widgets import HeaderWidget, TitleWidget, ContentWidget, StatusBarWidget, ProgressNavigator
from ui.dialogs import UpdateSettingsDialog, SwitchUserDialog
from managers import TestManager
from models.enums import InputType, TimerStatus
from persistence import ContinuousWriter
import config
from utils.logger import setup_logger
from ui.dialogs.test_step_editor_dialog import TestStepEditorDialog
logger = setup_logger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window with menu bar, sidebar, continuous data writing, and Excel export.
    
    Layout:
    - Menu Bar: File, View, and User menus
    - Row 1: Header (test info + timestamp)
    - Row 2: Step title
    - Row 3: Content (image + description + input + export button)
    - Row 4: Status bar (timer + progress + emoji)
    - Sidebar: Progress navigator (toggleable)
    - Status Bar: Show continuous writer status
    """
    
    def __init__(self, auth_manager=None):
        super().__init__()
        
        self.auth_manager = auth_manager
        self.test_manager = TestManager(auth_manager=auth_manager)
        self.sidebar_visible = False
        
        self._init_ui()              # ← Sidebar created here
        self._create_menu_bar()
        self._create_status_bar()
        self._connect_signals()
        
        # Update user display in menu after menu is created
        if self.auth_manager:
            self._update_user_display()
        
        # Enable sidebar clicking if admin
        if self.auth_manager and self.auth_manager.is_admin():
            if hasattr(self, 'sidebar') and self.sidebar is not None:
                self.sidebar.set_clickable(True)
                logger.info("✓ Sidebar set to clickable mode (admin user)")
            else:
                logger.warning("✗ Sidebar not found - cannot enable clickable")
        else:
            logger.info("Operator mode - sidebar not clickable")
        
        logger.info("MainWindow initialized with authentication support")
    
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
        """Create menu bar with File, View, and User menus"""
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
            QMenu::item:disabled {{
                color: {config.Colors.TEXT_SECONDARY};
            }}
        """)
        
        # ====================================================================
        # File menu
        # ====================================================================
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
        
        # ====================================================================
        # View menu
        # ====================================================================
        view_menu = menubar.addMenu(config.Labels.MENU_VIEW)
        
        # Toggle sidebar action
        self.toggle_sidebar_action = QAction(config.Labels.TOGGLE_SIDEBAR, self)
        self.toggle_sidebar_action.setCheckable(True)
        self.toggle_sidebar_action.setChecked(False)
        self.toggle_sidebar_action.setShortcut("F2")
        self.toggle_sidebar_action.triggered.connect(self.toggle_sidebar)
        view_menu.addAction(self.toggle_sidebar_action)
        
        # ====================================================================
        # User menu (NEW)
        # ====================================================================
        self.user_menu = menubar.addMenu("Kullanıcı")
        
        # Current user display (disabled, just for info)
        self.current_user_action = QAction("", self)
        self.current_user_action.setEnabled(False)
        self.user_menu.addAction(self.current_user_action)
        
        self.user_menu.addSeparator()
        
        # Switch user action
        self.switch_user_action = QAction("Kullanıcı Değiştir...", self)
        self.switch_user_action.setShortcut("Ctrl+U")
        self.switch_user_action.triggered.connect(self._on_switch_user)
        self.user_menu.addAction(self.switch_user_action)
        
        logger.debug("Menu bar created with File, View, and User menus")
        # ====================================================================
        # Developer menu (Only visible to Developers and Admins)
        # ====================================================================
        if self.auth_manager:
            role = self.auth_manager.get_role()
            if role in [config.UserRole.DEVELOPER, config.UserRole.ADMIN]:
                self.developer_menu = menubar.addMenu("Geliştirici")
                
                # Edit test steps action
                self.edit_steps_action = QAction("Test Adımlarını Düzenle...", self)
                self.edit_steps_action.setShortcut("Ctrl+E")
                self.edit_steps_action.triggered.connect(self._on_edit_test_steps)
                self.developer_menu.addAction(self.edit_steps_action)
                
                logger.debug("Developer menu created")
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
    
    # ========================================================================
    # User Switching Methods (NEW)
    # ========================================================================
    
    def _update_user_display(self):
        """
        Update the current user display in menu and window title.
        
        Called when:
        - Application starts
        - User switches role
        """
        if not self.auth_manager:
            return
        
        role = self.auth_manager.get_role()
        display_name = self.auth_manager.get_display_name()
        
        # Update menu item text
        if role == config.UserRole.ADMIN:
            role_text = "Yönetici"
            self.current_user_action.setText(f"👤 {display_name} ({role_text})")
            self.setWindowTitle(f"{config.WINDOW_TITLE} - YÖNETİCİ MODU")
        else:
            role_text = "Operatör"
            self.current_user_action.setText(f"👤 {display_name} ({role_text})")
            self.setWindowTitle(config.WINDOW_TITLE)
        
        logger.debug(f"User display updated: {display_name} ({role_text})")
    
    def _on_switch_user(self):
        """
        Open switch user dialog.
        
        Triggered by:
        - Menu: Kullanıcı → Kullanıcı Değiştir...
        - Shortcut: Ctrl+U
        """
        if not self.auth_manager:
            logger.warning("No auth manager available for user switching")
            QMessageBox.warning(
                self,
                "Uyarı",
                "Kullanıcı yönetimi aktif değil.",
                QMessageBox.Ok
            )
            return
        
        dialog = SwitchUserDialog(self.auth_manager, self)
        dialog.user_switched.connect(self._on_user_switched)
        dialog.exec_()
    
    def _on_user_switched(self, new_role: str):
        """
        Handle user role change.
        
        Updates:
        - Menu display
        - Window title
        - Sidebar clickable state
        - Status bar message
        
        Args:
            new_role: The new user role (config.UserRole.ADMIN or OPERATOR)
        """
        logger.info(f"User role changed to: {new_role}")
        
        # Update user display in menu and title
        self._update_user_display()
        
        # Update sidebar clickable state based on new role
        if hasattr(self, 'sidebar') and self.sidebar is not None:
            is_admin = self.auth_manager.is_admin()
            self.sidebar.set_clickable(is_admin)
            
            if is_admin:
                logger.info("✓ Sidebar navigation enabled (admin mode)")
            else:
                logger.info("✗ Sidebar navigation disabled (operator mode)")
        
        # Show status bar message
        if hasattr(self, 'status_bar') and self.status_bar:
            role_text = "Yönetici" if new_role == config.UserRole.ADMIN else "Operatör"
            self.status_bar.showMessage(f"Kullanıcı değiştirildi: {role_text}", 5000)
    
    # ========================================================================
    # Existing Methods
    # ========================================================================
    
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
        if hasattr(self, 'sidebar') and self.sidebar:
            self.sidebar.step_clicked.connect(self._on_sidebar_step_clicked)
            logger.debug("Sidebar step_clicked signal connected")
    
    def _on_open_update_settings(self):
        """Open update settings dialog"""
        dialog = UpdateSettingsDialog(
            self.test_manager.continuous_writer.settings,
            self
        )
        dialog.settings_changed.connect(self._on_settings_changed)
        dialog.exec_()
    
    def _on_sidebar_step_clicked(self, step_index: int):
        """
        Handle sidebar step click (backward navigation for admin).
        
        Args:
            step_index: Index of clicked step
        """
        from models.enums import NavigationMode
        logger.info(f"Sidebar step clicked: navigating to step {step_index}")
        self.test_manager.navigate_to_step(step_index, NavigationMode.VIEW_ONLY)
    
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
            
            # Update export button with session
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
            # Update export button with started session
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
        
        # Update export button with latest session state
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
        
        # Final update to export button with completed session
        if hasattr(self.test_manager, 'session') and self.test_manager.session:
            self.content_widget.set_session(self.test_manager.session)
            logger.debug("Export button updated with completed session")
        
        # Prompt for export
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
    def _on_edit_test_steps(self):
        """
        Open the test step editor dialog.
        
        Permission levels:
        - Developer: Can edit all fields, add/delete steps
        - Admin: Can only edit time_limit field
        
        Triggered by:
        - Menu: Geliştirici → Test Adımlarını Düzenle...
        - Shortcut: Ctrl+E
        """
        from ui.dialogs.test_step_editor_dialog import TestStepEditorDialog
        
        if not self.test_manager.steps:
            QMessageBox.warning(
                self,
                "Uyarı",
                "Düzenlenecek test adımı bulunamadı. Önce bir test yükleyin.",
                QMessageBox.Ok
            )
            return
        
        # Pass the actual TestStep objects to the dialog
        dialog = TestStepEditorDialog(self.test_manager.steps, self.auth_manager, self)
        dialog.steps_updated.connect(self._on_steps_updated)
        dialog.exec_()
    
    def _on_steps_updated(self, updated_steps: list):
        """
        Handle updated steps from the editor.
        
        Args:
            updated_steps: List of step dictionaries with ALL required fields
        """
        from models.test_step import TestStep
        
        try:
            # Convert dictionaries back to TestStep objects
            new_steps = []
            for step_data in updated_steps:
                step = TestStep.from_dict(step_data)
                new_steps.append(step)
            
            # Update test manager
            self.test_manager.steps = new_steps
            
            # Update session steps if session exists
            if self.test_manager.session:
                self.test_manager.session.steps = new_steps
            
            # Refresh sidebar
            if hasattr(self, 'sidebar') and self.sidebar:
                self.sidebar.set_steps(new_steps)
            
            # Save to file
            self._save_steps_to_file(updated_steps)
            
            # Show success message
            self.status_bar.showMessage(
                f"Test adımları güncellendi ({len(new_steps)} adım)", 
                5000
            )
            
            logger.info(f"Steps updated from editor: {len(new_steps)} steps")
            
        except Exception as e:
            logger.error(f"Failed to update steps: {e}")
            QMessageBox.critical(
                self,
                "Hata",
                f"Adımlar güncellenirken hata oluştu: {e}",
                QMessageBox.Ok
            )
    
    def _save_steps_to_file(self, steps_data: list):
        """
        Save updated steps to the test procedure JSON file.
        
        Args:
            steps_data: List of step dictionaries
        """
        import json
        
        # Default test file path
        test_file_path = "data/sample_test.json"
        
        try:
            # Load existing file
            with open(test_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Clean up step data for JSON (remove runtime state)
            clean_steps = []
            for step in steps_data:
                clean_step = {
                    'step_id': step['step_id'],
                    'name': step['name'],
                    'description': step['description'],
                    'time_limit': step['time_limit'],
                    'image_path': step.get('image_path'),
                    'input_type': step['input_type'],
                    'input_label': step.get('input_label', 'Test Sonucu'),
                    'input_validation': step.get('input_validation', {})
                }
                clean_steps.append(clean_step)
            
            # Update steps in data
            data['steps'] = clean_steps
            
            # Save back
            with open(test_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Steps saved to {test_file_path}")
            
        except Exception as e:
            logger.error(f"Failed to save steps to file: {e}")
```

# ui\widgets\__init__.py

```py
"""
Widgets Package
UI widget components
"""
from ui.widgets.header_widget import HeaderWidget
from ui.widgets.title_widget import TitleWidget
from ui.widgets.content import ContentWidget
from ui.widgets.status_bar_widget import StatusBarWidget
from ui.widgets.progress_navigator import ProgressNavigator  # NEW

__all__ = ['HeaderWidget', 'TitleWidget', 'ContentWidget', 'StatusBarWidget', 'ProgressNavigator']
```

# ui\widgets\content\__init__.py

```py
# -*- coding: utf-8 -*-

"""
Content Widgets Package
Row 3 content area components
"""
from ui.widgets.content.content_widget import ContentWidget

__all__ = ['ContentWidget']
```

# ui\widgets\content\button_panel.py

```py
"""
Button Panel Widget
Contains comment field and İlerle button
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import pyqtSignal
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ButtonPanel(QWidget):
    """
    Button panel for test step actions.
    
    Contains:
    - YORUM EKLE button (toggles comment field)
    - Comment text field (hidden by default)
    - İlerle > button (proceed to next step)
    
    Signals:
        proceed_clicked: Emitted when İlerle clicked
    """
    
    proceed_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Comment text area (hidden by default)
        self.comment_text = QTextEdit()
        self.comment_text.setPlaceholderText(config.Labels.COMMENT_PLACEHOLDER)
        self.comment_text.setMaximumHeight(config.COMMENT_FIELD_HEIGHT)
        self.comment_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
            }}
        """)
        self.comment_text.hide()
        
        # Button container
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        
        # YORUM EKLE button
        self.comment_button = QPushButton(config.Labels.ADD_COMMENT)
        self.comment_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_SECONDARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
                min-width: {config.BUTTON_COMMENT_WIDTH}px;
                min-height: {config.BUTTON_COMMENT_HEIGHT}px;
            }}
            QPushButton:hover {{
                background-color: #9e9e9e;
            }}
        """)
        self.comment_button.clicked.connect(self._toggle_comment)
        
        # İlerle button
        self.proceed_button = QPushButton(config.Labels.PROCEED)
        self.proceed_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                padding: 12px 24px;
                font-size: {config.FONT_SIZE_BUTTON}pt;
                font-weight: bold;
                min-width: {config.BUTTON_PROCEED_WIDTH}px;
                min-height: {config.BUTTON_PROCEED_HEIGHT}px;
            }}
            QPushButton:hover {{
                background-color: {config.Colors.BUTTON_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {config.Colors.ACCENT_BLUE};
            }}
        """)
        self.proceed_button.clicked.connect(self._on_proceed_clicked)
        
        # Add to button layout
        button_layout.addWidget(self.comment_button)
        button_layout.addStretch()
        button_layout.addWidget(self.proceed_button)
        button_container.setLayout(button_layout)
        
        # Add to main layout
        layout.addWidget(self.comment_text)
        layout.addWidget(button_container)
        
        self.setLayout(layout)
        
        logger.debug("ButtonPanel initialized")
    
    def _toggle_comment(self):
        """Toggle comment field visibility"""
        if self.comment_text.isVisible():
            self.comment_text.hide()
            self.comment_button.setText(config.Labels.ADD_COMMENT)
        else:
            self.comment_text.show()
            self.comment_text.setFocus()
            self.comment_button.setText(config.Labels.HIDE_COMMENT)
    
    def _on_proceed_clicked(self):
        """Handle İlerle button click"""
        self.proceed_clicked.emit()
    
    def get_comment(self) -> str:
        """
        Get comment text.
        
        Returns:
            Comment text (empty string if none)
        """
        return self.comment_text.toPlainText().strip()
    
    def clear_comment(self):
        """Clear comment field and hide it"""
        self.comment_text.clear()
        self.comment_text.hide()
        self.comment_button.setText(config.Labels.ADD_COMMENT)# -*- coding: utf-8 -*-


```

# ui\widgets\content\content_widget.py

```py
# -*- coding: utf-8 -*-
"""
Content Widget - Row 3 (STEP 1: BOTTOM SECTION REORGANIZED)
Main orchestrator with all controls in single horizontal row

CHANGES FROM ORIGINAL:
1. Description panel gets 80% vertical space (was 50%)
2. All controls moved to single horizontal row (15% space)
3. Image padding reduced from 10px to 5px
4. Button heights standardized to 45px
5. Logical left-to-right flow for controls

FIX APPLIED: Buttons now use setFixedWidth() to prevent shrinking when İlerleme Paneli opens
"""
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel,
                             QMessageBox, QPushButton, QTextEdit, QSizePolicy)
from PyQt5.QtCore import pyqtSignal
from typing import Optional

import config
from models.enums import InputType
from ui.widgets.content.image_viewer import ImageViewer
from ui.widgets.content.description_panel import DescriptionPanel
from ui.widgets.content.input_widgets import NumberInputWidget, PassFailInputWidget
from ui.widgets.content.export_button import ExportButton
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ContentWidget(QWidget):
    """
    Row 3: Main Content Area (REORGANIZED - Step 1)
    
    Layout:
    - Left (40%): ImageViewer (reduced padding for larger image)
    - Right (60%): 
        - DescriptionPanel (80% - MORE SPACE)
        - Single horizontal control row (15%)
        - Comment field (5%, hidden by default)
    
    NEW: All controls in ONE horizontal row:
    [Input widgets] [YAZ] Sonuç:__ [Raporla] [YORUM EKLE] [İlerle >]
    
    Signals:
        result_submitted: (result_value, checkbox_value, comment, is_valid)
        emoji_update_requested: (is_happy)
    """
    
    result_submitted = pyqtSignal(object, object, str, object)
    emoji_update_requested = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_input_type = InputType.NONE
        self.current_input_widget = None
        self.comment_visible = False
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.Colors.BACKGROUND_PRIMARY};
            }}
        """)
        
        # Main horizontal layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Left: Image viewer (40%)
        self.image_viewer = ImageViewer()
        # CHANGE: Reduce padding in ImageViewer for larger image display
        main_layout.addWidget(self.image_viewer, 40)
        
        # Right: Content area (60%)
        right_container = self._create_right_container()
        main_layout.addWidget(right_container, 60)
        
        self.setLayout(main_layout)
        
        logger.debug("ContentWidget initialized (Step 1: Reorganized)")
    
    def _create_right_container(self) -> QWidget:
        """Create right side with NEW single-row controls layout"""
        container = QWidget()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(
            config.ROW_3_DESCRIPTION_PADDING,
            config.ROW_3_DESCRIPTION_PADDING,
            config.ROW_3_DESCRIPTION_PADDING,
            config.ROW_3_DESCRIPTION_PADDING
        )
        layout.setSpacing(15)
        
        # CHANGE 1: Description panel - NOW GETS 80% of vertical space (was 50%)
        self.description_panel = DescriptionPanel()
        layout.addWidget(self.description_panel, 80)
        
        # CHANGE 2: NEW single horizontal row for ALL controls (15% of space)
        self.controls_row = self._create_controls_row()
        layout.addWidget(self.controls_row, 15)
        
        # CHANGE 3: Comment field (5% of space, shown below controls when toggled)
        self.comment_field = QTextEdit()
        self.comment_field.setPlaceholderText(config.Labels.COMMENT_PLACEHOLDER)
        self.comment_field.setMaximumHeight(80)
        self.comment_field.setStyleSheet(f"""
            QTextEdit {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
            }}
        """)
        self.comment_field.hide()
        layout.addWidget(self.comment_field, 5)
        
        # Error label
        self.error_label = QLabel()
        self.error_label.setStyleSheet(f"""
            color: {config.Colors.ERROR};
            font-size: {config.FONT_SIZE_ERROR}pt;
        """)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        container.setLayout(layout)
        return container
    
    def _create_controls_row(self) -> QWidget:
        """
        Create single horizontal row with all controls:
        [Input widgets] [YAZ] Sonuç:__ <--stretch--> [Raporla] [YORUM EKLE] [İlerle >]
        
        Layout flow (left to right):
        1. Input section (NUMBER or PASS/FAIL widgets dynamically inserted)
        2. Stretch (pushes action buttons to the right)
        3. Raporla (Export) button
        4. YORUM EKLE (Comment toggle) button
        5. İlerle > (Proceed) button
        
        FIX: All buttons use setFixedWidth() to prevent shrinking when İlerleme Paneli opens
        """
        container = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        
        # Section 1: Input widgets container (left side, dynamic content)
        self.input_container = QWidget()
        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(0, 0, 0, 0)
        self.input_layout.setSpacing(10)
        self.input_container.setLayout(self.input_layout)
        # Use Minimum so it can shrink if needed, but input widgets inside will maintain their size
        self.input_container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        main_layout.addWidget(self.input_container)
        
        # Stretch between input and action buttons - this absorbs extra space
        main_layout.addStretch(1)
        
        # Section 2: Export button (Raporla)
        self.export_button = ExportButton()
        # FIX: Use setFixedSize to absolutely prevent shrinking
        self.export_button.setFixedHeight(45)
        self.export_button.setFixedWidth(120)  # FIX: Fixed width prevents shrinking
        main_layout.addWidget(self.export_button)
        
        # Section 3: Comment toggle button (YORUM EKLE)
        self.comment_button = QPushButton(config.Labels.ADD_COMMENT)
        # FIX: Use setFixedSize to absolutely prevent shrinking
        self.comment_button.setFixedHeight(45)
        self.comment_button.setFixedWidth(130)  # FIX: Fixed width prevents shrinking
        self.comment_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 10px 15px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                border-color: {config.Colors.ACCENT_BLUE};
            }}
            QPushButton:checked {{
                background-color: {config.Colors.ACCENT_BLUE};
                border-color: {config.Colors.ACCENT_BLUE};
            }}
        """)
        self.comment_button.setCheckable(True)
        self.comment_button.clicked.connect(self._on_comment_toggle)
        main_layout.addWidget(self.comment_button)
        
        # Section 4: Proceed button (İlerle >)
        self.proceed_button = QPushButton(config.Labels.PROCEED)
        # FIX: Use setFixedSize to absolutely prevent shrinking
        self.proceed_button.setFixedHeight(45)
        self.proceed_button.setFixedWidth(130)  # FIX: Fixed width prevents shrinking
        self.proceed_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {config.Colors.BUTTON_HOVER};
            }}
        """)
        self.proceed_button.clicked.connect(self._on_proceed_clicked)
        main_layout.addWidget(self.proceed_button)
        
        container.setLayout(main_layout)
        return container
    
    def _on_comment_toggle(self):
        """Toggle comment field visibility"""
        self.comment_visible = not self.comment_visible
        if self.comment_visible:
            self.comment_field.show()
            self.comment_button.setText(config.Labels.HIDE_COMMENT)
        else:
            self.comment_field.hide()
            self.comment_button.setText(config.Labels.ADD_COMMENT)
    
    def get_comment(self) -> str:
        """Get comment text"""
        return self.comment_field.toPlainText().strip()
    
    def clear_comment(self):
        """Clear comment field and reset state"""
        self.comment_field.clear()
        self.comment_field.hide()
        self.comment_visible = False
        self.comment_button.setChecked(False)
        self.comment_button.setText(config.Labels.ADD_COMMENT)
    
    def set_step_content(self, step_name: str, description: str, image_path: Optional[str],
                        input_type: InputType, input_label: str = "Test Sonucu",
                        input_validation: dict = None):
        """
        Update content for current step.
        
        Args:
            step_name: Step name
            description: Step description
            image_path: Image file path
            input_type: InputType enum
            input_label: Input field label (unused)
            input_validation: Validation rules
        """
        # Update image
        self.image_viewer.load_image(image_path)
        
        # Update description
        self.description_panel.set_text(description)
        
        # Clear previous input widget
        if self.current_input_widget:
            self.input_layout.removeWidget(self.current_input_widget)
            self.current_input_widget.deleteLater()
            self.current_input_widget = None
        
        # Create new input widget based on type
        self.current_input_type = input_type
        
        if input_type == InputType.NUMBER:
            self.current_input_widget = NumberInputWidget(input_validation)
            self.current_input_widget.emoji_update_requested.connect(
                self.emoji_update_requested.emit
            )
            self.input_layout.addWidget(self.current_input_widget)
        
        elif input_type == InputType.PASS_FAIL:
            self.current_input_widget = PassFailInputWidget(input_validation)
            self.current_input_widget.emoji_update_requested.connect(
                self.emoji_update_requested.emit
            )
            self.input_layout.addWidget(self.current_input_widget)
        
        # Clear error and comment
        self.error_label.hide()
        self.clear_comment()
        
        logger.info(f"Content updated for step: {step_name} (type: {input_type.value})")
    
    def set_session(self, session):
        """
        Update the export button with current test session.
        
        Args:
            session: TestSession object containing test data and results
        """
        if hasattr(self, 'export_button'):
            self.export_button.set_session(session)
            logger.debug(f"Export button updated with session: {session.session_id if session else None}")
    
    def _on_proceed_clicked(self):
        """Handle İlerle button click"""
        # Handle InputType.NONE - no validation needed
        if self.current_input_type == InputType.NONE:
            comment = self.get_comment()
            self.result_submitted.emit(None, None, comment, None)
            logger.info("NONE type step - proceeding without validation")
            return
        
        # Validate that result has been written
        if not self.current_input_widget or not self.current_input_widget.is_result_written():
            QMessageBox.warning(
                self,
                config.Labels.WARNING_TITLE,
                config.Labels.NO_VALUE_WRITTEN
            )
            return
        
        # Get result and validity
        result_value, checkbox_value, is_valid = self._get_result_values()
        comment = self.get_comment()
        
        # Emit result
        self.result_submitted.emit(result_value, checkbox_value, comment, is_valid)
        logger.info(f"Result submitted: {result_value}/{checkbox_value}, valid={is_valid}")
    
    def _get_result_values(self) -> tuple:
        """
        Get result values from current input widget.
        
        Returns:
            (result_value, checkbox_value, is_valid) tuple
        """
        if self.current_input_type == InputType.NUMBER:
            result_value, is_valid = self.current_input_widget.get_result()
            return (result_value, None, is_valid)
        
        elif self.current_input_type == InputType.PASS_FAIL:
            checkbox_value, is_valid = self.current_input_widget.get_result()
            return (None, checkbox_value, is_valid)
        
        return (None, None, False)
    
    def has_result_written(self) -> bool:
        """Check if result has been written"""
        if self.current_input_widget:
            return self.current_input_widget.is_result_written()
        return False
```

# ui\widgets\content\description_panel.py

```py
"""
Description Panel Widget
Displays scrollable test step description text
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DescriptionPanel(QWidget):
    """
    Scrollable description text area.
    
    Displays:
    - Test step description (read-only)
    - Automatic scrolling for long text
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Description text area (read-only, scrollable)
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet(f"""
            QTextEdit {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: 1px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 10px;
                font-size: {config.FONT_SIZE_DESCRIPTION}pt;
                line-height: 1.5;
            }}
        """)
        
        layout.addWidget(self.text_area)
        self.setLayout(layout)
        
        logger.debug("DescriptionPanel initialized")
    
    def set_text(self, text: str):
        """
        Set description text.
        
        Args:
            text: Description text to display
        """
        self.text_area.setPlainText(text)
        logger.debug(f"Description updated ({len(text)} chars)")# -*- coding: utf-8 -*-


```

# ui\widgets\content\export_button.py

```py
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
```

# ui\widgets\content\image_viewer.py

```py
"""
Image Viewer Widget (STEP 1 UPDATE: Reduced padding)
Displays test step images with fallback placeholder
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from typing import Optional
import os
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ImageViewer(QWidget):
    """
    Image display widget for test steps.
    
    STEP 1 CHANGE: Reduced padding from 10px to 5px for larger image display
    
    Displays:
    - Test step image (scaled to fit)
    - Placeholder text if no image
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                border: 1px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
            }}
        """)
        
        layout = QVBoxLayout()
        # CHANGE: Reduced padding from 10 to 5 for larger image display
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(False)
        self.image_label.setStyleSheet("border: none;")
        
        # Load placeholder by default
        self.show_placeholder()
        
        layout.addWidget(self.image_label)
        self.setLayout(layout)
        
        logger.debug("ImageViewer initialized (Step 1: Reduced padding)")
    
    def load_image(self, image_path: Optional[str]):
        """
        Load and display image.
        
        Args:
            image_path: Path to image file (or None for placeholder)
        """
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Scale to fit while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                logger.debug(f"Image loaded: {image_path}")
                return
        
        # Fallback to placeholder
        self.show_placeholder()
    
    def show_placeholder(self):
        """Display placeholder text when no image available"""
        self.image_label.clear()
        self.image_label.setText("Görsel Yok")
        self.image_label.setStyleSheet(f"""
            color: {config.Colors.TEXT_SECONDARY};
            font-size: 18pt;
            border: none;
        """)
        logger.debug("Placeholder image displayed")
```

# ui\widgets\content\input_widgets\__init__.py

```py
"""
Input Widgets Package
Different input types for test steps
"""
from ui.widgets.content.input_widgets.number_input_widget import NumberInputWidget
from ui.widgets.content.input_widgets.passfail_input_widget import PassFailInputWidget

__all__ = ['NumberInputWidget', 'PassFailInputWidget']# -*- coding: utf-8 -*-


```

# ui\widgets\content\input_widgets\base_input_widget.py

```py
"""
Base Input Widget
Common interface for all input types
"""
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal


class BaseInputWidget(QWidget):
    """
    Base class for input widgets.
    
    All input widgets should implement:
    - get_result() -> Returns entered value
    - is_result_written() -> Returns True if YAZ clicked
    - clear() -> Resets widget state
    
    Signals:
        emoji_update_requested(bool): Request emoji update (happy/sad)
    """
    
    emoji_update_requested = pyqtSignal(bool)  # is_happy
    
    def __init__(self, validation: dict = None, parent=None):
        super().__init__(parent)
        self.validation = validation or {}
        self.result_written = False
    
    def get_result(self) -> tuple:
        """
        Get current result value and validity.
        
        Returns:
            (result_value, is_valid) tuple
            - result_value: The entered value
            - is_valid: True if valid, False if invalid
            
        Note: Subclasses should override this method
        """
        raise NotImplementedError("Subclass must implement get_result()")
    
    def is_result_written(self) -> bool:
        """
        Check if result has been written (YAZ clicked).
        
        Returns:
            True if YAZ button clicked
            
        Note: Subclasses should override this method
        """
        raise NotImplementedError("Subclass must implement is_result_written()")
    
    def clear(self):
        """
        Reset widget to initial state.
        
        Note: Subclasses should override this method
        """
        raise NotImplementedError("Subclass must implement clear()")
```

# ui\widgets\content\input_widgets\number_input_widget.py

```py
"""
Number Input Widget
Handles numeric input with validation
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import config
from ui.widgets.content.input_widgets.base_input_widget import BaseInputWidget
from utils.logger import setup_logger

logger = setup_logger(__name__)


class NumberInputWidget(BaseInputWidget):
    """
    NUMBER input type: [Input] [YAZ] [Result]
    
    UPDATED: Removed "Sonuç:" label, result displays directly with larger font
    
    Features:
    - Numeric input field
    - YAZ button to confirm entry
    - Result display (green=valid, orange=invalid)
    - Range validation (allows invalid but marks as failed)
    """
    
    def __init__(self, validation: dict = None, parent=None):
        super().__init__(validation, parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Input field
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText(config.Labels.ENTER_VALUE)
        self.number_input.setFixedWidth(config.INPUT_FIELD_WIDTH)
        self.number_input.setFixedHeight(config.INPUT_FIELD_HEIGHT)
        self.number_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                color: {config.Colors.TEXT_PRIMARY};
                border: 2px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
            }}
            QLineEdit:focus {{
                border: 2px solid {config.Colors.ACCENT_BLUE};
            }}
        """)
        
        # YAZ button
        self.write_button = QPushButton(config.Labels.WRITE)
        self.write_button.setFixedWidth(config.BUTTON_WRITE_WIDTH)
        self.write_button.setFixedHeight(config.BUTTON_WRITE_HEIGHT)
        self.write_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {config.Colors.BUTTON_HOVER};
            }}
        """)
        self.write_button.clicked.connect(self._on_write_clicked)
        
        # Result display - BIGGER FONT, NO LABEL
        self.result_display = QLabel("")
        self.result_display.setMinimumWidth(config.RESULT_DISPLAY_MIN_WIDTH)
        self.result_display.setStyleSheet(f"""
            QLabel {{
                color: {config.Colors.SUCCESS};
                font-size: 20pt;
                font-weight: bold;
            }}
        """)
        
        # Add to layout - NO "Sonuç:" LABEL ANYMORE
        layout.addWidget(self.number_input)
        layout.addWidget(self.write_button)
        layout.addWidget(self.result_display)  # Just the value!
        layout.addStretch()
        
        self.setLayout(layout)
        
        logger.debug("NumberInputWidget initialized (no Sonuç label, bigger font)")
    
    def _on_write_clicked(self):
        """Handle YAZ button click - ALLOWS INVALID VALUES"""
        input_text = self.number_input.text().strip()
        
        if not input_text:
            # Don't write empty values
            return
        
        # Try to parse as number
        try:
            value = float(input_text)
        except ValueError:
            # Invalid number format - don't write
            return
        
        # Check if value is in valid range
        is_valid = self._check_number_range(value)
        
        if not is_valid:
            # Write in ORANGE (warning color) - BIGGER FONT
            self.result_display.setText(input_text)
            self.result_display.setStyleSheet(f"""
                QLabel {{
                    color: {config.Colors.WARNING};
                    font-size: 20pt;
                    font-weight: bold;
                }}
            """)
            
            # Update emoji to sad (invalid = failed)
            self.emoji_update_requested.emit(False)
        else:
            # Write in GREEN (valid) - BIGGER FONT
            self.result_display.setText(input_text)
            self.result_display.setStyleSheet(f"""
                QLabel {{
                    color: {config.Colors.SUCCESS};
                    font-size: 20pt;
                    font-weight: bold;
                }}
            """)
            
            # Update emoji to happy (valid = passed)
            self.emoji_update_requested.emit(True)
        
        # Mark as written
        self.result_written = True
        
        logger.info(f"Value written: {input_text} (valid={is_valid})")
    
    def _check_number_range(self, value: float) -> bool:
        """
        Check if number is in valid range.
        
        Args:
            value: Number to check
            
        Returns:
            True if valid, False if out of range
        """
        min_val = self.validation.get('min')
        max_val = self.validation.get('max')
        
        if min_val is not None and value < min_val:
            return False
        
        if max_val is not None and value > max_val:
            return False
        
        return True
    
    def get_result(self) -> tuple:
        """
        Get current result value and validity.
        
        Returns:
            (result_value, is_valid) tuple
        """
        result_text = self.result_display.text()
        
        if not result_text:
            return (None, False)
        
        try:
            value = float(result_text)
            is_valid = self._check_number_range(value)
            return (result_text, is_valid)
        except ValueError:
            return (result_text, False)
    
    def is_result_written(self) -> bool:
        """Check if YAZ button has been clicked"""
        return self.result_written
    
    def clear(self):
        """Reset widget to initial state"""
        self.number_input.clear()
        self.result_display.clear()
        self.result_written = False
```

# ui\widgets\content\input_widgets\passfail_input_widget.py

```py
"""
Pass/Fail Input Widget
Handles GEÇTİ/KALDI checkbox input
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox, QPushButton
from PyQt5.QtCore import Qt
import config
from ui.widgets.content.input_widgets.base_input_widget import BaseInputWidget
from utils.logger import setup_logger

logger = setup_logger(__name__)


class PassFailInputWidget(BaseInputWidget):
    """
    PASS_FAIL input type: [GEÇTİ] [KALDI] [YAZ] [Result]
    
    UPDATED: Removed "Sonuç:" label, result displays directly with larger font
    
    Features:
    - Mutually exclusive checkboxes
    - YAZ button to confirm selection
    - Result display (green=pass, red=fail)
    """
    
    def __init__(self, validation: dict = None, parent=None):
        super().__init__(validation, parent)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components"""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(config.CHECKBOX_SPACING)
        
        # GEÇTİ checkbox
        self.pass_checkbox = QCheckBox(config.Labels.PASS)
        self.pass_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {config.Colors.TEXT_PRIMARY};
                font-size: {config.FONT_SIZE}pt;
                spacing: 10px;
            }}
            QCheckBox::indicator {{
                width: 25px;
                height: 25px;
            }}
        """)
        self.pass_checkbox.stateChanged.connect(
            lambda state: self._on_checkbox_changed(state, 'pass')
        )
        
        # KALDI checkbox
        self.fail_checkbox = QCheckBox(config.Labels.FAIL)
        self.fail_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {config.Colors.TEXT_PRIMARY};
                font-size: {config.FONT_SIZE}pt;
                spacing: 10px;
            }}
            QCheckBox::indicator {{
                width: 25px;
                height: 25px;
            }}
        """)
        self.fail_checkbox.stateChanged.connect(
            lambda state: self._on_checkbox_changed(state, 'fail')
        )
        
        # YAZ button
        self.write_button = QPushButton(config.Labels.WRITE)
        self.write_button.setFixedWidth(config.BUTTON_WRITE_WIDTH)
        self.write_button.setFixedHeight(config.BUTTON_WRITE_HEIGHT)
        self.write_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.Colors.BUTTON_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 5px;
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {config.Colors.BUTTON_HOVER};
            }}
        """)
        self.write_button.clicked.connect(self._on_write_clicked)
        
        # Result display - BIGGER FONT, NO LABEL
        self.result_display = QLabel("")
        self.result_display.setMinimumWidth(config.RESULT_DISPLAY_MIN_WIDTH)
        self.result_display.setStyleSheet(f"""
            QLabel {{
                color: {config.Colors.SUCCESS};
                font-size: 20pt;
                font-weight: bold;
            }}
        """)
        
        # Add to layout - NO "Sonuç:" LABEL ANYMORE
        layout.addWidget(self.pass_checkbox)
        layout.addWidget(self.fail_checkbox)
        layout.addWidget(self.write_button)
        layout.addWidget(self.result_display)  # Just GEÇTİ/KALDI!
        layout.addStretch()
        
        self.setLayout(layout)
        
        logger.debug("PassFailInputWidget initialized (no Sonuç label, bigger font)")
    
    def _on_checkbox_changed(self, state, checkbox_type):
        """Handle checkbox state change (mutually exclusive)"""
        if state == Qt.Checked:
            if checkbox_type == 'pass':
                self.fail_checkbox.setChecked(False)
            else:
                self.pass_checkbox.setChecked(False)
    
    def _on_write_clicked(self):
        """Handle YAZ button click for checkboxes"""
        # Check if at least one checkbox is selected
        if not (self.pass_checkbox.isChecked() or self.fail_checkbox.isChecked()):
            # Don't write if nothing selected
            return
        
        # Determine which checkbox is selected
        if self.pass_checkbox.isChecked():
            result_text = config.Labels.PASS  # "GEÇTİ"
            result_color = config.Colors.SUCCESS  # Green
            is_happy = True
        else:  # fail_checkbox is checked
            result_text = config.Labels.FAIL  # "KALDI"
            result_color = config.Colors.ERROR  # Red
            is_happy = False
        
        # Write to result display - BIGGER FONT
        self.result_display.setText(result_text)
        self.result_display.setStyleSheet(f"""
            QLabel {{
                color: {result_color};
                font-size: 20pt;
                font-weight: bold;
            }}
        """)
        
        # Update emoji immediately
        self.emoji_update_requested.emit(is_happy)
        
        # Mark as written
        self.result_written = True
        
        logger.info(f"Checkbox result written: {result_text}")
    
    def get_result(self) -> tuple:
        """
        Get current result value and validity.
        
        Returns:
            (checkbox_value, is_valid) tuple
            - "PASS" or "FAIL" or None
            - True if PASS, False if FAIL
        """
        result_text = self.result_display.text()
        
        if result_text == config.Labels.PASS:
            return ("PASS", True)
        elif result_text == config.Labels.FAIL:
            return ("FAIL", False)
        else:
            return (None, False)
    
    def is_result_written(self) -> bool:
        """Check if YAZ button has been clicked"""
        return self.result_written
    
    def clear(self):
        """Reset widget to initial state"""
        self.pass_checkbox.setChecked(False)
        self.fail_checkbox.setChecked(False)
        self.result_display.clear()
        self.result_written = False
```

# ui\widgets\header_widget.py

```py
"""
Header Widget - Row 1 (PHASE 1 UPDATED)
Displays session metadata with larger fonts
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt
from datetime import datetime
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class HeaderWidget(QWidget):
    """
    Row 1: Header Information Bar
    
    Displays:
    - STOK NO: xxx | SERİ: xxx | İSTASYON: xxx | SİP: xxx | DD/MM/YYYY HH:MM:SS
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.test_info = {}
        self._init_ui()
        self._setup_timer()
        
    def _init_ui(self):
        """Initialize the UI components"""
        # Set fixed height
        self.setFixedHeight(config.ROW_1_HEIGHT)
        
        # Set background color
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.Colors.BACKGROUND_PRIMARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
        """)
        
        # Create layout
        layout = QHBoxLayout()
        layout.setContentsMargins(
            config.ROW_1_PADDING_H, 0,
            config.ROW_1_PADDING_H, 0
        )
        layout.setSpacing(15)
        
        # Create labels
        self.stock_label = QLabel(f"{config.Labels.STOCK_NO}: ---")
        self.serial_label = QLabel(f"{config.Labels.SERIAL}: ---")
        self.station_label = QLabel(f"{config.Labels.STATION}: ---")
        self.sip_label = QLabel(f"{config.Labels.SIP}: ---")
        self.datetime_label = QLabel(self._format_datetime())
        
        # Style labels with larger font
        font_style = f"font-size: {config.FONT_SIZE}pt;"
        for label in [self.stock_label, self.serial_label, self.station_label, self.sip_label, self.datetime_label]:
            label.setStyleSheet(font_style)
        
        # Add to layout with separators
        layout.addWidget(self.stock_label)
        layout.addWidget(self._create_separator(), 0)
        layout.addWidget(self.serial_label)
        layout.addWidget(self._create_separator(), 0)
        layout.addWidget(self.station_label)
        layout.addWidget(self._create_separator(), 0)
        layout.addWidget(self.sip_label)
        layout.addWidget(self._create_separator(), 0)
        layout.addWidget(self.datetime_label)
        layout.addStretch()
        
        self.setLayout(layout)
        
        logger.debug("HeaderWidget initialized")
    
    def _create_separator(self) -> QLabel:
        """Create a separator label |"""
        sep = QLabel("|")
        sep.setStyleSheet(f"""
            color: {config.Colors.TEXT_SECONDARY};
            font-size: {config.FONT_SIZE}pt;
        """)
        return sep
    
    def _setup_timer(self):
        """Setup timer to update datetime every second"""
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_datetime)
        self.timer.start(1000)  # Update every second
    
    def _update_datetime(self):
        """Update the datetime label"""
        self.datetime_label.setText(self._format_datetime())
    
    def _format_datetime(self) -> str:
        """Format current datetime in Turkish format"""
        return datetime.now().strftime(config.DATETIME_FORMAT)
    
    def set_test_info(self, test_info: dict):
        """
        Update header with test information.
        
        Args:
            test_info: Dictionary with keys: stock_number, serial_number, 
                      station_number, sip_code
        """
        self.test_info = test_info
        
        stock = test_info.get('stock_number', '---')
        serial = test_info.get('serial_number', '---')
        station = test_info.get('station_number', '---')
        sip = test_info.get('sip_code', '---')
        
        self.stock_label.setText(f"{config.Labels.STOCK_NO}: {stock}")
        self.serial_label.setText(f"{config.Labels.SERIAL}: {serial}")
        self.station_label.setText(f"{config.Labels.STATION}: {station}")
        self.sip_label.setText(f"{config.Labels.SIP}: {sip}")
        
        logger.info(f"Header updated with test info: {stock}, {serial}")
```

# ui\widgets\progress_navigator.py

```py
# -*- coding: utf-8 -*-

"""
Progress Navigator - Sidebar showing all test steps
UPDATED: Added clickable backward navigation for admin users
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QLabel, 
                             QFrame, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QCursor
from typing import List, Optional
import config
from models.enums import TestStatus
from models.test_step import TestStep
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ProgressNavigator(QWidget):
    """
    Sidebar showing all test steps with status indicators.
    
    Features:
    - Visual display of all steps with status
    - Click to navigate backward (admin only)
    - Auto-scroll to current step
    
    Signals:
        step_clicked: Emitted when step is clicked (step_index)
    """
    
    step_clicked = pyqtSignal(int)  # step_index
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.steps: List[TestStep] = []
        self.current_step_index: int = -1
        self.step_widgets: List[QFrame] = []
        self.clickable = False  # Default: not clickable (operator mode)
        self._init_ui()
        
        logger.debug("ProgressNavigator initialized")
    
    def _init_ui(self):
        """Initialize the UI"""
        # Fixed width
        self.setFixedWidth(config.SIDEBAR_WIDTH)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Scroll area for steps
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {config.Colors.BACKGROUND_SECONDARY};
            }}
        """)
        
        # Container for step items
        self.steps_container = QWidget()
        self.steps_layout = QVBoxLayout()
        self.steps_layout.setContentsMargins(5, 5, 5, 5)
        self.steps_layout.setSpacing(5)
        self.steps_layout.addStretch()
        self.steps_container.setLayout(self.steps_layout)
        
        scroll_area.setWidget(self.steps_container)
        main_layout.addWidget(scroll_area)
        
        # Store scroll area reference for later
        self.scroll_area = scroll_area
        
        self.setLayout(main_layout)
        
        # Styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
            }}
        """)
    
    def _create_header(self) -> QWidget:
        """Create sidebar header"""
        header = QWidget()
        header.setFixedHeight(40)
        header.setStyleSheet(f"""
            background-color: {config.Colors.BACKGROUND_PRIMARY};
            border-bottom: 2px solid {config.Colors.ACCENT_BLUE};
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        
        label = QLabel(config.Labels.PROGRESS_NAVIGATOR)
        label.setStyleSheet(f"""
            color: {config.Colors.TEXT_PRIMARY};
            font-size: {config.FONT_SIZE}pt;
            font-weight: bold;
        """)
        label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(label)
        header.setLayout(layout)
        
        return header
    
    def set_steps(self, steps: List[TestStep]):
        """Set the list of test steps"""
        self.steps = steps
        self._rebuild_step_list()
    
    def set_clickable(self, clickable: bool):
        """
        Enable/disable clicking on steps.
        
        Args:
            clickable: True for admin mode (can click), False for operator mode
        """
        self.clickable = clickable
        logger.info(f"Sidebar clickable mode: {clickable}")
        
        # Update cursor for all existing widgets
        self._update_all_cursors()
    
    def _update_all_cursors(self):
        """Update cursor for all step widgets based on clickable state"""
        for i, widget in enumerate(self.step_widgets):
            self._update_widget_cursor(widget, i)
    
    def _update_widget_cursor(self, widget: QFrame, index: int):
        '''
        Update cursor for a single widget.
        
        Shows pointer cursor for:
        - Previous steps (backward navigation)
        - Completed steps even if forward (PASSED or FAILED)
        
        Args:
            widget: The step widget
            index: Step index
        '''
        if not self.clickable:
            widget.setCursor(QCursor(Qt.ArrowCursor))
            return
        
        # Don't show pointer on current step
        if index == self.current_step_index:
            widget.setCursor(QCursor(Qt.ArrowCursor))
            return
        
        # Check if step is valid
        if index < 0 or index >= len(self.steps):
            widget.setCursor(QCursor(Qt.ArrowCursor))
            return
        
        step = self.steps[index]
        
        # Show pointer for:
        # 1. Previous steps (backward navigation)
        # 2. Completed steps (PASSED or FAILED) even if forward
        if index < self.current_step_index:
            # Previous step - clickable
            widget.setCursor(QCursor(Qt.PointingHandCursor))
        elif step.status in [TestStatus.PASSED, TestStatus.FAILED]:
            # Completed step - clickable
            widget.setCursor(QCursor(Qt.PointingHandCursor))
        else:
            # Future not-started step - not clickable
            widget.setCursor(QCursor(Qt.ArrowCursor))
    
    def _rebuild_step_list(self):
        """Rebuild the entire step list"""
        # Clear existing widgets
        for widget in self.step_widgets:
            widget.deleteLater()
        self.step_widgets.clear()
        
        # Remove stretch
        if self.steps_layout.count() > 0:
            self.steps_layout.takeAt(self.steps_layout.count() - 1)
        
        # Create new step widgets
        for i, step in enumerate(self.steps):
            step_widget = self._create_step_widget(i, step)
            self.step_widgets.append(step_widget)
            self.steps_layout.addWidget(step_widget)
        
        # Add stretch at bottom
        self.steps_layout.addStretch()
        
        logger.debug(f"Rebuilt step list with {len(self.steps)} steps")
    
    def _create_step_widget(self, index: int, step: TestStep) -> QFrame:
        """Create a single step item widget"""
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        
        # Store index in widget for click handling
        frame.setProperty("step_index", index)
        
        # ====================================================================
        # NEW: Install event filter for click handling
        # ====================================================================
        frame.installEventFilter(self)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # Step name with icon
        name_layout = QVBoxLayout()
        name_layout.setSpacing(2)
        
        # Icon + Name
        name_label = QLabel(f"{self._get_status_icon(step.status)} {index + 1}. {step.name}")
        name_label.setWordWrap(True)
        name_label.setStyleSheet(f"""
            color: {self._get_status_color(step.status)};
            font-size: {config.FONT_SIZE}pt;
            font-weight: {'bold' if index == self.current_step_index else 'normal'};
        """)
        
        # Timer/duration info
        info_label = QLabel(self._get_step_info(step))
        info_label.setStyleSheet(f"""
            color: {config.Colors.TEXT_SECONDARY};
            font-size: 9pt;
        """)
        
        name_layout.addWidget(name_label)
        name_layout.addWidget(info_label)
        
        layout.addLayout(name_layout)
        frame.setLayout(layout)
        
        # Background color for current step
        if index == self.current_step_index:
            bg_color = config.Colors.ACCENT_BLUE
        else:
            bg_color = config.Colors.BACKGROUND_TERTIARY
        
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 5px;
                border: 1px solid {config.Colors.BORDER_COLOR};
            }}
            QFrame:hover {{
                border: 1px solid {config.Colors.ACCENT_BLUE};
            }}
        """)
        
        # Set cursor based on clickable state
        self._update_widget_cursor(frame, index)
        
        return frame
    
    def eventFilter(self, obj, event):
        """
        Event filter to handle mouse clicks on step widgets.
        
        Args:
            obj: Object that triggered event
            event: Event object
            
        Returns:
            True if event handled, False otherwise
        """
        # Check if this is a mouse press event on a step widget
        if event.type() == event.MouseButtonPress and isinstance(obj, QFrame):
            step_index = obj.property("step_index")
            
            if step_index is not None:
                self._on_step_clicked(step_index)
                return True
        
        return super().eventFilter(obj, event)
    
    def _on_step_clicked(self, index: int):
        '''
        Handle step click.
        
        Allows clicking on:
        - Any previous step (backward navigation)
        - Any completed step (PASSED or FAILED) even if forward
        - NOT allowed: Current step or future not-started steps
        
        Only works if clickable mode is enabled (admin mode).
        
        Args:
            index: Index of clicked step
        '''
        # Check if clickable mode is enabled
        if not self.clickable:
            logger.debug(f"Step {index} clicked but sidebar not in clickable mode")
            return
        
        # Don't allow clicking the current step
        if index == self.current_step_index:
            logger.debug(f"Cannot click current step: {index}")
            return
        
        # Check if step exists
        if index < 0 or index >= len(self.steps):
            logger.warning(f"Invalid step index clicked: {index}")
            return
        
        step = self.steps[index]
        
        # Allow clicking if:
        # 1. Going backward (any previous step)
        # 2. Going forward BUT step is completed (PASSED or FAILED)
        if index < self.current_step_index:
            # Backward navigation - always allowed
            logger.info(f"Sidebar step clicked (backward): {index}")
            self.step_clicked.emit(index)
        elif step.status in [TestStatus.PASSED, TestStatus.FAILED]:
            # Forward navigation to completed step - allowed
            logger.info(f"Sidebar step clicked (forward to completed): {index}")
            self.step_clicked.emit(index)
        else:
            # Future not-started step - not allowed
            logger.debug(f"Cannot click future not-started step: {index} (status: {step.status.value})")
    
    def _get_status_icon(self, status: TestStatus) -> str:
        """Get icon for status"""
        icons = {
            TestStatus.NOT_STARTED: "○",
            TestStatus.IN_PROGRESS: "►",
            TestStatus.PASSED: "✓",
            TestStatus.FAILED: "✗",
            TestStatus.SKIPPED: "⊘",
        }
        return icons.get(status, "○")
    
    def _get_status_color(self, status: TestStatus) -> str:
        """Get color for status"""
        colors = {
            TestStatus.NOT_STARTED: config.Colors.TEXT_DISABLED,
            TestStatus.IN_PROGRESS: config.Colors.ACCENT_BLUE,
            TestStatus.PASSED: config.Colors.SUCCESS,
            TestStatus.FAILED: config.Colors.ERROR,
            TestStatus.SKIPPED: config.Colors.WARNING,
        }
        return colors.get(status, config.Colors.TEXT_DISABLED)
    
    def _get_step_info(self, step: TestStep) -> str:
        """Get info text for step"""
        if step.status == TestStatus.IN_PROGRESS:
            return "⏱ Devam ediyor..."
        elif step.status in [TestStatus.PASSED, TestStatus.FAILED, TestStatus.SKIPPED]:
            if step.actual_duration:
                warning = " ⚠️" if step.status == TestStatus.FAILED else ""
                return f"⏰ Tamamlandı: {step.actual_duration}s{warning}"
            return "⏰ Tamamlandı"
        else:
            return ""
    
    def update_current_step(self, step_index: int):
        """Update which step is current"""
        old_index = self.current_step_index
        self.current_step_index = step_index
        
        # Refresh affected widgets
        if 0 <= old_index < len(self.step_widgets):
            self._refresh_step_widget(old_index)
        if 0 <= step_index < len(self.step_widgets):
            self._refresh_step_widget(step_index)
            self._scroll_to_step(step_index)
        
        # Update cursors (previous steps become clickable)
        self._update_all_cursors()
        
        logger.debug(f"Current step updated: {old_index} → {step_index}")
    
    def update_step_status(self, step_index: int):
        """Update a specific step's display"""
        if 0 <= step_index < len(self.step_widgets):
            self._refresh_step_widget(step_index)
    
    def _refresh_step_widget(self, index: int):
        """Refresh a single step widget"""
        if index < 0 or index >= len(self.steps):
            return
        
        step = self.steps[index]
        widget = self.step_widgets[index]
        
        # Update widget content
        layout = widget.layout()
        if layout and layout.count() > 0:
            # Get name layout
            name_layout = layout.itemAt(0).layout()
            if name_layout and name_layout.count() >= 2:
                # Update name label
                name_label = name_layout.itemAt(0).widget()
                name_label.setText(f"{self._get_status_icon(step.status)} {index + 1}. {step.name}")
                name_label.setStyleSheet(f"""
                    color: {self._get_status_color(step.status)};
                    font-size: {config.FONT_SIZE}pt;
                    font-weight: {'bold' if index == self.current_step_index else 'normal'};
                """)
                
                # Update info label
                info_label = name_layout.itemAt(1).widget()
                info_label.setText(self._get_step_info(step))
        
        # Update background
        if index == self.current_step_index:
            bg_color = config.Colors.ACCENT_BLUE
        else:
            bg_color = config.Colors.BACKGROUND_TERTIARY
        
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 5px;
                border: 1px solid {config.Colors.BORDER_COLOR};
            }}
            QFrame:hover {{
                border: 1px solid {config.Colors.ACCENT_BLUE};
            }}
        """)
        
        # Update cursor
        self._update_widget_cursor(widget, index)
    
    def _scroll_to_step(self, step_index: int):
        """Auto-scroll to make step visible"""
        if 0 <= step_index < len(self.step_widgets):
            widget = self.step_widgets[step_index]
            if self.scroll_area:
                self.scroll_area.ensureWidgetVisible(widget, 50, 50)
```

# ui\widgets\status_bar_widget.py

```py
"""
Status Bar Widget - Row 4 (PHASE 1 UPDATED)
Timer + Progress + Status Emoji with enhanced spacing
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import config
from models.enums import TimerStatus
from utils.logger import setup_logger
from PyQt5.QtGui import QFont, QPixmap

logger = setup_logger(__name__)


class StatusBarWidget(QWidget):
    """
    Row 4: Status Bar
    
    4 sections:
    - Reserved (placeholder)
    - Timer (countdown/countup)
    - Progress (step X/N + progress bar)
    - Status emoji (😊/☹️)
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the UI components"""
        # Set fixed height with better spacing
        self.setFixedHeight(config.ROW_4_HEIGHT)
        
        # Set background
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
        """)
        
        # Main horizontal layout (4 equal sections) with enhanced padding
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(
            config.ROW_4_PADDING_LEFT,
            config.ROW_4_PADDING_TOP,
            config.ROW_4_PADDING_RIGHT,
            config.ROW_4_PADDING_BOTTOM
        )
        main_layout.setSpacing(config.ROW_4_SECTION_SPACING)
        
        # Section 1: Reserved
        self.reserved_section = self._create_reserved_section()
        main_layout.addWidget(self.reserved_section, 25)
        
        # Section 2: Timer
        self.timer_section = self._create_timer_section()
        main_layout.addWidget(self.timer_section, 25)
        
        # Section 3: Progress
        self.progress_section = self._create_progress_section()
        main_layout.addWidget(self.progress_section, 25)
        
        # Section 4: Status Emoji
        self.emoji_section = self._create_emoji_section()
        main_layout.addWidget(self.emoji_section, 25)
        
        self.setLayout(main_layout)
        
        logger.debug("StatusBarWidget initialized")
    
    def _create_reserved_section(self) -> QWidget:
        """Create reserved placeholder section"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        label = QLabel(config.Labels.RESERVED)
        label.setStyleSheet(f"""
            color: {config.Colors.TEXT_DISABLED};
            font-size: {config.FONT_SIZE}pt;
        """)
        label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(label)
        widget.setLayout(layout)
        
        return widget
    
    def _create_timer_section(self) -> QWidget:
        """Create timer display section"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)
        
        # Timer label with larger font
        self.timer_label = QLabel("00:00")
        self.timer_label.setStyleSheet(f"""
            color: {config.Colors.SUCCESS};
            font-size: {config.FONT_SIZE_TIMER}pt;
            font-weight: bold;
            font-family: 'Courier New', monospace;
        """)
        self.timer_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.timer_label)
        widget.setLayout(layout)
        
        return widget
    
    def _create_progress_section(self) -> QWidget:
        """Create progress indicator section"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(5)
        
        # Step counter label with larger font
        self.step_label = QLabel(f"{config.Labels.STEP}: 0/0")
        self.step_label.setStyleSheet(f"""
            color: {config.Colors.TEXT_PRIMARY};
            font-size: {config.FONT_SIZE_PROGRESS}pt;
            font-weight: bold;
        """)
        self.step_label.setAlignment(Qt.AlignCenter)
        
        # Progress bar with increased height
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {config.Colors.BORDER_COLOR};
                border-radius: 5px;
                background-color: {config.Colors.INPUT_BACKGROUND};
                text-align: center;
                color: {config.Colors.TEXT_PRIMARY};
                height: {config.PROGRESS_BAR_HEIGHT}px;
                font-size: {config.FONT_SIZE}pt;
            }}
            QProgressBar::chunk {{
                background-color: {config.Colors.ACCENT_BLUE};
                border-radius: 4px;
            }}
        """)
        
        layout.addWidget(self.step_label)
        layout.addWidget(self.progress_bar)
        widget.setLayout(layout)
        
        return widget
    
    def _create_emoji_section(self) -> QWidget:
        """Create status emoji section with image that fills the container"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Emoji label - uses QPixmap, preserves aspect ratio
        self.emoji_label = QLabel()
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setMinimumSize(60, 60)
        
        # Set size policy to expand
        from PyQt5.QtWidgets import QSizePolicy
        self.emoji_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Store original pixmaps for resizing
        self._happy_pixmap = QPixmap(config.ICON_HAPPY)
        self._sad_pixmap = QPixmap(config.ICON_SAD)
        self._is_happy = True
        
        # Load default (happy) image
        self._set_emoji_image(True)
        
        layout.addWidget(self.emoji_label)
        widget.setLayout(layout)
        
        return widget
    
    def _set_emoji_image(self, is_happy: bool):
        """
        Load and set emoji image with aspect ratio preserved.
        
        Args:
            is_happy: True for happy face, False for sad face
        """
        self._is_happy = is_happy
        pixmap = self._happy_pixmap if is_happy else self._sad_pixmap
        
        if not pixmap.isNull():
            # Scale to fit label size while keeping aspect ratio
            label_size = self.emoji_label.size()
            scaled_pixmap = pixmap.scaled(
                label_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.emoji_label.setPixmap(scaled_pixmap)
            logger.debug(f"Emoji image loaded: {'happy' if is_happy else 'sad'}")
        else:
            # Fallback to text if image not found
            fallback = "😊" if is_happy else "☹️"
            self.emoji_label.setText(fallback)
            self.emoji_label.setStyleSheet(f"""
                font-size: {config.FONT_SIZE_EMOJI}pt;
                background-color: {config.Colors.INPUT_BACKGROUND};
            """)
            logger.warning(f"Emoji image not found, using text fallback")
    
    def resizeEvent(self, event):
        """Handle resize to update emoji image size"""
        super().resizeEvent(event)
        # Re-apply image with new size
        if hasattr(self, '_is_happy'):
            self._set_emoji_image(self._is_happy)
    
    def update_timer(self, remaining_seconds: int, status: str):
        """
        Update timer display.
        
        Args:
            remaining_seconds: Remaining time (negative if overtime)
            status: Timer status (normal, warning, critical, overtime)
        """
        # Format time
        abs_seconds = abs(remaining_seconds)
        minutes = abs_seconds // 60
        seconds = abs_seconds % 60
        
        if remaining_seconds < 0:
            time_str = f"-{minutes:02d}:{seconds:02d}"
        else:
            time_str = f"{minutes:02d}:{seconds:02d}"
        
        self.timer_label.setText(time_str)
        
        # Update color based on status
        if status == TimerStatus.NORMAL.value:
            color = config.Colors.SUCCESS
        elif status == TimerStatus.WARNING.value:
            color = config.Colors.WARNING
        elif status == TimerStatus.CRITICAL.value or status == TimerStatus.OVERTIME.value:
            color = config.Colors.ERROR
        else:
            color = config.Colors.TEXT_PRIMARY
        
        self.timer_label.setStyleSheet(f"""
            color: {color};
            font-size: {config.FONT_SIZE_TIMER}pt;
            font-weight: bold;
            font-family: 'Courier New', monospace;
        """)
    
    def update_progress(self, current_step: int, total_steps: int):
        """
        Update progress indicator.
        
        Args:
            current_step: Current step number (1-based)
            total_steps: Total number of steps
        """
        self.step_label.setText(f"{config.Labels.STEP}: {current_step}/{total_steps}")
        
        if total_steps > 0:
            percentage = int((current_step / total_steps) * 100)
            self.progress_bar.setValue(percentage)
    
    def update_emoji(self, is_happy: bool):
        """
        Update status emoji image.
        
        Args:
            is_happy: True for happy face, False for sad face
        """
        self._set_emoji_image(is_happy)
        logger.debug(f"Emoji updated: {'happy' if is_happy else 'sad'}")
```

# ui\widgets\title_widget.py

```py
"""
Title Widget - Row 2 (PHASE 1 UPDATED)
Displays current test step title with proper padding
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TitleWidget(QWidget):
    """
    Row 2: Test Step Title
    
    Displays the name/title of the current test step.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the UI components"""
        # Set fixed height
        self.setFixedHeight(config.ROW_2_HEIGHT)
        
        # Set background color
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                color: {config.Colors.TEXT_PRIMARY};
            }}
        """)
        
        # Create layout with padding
        layout = QHBoxLayout()
        layout.setContentsMargins(
            config.ROW_2_PADDING_LEFT,
            config.ROW_2_PADDING_TOP,
            config.ROW_2_PADDING_RIGHT,
            config.ROW_2_PADDING_BOTTOM
        )
        
        # Create title label
        self.title_label = QLabel("---")
        self.title_label.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_LARGE}pt;
            font-weight: bold;
            color: {config.Colors.TEXT_PRIMARY};
        """)
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title_label.setWordWrap(False)
        
        layout.addWidget(self.title_label)
        
        self.setLayout(layout)
        
        logger.debug("TitleWidget initialized")
    
    def set_title(self, title: str):
        """
        Set the step title.
        
        Args:
            title: The step title/name to display
        """
        self.title_label.setText(title)
        logger.debug(f"Title updated: {title}")
```

# utils\__init__.py

```py
"""
Utils Package
Utility functions and helpers
"""
from utils.logger import setup_logger

__all__ = ['setup_logger']
```

# utils\auth_manager.py

```py
# -*- coding: utf-8 -*-

"""
Authentication Manager
3-Role System: Admin, Operator, Developer

Features:
- Load users from data/users.json (organized by role folders)
- Admin: Can navigate back, edit results, export
- Operator: Basic test execution only (no password)
- Developer: All admin rights + can edit test steps (future)
"""
import hashlib
import json
import os
from typing import Optional, Dict, List, Any
from pathlib import Path
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)


class UserRole:
    """
    3 User role types with different permission levels.
    
    Hierarchy:
    1. DEVELOPER - All admin rights + can edit test steps (future)
    2. ADMIN - Can navigate back, edit results, manage users
    3. OPERATOR - Basic test execution only
    """
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
    
    # Roles that can edit test steps (future feature)
    EDIT_STEPS_ROLES = [DEVELOPER]
    
    # Roles that require password
    PASSWORD_REQUIRED_ROLES = [ADMIN, DEVELOPER]


class AuthManager:
    """
    3-Role Authentication Manager.
    
    Roles:
    - ADMIN: Can navigate back, edit results, export reports
    - OPERATOR: Basic test execution only (no password required)
    - DEVELOPER: All admin rights + can edit test steps (future)
    
    Users are organized in folders/lists in users.json:
    - users.admins[]
    - users.operators[]
    - users.developers[]
    
    Usage:
        auth = AuthManager()
        
        # Operator login (no password)
        auth.login_as_operator("op1")
        
        # Admin/Developer login (with password)
        if auth.authenticate("admin", "admin123"):
            print(f"Welcome {auth.get_display_name()}")
    """
    
    # Path to users file
    USERS_FILE = "data/users.json"
    
    def __init__(self):
        """Initialize AuthManager and load users from file."""
        self.current_user: Optional[Dict] = None
        
        # Users organized by role
        self.admins: List[Dict] = []
        self.operators: List[Dict] = []
        self.developers: List[Dict] = []
        
        # Role permissions
        self.roles: Dict[str, Dict] = {}
        
        # Try to load users from file
        self._load_users_from_file()
        
        total_users = len(self.admins) + len(self.operators) + len(self.developers)
        logger.info(f"AuthManager initialized: {len(self.admins)} admins, {len(self.operators)} operators, {len(self.developers)} developers")
    
    # ========================================================================
    # USER LOADING
    # ========================================================================
    
    def _load_users_from_file(self) -> bool:
        """
        Load users from data/users.json file.
        
        JSON structure:
        {
            "users": {
                "admins": [...],
                "operators": [...],
                "developers": [...]
            },
            "roles": {...}
        }
        
        Returns:
            True if loaded successfully, False otherwise
        """
        # Try multiple paths
        possible_paths = [
            Path(self.USERS_FILE),
            Path(__file__).parent.parent / "data" / "users.json",
            Path.cwd() / "data" / "users.json"
        ]
        
        users_file = None
        for path in possible_paths:
            if path.exists():
                users_file = path
                break
        
        if users_file is None:
            logger.warning("users.json not found, using default users")
            self._create_default_users()
            return False
        
        try:
            with open(users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            users_data = data.get('users', {})
            
            # Load users by role folder
            self.admins = [u for u in users_data.get('admins', []) if u.get('active', True)]
            self.operators = [u for u in users_data.get('operators', []) if u.get('active', True)]
            self.developers = [u for u in users_data.get('developers', []) if u.get('active', True)]
            
            # Add role field to each user
            for user in self.admins:
                user['role'] = UserRole.ADMIN
            for user in self.operators:
                user['role'] = UserRole.OPERATOR
            for user in self.developers:
                user['role'] = UserRole.DEVELOPER
            
            # Load role permissions
            self.roles = data.get('roles', {})
            
            logger.info(f"Loaded users from {users_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load users.json: {e}")
            self._create_default_users()
            return False
    
    def _create_default_users(self):
        """Create default users if users.json doesn't exist."""
        self.admins = [
            {
                "username": "admin",
                "password_hash": self._hash_password("admin123"),
                "display_name": "Yönetici",
                "employee_id": "ADM001",
                "role": UserRole.ADMIN,
                "active": True
            }
        ]
        
        self.operators = [
            {
                "username": "operator",
                "password_hash": "",
                "display_name": "Operatör",
                "employee_id": "OP000",
                "role": UserRole.OPERATOR,
                "active": True
            }
        ]
        
        self.developers = [
            {
                "username": "dev",
                "password_hash": self._hash_password("dev123"),
                "display_name": "Geliştirici",
                "employee_id": "DEV001",
                "role": UserRole.DEVELOPER,
                "active": True
            }
        ]
        
        self.roles = {
            UserRole.ADMIN: {"can_navigate_back": True, "can_edit_results": True, "can_edit_test_steps": False},
            UserRole.OPERATOR: {"can_navigate_back": False, "can_edit_results": False, "can_edit_test_steps": False},
            UserRole.DEVELOPER: {"can_navigate_back": True, "can_edit_results": True, "can_edit_test_steps": True}
        }
        
        logger.info("Created default users (1 admin, 1 operator, 1 developer)")
    
    # ========================================================================
    # AUTHENTICATION
    # ========================================================================
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate user with username and password.
        Used for Admin and Developer logins.
        
        Args:
            username: Username to authenticate
            password: Password to check
            
        Returns:
            True if authenticated successfully
        """
        # Find user in all lists
        user = self._find_user(username)
        
        if user is None:
            logger.warning(f"Authentication failed: User '{username}' not found")
            return False
        
        # Check if user is active
        if not user.get('active', True):
            logger.warning(f"Authentication failed: User '{username}' is inactive")
            return False
        
        # Check password
        password_hash = self._hash_password(password)
        stored_hash = user.get('password_hash', '')
        
        if password_hash != stored_hash:
            logger.warning(f"Authentication failed: Invalid password for '{username}'")
            return False
        
        # Set current user
        self.current_user = user.copy()
        logger.info(f"User authenticated: {user['display_name']} ({user['role']})")
        
        return True
    
    def authenticate_by_password_only(self, password: str) -> bool:
        """
        Authenticate using only password (for quick admin/dev login).
        Searches admins and developers for matching password.
        
        Args:
            password: Password to check
            
        Returns:
            True if authenticated successfully
        """
        password_hash = self._hash_password(password)
        
        # Search admins and developers (not operators - they don't have passwords)
        for user in self.admins + self.developers:
            if not user.get('active', True):
                continue
                
            if user.get('password_hash') == password_hash:
                self.current_user = user.copy()
                logger.info(f"User authenticated by password: {user['display_name']}")
                return True
        
        # Fallback: check default admin password
        if password == config.DEFAULT_ADMIN_PASSWORD:
            self.current_user = {
                'role': UserRole.ADMIN,
                'username': 'admin',
                'display_name': 'Yönetici',
                'employee_id': 'ADM001'
            }
            logger.info("Admin authenticated with default password")
            return True
        
        logger.warning("Authentication failed: No matching password found")
        return False
    
    def login_as_operator(self, username: str = None):
        """
        Login as operator (no password required).
        
        Args:
            username: Specific operator username, or None for default
        """
        if username:
            # Find specific operator
            for op in self.operators:
                if op.get('username') == username and op.get('active', True):
                    self.current_user = op.copy()
                    logger.info(f"Logged in as operator: {op['display_name']}")
                    return
        
        # Use first active operator or create default
        if self.operators:
            self.current_user = self.operators[0].copy()
            logger.info(f"Logged in as operator: {self.current_user['display_name']}")
        else:
            self.current_user = {
                'role': UserRole.OPERATOR,
                'username': 'operator',
                'display_name': 'Operatör',
                'employee_id': 'OP000'
            }
            logger.info("Logged in as default operator")
    
    # Alias for backward compatibility
    def authenticate_as_operator(self, username: str = None):
        """Alias for login_as_operator."""
        self.login_as_operator(username)
    
    def logout(self):
        """Clear current user session."""
        if self.current_user:
            logger.info(f"User logged out: {self.current_user.get('display_name')}")
        self.current_user = None
    
    # ========================================================================
    # USER LOOKUP
    # ========================================================================
    
    def _find_user(self, username: str) -> Optional[Dict]:
        """
        Find user by username in all role lists.
        
        Args:
            username: Username to find
            
        Returns:
            User dict or None
        """
        username_lower = username.lower()
        
        # Search all role lists
        for user in self.admins + self.operators + self.developers:
            if user.get('username', '').lower() == username_lower:
                return user
        return None
    
    def get_all_users(self, active_only: bool = True) -> List[Dict]:
        """
        Get list of all users from all roles.
        
        Args:
            active_only: If True, return only active users
            
        Returns:
            List of user dictionaries
        """
        all_users = self.admins + self.operators + self.developers
        
        if active_only:
            return [u for u in all_users if u.get('active', True)]
        return all_users
    
    def get_admins(self) -> List[Dict]:
        """Get list of all admin users."""
        return [u for u in self.admins if u.get('active', True)]
    
    def get_operators(self) -> List[Dict]:
        """Get list of all operator users."""
        return [u for u in self.operators if u.get('active', True)]
    
    def get_developers(self) -> List[Dict]:
        """Get list of all developer users."""
        return [u for u in self.developers if u.get('active', True)]
    
    # ========================================================================
    # CURRENT USER INFO
    # ========================================================================
    
    def get_role(self) -> str:
        """Get current user's role."""
        if self.current_user:
            return self.current_user.get('role', UserRole.OPERATOR)
        return UserRole.OPERATOR
    
    def get_display_name(self) -> str:
        """Get current user's display name."""
        if self.current_user:
            return self.current_user.get('display_name', 'Kullanıcı')
        return "Kullanıcı"
    
    def get_username(self) -> str:
        """Get current user's username."""
        if self.current_user:
            return self.current_user.get('username', '')
        return ""
    
    def get_employee_id(self) -> str:
        """Get current user's employee ID."""
        if self.current_user:
            return self.current_user.get('employee_id', '')
        return ""
    
    def get_department(self) -> str:
        """Get current user's department."""
        if self.current_user:
            return self.current_user.get('department', '')
        return ""
    
    # ========================================================================
    # PERMISSION CHECKS
    # ========================================================================
    
    def is_admin(self) -> bool:
        """Check if current user is admin."""
        return self.get_role() == UserRole.ADMIN
    
    def is_operator(self) -> bool:
        """Check if current user is operator."""
        return self.get_role() == UserRole.OPERATOR
    
    def is_developer(self) -> bool:
        """Check if current user is developer."""
        return self.get_role() == UserRole.DEVELOPER
    
    def can_navigate_back(self) -> bool:
        """
        Check if current user can navigate to previous steps.
        Admins and Developers can navigate back.
        """
        role = self.get_role()
        
        # Check role permissions from loaded data
        if role in self.roles:
            return self.roles[role].get('can_navigate_back', False)
        
        # Fallback to hardcoded list
        return role in UserRole.BACKWARD_NAV_ROLES
    
    def can_edit_results(self) -> bool:
        """
        Check if current user can edit submitted results.
        Admins and Developers can edit results.
        """
        role = self.get_role()
        
        if role in self.roles:
            return self.roles[role].get('can_edit_results', False)
        
        return role in UserRole.EDIT_ROLES
    
    def can_export(self) -> bool:
        """
        Check if current user can export reports.
        Admins and Developers can export.
        """
        role = self.get_role()
        
        if role in self.roles:
            return self.roles[role].get('can_export', True)
        
        return role in UserRole.EXPORT_ROLES
    
    def can_edit_test_steps(self) -> bool:
        """
        Check if current user can edit test steps (Developer mode).
        Only Developers can edit test steps.
        
        Future feature: UI for adding/editing test steps.
        """
        role = self.get_role()
        
        if role in self.roles:
            return self.roles[role].get('can_edit_test_steps', False)
        
        return role in UserRole.EDIT_STEPS_ROLES
    
    def has_permission(self, permission: str) -> bool:
        """
        Check if current user has a specific permission.
        
        Args:
            permission: Permission name (e.g., 'can_navigate_back', 'can_edit_test_steps')
            
        Returns:
            True if user has the permission
        """
        role = self.get_role()
        
        if role in self.roles:
            return self.roles[role].get(permission, False)
        
        return False
    
    # ========================================================================
    # PASSWORD UTILITIES
    # ========================================================================
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hash password using MD5 (for demo compatibility).
        
        Note: Use SHA-256 in production!
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        return hashlib.md5(password.encode()).hexdigest()
    
    @staticmethod
    def hash_password_sha256(password: str) -> str:
        """
        Hash password using SHA-256 (recommended for production).
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    # ========================================================================
    # USER MANAGEMENT (Future)
    # ========================================================================
    
    def add_user(self, username: str, password: str, role: str, 
                 display_name: str, employee_id: str = "", 
                 department: str = "") -> bool:
        """
        Add a new user (for future admin panel).
        
        Args:
            username: Unique username
            password: Plain text password (will be hashed)
            role: User role
            display_name: Display name
            employee_id: Employee ID
            department: Department name
            
        Returns:
            True if user added successfully
        """
        # Check if username exists
        if self._find_user(username):
            logger.warning(f"Cannot add user: '{username}' already exists")
            return False
        
        new_user = {
            "username": username,
            "password_hash": self._hash_password(password),
            "role": role,
            "display_name": display_name,
            "employee_id": employee_id,
            "department": department,
            "active": True
        }
        
        self.users.append(new_user)
        logger.info(f"User added: {display_name} ({role})")
        
        return True
    
    def save_users_to_file(self) -> bool:
        """
        Save current users list to JSON file.
        
        Returns:
            True if saved successfully
        """
        try:
            data = {
                "version": "1.0",
                "users": self.users,
                "roles": self.roles
            }
            
            with open(self.USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            logger.info(f"Users saved to {self.USERS_FILE}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save users: {e}")
            return False
```

# utils\logger.py

```py
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
```

# utils\settings_manager.py

```py
"""
Settings Manager
Handles persistent application settings (saves to disk)

Extended with session metadata memory feature:
- Remembers last entered session metadata values
- Pre-populates fields for faster entry
"""
import json
import os
from typing import Optional, Dict, Any
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SettingsManager:
    """
    Manages application settings that persist between sessions.
    Settings are saved to a JSON file in the application directory.
    
    Extended Features:
    - Session metadata memory (remembers last entered values)
    """
    
    # Default settings file location
    SETTINGS_FILE = "app_settings.json"
    
    # Default values
    DEFAULT_UPDATE_FOLDER = "data/updates"
    DEFAULT_UPDATE_INTERVAL = 10  # seconds
    
    def __init__(self):
        self.settings_path = self.SETTINGS_FILE
        self.settings: Dict[str, Any] = {}
        self._load_settings()
        
    def _load_settings(self):
        """Load settings from disk, create defaults if not exists"""
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
                logger.info(f"Settings loaded from {self.settings_path}")
            else:
                # Create default settings
                self._create_default_settings()
                logger.info("Created default settings")
                
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            self._create_default_settings()
    
    def _create_default_settings(self):
        """Create default settings"""
        self.settings = {
            'update_folder': self.DEFAULT_UPDATE_FOLDER,
            'update_interval': self.DEFAULT_UPDATE_INTERVAL,
            'last_station': '',
            'window_geometry': None,
            'version': '1.0',
            # NEW: Session metadata memory
            'last_session_metadata': {}
        }
        self._save_settings()
    
    def _save_settings(self):
        """Save current settings to disk"""
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            logger.debug(f"Settings saved to {self.settings_path}")
            
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
    
    def get_update_folder(self) -> str:
        """
        Get the update folder path.
        
        Returns:
            Path to update folder (always returns a value, never None)
        """
        folder = self.settings.get('update_folder', self.DEFAULT_UPDATE_FOLDER)
        
        # Ensure the folder exists
        try:
            os.makedirs(folder, exist_ok=True)
        except Exception as e:
            logger.warning(f"Could not create update folder {folder}: {e}")
            # Fall back to default if current folder fails
            folder = self.DEFAULT_UPDATE_FOLDER
            os.makedirs(folder, exist_ok=True)
        
        return folder
    
    def set_update_folder(self, folder: str):
        """
        Set and save the update folder path.
        
        Args:
            folder: Path to update folder
        """
        self.settings['update_folder'] = folder
        self._save_settings()
        logger.info(f"Update folder saved: {folder}")
    
    def get_last_station(self) -> str:
        """Get last used station number"""
        return self.settings.get('last_station', '')
    
    def set_last_station(self, station: str):
        """Save last used station number"""
        self.settings['last_station'] = station
        self._save_settings()
    
    def get_update_interval(self) -> int:
        """
        Get update interval in seconds.
        
        Returns:
            Update interval in seconds (default 10)
        """
        return self.settings.get('update_interval', self.DEFAULT_UPDATE_INTERVAL)
    
    def set_update_interval(self, interval: int):
        """
        Set and save the update interval.
        
        Args:
            interval: Update interval in seconds (minimum 5)
        """
        # Ensure minimum 5 seconds
        interval = max(5, interval)
        self.settings['update_interval'] = interval
        self._save_settings()
        logger.info(f"Update interval saved: {interval} seconds")
    
    # =========================================================================
    # NEW: Session Metadata Memory
    # =========================================================================
    
    def get_last_session_metadata(self) -> Dict[str, Any]:
        """
        Get last entered session metadata values.
        
        Used to pre-populate the TestSessionSetupDialog for faster entry.
        
        Returns:
            Dictionary with last session metadata, or empty dict if none
        """
        return self.settings.get('last_session_metadata', {})
    
    def set_last_session_metadata(self, metadata: Dict[str, Any]):
        """
        Save session metadata for next session.
        
        Args:
            metadata: Dictionary with session metadata values
        """
        self.settings['last_session_metadata'] = metadata
        self._save_settings()
        logger.info("Last session metadata saved for quick entry")
    
    def clear_last_session_metadata(self):
        """Clear saved session metadata"""
        self.settings['last_session_metadata'] = {}
        self._save_settings()
        logger.info("Last session metadata cleared")
    
    # =========================================================================
    # General Methods
    # =========================================================================
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self._create_default_settings()
        logger.info("Settings reset to defaults")
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings as dictionary"""
        return self.settings.copy()
```

# version_info.txt

```txt
# UTF-8
#
# For more details about fixed file info:
# See https://msdn.microsoft.com/en-us/library/ms646997.aspx

VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x40004,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'ASELSAN'),  # CHANGE THIS TO YOUR COMPANY NAME
        StringStruct(u'FileDescription', u'Test Prosedürü Uygulaması - Manufacturing Quality Control System'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'TestProcedure'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2026 ASELSAN'),  # CHANGE THIS
        StringStruct(u'OriginalFilename', u'TestProcedureDEMO.exe'),
        StringStruct(u'ProductName', u'261 Test Kiosk DEMO'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)

```

