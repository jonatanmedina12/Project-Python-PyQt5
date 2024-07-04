# -*- mode: python ; coding: utf-8 -*-

img_dir = 'C:\\Python\\Atellica_proyect\\Visual_element\\image\\*'
a = Analysis(
    ['visual_main.py'],
    pathex=[
        'C:\\Python\\Atellica_proyect\\Visual_element\\',
        'C:\\Python\\Atellica_proyect\\SqlLiteData\\',
    ],
    binaries=[],
    datas=[
        (img_dir, 'images\\'),

    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='nombre_ejecutable',
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
    icon=None,  # Agrega esta línea si deseas especificar un icono para el ejecutable
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='internal',
)