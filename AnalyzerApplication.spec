# Sample .spec file
# Usage:  pyinstaller ./AnalyzerApplication.spec


a = Analysis(
    ['main.py'],
    pathex=[
        'E:/Projects/Carcinoma/p-analyzer'
    ],
    binaries=[],
    datas=[
        ('./conf', './conf'),
        ('./logs', './logs'),
        ('./data', './data'),
        ('./resources', './resources'),
        ('./vips-dev-8.14', './vips-dev-8.14'),
        ('./weights', './weights')
    ],
    hiddenimports=['PySide2.QtXml'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['./build', './dist', './tmp'],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AnalyzerApplication',
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
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AnalyzerApplication',
)
