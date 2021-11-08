from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['D:\\Programming\\Work_Projects\\InvoicesApp\\copy_files_package\\app.py'],
             pathex=['D:\\Programming\\Work_Projects\\InvoicesApp\\App_exe','D:\\Programming\\Work_Projects\\InvoicesApp\\ENV'],
             binaries=[],
             datas=[],
             hiddenimports=["sqlite3","selenium","kivy","selenium.webdriver.common","cryptography","Kivy-Garden","kivymd","pandas","XlsxWriter","openpyxl"],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='InvoicesAPP',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='D:\\Programming\\Work_Projects\\InvoicesApp\\copy_files_package\\views\\resources\\icons\\invoices.ico')
coll = COLLECT(exe,Tree('D:\\Programming\\Work_Projects\\\InvoicesApp\\copy_files_package'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='InvoicesAPP')
