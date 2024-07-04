# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['visual_main.py'],
    pathex=[
        'C:\\Python\\Atellica_proyect\\Visual_element\\sidebar.py',
        'C:\\Python\\Atellica_proyect\\Visual_element\\settings.py',
        'C:\\Python\\Atellica_proyect\\Visual_element\\inicio.py',
        'C:\\Python\\Atellica_proyect\\Visual_element\\settingslogic\\settingsConfiguracion.py',
        'C:\\Python\\Atellica_proyect\\Visual_element\\settingsHistory\\historial.py',
        'C:\\Python\\Atellica_proyect\\Visual_element\\settingsDm\\dmSettings.py',
        'C:\\Python\\Atellica_proyect\\SqlLiteData\\sqlLogic.py',
    ],
    binaries=[],
    datas=[
        ('C:\\Python\\Atellica_proyect\\Visual_element\\image\\*', 'image'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='nombre_aplicacion',
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='nombre_aplicacion',
)

if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='nombre_aplicacion.app',
        icon=None,
        bundle_identifier=None,
    )