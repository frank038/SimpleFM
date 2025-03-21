#!/usr/bin/env python3

from PyQt5.QtCore import (Qt,)
from PyQt5.QtWidgets import (QFileDialog, qApp, QBoxLayout, QPushButton, QApplication, QDialog, QMessageBox, QLineEdit, QWidget, QTreeWidget, QTreeWidgetItem)
from PyQt5.QtGui import (QIcon,)

import sys
import os
import shutil
import subprocess
#
from Utility import pop_menu

##########################

class listMenu(QWidget):
    
    def __init__(self, infile=None):
        super().__init__()
        self.infile = infile
        self.setWindowIcon(QIcon("icons/file-manager-red.svg"))
        self.setWindowTitle("Menu")
        self.setWindowModality(Qt.ApplicationModal)
        # self.resize(300, 600)
        #
        vbox = QBoxLayout(QBoxLayout.TopToBottom)
        vbox.setContentsMargins(5,5,5,5)
        self.setLayout(vbox)
        # treewidget
        self.TWD = QTreeWidget()
        self.TWD.setHeaderLabels(["Applications"])
        self.TWD.setAlternatingRowColors(False)
        self.TWD.itemClicked.connect(self.fitem)
        vbox.addWidget(self.TWD)
        # entry
        hbox2 = QBoxLayout(QBoxLayout.LeftToRight)
        vbox.addLayout(hbox2)
        self.LE = QLineEdit()
        #self.LE.setReadOnly(True)
        hbox2.addWidget(self.LE)
        # select program
        self.buttonOF = QPushButton("Select...")
        self.buttonOF.clicked.connect(self.fOpenWith)
        hbox2.addWidget(self.buttonOF)
        ### buttons
        hbox = QBoxLayout(QBoxLayout.LeftToRight)
        vbox.addLayout(hbox)
        button1 = QPushButton("Ok")
        hbox.addWidget(button1)
        button1.clicked.connect(self.fexecute)
        #
        button2 = QPushButton("Cancel")
        hbox.addWidget(button2)
        button2.clicked.connect(self.fcancel)
        #### the menu
        # get the menu
        amenu = pop_menu.getMenu()
        self.menu = amenu.retList()
        #
        # populate the categories
        self.fpopMenu()
        #
        self.Value = None
    
    #
    def fOpenWith(self):
        ret = QFileDialog.getOpenFileName(parent=None, caption="Select...", directory="/")
        if ret[0]:
            # set the text
            self.LE.setText(os.path.basename(ret[0]))
            # set the variable
            self.Value = ret[0]
    
    # create a menu of installed applications
    def fpopMenu(self):
        categories_found = []
        # [fname, fcategory or "Other", fexec, fpath, fmimetypes, ftryexec]
        for el in self.menu:
            categ = el[1]
            if not categ in categories_found:
                categories_found.append(categ)
                # add the category
                tl = QTreeWidgetItem([categ])
                self.TWD.addTopLevelItem(tl)
            #
            # populate the categories
            # find the index of the category in the treeview
            witem = self.TWD.findItems(categ, Qt.MatchExactly, 0)[0]
            idx = self.TWD.indexOfTopLevelItem(witem)
            # add the item
            tw_child = QTreeWidgetItem([el[0], el[2], el[5]])
            witem.addChild(tw_child)
        #
        del self.menu
        self.TWD.setSortingEnabled(True)
        self.TWD.sortByColumn(0, 0)

    # an item in the treewidget is clicked
    def fitem(self, item, col):
        self.LE.setText("")
        # skip categories
        if item.childCount() > 0:
            return
        # get the executable
        appExec = item.text(1)
        tryExec = item.text(2)
        _prog = appExec
        if tryExec:
            _prog = tryExec
        # if the executable exists
        # if shutil.which(appExec):
        if shutil.which(_prog):
            # set the name of the program in the line edit widget
            self.LE.setText(item.text(0))
            # self.LE.setEnabled(False)
            # set the variable
            self.Value = appExec
        #
        else:
            # the program exists but cannot be executed
            # if os.path.exists(appExec):
            if os.path.exists(_prog):
                self.fdialog("The program\n"+appExec+"\ncannot be executed.")
            # the program doesn't exist
            else:
                # self.fdialog("The program\n"+appExec+"\ncannot be found.")
                # trying to remove options from the command line of some apps, e.g. libreoffice
                comm_line = []
                comm_line = appExec.split(" ")
                if comm_line:
                    for ff in comm_line:
                        if shutil.which(ff):
                            self.Value = appExec
                            self.LE.setText(appExec)
                        break
                    return
                self.fdialog("The program\n"+appExec+"\ncannot be found.")
    
    # execute the program with the file as argument
    def fexecute(self):
        # program choosen from list or from dialog
        if self.Value:
            #if shutil.which(self.Value):
            try:
                # subprocess.Popen([self.Value, self.infile])
                _cmd = "{0} '{1}'".format(self.Value,self.infile)
                subprocess.Popen(_cmd, shell=True)
            except Exception as E:
                self.fdialog(str(E))
            # else:
                # self.fdialog("The program\n"+self.Value+"\ncannot be found.")
            self.close()
        # program written in the line edit widget directly
        else:
            if self.LE.text():
                if shutil.which(self.LE.text()):
                    try:
                        subprocess.Popen([self.LE.text(), self.infile])
                    except Exception as E:
                        self.fdialog(str(E))
                else:
                    self.fdialog("The program\n"+self.LE.text()+"\ncannot be found.")
                self.close()
    
    def fcancel(self):
        self.close()

    # dialog
    def fdialog(self, msg):
        dialog = QMessageBox()
        dialog.setWindowTitle("Info")
        dialog.setModal(True)
        dialog.setWindowIcon(QIcon("icons/file-manager-red.svg"))
        dialog.setText(msg)
        dialog.exec()

###################
