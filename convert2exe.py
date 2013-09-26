#coding=utf-8
'''
Created on 2013年9月22日

@author: hongkangzy
'''
from distutils.core import setup
import py2exe

setup(
      options = {  
      "py2exe": {  
        "dll_excludes": ["MSVCP90.dll"],  
      }  
    },windows=[{"script": "main.py"}])

