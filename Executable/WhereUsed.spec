a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'WhereUsed.py'],
             pathex=['C:\\Python25\\tim\\GoodScripts\\MapBOM\\WhereUsed'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          name='WhereUsed.exe',
          debug=False,
          strip=False,
          upx=False,
          console=True , icon='whereused.ico')
