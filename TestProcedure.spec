# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File for Test Procedure Application
Publisher: X
Version: 1.0
FIXED: Excludes pandas/numpy to reduce size and prevent errors
FIXED: Removed problematic empty list causing icon error
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Application metadata
APP_NAME = 'TestProcedure'
APP_VERSION = '1.0'
APP_PUBLISHER = 'X'  # Change this to your actual publisher name
APP_COPYRIGHT = 'Copyright (c) 2026 X'
APP_DESCRIPTION = 'Test Prosedürü Uygulaması - Manufacturing Quality Control System'

# Collect all data files
datas = []
datas += collect_data_files('qt_material')
datas += collect_data_files('qdarkstyle')

# Add your data folders
datas += [('data', 'data')]
datas += [('resources', 'resources')]

# Collect only necessary submodules
hiddenimports = [
    'openpyxl.cell._writer',
]

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude heavy packages not needed
        'tkinter',
        'matplotlib',
        'numpy',           # NOT NEEDED - pandas is imported but not used
        'scipy',
        'pandas',          # NOT NEEDED - imported but not actually used
        'IPython',         # NOT NEEDED - Spyder/Jupyter stuff
        'jedi',            # NOT NEEDED - Code completion
        'parso',           # NOT NEEDED - Parser
        'black',           # NOT NEEDED - Code formatter
        'sphinx',          # NOT NEEDED - Documentation
        'docutils',        # NOT NEEDED
        'pygments',        # NOT NEEDED - Syntax highlighting
        'astroid',         # NOT NEEDED - Code analysis
        'wcwidth',         # NOT NEEDED
        'zmq',             # NOT NEEDED - Messaging
        'nbformat',        # NOT NEEDED - Jupyter notebooks
        'jsonschema',      # NOT NEEDED
        'cryptography',    # NOT NEEDED - unless you use encryption
        'bcrypt',          # NOT NEEDED
        'certifi',         # NOT NEEDED
        'urllib3',         # NOT NEEDED
        'charset_normalizer', # NOT NEEDED
        'psutil',          # NOT NEEDED
        'cloudpickle',     # NOT NEEDED
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to False for GUI-only app (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Windows-specific metadata
    version='version_info.txt',
    # icon='resources/icons/app_icon.ico',  # Add icon later if needed
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)
