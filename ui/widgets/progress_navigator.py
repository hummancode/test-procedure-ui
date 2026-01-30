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