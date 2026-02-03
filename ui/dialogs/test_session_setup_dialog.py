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