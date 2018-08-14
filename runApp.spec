# -*- mode: python -*-
from kivy.deps import sdl2, glew, gstreamer
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks

block_cipher = None


a = Analysis(['C:\\workspace\\soundboard\main.py'],
             pathex=['C:\\workspace\\soundboard'],
             binaries=[],
             datas=[],
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             **get_deps_minimal(video=None))
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='LADSoundboard',
          icon='C:\\workspace\\soundboard\images\scully.ico',
          debug=False,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe, Tree('C:\\workspace\\soundboard'),
               a.binaries,
               a.zipfiles,
               a.datas,
               Tree('C:\\workspace\\soundboard'),
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)], 
               strip=False,
               upx=True,
               name='run')
