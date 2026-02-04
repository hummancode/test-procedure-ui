# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

"""
User Management Dialog
Allows Admin and Developer users to manage operators (Add, Edit, Delete).

Features:
- Left panel: List of all operators with status indicators
- Right panel: User details form for add/edit
- Role-based access: Only Admin/Developer can access
- Persistent storage: Saves to data/users.json

Location: ui/dialogs/user_management_dialog.py
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
    QPushButton, QLineEdit, QTextEdit, QComboBox,
    QListWidget, QListWidgetItem, QGroupBox, QScrollArea,
    QMessageBox, QFrame, QSplitter, QFormLayout, QCheckBox,
    QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIcon
from typing import Optional, List, Dict, Any
import json
import os

import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class UserManagementDialog(QDialog):
    """
    Dialog for managing operators (Add, Edit, Delete).
    
    Only accessible by Admin and Developer users.
    
    Layout:
    ┌────────────────────────────────────────────────────────────────────┐
    │                    Kullanıcı Yönetimi                              │
    ├──────────────────────┬─────────────────────────────────────────────┤
    │  Operatör Listesi    │  Operatör Detayları                         │
    │  (Scrollable)        │                                             │
    │                      │  Kullanıcı Adı: [_______________]           │
    │  ● Ali Yılmaz        │  Görünen Ad: [________________]             │
    │  ● Ayşe Kaya         │  Sicil No: [___________]                    │
    │  ○ Mehmet Demir ◄    │  Departman: [___________]                   │
    │  ● Fatma Öztürk      │                                             │
    │                      │  ☑ Aktif                                    │
    │                      │                                             │
    │  [+ Yeni Ekle]       │  [Kaydet]  [İptal]                          │
    ├──────────────────────┴─────────────────────────────────────────────┤
    │                      [Kapat]                                       │
    └────────────────────────────────────────────────────────────────────┘
    
    Signals:
        users_updated: Emitted when users list is modified
    """
    
    # Signal emitted when users are updated
    users_updated = pyqtSignal()
    
    def __init__(self, auth_manager, parent=None):
        """
        Initialize the User Management Dialog.
        
        Args:
            auth_manager: AuthManager instance for user operations
            parent: Parent widget (usually MainWindow)
        """
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.current_operator: Optional[Dict] = None
        self.is_new_user = False
        
        self.setWindowTitle("Kullanıcı Yönetimi - Operatörler")
        self.setMinimumSize(900, 600)
        self.setModal(True)
        
        self._init_ui()
        self._load_operators()
        self._connect_signals()
        
        logger.debug("UserManagementDialog initialized")
    
    def _init_ui(self):
        """Initialize the UI components."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # ====================================================================
        # Header
        # ====================================================================
        header_label = QLabel("Kullanıcı Yönetimi - Operatörler")
        header_label.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_LARGE}pt;
            color: {config.Colors.TEXT_PRIMARY};
            font-weight: bold;
            padding: 10px;
        """)
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Info label showing current user role
        current_role = self.auth_manager.get_role()
        role_display = config.UserRole.get_display_name(current_role) if hasattr(config, 'UserRole') else current_role.capitalize()
        info_label = QLabel(f"Giriş yapan: {self.auth_manager.get_display_name()} ({role_display})")
        info_label.setStyleSheet(f"""
            font-size: {config.FONT_SIZE}pt;
            color: {config.Colors.TEXT_SECONDARY};
            padding: 5px;
        """)
        info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(info_label)
        
        # ====================================================================
        # Main Content - Splitter with List and Details
        # ====================================================================
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {config.Colors.BORDER};
                width: 2px;
            }}
        """)
        
        # Left Panel - Operator List
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right Panel - Operator Details
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set initial splitter sizes (35% / 65%)
        splitter.setSizes([300, 550])
        
        main_layout.addWidget(splitter, 1)
        
        # ====================================================================
        # Bottom Buttons
        # ====================================================================
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        self.close_btn = QPushButton("Kapat")
        self.close_btn.setFixedSize(120, 40)
        self.close_btn.setStyleSheet(self._get_button_style(secondary=True))
        self.close_btn.clicked.connect(self.accept)
        bottom_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(bottom_layout)
        
        # Apply dialog styling
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {config.Colors.BACKGROUND_PRIMARY};
            }}
            QLabel {{
                color: {config.Colors.TEXT_PRIMARY};
            }}
            QLineEdit, QComboBox {{
                background-color: {config.Colors.INPUT_BACKGROUND};
                color: {config.Colors.TEXT_PRIMARY};
                border: 1px solid {config.Colors.BORDER};
                border-radius: 4px;
                padding: 8px;
                font-size: {config.FONT_SIZE}pt;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border: 2px solid {config.Colors.ACCENT_BLUE};
            }}
            QLineEdit:disabled {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                color: {config.Colors.TEXT_DISABLED};
            }}
            QCheckBox {{
                color: {config.Colors.TEXT_PRIMARY};
                font-size: {config.FONT_SIZE}pt;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
            }}
            QCheckBox::indicator:unchecked {{
                border: 2px solid {config.Colors.BORDER};
                background-color: {config.Colors.INPUT_BACKGROUND};
                border-radius: 4px;
            }}
            QCheckBox::indicator:checked {{
                border: 2px solid {config.Colors.SUCCESS};
                background-color: {config.Colors.SUCCESS};
                border-radius: 4px;
            }}
            QGroupBox {{
                color: {config.Colors.TEXT_PRIMARY};
                font-size: {config.FONT_SIZE}pt;
                font-weight: bold;
                border: 1px solid {config.Colors.BORDER};
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
    
    def _create_left_panel(self) -> QWidget:
        """Create the left panel with operator list."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # List header
        list_header = QLabel("Operatör Listesi")
        list_header.setStyleSheet(f"""
            font-size: {config.FONT_SIZE + 2}pt;
            font-weight: bold;
            color: {config.Colors.TEXT_PRIMARY};
            padding: 5px;
        """)
        layout.addWidget(list_header)
        
        # Operator list
        self.operator_list = QListWidget()
        self.operator_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {config.Colors.BACKGROUND_SECONDARY};
                border: 1px solid {config.Colors.BORDER};
                border-radius: 6px;
                padding: 5px;
            }}
            QListWidget::item {{
                color: {config.Colors.TEXT_PRIMARY};
                padding: 10px;
                margin: 2px;
                border-radius: 4px;
            }}
            QListWidget::item:selected {{
                background-color: {config.Colors.ACCENT_BLUE};
                color: white;
            }}
            QListWidget::item:hover:!selected {{
                background-color: {config.Colors.BACKGROUND_TERTIARY};
            }}
        """)
        self.operator_list.setFont(QFont("Segoe UI", config.FONT_SIZE))
        layout.addWidget(self.operator_list, 1)
        
        # Add new button
        self.add_new_btn = QPushButton("+ Yeni Operatör Ekle")
        self.add_new_btn.setFixedHeight(45)
        self.add_new_btn.setStyleSheet(self._get_button_style(accent=True))
        layout.addWidget(self.add_new_btn)
        
        return panel
    
    def _create_right_panel(self) -> QWidget:
        """Create the right panel with operator details form."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)
        
        # Details header
        self.details_header = QLabel("Operatör Detayları")
        self.details_header.setStyleSheet(f"""
            font-size: {config.FONT_SIZE + 2}pt;
            font-weight: bold;
            color: {config.Colors.TEXT_PRIMARY};
            padding: 5px;
        """)
        layout.addWidget(self.details_header)
        
        # Form group
        form_group = QGroupBox("Bilgiler")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(15, 25, 15, 15)
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Benzersiz kullanıcı adı...")
        self.username_input.setMinimumHeight(40)
        form_layout.addRow("Kullanıcı Adı:", self.username_input)
        
        # Display name field
        self.display_name_input = QLineEdit()
        self.display_name_input.setPlaceholderText("Görünen ad (örn: Ali Yılmaz)...")
        self.display_name_input.setMinimumHeight(40)
        form_layout.addRow("Görünen Ad:", self.display_name_input)
        
        # Employee ID field
        self.employee_id_input = QLineEdit()
        self.employee_id_input.setPlaceholderText("Sicil numarası (örn: OP001)...")
        self.employee_id_input.setMinimumHeight(40)
        form_layout.addRow("Sicil No:", self.employee_id_input)
        
        # Department field
        self.department_input = QLineEdit()
        self.department_input.setPlaceholderText("Departman (örn: Üretim Hattı A)...")
        self.department_input.setMinimumHeight(40)
        form_layout.addRow("Departman:", self.department_input)
        
        # Active checkbox
        self.active_checkbox = QCheckBox("Aktif")
        self.active_checkbox.setChecked(True)
        form_layout.addRow("Durum:", self.active_checkbox)
        
        layout.addWidget(form_group)
        
        # Spacer
        layout.addStretch()
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)
        
        # Delete button (left side)
        self.delete_btn = QPushButton("Sil")
        self.delete_btn.setFixedSize(100, 40)
        self.delete_btn.setStyleSheet(self._get_button_style(danger=True))
        self.delete_btn.setVisible(False)
        action_layout.addWidget(self.delete_btn)
        
        action_layout.addStretch()
        
        # Cancel button
        self.cancel_btn = QPushButton("İptal")
        self.cancel_btn.setFixedSize(100, 40)
        self.cancel_btn.setStyleSheet(self._get_button_style(secondary=True))
        self.cancel_btn.setVisible(False)
        action_layout.addWidget(self.cancel_btn)
        
        # Save button
        self.save_btn = QPushButton("Kaydet")
        self.save_btn.setFixedSize(120, 40)
        self.save_btn.setStyleSheet(self._get_button_style(primary=True))
        self.save_btn.setVisible(False)
        action_layout.addWidget(self.save_btn)
        
        layout.addLayout(action_layout)
        
        # Initially disable form
        self._set_form_enabled(False)
        
        return panel
    
    def _get_button_style(self, primary=False, secondary=False, danger=False, accent=False) -> str:
        """Get button stylesheet based on type."""
        if primary:
            return f"""
                QPushButton {{
                    background-color: {config.Colors.SUCCESS};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: {config.FONT_SIZE}pt;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #66bb6a;
                }}
                QPushButton:pressed {{
                    background-color: #43a047;
                }}
                QPushButton:disabled {{
                    background-color: {config.Colors.TEXT_DISABLED};
                }}
            """
        elif danger:
            return f"""
                QPushButton {{
                    background-color: {config.Colors.ERROR};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: {config.FONT_SIZE}pt;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #ef5350;
                }}
                QPushButton:pressed {{
                    background-color: #e53935;
                }}
            """
        elif accent:
            return f"""
                QPushButton {{
                    background-color: {config.Colors.ACCENT_BLUE};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: {config.FONT_SIZE}pt;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {config.Colors.ACCENT_LIGHT};
                }}
                QPushButton:pressed {{
                    background-color: #1976d2;
                }}
            """
        else:  # secondary
            return f"""
                QPushButton {{
                    background-color: {config.Colors.BACKGROUND_TERTIARY};
                    color: {config.Colors.TEXT_PRIMARY};
                    border: 1px solid {config.Colors.BORDER};
                    border-radius: 6px;
                    font-size: {config.FONT_SIZE}pt;
                }}
                QPushButton:hover {{
                    background-color: {config.Colors.BACKGROUND_SECONDARY};
                    border-color: {config.Colors.ACCENT_BLUE};
                }}
                QPushButton:pressed {{
                    background-color: {config.Colors.BACKGROUND_PRIMARY};
                }}
            """
    
    def _connect_signals(self):
        """Connect UI signals to slots."""
        self.operator_list.currentItemChanged.connect(self._on_operator_selected)
        self.add_new_btn.clicked.connect(self._on_add_new)
        self.save_btn.clicked.connect(self._on_save)
        self.cancel_btn.clicked.connect(self._on_cancel)
        self.delete_btn.clicked.connect(self._on_delete)
    
    def _load_operators(self):
        """Load operators from auth_manager into the list."""
        self.operator_list.clear()
        
        # Get all operators (including inactive)
        all_operators = self.auth_manager.operators if hasattr(self.auth_manager, 'operators') else []
        
        for op in all_operators:
            display_name = op.get('display_name', op.get('username', 'Operatör'))
            dept = op.get('department', '')
            is_active = op.get('active', True)
            
            # Create display text
            text = display_name
            if dept:
                text += f" - {dept}"
            if not is_active:
                text += " (Pasif)"
            
            # Add status indicator
            status_icon = "●" if is_active else "○"
            text = f"{status_icon} {text}"
            
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, op)
            
            # Gray out inactive users
            if not is_active:
                item.setForeground(QColor(config.Colors.TEXT_DISABLED))
            
            self.operator_list.addItem(item)
        
        logger.debug(f"Loaded {len(all_operators)} operators into list")
    
    def _on_operator_selected(self, current, previous):
        """Handle operator selection in list."""
        if current is None:
            self._clear_form()
            self._set_form_enabled(False)
            return
        
        self.current_operator = current.data(Qt.UserRole)
        self.is_new_user = False
        
        if self.current_operator:
            self._populate_form(self.current_operator)
            self._set_form_enabled(True)
            self.delete_btn.setVisible(True)
            self.save_btn.setVisible(True)
            self.cancel_btn.setVisible(True)
            self.details_header.setText("Operatör Düzenle")
            
            # Username cannot be edited for existing users
            self.username_input.setEnabled(False)
    
    def _on_add_new(self):
        """Handle adding a new operator."""
        self.operator_list.clearSelection()
        self.current_operator = None
        self.is_new_user = True
        
        self._clear_form()
        self._set_form_enabled(True)
        self.username_input.setEnabled(True)
        self.delete_btn.setVisible(False)
        self.save_btn.setVisible(True)
        self.cancel_btn.setVisible(True)
        self.details_header.setText("Yeni Operatör Ekle")
        
        # Focus on username field
        self.username_input.setFocus()
    
    def _on_save(self):
        """Save the current operator (add or update)."""
        # Validate form
        username = self.username_input.text().strip()
        display_name = self.display_name_input.text().strip()
        employee_id = self.employee_id_input.text().strip()
        department = self.department_input.text().strip()
        is_active = self.active_checkbox.isChecked()
        
        # Validation
        if not username:
            QMessageBox.warning(
                self,
                "Uyarı",
                "Kullanıcı adı zorunludur!",
                QMessageBox.Ok
            )
            self.username_input.setFocus()
            return
        
        if not display_name:
            QMessageBox.warning(
                self,
                "Uyarı",
                "Görünen ad zorunludur!",
                QMessageBox.Ok
            )
            self.display_name_input.setFocus()
            return
        
        if self.is_new_user:
            # Check if username already exists
            existing = self.auth_manager._find_user(username)
            if existing:
                QMessageBox.warning(
                    self,
                    "Uyarı",
                    f"'{username}' kullanıcı adı zaten mevcut!",
                    QMessageBox.Ok
                )
                self.username_input.setFocus()
                return
            
            # Add new operator
            new_operator = {
                "username": username,
                "password_hash": "",  # Operators don't have passwords
                "display_name": display_name,
                "employee_id": employee_id,
                "department": department,
                "role": "operator",
                "active": is_active
            }
            
            self.auth_manager.operators.append(new_operator)
            logger.info(f"Added new operator: {display_name} ({username})")
            
        else:
            # Update existing operator
            if self.current_operator:
                # Find and update in the list
                for i, op in enumerate(self.auth_manager.operators):
                    if op.get('username') == self.current_operator.get('username'):
                        self.auth_manager.operators[i]['display_name'] = display_name
                        self.auth_manager.operators[i]['employee_id'] = employee_id
                        self.auth_manager.operators[i]['department'] = department
                        self.auth_manager.operators[i]['active'] = is_active
                        logger.info(f"Updated operator: {display_name}")
                        break
        
        # Save to file
        if self._save_users_to_file():
            QMessageBox.information(
                self,
                "Başarılı",
                "Operatör başarıyla kaydedildi!",
                QMessageBox.Ok
            )
            
            # Reload list and clear form
            self._load_operators()
            self._clear_form()
            self._set_form_enabled(False)
            self.delete_btn.setVisible(False)
            self.save_btn.setVisible(False)
            self.cancel_btn.setVisible(False)
            self.details_header.setText("Operatör Detayları")
            
            # Emit signal
            self.users_updated.emit()
        else:
            QMessageBox.critical(
                self,
                "Hata",
                "Kullanıcı kaydedilemedi! Lütfen tekrar deneyin.",
                QMessageBox.Ok
            )
    
    def _on_cancel(self):
        """Cancel current operation."""
        self.operator_list.clearSelection()
        self._clear_form()
        self._set_form_enabled(False)
        self.delete_btn.setVisible(False)
        self.save_btn.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.details_header.setText("Operatör Detayları")
        self.current_operator = None
        self.is_new_user = False
    
    def _on_delete(self):
        """Delete the selected operator."""
        if not self.current_operator:
            return
        
        display_name = self.current_operator.get('display_name', 'Operatör')
        username = self.current_operator.get('username', '')
        
        # Confirm deletion
        result = QMessageBox.question(
            self,
            "Silme Onayı",
            f"'{display_name}' operatörünü silmek istediğinizden emin misiniz?\n\n"
            "Bu işlem geri alınamaz!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if result != QMessageBox.Yes:
            return
        
        # Remove from list
        self.auth_manager.operators = [
            op for op in self.auth_manager.operators 
            if op.get('username') != username
        ]
        
        logger.info(f"Deleted operator: {display_name} ({username})")
        
        # Save to file
        if self._save_users_to_file():
            QMessageBox.information(
                self,
                "Başarılı",
                f"'{display_name}' operatörü silindi!",
                QMessageBox.Ok
            )
            
            # Reload list and clear form
            self._load_operators()
            self._clear_form()
            self._set_form_enabled(False)
            self.delete_btn.setVisible(False)
            self.save_btn.setVisible(False)
            self.cancel_btn.setVisible(False)
            self.details_header.setText("Operatör Detayları")
            self.current_operator = None
            
            # Emit signal
            self.users_updated.emit()
        else:
            QMessageBox.critical(
                self,
                "Hata",
                "Operatör silinemedi! Lütfen tekrar deneyin.",
                QMessageBox.Ok
            )
    
    def _populate_form(self, operator: Dict):
        """Populate form fields with operator data."""
        self.username_input.setText(operator.get('username', ''))
        self.display_name_input.setText(operator.get('display_name', ''))
        self.employee_id_input.setText(operator.get('employee_id', ''))
        self.department_input.setText(operator.get('department', ''))
        self.active_checkbox.setChecked(operator.get('active', True))
    
    def _clear_form(self):
        """Clear all form fields."""
        self.username_input.clear()
        self.display_name_input.clear()
        self.employee_id_input.clear()
        self.department_input.clear()
        self.active_checkbox.setChecked(True)
    
    def _set_form_enabled(self, enabled: bool):
        """Enable or disable form fields."""
        self.username_input.setEnabled(enabled)
        self.display_name_input.setEnabled(enabled)
        self.employee_id_input.setEnabled(enabled)
        self.department_input.setEnabled(enabled)
        self.active_checkbox.setEnabled(enabled)
    
    def _save_users_to_file(self) -> bool:
        """
        Save users to data/users.json file.
        
        Returns:
            True if saved successfully
        """
        try:
            # Get the users file path
            users_file = self.auth_manager.USERS_FILE
            
            # Also try alternative paths
            possible_paths = [
                users_file,
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "users.json"),
                os.path.join(os.getcwd(), "data", "users.json")
            ]
            
            # Find the first existing path or use the first one
            save_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    save_path = path
                    break
            
            if save_path is None:
                save_path = possible_paths[0]
                # Ensure directory exists
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Build the data structure
            data = {
                "version": "1.0",
                "description": "Kullanıcı tanımları - 3 Rol Tipi: Admin, Operator, Developer",
                "users": {
                    "admins": self.auth_manager.admins,
                    "operators": self.auth_manager.operators,
                    "developers": self.auth_manager.developers
                },
                "roles": self.auth_manager.roles if hasattr(self.auth_manager, 'roles') else {
                    "admin": {"can_navigate_back": True, "can_edit_results": True, "can_edit_test_steps": False},
                    "operator": {"can_navigate_back": False, "can_edit_results": False, "can_edit_test_steps": False},
                    "developer": {"can_navigate_back": True, "can_edit_results": True, "can_edit_test_steps": True}
                }
            }
            
            # Remove 'role' field from user dicts (it's implied by the list)
            for user_list in [data['users']['admins'], data['users']['operators'], data['users']['developers']]:
                for user in user_list:
                    if 'role' in user:
                        del user['role']
            
            # Write to file
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            logger.info(f"Users saved to {save_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save users: {e}")
            return False