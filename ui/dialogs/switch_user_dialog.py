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