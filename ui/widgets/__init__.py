"""
Widgets Package
UI widget components
"""
from ui.widgets.header_widget import HeaderWidget
from ui.widgets.title_widget import TitleWidget
from ui.widgets.content.content_widget import ContentWidget  # ← CHANGED
from ui.widgets.status_bar_widget import StatusBarWidget

__all__ = ['HeaderWidget', 'TitleWidget', 'ContentWidget', 'StatusBarWidget']