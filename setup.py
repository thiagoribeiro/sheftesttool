# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable

# Process the includes, excludes and packages first

includes = ['numpy', 'numpy.core.multiarray']
#excludes = []
packages = []

setup(

    version = "1.0",
    description = "Shef Test Tool",
    author = "Censanet",
    name = "Shef Test Tool Censanet",

    options = {"build_exe": {
                             "packages": packages,
			     "includes": includes
                             }
               },

    executables = [Executable("shef.py", base='Win32GUI', icon = 'img/shef.ico', path = 'C:\Projetos\SHEF', compress = True)]
    )