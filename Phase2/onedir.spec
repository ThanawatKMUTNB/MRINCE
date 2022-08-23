block_cipher = None


a = Analysis(
    ['GUI2.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
# add directory src
a.datas += Tree('./src', prefix='src')
# Avoid warning
to_remove = ["_AES", "_ARC4", "_DES", "_DES3", "_SHA256", "_counter"]
for b in a.binaries:
    found = any(
        f'{crypto}.cp37-win_amd64.pyd' in b[1]
        for crypto in to_remove
    )
    if found:
        print(f"Removing {b[1]}")
        a.binaries.remove(b)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
excluded_binaries = [
    'VCRUNTIME140.dll',
    'msvcp140.dll',
    'mfc140u.dll']
a.binaries = TOC([x for x in a.binaries if x[0] not in excluded_binaries])

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GUI2',
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
    name='GUI2',
)