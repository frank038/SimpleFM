#!/usr/bin/env python3
"""
calculate the checksum of the selected item
"""
import os
import stat
from PyQt5.QtWidgets import (QDialog,QGridLayout,QLabel,QPushButton,QComboBox,QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QPalette,QColor,QIcon,QFont)
import subprocess
import shutil

# action name: this appears in the menu
def mmodule_name():
    return "Checksum"

# 1 : one item selected - 2 : more than one item selected - 3 : one or more items selected- 4 on background - 5 always
# action type
def mmodule_type(mainLView):
    return 1

class checkSum(QDialog):
    def __init__(self, path, parent=None):
        super(checkSum, self).__init__(parent)
        self.setWindowIcon(QIcon("icons/file-manager-red.svg"))
        self.setWindowTitle("Checksum")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(600,300)
        self.path = path
        #thefont = QFont()
        #FONT_SIZE = 14
        #thefont.setPointSize(FONT_SIZE)
        #self.setFont(thefont)
        #
        chks_list = ["MD5", "SHA256", "SHA1"]
        self.chks_exec = ["md5sum", "sha256sum", "sha1sum"]
        #
        grid = QGridLayout()
        grid.setContentsMargins(5,5,5,5)
        #
        label = QLabel("Type")
        #
        self.cb = QComboBox()
        self.cb.addItems(chks_list)
        #
        button1 = QPushButton("Calculate")
        button1.clicked.connect(self.fcalculate)
        #
        self.le1 = QLineEdit()
        #
        self.le2 = QLineEdit()
        #
        button2 = QPushButton("Check")
        button2.clicked.connect(self.fverify)
        #
        button_ok = QPushButton("     Exit     ")
        grid.addWidget(label, 0, 0, 1, 1, Qt.AlignCenter)
        grid.addWidget(self.cb, 0, 1, 1, 1, Qt.AlignCenter)
        grid.addWidget(button1, 0, 2, 1, 1, Qt.AlignCenter)
        grid.addWidget(self.le1, 1, 0, 1, 3)
        grid.addWidget(self.le2, 2, 0, 1, 3)
        grid.addWidget(button2, 3, 0, 1, 3)
        grid.addWidget(button_ok, 5, 0, 1, 3)
        self.setLayout(grid)
        button_ok.clicked.connect(self.close)
        self.exec_()

    #
    def fcalculate(self):
        index = self.cb.currentIndex()
        command = self.chks_exec[index]
        if shutil.which(command):
            checksum = subprocess.check_output([command, self.path], universal_newlines=True)
            self.le1.setText(checksum.split(" ")[0])

    def fverify(self):
        data1 = self.le1.text()
        data2 = self.le2.text()
        if data1 and data2:
            if data1 == data2:
                editor = self.le2
                palette = editor.palette()
                palette.setColor(QPalette.Active, QPalette.Text, QColor(0, 155, 0))
                editor.setPalette(palette)
            else:
                editor = self.le2
                palette = editor.palette()
                palette.setColor(QPalette.Active, QPalette.Text, QColor(190, 0, 0))
                editor.setPalette(palette)
                

class ModuleCustom():
    
    def __init__(self, mainLView):
        index = mainLView.selection[0]
        path = mainLView.fileModel.fileInfo(index).absoluteFilePath()
        if os.access(path, os.R_OK):
            if stat.S_ISREG(os.stat(path).st_mode):
                cs = checkSum(path)
