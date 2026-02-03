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