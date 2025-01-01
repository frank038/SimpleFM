#!/usr/bin/env python3
"""
extract the content of the selected archive
"""
import os
import stat
from PyQt5.QtWidgets import (QDialog,QBoxLayout,QLabel,QPushButton,QLineEdit,QApplication)
from PyQt5.QtCore import (Qt,QFileInfo,QMimeDatabase,QTimer)
from PyQt5.QtGui import (QIcon,QFontMetrics,QFont)
import subprocess
import shutil

#  module_type: this appears in the menu
def mmodule_name():
    return "Extract here"

# 1 : one item selected - 2 : more than one item selected - 3 : one or more items selected- 4 on background - 5 always
# action type
def mmodule_type(mainLView):
    # mimetype not handled by this module
    mime_discharged = ["application/x-sharedlib","application/x-cd-image","application/pdf",
                       "application/x-mozilla-bookmarks","application/json"]
    command = "7z"
    if shutil.which(command):
        if mainLView.selection:
            index = mainLView.selection[0]
            path = mainLView.fileModel.fileInfo(index).absoluteFilePath()
            if os.path.islink(path):
                return 0
            fileInfo = QFileInfo(path)
            imime = QMimeDatabase().mimeTypeForFile(path, QMimeDatabase.MatchDefault)
            imime_name = imime.name()
            if "application" in imime_name:
                if imime_name not in mime_discharged:
                    return 1
    return 0


class MyDialog(QDialog):
    def __init__(self, *args, parent=None):
        super(MyDialog, self).__init__(parent)
        self.setWindowIcon(QIcon("icons/file-manager-red.svg"))
        self.setWindowTitle(args[0])
        # self.resize(400,300)
        # main box
        mbox = QBoxLayout(QBoxLayout.TopToBottom)
        mbox.setContentsMargins(5,5,5,5)
        self.setLayout(mbox)
        #
        label = QLabel(args[1])
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        mbox.addWidget(label)
        #
        button_ok = QPushButton("   Close   ")
        mbox.addWidget(button_ok)
        #
        button_ok.clicked.connect(self.close)
        self.exec_()


class MyDialogExtract(QDialog):
    def __init__(self, *args, parent=None):
        super(MyDialogExtract, self).__init__(parent)
        self.setWindowIcon(QIcon("icons/file-manager-red.svg"))
        self.setWindowTitle(args[0])
        # self.resize(400,300)
        # main box
        mbox = QBoxLayout(QBoxLayout.TopToBottom)
        mbox.setContentsMargins(5,5,5,5)
        self.setLayout(mbox)
        #
        label_text = ""
        self.rret = args[1]
        self.pret = args[2]
        self.ppath = args[3]
        if self.rret == "1" or self.rret == "2":
            label_text = "Extracting..."
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        mbox.addWidget(self.label)
        #
        self.button_ok = QPushButton("   Close   ")
        mbox.addWidget(self.button_ok)
        #
        self.button_ok.clicked.connect(self.close)
        #
        self.timer=QTimer()
        self.timer.timeout.connect(self.startTime)
        self.timer.start(1000)
        self.timer_count = 0
        #
        self.exec_()
        
    def closeEvent(self, event):
        if self.timer_count == -1:
            super(MyDialogExtract, self).closeEvent(event)
        else:
            event.ignore()
        
    def startTime(self):
        self.timer_count += 1
        if self.timer_count == 6:
            self.timer_count = -1
            self.timer.stop()
            # # close this dialog
            # self.done(1)
        #
        if self.isVisible():
            if self.rret == "1":
                try:
                    ret = subprocess.check_output('7z x "-o{}" -y -aou -- "{}"'.format(os.path.dirname(self.ppath), self.ppath), shell=True)
                    if "Everything is Ok" in ret.decode():
                        self.label.setText("Archive extracted.")
                    else:
                        self.label.setText("Issues while extracting the archive.")
                except Exception as E:
                    self.label.setText("Issues while extracting the archive:\n{}.".format(E))
            elif self.rret == "2":
                try:
                    ret = subprocess.check_output('7z x "-p{}" "-o{}" -y -aou -- "{}"'.format(self.pret, os.path.dirname(self.ppath), self.ppath), shell=True)
                    if "Everything is Ok" in ret.decode():
                        self.label.setText("Archive extracted.")
                    else:
                        self.label.setText("Issues while extracting the archive.")
                except Exception as E:
                    self.label.setText("Issues while extracting the archive:\n{}.".format(E))
            #
            self.adjustSize()
            self.updateGeometry()
            self.timer_count = -1
            self.timer.stop()

class passWord(QDialog):
    def __init__(self, path, parent=None):
        super(passWord, self).__init__(parent)
        self.setWindowIcon(QIcon("icons/file-manager-red.svg"))
        self.setWindowTitle("7z extractor")
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # self.resize(600,100)
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
                    #
                    if ret == 0:
                        MyDialog("ERROR", "Issues while checking the archive.")
                    else:
                        pret = ""
                        if ret == 2:
                            pret = passWord(path).arpass
                            if pret == "":
                                return
                        #
                        MyDialogExtract("Info", str(ret), pret, path)
                    
    
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
