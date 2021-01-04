# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\gmdev\\Desktop\\python_projects\\PasswordManager\\src\\main\\python\\main.py'],
             pathex=['C:\\Users\\gmdev\\Desktop\\python_projects\\PasswordManager\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['C:\\Users\\gmdev\\Desktop\\venv3_6\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['C:\\Users\\gmdev\\Desktop\\python_projects\\PasswordManager\\target\\PyInstaller\\fbs_pyinstaller_hook.py'],
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
          name='PasswordManager',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='C:\\Users\\gmdev\\Desktop\\python_projects\\PasswordManager\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='PasswordManager')
