#!/usr/bin/env python3

"""
open a supported archive with archivemount
"""
import os
import stat
from PyQt5.QtWidgets import (QDialog,QBoxLayout,QLabel,QPushButton,QApplication,QMenu)
from PyQt5.QtGui import (QIcon,QFont)
from PyQt5.QtCore import (Qt,QFileInfo,QMimeDatabase,QSize)
import shutil
import subprocess
from cfg import BUTTON_SIZE

#  module_type: this appears in the menu
def mmodule_name():
    return "Open archive"

# 1 : one item selected - 2 : more than one item selected - 3 : one or more items selected- 4 on background - 5 always
# action type
def mmodule_type(mainLView):
    #
    if shutil.which("archivemount"):
        if mainLView.selection:
            index = mainLView.selection[0]
            path = mainLView.fileModel.fileInfo(index).absoluteFilePath()
            fileInfo = QFileInfo(path)
            imime = QMimeDatabase().mimeTypeForFile(path, QMimeDatabase.MatchDefault)
            if imime.name() in ["application/x-cd-image","application/zip","application/x-compressed-tar","application/x-tar","application/x-bzip-compressed-tar","application/x-xz-compressed-tar"]:
                return 1
    return 0
    
#
class ModuleCustom():
    def __init__(self, mainLView):
        udate = subprocess.check_output(["date","+%s"], universal_newlines=True, shell=False).strip("\n")
        dest_dir = os.path.join("/tmp/archivemount", udate)
        index = mainLView.selection[0]
        path = mainLView.fileModel.fileInfo(index).absoluteFilePath()
        if os.access(path, os.R_OK):
            try:
                if not os.path.exists("/tmp/archivemount"):
                    os.mkdir("/tmp/archivemount")
                if not os.path.exists(dest_dir):
                    os.mkdir(dest_dir)
                #
                ret = os.system("archivemount {} {}". format(path, dest_dir))
                if ret == 0:
                    # add a button
                    self.win = mainLView.window
                    self.media_btn = QPushButton(QIcon("icons/fuse-archive.png"),"")
                    self.media_btn.setIconSize(QSize(BUTTON_SIZE, BUTTON_SIZE))
                    self.win.disk_box.addWidget(self.media_btn)
                    self.media_btn.setToolTip(os.path.basename(path))
                    self.media_btn_menu = QMenu()
                    self.media_btn_menu.addAction("Open", lambda:self.win.openDir(dest_dir, 1))
                    self.media_btn_menu.addAction("Umount", lambda:self.fuserumountf(dest_dir))
                    self.media_btn.setMenu(self.media_btn_menu)
                    #
                    MyDialog("Info", "{}\nmounted.".format(os.path.basename(path)))
                else:
                    MyDialog("Info", "{}\nError: {}".format(os.path.basename(path), ret))
            except Exception as E:
                MyDialog("ERROR", "Issues while opening the archive:\n{}\n{}.".format(os.path.basename(path), str(E)))

    # umount the mounted archive
    def fuserumountf(self, mpath):
        ret = os.system("fusermount -u {}".format(mpath))
        if ret == 0:
            self.media_btn.deleteLater()
            
    
class MyDialog(QDialog):
    def __init__(self, *args, parent=None):
        super(MyDialog, self).__init__(parent)
        self.setWindowIcon(QIcon("icons/file-manager-red.svg"))
        self.setWindowTitle(args[0])
        self.resize(400,300)
        # main box
        mbox = QBoxLayout(QBoxLayout.TopToBottom)
        mbox.setContentsMargins(5,5,5,5)
        self.setLayout(mbox)
        #
        label = QLabel(args[1])
        label.setWordWrap(True)
        mbox.addWidget(label)
        #
        button_ok = QPushButton("     Ok     ")
        mbox.addWidget(button_ok)
        #
        button_ok.clicked.connect(self.close)
        self.exec_()