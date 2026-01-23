# -*- coding: utf-8 -*-

"""
Progress Navigator - Sidebar showing all test steps
Visual-only in Phase 3A (no clicking)
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QLabel, 
                             QFrame, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont
from typing import List, Optional
import config
from models.enums import TestStatus
from models.test_step import TestStep
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ProgressNavigator(QWidget):
    """
    Sidebar showing all test steps with status indicators.
    
    Phase 3A: Visual only, no interaction
    Phase 3B: Clickable navigation (future)
    
    Signals:
        step_clicked: Emitted when step is clicked (future)
    """
    
    step_clicked = pyqtSignal(int)  # step_index (not used in Phase 3A)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.steps: List[TestStep] = []
        self.current_step_index: int = -1
        self.step_widgets: List[QFrame] = []
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
        """)
        
        return frame
    
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
        """)
    
    def _scroll_to_step(self, step_index: int):
        """Auto-scroll to make step visible"""
        if 0 <= step_index < len(self.step_widgets):
            widget = self.step_widgets[step_index]
            # Find scroll area parent
            scroll_area = self.findChild(QScrollArea)
            if scroll_area:
                scroll_area.ensureWidgetVisible(widget, 50, 50)