#!/usr/bin/env python3

import os
import sys
from shutil import which
import hashlib
import urllib.parse
import glob
import importlib

from PyQt5.QtGui import (QImageReader,QPen,QColor,QPainter,QImageWriter)

from cfg import BORDER_COLOR_R, BORDER_COLOR_G, BORDER_COLOR_B, XDG_CACHE_LARGE

try:
    if not os.path.exists("sh_thumbnails"):
        os.mkdir("sh_thumbnails")
    if not os.path.exists("sh_thumbnails/large"):
        os.mkdir("sh_thumbnails/large")
except:
    print("Cannot create the sh_thumbnails folder or its subfolder. Exiting...")
    sys.exit()

if not os.path.exists("modules_thumb"):
    try:
        os.mkdir("modules_thumb")
    except:
        print("Cannot create the modules_thumb folder. Exiting...")
        sys.exit()

sys.path.append("modules_thumb")
mmod_bg = glob.glob("modules_thumb/*.py")

menu_bg_module = []
for el in mmod_bg:
    try:
        ee = importlib.import_module(os.path.basename(el)[:-3])
        menu_bg_module.append(ee)
    except ImportError as ioe:
        print("Error while importing the plugin {}".format(ioe))

def eencode(fpath):
    hmd5 = hashlib.md5(bytes("file://"+urllib.parse.quote(fpath, safe='/', encoding=None, errors=None),"utf-8")).hexdigest()
    return hmd5

def check_mtime(fpath):
    omtime = 0
    fmtime = int(os.path.getmtime(fpath))
    hmd5 = eencode(fpath)
    tpath = XDG_CACHE_LARGE+hmd5+".png"
    if os.path.isfile(tpath):
        ireader = QImageReader(tpath, b'png')
        omtime = ireader.text("ThumbMTime")
    if omtime == "":
        omtime = 0
    return [fmtime, omtime]

def createimagethumb(fpath, el):
    md5=eencode(fpath)
    infile = os.path.basename(fpath)
    uuri = "file://"+urllib.parse.quote(fpath, safe='/', encoding=None, errors=None)
    fmtime = int(os.path.getmtime(fpath))
    try:

        image = el.picture_to_img(fpath)
        if image == "Null":
            return "Null"
        # draw a colored border around the image
        img_w = image.width()
        img_h = image.height()
        pen = QPen(QColor(BORDER_COLOR_R,BORDER_COLOR_G,BORDER_COLOR_B))
        pwidth = 2
        pen.setWidth(pwidth)
        painter = QPainter()
        painter.begin(image)
        painter.setPen(pen)
        painter.drawRect(pwidth-1,pwidth-1,img_w-pwidth,img_h-pwidth)
        painter.end()
        #
        writer = QImageWriter(XDG_CACHE_LARGE+md5+".png", b'png')
        writer.setText("ThumbURI", uuri)
        writer.setText("ThumbMTime", str(int(fmtime)))
        writer.setText("Software", "QT5")
        writer.write(image)
        return md5

    except Exception as E:
        return "Null"

def create_thumbnail(fpath, imime):

    path = fpath

    fmtime, omtime = check_mtime(path)
    md5 = None

    if int(fmtime) != int(omtime):

        if len(menu_bg_module) == 0:
            return "Null"
        
        for ii in range(len(menu_bg_module)):
            if imime in menu_bg_module[ii].list_mime:
                md5 = createimagethumb(path, menu_bg_module[ii])
                if md5 != "Null":
                    return str(md5)
            else:
                continue
        else:
            return "Null"
    else:
        return eencode(path)
