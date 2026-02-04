# -*- coding: utf-8 -*-

"""
Dialogs Package
Dialog windows for the application
"""
from ui.dialogs.update_settings_dialog import UpdateSettingsDialog
from ui.dialogs.switch_user_dialog import SwitchUserDialog
from ui.dialogs.test_session_setup_dialog import TestSessionSetupDialog
from ui.dialogs.test_step_editor_dialog import TestStepEditorDialog
from ui.dialogs.user_management_dialog import UserManagementDialog

__all__ = [
    'UpdateSettingsDialog', 
    'SwitchUserDialog',
    'TestSessionSetupDialog',
    'TestStepEditorDialog'
    'UserManagementDialog',
]