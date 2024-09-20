# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.pyw'],
    pathex=[],
    binaries=[],
    datas=[('requirements.txt', '.'), ('main.pyw', '.'), ('C:\\Users\\L33T\\Documents\\Cashout Cookie Checker\\Config Config Developer\\main.spec', '.'), ('C:\\Users\\L33T\\Documents\\Cashout Cookie Checker\\Config Config Developer\\Config_Creator.py', '.'), ('C:\\Users\\L33T\\Documents\\Cashout Cookie Checker\\Config Config Developer\\cookie_creator.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CashOutCookieCreator',
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
    icon=['cookie_creator.ico'],
)
