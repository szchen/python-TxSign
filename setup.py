# -*- coding: UTF-8 -*-
from distutils.core import setup
import py2exe
import sys


sys.argv.append('py2exe')
 
py2exe_options = {
        "includes": ["sip"],
        "dll_excludes": ["MSVCR90.dll",'Microsoft.VC90.CRT'],
        "compressed": 1,
        "optimize": 2,
        "ascii": 0,
        "bundle_files": 1,
        }
 
setup(
      name = 'tapd helper',
      version = '1.0',
      windows = [{'script' : 'main.py',"icon_resources":[(1,'t1.ico')]}],

      zipfile = None,
      options = {'py2exe': py2exe_options}
      
      )
