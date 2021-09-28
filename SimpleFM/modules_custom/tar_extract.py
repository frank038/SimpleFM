#!/usr/bin/env python3

"""
extract the content of the selected tar archive file
needs xz-utils to handle tar.xz archive format
format recognized: tar, tar.gz, tar.bzip2, tar.xz
"""
import os
import stat
from PyQt5.QtWidgets import (QDialog,QBoxLayout,QLabel,QPushButton,QApplication)
from PyQt5.QtGui import (QIcon,QFont)
from PyQt5.QtCore import (Qt, QFileInfo,QMimeDatabase)
import shutil
import subprocess

#  module_type: this appears in the menu
def mmodule_name():
    return "Extract tar here"

# 1 : one item selected - 2 : more than one item selected - 3 : one or more items selected- 4 on background - 5 always
# action type
def mmodule_type(mainLView):
    #
    if shutil.which("tar"):
        if mainLView.selection:
            index = mainLView.selection[0]
            path = mainLView.fileModel.fileInfo(index).absoluteFilePath()
            fileInfo = QFileInfo(path)
            imime = QMimeDatabase().mimeTypeForFile(path, QMimeDatabase.MatchDefault)
            #if imime.name() in ["application/x-compressed-tar","application/x-tar","application/x-bzip-compressed-tar","application/x-xz-compressed-tar","application/x-lzma-compressed-tar"]:
            if imime.name() in ["application/x-compressed-tar","application/x-tar","application/x-bzip-compressed-tar","application/x-xz-compressed-tar"]:
                return 1
    return 0
    
#
class ModuleCustom():
    def __init__(self, mainLView):
        index = mainLView.selection[0]
        path = mainLView.fileModel.fileInfo(index).absoluteFilePath()
        if os.access(path, os.R_OK):
            if stat.S_ISREG(os.stat(path).st_mode):
                if os.access(mainLView.lvDir, os.W_OK):
                    try:
                        fileInfo = QFileInfo(path)
                        imime = QMimeDatabase().mimeTypeForFile(path, QMimeDatabase.MatchDefault)
                        if imime.name() in ["application/x-compressed-tar","application/x-tar","application/x-bzip-compressed-tar"]:
                            #subprocess.Popen(['tar', '--backup=numbered', '-xf', "{}".format(path), '-C', "{}".format(os.path.dirname(path))])
                            ret = subprocess.check_output('tar --backup=numbered -xf "{}" -C "{}"'.format(path, os.path.dirname(path)), shell=True)
                            # ret == b'' if everything goes ok
                            if ret.decode() == "":
                                MyDialog("Info", "Done.")
                        #if imime.name() == "application/x-compressed-tar":
                        #    subprocess.Popen(['tar', '-zxf', "{}".format(path), '-C', "{}".format(os.path.dirname(path))])
                        #elif imime.name() == "application/x-tar":
                        #    subprocess.Popen(['tar', '-xf', "{}".format(path), '-C', "{}".format(os.path.dirname(path))])
                        #elif imime.name() == "application/x-bzip-compressed-tar":
                        #    subprocess.Popen(['tar', '-jxf', "{}".format(path), '-C', "{}".format(os.path.dirname(path))])
                        #elif imime.name() == "application/x-xz-compressed-tar":
                        #    subprocess.Popen(['tar', '-Jxf', "{}".format(path), '-C', "{}".format(os.path.dirname(path))])
                        else:
                            MyDialog("ERROR", "Issues while extracting the archive.")
                    except Exception as E:
                        MyDialog("ERROR", "Issues while extracting the archive:\n{}.".format(E))

                    
class MyDialog(QDialog):
    def __init__(self, *args, parent=None):
        super(MyDialog, self).__init__(parent)
        self.setWindowIcon(QIcon("icons/file-manager-red.svg"))
        self.setWindowTitle(args[0])
        self.resize(400,300)
        thefont = QFont()
        FONT_SIZE = 14
        thefont.setPointSize(FONT_SIZE)
        self.setFont(thefont)
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
