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