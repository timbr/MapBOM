a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'MapBom.py'],
             pathex=['C:\\Python25\\tim\\mapbomclass'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          name='MapBom.exe',
          debug=False,
          strip=False,
          upx=False,
          console=True , icon='mapbom.ico')
