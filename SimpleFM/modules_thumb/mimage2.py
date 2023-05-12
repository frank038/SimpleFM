#!/usr/bin/env python3
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt

import subprocess

# imagemagick required

list_mime = ['image/webp', 'image/wmf', 'image/x-tga', 'image/avif']

def picture_to_img(fpath):
    
    try:
        data = subprocess.check_output(["/usr/bin/convert", "-thumbnail", "256", fpath, "JPEG:-"])
        img = QImage.fromData(data)
        
    except:
        return "Null"
    
    if not img.isNull():
        
        img_scaled = img #.scaled(256, 256, Qt.KeepAspectRatio, Qt.FastTransformation)
        
        return img_scaled
    else:
        return "Null"
