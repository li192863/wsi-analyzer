# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['SlicerApplication.py'], # 入口文件
    pathex=['ImageSlicer.py'],  # python模块
    binaries=[],
    datas=[('./resources', './resources'), ('./vips-dev-8.14', './vips-dev-8.14')],  # 资源文件
    hiddenimports=['PySide6.QtXml'],  # 隐式导入
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
    [],
    exclude_binaries=True,
    name='SlicerApplication',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='./resources/favicon.ico'  # 图标
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SlicerApplication',
)
