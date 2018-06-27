# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py','FSM.py','biu.py','menu.py','commons.py','vector.py'],
             pathex=['E:\\code\\_repository\\Biu'],
             binaries=[],
             datas=[('E:\\code\\_repository\\Biu\\data','data'),
			 ('E:\\code\\_repository\\Biu\\sounds','sounds')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
