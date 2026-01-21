# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置
将销售网点查询系统打包成Windows桌面应用
"""

from PyInstaller.utils.hooks import collect_all
from PyInstaller.building.build_main import Analysis, PYZ, EXE
from PyInstaller.building.datastruct import Tree

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('customer_data.py', '.'),
        ('local_data.py', '.'),
    ],
    hiddenimports=[
        'requests',
        'flask',
        'jinja2',
        'markupsafe',
        'werkzeug',
        'click',
        'itsdangerous',
        'certifi',
        'charset_normalizer',
        'idna',
        'urllib3',
        'charset_normalizer',
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
    name='销售网点查询系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # 如果有图标文件
)
