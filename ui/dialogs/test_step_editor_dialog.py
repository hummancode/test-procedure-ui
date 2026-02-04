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
        self.setMinimumSize(1400, 1000)
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
        splitter.setSizes([450, 1000])
        
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
        self.step_list.setMinimumWidth(350)
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
        image_label.setFixedWidth(130)
        self.image_path_input = QLineEdit()
        self.image_path_input.setPlaceholderText("resources/images/step_xxx.png")
        self.image_path_input.setEnabled(self.is_developer)
        self.image_path_input.textChanged.connect(self._on_field_changed)
        
        browse_btn = QPushButton("Gözat...")
        browse_btn.setFixedWidth(150)
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