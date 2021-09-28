#!/usr/bin/env python3
"""
extract the content of the selected archive
"""
import os
import stat
from PyQt5.QtWidgets import (QDialog,QBoxLayout,QLabel,QPushButton,QLineEdit,QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QIcon,QFontMetrics,QFont)
import subprocess
import shutil

#  module_type: this appears in the menu
def mmodule_name():
    return "Extract here"

# 1 : one item selected - 2 : more than one item selected - 3 : one or more items selected- 4 on background - 5 always
# action type
def mmodule_type(mainLView):
    command = "7z"
    if shutil.which(command):
        return 1
    else:
        return 0


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


class passWord(QDialog):
    def __init__(self, path, parent=None):
        super(passWord, self).__init__(parent)
        self.setWindowIcon(QIcon("icons/file-manager-red.svg"))
        self.setWindowTitle("7z extractor")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(600,100)
        #
        self.path = path
        # main box
        mbox = QBoxLayout(QBoxLayout.TopToBottom)
        mbox.setContentsMargins(5,5,5,5)
        # label
        self.label = QLabel("Enter The Password:")
        mbox.addWidget(self.label)
        # lineedit
        self.le1 = QLineEdit()
        mbox.addWidget(self.le1)
        ##
        button_box = QBoxLayout(QBoxLayout.LeftToRight)
        button_box.setContentsMargins(0,0,0,0)
        mbox.addLayout(button_box)
        #
        button_ok = QPushButton("     Extract     ")
        button_box.addWidget(button_ok)
        #
        button_close = QPushButton("     Close     ")
        button_box.addWidget(button_close)
        #
        self.setLayout(mbox)
        button_ok.clicked.connect(self.getpswd)
        button_close.clicked.connect(self.close)
        #
        self.arpass = ""
        #
        self.exec_()
    
    def getpswd(self):
        
        passwd = self.le1.text()
        
        try:
            ptest = subprocess.check_output('7z t -p{} -bso0 -- "{}"'.format(passwd, self.path), shell=True)
            
            if ptest.decode() == "":
                
                self.arpass = passwd
                self.close()
        except:
            self.label.setText("Wrong Password:")
            self.le1.setText("")
       

class ModuleCustom():
    
    def __init__(self, mainLView):
        index = mainLView.selection[0]
        path = mainLView.fileModel.fileInfo(index).absoluteFilePath()
        
        if os.access(path, os.R_OK):
            
            if stat.S_ISREG(os.stat(path).st_mode):
                
                if os.access(mainLView.lvDir, os.W_OK):
                    
                    ret = self.test_archive(path)
                    
                    if ret == 1:
                        try:
                            subprocess.Popen(['7z', 'x', "-o{}".format(os.path.dirname(path)), '-y', '-aou', '--', path])
                            
                            MyDialog("Info", "Archive extracted.")
                        except:
                            MyDialog("ERROR", "Issues while extracting the archive.")
                    
                    elif ret == 2:
                        pret = passWord(path).arpass
                        
                        try:
                            subprocess.Popen(['7z', 'x', '-p{}'.format(pret), '-o{}'.format(os.path.dirname(path)), '-y', '-aou', '--', path])
                            MyDialog("Info", "Archive extracted.")
                        except:
                            MyDialog("ERROR", "Issues while extracting the archive.")
                    
                    elif ret == 0:
                        MyDialog("ERROR", "Issues while checking the archive.")
    
    def test_archive(self, path):
        
        szdata = None
        try:
            szdata = subprocess.check_output('7z l -slt -bso0 -- "{}"'.format(path), shell=True)
        except:
            return 0
        
        if szdata != None:
            szdata_decoded = szdata.decode()
            ddata = szdata_decoded.splitlines()
            if "Encrypted = +" in ddata:
                return 2
            else:
                return 1
