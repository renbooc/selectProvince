# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

templates_path = os.path.join(os.getcwd(), 'templates')

a = Analysis(
    ['app_desktop.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[(templates_path, 'templates')],
    hiddenimports=[
        'flask',
        'flask.globals',
        'flask.json.provider',
        'requests',
        'urllib3',
        'charset_normalizer',
        'certifi',
        'idna',
        'werkzeug',
        'markupsafe',
        'jinja2',
        'itsdangerous',
        'click',
        'webview',
        'webview.dom',
        'webview.window',
        'pywebview',
        'clr_loader',
        'pythonnet',
        'proxy_tools',
        'bottle',
        'cffi',
        'pycparser',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='海元堂查询系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)
