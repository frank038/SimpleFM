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
        index = mainLView.selection[0]
        path = mainLView.fileModel.fileInfo(index).absoluteFilePath()
        # test the archive for password
        # archivemount do not support passworded archives
        if shutil.which("7z"):
            ret = self.test_archive(path)
            if ret == 2:
                MyDialog("Info", "This archive is password-protected\nand cannot be mounted.")
                return
        #
        base_dest_dir = "/tmp/archivemount"
        try:
            if not os.path.exists(base_dest_dir):
                os.mkdir(base_dest_dir)
        except Exception as E:
            MyDialog("ERROR", "\n{}".format(str(E)))
        #
        self.fuse_mounted = os.path.join(base_dest_dir, "fuse_mounted")
        file_name = os.path.basename(path)
        mount_name = file_name
        #
        if os.access(path, os.R_OK):
            try:
                i = 1
                while os.path.exists(os.path.join(base_dest_dir, mount_name)):
                    mount_name = file_name+"_{}".format(i)
                    i += 1
                dest_dir = os.path.join(base_dest_dir, mount_name)
                os.mkdir(dest_dir)
                #
                ret = os.system("archivemount '{}' '{}'". format(path, dest_dir))
                if ret == 0:
                    # add a button
                    self.win = mainLView.window
                    self.media_btn = QPushButton(QIcon("icons/fuse-archive.png"),"")
                    if BUTTON_SIZE:
                        self.media_btn.setIconSize(QSize(BUTTON_SIZE, BUTTON_SIZE))
                    self.win.disk_box.addWidget(self.media_btn)
                    if mount_name == file_name:
                        self.media_btn.setToolTip(file_name)
                    else:
                        self.media_btn.setToolTip(file_name+" - ("+mount_name+")")
                    self.media_btn_menu = QMenu()
                    self.media_btn_menu.addAction("Open", lambda x=dest_dir: self.win.openDir(x, 1))
                    self.media_btn_menu.addAction("Umount", lambda x=dest_dir,y=self.media_btn: self.fuserumountf(x,y))
                    self.media_btn.setMenu(self.media_btn_menu)
                    # 
                    with open(self.fuse_mounted, "a") as ff:
                        ff.write("{}\n{}\n".format(file_name, mount_name))
                    #
                    MyDialog("Info", "{}\nmounted".format(file_name))
                else:
                    MyDialog("Info", "{}\nError: {}".format(file_name, ret))
            except Exception as E:
                MyDialog("ERROR", "Issues while opening the archive:\n{}\n{}".format(file_name, str(E)))
    
    # umount the mounted archive
    def fuserumountf(self, dest_dir, btn):
        ret = os.system("fusermount -u '{}'".format(dest_dir))
        if ret == 0:
            btn.deleteLater()
            try:
                os.rmdir(dest_dir)
                fuse_mounted_list = []
                with open(self.fuse_mounted, "r") as ff:
                    fuse_mounted_list = ff.readlines()
                #
                len_fuse_mounted_list = len(fuse_mounted_list)
                #
                for idx in range(len_fuse_mounted_list-1, -1, -2):
                    item_mount = fuse_mounted_list[idx]
                    item = fuse_mounted_list[idx-1]
                    if os.path.basename(dest_dir) == item_mount.strip("\n"):
                        del fuse_mounted_list[idx]
                        del fuse_mounted_list[idx-1]
                with open(self.fuse_mounted, "w") as ff:
                    for item in fuse_mounted_list:
                        ff.write(item)
            except Exception as E:
                MyDialog("Info", "Error while umount the folder\n{}\n{}".format(dest_dir, str(E)))
        else:
            MyDialog("Info", "Error while umount the folder\n{}\n{}".format(dest_dir, ret))

        
    # test the archive for password using 7z
    def test_archive(self, path):
        szdata = None
        try:
            szdata = subprocess.check_output('7z l -slt -bso0 -- "{}"'.format(path), shell=True)
        except:
            return 0
        #
        if szdata != None:
            szdata_decoded = szdata.decode()
            ddata = szdata_decoded.splitlines()
            if "Encrypted = +" in ddata:
                return 2
            else:
                return 1   


class MyDialog(QDialog):
    def __init__(self, *args, parent=None):
        super(MyDialog, self).__init__(parent)
        self.setWindowIcon(QIcon("icons/file-manager-red.svg"))
        self.setWindowTitle(args[0])
        self.resize(500,300)
        # main box
        mbox = QBoxLayout(QBoxLayout.TopToBottom)
        mbox.setContentsMargins(5,5,5,5)
        self.setLayout(mbox)
        #
        label = QLabel(args[1])
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        mbox.addWidget(label)
        #
        button_ok = QPushButton("     Ok     ")
        mbox.addWidget(button_ok)
        #
        button_ok.clicked.connect(self.close)
        self.exec_()
