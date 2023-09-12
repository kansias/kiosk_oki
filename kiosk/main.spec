# -*- mode: python ; coding: utf-8 -*-

# from math import e
#import time
#import cv2
#import numpy as np
#import pyaudio
#import wave
#import openai
#from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
#from PySide2.QtGui import QImage, QPixmap
#from PySide2.QtWidgets import QTextEdit
#from PySide2.QtCore import Qt
#from PySide2.QtCore import QTimer, Signal
#from ui import QThread, Ui_MainWindow
#import serial
#import serial.tools.list_ports
#from konlpy.tag import Okt
#from openai.api_resources import file

block_cipher = None


a = Analysis(
    ['main.py'], 
    pathex=[], 
    binaries=[],
    datas=[ ('./img/*', './img'),
            ('./haarcascade_frontalface_default.xml', '.'),
            ('../.env', '..')
     ],
    hiddenimports=[
        'pyaudio',
        'wave',
        'cv2',
        'numpy',
        'openai',
        'serial',
        'serial.tools.list_ports',
        'konlpy',
        'konlpy.*',
        'konlpy.tag',
        'konlpy.tag._okt'
        'gtts',
        'pygame',

    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes= [],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='오키',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
