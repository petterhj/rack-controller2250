# -*- mode: python -*-
import os, sys

BASE_PATH = os.path.abspath(os.path.dirname(__name__))
RESOURCE_PATH = BASE_PATH + '\\resources'
LIB_PATH = BASE_PATH + '\\lib'

sys.path.append(BASE_PATH)

import config

block_cipher = None
version = config.VERSION
debug = config.DEBUG
resources = [f for f in os.listdir(RESOURCE_PATH) if os.path.isfile(os.path.join(RESOURCE_PATH, f))]
libraries = [f for f in os.listdir(LIB_PATH) if os.path.isfile(os.path.join(LIB_PATH, f))]
datas = []

# for r in resources:
#   src = ('%s\\%s' % ('resources', r), '.')
#   print('> Adding res', src)
#   datas.append(src)
# for r in libraries:
#   src = ('%s\\%s' % ('lib', r), '.')
#   print('> Adding lib', src)
#   datas.append(src)

a = Analysis(['client.py'],
             pathex=[BASE_PATH],
             binaries=[],
             datas=datas,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=config.DIST_FILE_NAME,
          debug=debug,
          strip=False,
          upx=True,
          console=debug,
          icon='controller2250.ico')
