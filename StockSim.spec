# -*- mode: python -*-

block_cipher = None


a = Analysis(['StockSim.py'],
             pathex=['/Users/kcfdaniel/Downloads/Stock Sim'],
             binaries=[],
             datas=[('transactionUI.ui', '.'), ('stocksUI.ui', '.'), ('stocks.txt', '.'), ('transactions.txt', '.')],
             hiddenimports=['tkinter', 'PyQt5.sip', 'pandas._libs.tslibs.np_datetime', 'pandas._libs.tslibs.nattype', 'pandas._libs.skiplist'],
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
          name='StockSim',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='stock.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='StockSim')
app = BUNDLE(coll,
             name='StockSim.app',
             icon='stock.icns',
             bundle_identifier=None)
