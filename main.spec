# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

pandas_datas, pandas_binaries, pandas_hiddenimports = collect_all('pandas')
PIL_datas, PIL_binaries, PIL_hiddenimports = collect_all('PIL')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[] + pandas_binaries + PIL_binaries,
    datas=[
        ('img', 'img'),
        ('sons', 'sons'),
        ('fonts', 'fonts'),
        ('base', 'base'),
        ('config.json', '.'),
    ] + pandas_datas + PIL_datas,
    hiddenimports=[
        'pyautogui',
        'pygetwindow',
        'pynput',
        'pynput.keyboard',
        'pynput.mouse',
    ] + pandas_hiddenimports + PIL_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RoletaRussa',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='img\\rr_icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RoletaRussa',
)
