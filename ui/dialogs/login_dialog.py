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