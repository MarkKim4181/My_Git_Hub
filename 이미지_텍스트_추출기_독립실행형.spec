# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['image_text_extractor.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\UnisCrew\\내 드라이브\\Git_Hub_DeskTop\\My_Git_Hub\\temp_build\\tesseract-ocr', 'tesseract')],
    hiddenimports=[],
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
    name='이미지_텍스트_추출기_독립실행형',
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
    icon='NONE',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='이미지_텍스트_추출기_독립실행형',
)
