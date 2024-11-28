#!/usr/bin/env python3

from PyQt5.QtCore import (QMargins,QEvent,QObject,Qt)
from PyQt5.QtWidgets import (QDialog, QListWidgetItem, QListWidget, QTreeWidget, QTreeWidgetItem, qApp,QBoxLayout,QLabel,QPushButton,QApplication,QDialog,QMessageBox,QLineEdit,QTabWidget,QWidget,QListView)
from PyQt5.QtGui import (QIcon,QPixmap,QFont)
from xdg import DesktopEntry
import sys
import os

#
try:
    from Utility import pop_menu
except:
    import pop_menu

WINW = 800
WINH = 600

# where to look for the *.desktop files
xdgDataDirs = ['/usr/local/share', '/usr/share', os.path.expanduser('~')+"/.local/share"]
# consinstency
for ppath in xdgDataDirs[:]:
    if not os.path.exists(os.path.join(ppath, "applications")):
        xdgDataDirs.remove(ppath)

# full path of the mimeapps.list file
from cfg import USER_MIMEAPPSLIST
if USER_MIMEAPPSLIST:
    MIMEAPPSLIST = os.path.expanduser('~')+"/.config/mimeapps.list"
else:
    MIMEAPPSLIST = "mimeapps.list"

# create the menu: name - categoty - exec - desktop file with full path - list of mimetypes
THE_MENU = pop_menu.getMenu().retList()

##########################

# main class
class MainWin(QDialog):
    
    def __init__(self, mimetype, parent):
        super(QDialog, self).__init__(parent)
        #
        self.setWindowModality(Qt.ApplicationModal)
        self.mimetype = mimetype
        # self.resize(int(WINW), int(WINH))
        self.setWindowTitle("Manage the mimetype")
        self.setWindowIcon(QIcon("icons/file-manager-red.svg"))
        # top container
        self.obox = QBoxLayout(QBoxLayout.LeftToRight)
        self.obox.setContentsMargins(QMargins(2,2,2,2))
        self.setLayout(self.obox)
        # the container
        self.vbox2 = QBoxLayout(QBoxLayout.TopToBottom)
        self.obox.addLayout(self.vbox2)
        ############ widgets in the container
        self.extLabel1 = QLabel("Mimetype")
        self.vbox2.addWidget(self.extLabel1)
        self.extLabel2 = QLineEdit()
        self.extLabel2.setReadOnly(True)
        self.vbox2.addWidget(self.extLabel2)
        # top label
        self.execLabel = QLabel("Executable(s)")
        self.vbox2.addWidget(self.execLabel)
        #### List
        self.plist = QTreeWidget()
        self.plist.setColumnCount(3)
        self.plist.header().hide()
        self.plist.setColumnHidden(2, True)
        self.vbox2.addWidget(self.plist)
        #### buttons
        self.buttonBox = QBoxLayout(QBoxLayout.LeftToRight)
        #
        self.b1 = QPushButton("Make default")
        self.b1.clicked.connect(self.make_default)
        self.buttonBox.addWidget(self.b1)
        #
        self.b2 = QPushButton("Add")
        self.b2.clicked.connect(self.add_association)
        self.buttonBox.addWidget(self.b2)
        #
        self.b3 = QPushButton("Remove")
        self.b3.clicked.connect(self.remove_association)
        self.buttonBox.addWidget(self.b3)
        #
        self.help = QPushButton("Help")
        self.help.clicked.connect(lambda:commDialog("help", 5))
        self.buttonBox.addWidget(self.help)
        #
        self.vbox2.addLayout(self.buttonBox)
        # the mimetype of the item
        self.imime = mimetype
        ### applications added or removed or default in mimeapps.list
        self.lA = []
        self.lR = []
        self.lD = []
        self.fillLARD()
        ### close application button
        self.closeBtn = QPushButton("Close")
        self.vbox2.addWidget(self.closeBtn)
        self.closeBtn.clicked.connect(self.fcancel)
        # populate
        self.fitem_first()
        #
        self.Value = None
    
    def getValue(self):
        return self.Value
    
    def fcancel(self):
        self.accept()
        self.close()
        
    # 1
    # function that found the mimetypes added, removed and default in the mimeapps.list
    def fillLARD(self):
        # mimeapps.list can have up to three not mandatory sectors
        #intest = ["[Added Associations]","[Removed Associations]","[Default Applications]"]
        # lists of mimetypes added or removed
        lista = []
        # reset
        lA1 = []
        lR1 = []
        lD1 = []
        # create an empty mimeapps.list if it doesnt exist
        if not os.path.exists(MIMEAPPSLIST):
            lD1.append("[Default Applications]\n")
            lD1.append("\n")
            lA1.append("[Added Associations]\n")
            lA1.append("\n")
            lR1.append("[Removed Associations]\n")
            lR1.append("\n")
            self.lA = lA1
            self.lR = lR1
            self.lD = lD1
            #
            return
        #
        # all the file in lista: one row one item added to lista
        with open(MIMEAPPSLIST, "r") as f:
            lista = f.readlines()
        # marker
        x = ""
        for el in lista:
            if el == "[Added Associations]\n":
                x = "A"
            elif el == "[Removed Associations]\n":
                x = "R"
            elif el == "[Default Applications]\n":
                x = "D"
            #
            if el:
                if el == "\n":
                    continue
                if x == "A":
                    lA1.append(el)
                elif x == "R":
                    lR1.append(el)
                elif x == "D":
                    lD1.append(el) 
        # consistency
        if lD1 == []:
            lD1.append("[Default Applications]\n")
            lD1.append("\n")
        if lA1 == []:
            lA1.append("[Added Associations]\n")
            lA1.append("\n")
        if lR1 == []:
            lR1.append("[Removed Associations]\n")
            lR1.append("\n")
        #
        self.lA = lA1
        self.lR = lR1
        self.lD = lD1
    
    # 2
    # populate
    def fitem_first(self):
        self.extLabel2.setText(self.mimetype)
        self.fitem2(self.mimetype)
    
    # # populate
    # def fitem(self, item, col):
        # ##### find the index of the item in the category
        # p = item.parent()
        # if p:
            # # clear the plist
            # self.plist.clear()
            # self.extLabel2.setText(item.text(1))
            # self.imime = p.text(0)+"/"+item.text(0)
            # self.fitem2(self.imime)
    
    # 3
    def fitem2(self, imime):
        # clear the plist
        self.plist.clear()
        # find the default or removed or default applications of the mimetype
        lAdded,lRemoved,lDefault = self.addMime(imime)
        #
        if lDefault:
            defApp = lDefault[0]
        else:
            defApp = "None"
        # desktop files found
        desktop_found = []
        # desktop files in HOME
        desk_home_dir = os.path.expanduser('~')+"/.local/share"+"/applications"
        apps_home_dir = os.listdir(desk_home_dir)
        # name - category - exec - desktop file with full path - mimetypes
        for el in THE_MENU:
            desk_dir = os.path.dirname(el[3])
            desk_name = os.path.basename(el[3])
            # search for the mimetype
            if imime in el[4]:
                # skip desktop files overrided in HOME
                if desk_dir != desk_home_dir:
                    if desk_name in apps_home_dir:
                        continue
                #
                if os.path.basename(el[3]) in lAdded:
                    if os.path.basename(el[3]) == defApp:
                        # code - exec - desktop file
                        item = QTreeWidgetItem(["+*", el[2], os.path.basename(el[3])])
                        desktop_found.append(os.path.basename(el[3]))
                    else:
                        item = QTreeWidgetItem(["+", el[2], os.path.basename(el[3])])
                        desktop_found.append(os.path.basename(el[3]))
                elif os.path.basename(el[3]) in lRemoved:
                    item = QTreeWidgetItem(["-", el[2], os.path.basename(el[3])])
                    desktop_found.append(os.path.basename(el[3]))
                else:
                    # it is the default application but it isnt in the lAdded list
                    if os.path.basename(el[3]) == defApp:
                        item = QTreeWidgetItem(["*", el[2], os.path.basename(el[3])])
                        desktop_found.append(os.path.basename(el[3]))
                    else:
                        # this is an application with a desktop file - it cannot be found in any lists
                        item = QTreeWidgetItem(["", el[2], os.path.basename(el[3])])
                        desktop_found.append(os.path.basename(el[3]))
                if item:
                    self.plist.addTopLevelItem(item)
        # find missing applications that can be found in mimeappes.list
        # added - search for other desktop files
        for el in lAdded:
            if el not in desktop_found:
                for elx in xdgDataDirs:
                    app_dir = os.path.join(elx, "applications")
                    for ellx in os.listdir(app_dir):
                        # skip desktop files in HOME
                        if ellx in apps_home_dir:
                            continue
                        if el == ellx:
                            desktop_found.append(os.path.basename(ellx))
                            entry = DesktopEntry.DesktopEntry(os.path.join(app_dir, el))
                            fexec = entry.getExec().split(" ")[0]
                            item = QTreeWidgetItem(["+", fexec, el])
                            self.plist.addTopLevelItem(item)
                            break
        # added - missing desktop files
        for el in lAdded:
            if el not in desktop_found:
                item = QTreeWidgetItem(["+?", el.split(".")[0], el])
                if item:
                    desktop_found.append(el)
                    self.plist.addTopLevelItem(item)
        # removed
        for el in lRemoved:
            if el not in desktop_found:
                item = QTreeWidgetItem(["-?", el.split(".")[0], el])
                if item:
                    desktop_found.append(el)
                    self.plist.addTopLevelItem(item)
        # the default application must have *
        # an added application that doesnt support the selected mimetype in
        # ... the desktop file have to be marked too
        witem = self.plist.findItems(defApp, Qt.MatchExactly, 2)
        if witem:
            witem_code = witem[0].text(0)
            if witem_code == "":
                witem[0].setText(0, "*")
            elif witem_code == "+":
                witem[0].setText(0, "+*")
        # resize the first column to content
        self.plist.resizeColumnToContents(0)
        
    # 4
    # find the default or removed or removed applications of the mimetype
    def addMime(self, imime):
        imime = imime+"="
        lAdded = []
        lRemoved = []
        lDefault = []
        for item in self.lA:
            if item[0:len(imime)] == imime:
                lAdded = item.strip(";\n").split("=")[1].split(";")
        for item in self.lD:
            if item[0:len(imime)] == imime:
                lDefault = item.strip(";\n").split("=")[1].split(";")
        for item in self.lR:
            if item[0:len(imime)] == imime:
                lRemoved = item.strip(";\n").split("=")[1].split(";")
        # consinstency: remove from the lRemoved list the items already in the lAdded or lDefault list
        for item in lRemoved[:]:
            if item in lAdded or item in lDefault:
                lRemoved.remove(item)
        #
        return lAdded,lRemoved,lDefault
    
    
    # make an application the default one for the selected mimetype
    def make_default(self):
        # selected item of plist
        itemSelected = self.plist.currentItem()
        if itemSelected:
            if itemSelected.text(0) in ["+*","*"]:
                commDialog("Already done.", 4)
                return
            if itemSelected.text(0) not in ["+*","*","+?","-?"]:
                dret = commDialog("Make default?", 3).getValue()
                # 2 means Execute
                if dret == 2:
                    # find the default or removed or default applications of the mimetype
                    lAdded,lRemoved,lDefault = self.addMime(self.imime)
                    # selected item of plist
                    # code - exec - desktop file
                    itemSelected = self.plist.currentItem()
                    item_desktop_file = itemSelected.text(2)
                    # remove the application from the removed associations if present
                    if item_desktop_file in lRemoved:
                        lRemoved.remove(item_desktop_file)
                    # make the Default Applications in the list
                    if item_desktop_file not in lDefault:
                        lDefault = [item_desktop_file]
                    #
                    ## update the mimeapps.list file
                    try:
                        ### removed
                        temp_lR = ["[Removed Associations]\n"]
                        for item in self.lR[1:]:
                            # remove the previous association
                            if item[0:len(self.imime)+1] == self.imime+"=":
                                self.lR.remove(item)
                        # add the new associations for the mimetype
                        if lRemoved:
                            tnew = self.imime+"="
                            for titem in lRemoved:
                                tnew += titem+";"
                            tnew += "\n"
                            temp_lR.append(tnew)
                        # add the other associations
                        for item in self.lR[1:]:
                            if item == "\n":
                                continue
                            temp_lR.append(item)
                        #
                        self.lR = temp_lR
                        #
                        ### default
                        temp_lD = ["[Default Applications]\n"]
                        for item in self.lD[1:]:
                            if item[0:len(self.imime)+1] == self.imime+"=":
                                self.lD.remove(item)
                        #
                        new_item = self.imime+"="+lDefault[0]+";\n"
                        temp_lD.append(new_item)
                        #
                        for item in self.lD[1:]:
                            if item == "\n":
                                continue
                            temp_lD.append(item)
                        #
                        self.lD = temp_lD
                        #
                        f = open(MIMEAPPSLIST, 'w')
                        for item in self.lD:
                            f.write(item)
                        for item in self.lA:
                            f.write(item)
                        for item in self.lR:
                            f.write(item)
                        f.close()
                    except Exception as E:
                        commDialog("Error:\n{}".format(str(E)), 5)
                    #
                    # rebuild the lists
                    self.fillLARD()
                    # reload treview
                    self.fitem2(self.mimetype)
                    #
                    self.Value = 1
    
    # 
    def remove_association(self):
        # confirmation dialog
        dret = commDialog("Confirm Delete?", 3).getValue()
        if dret == -1:
            return
        itemSelected = self.plist.currentItem()
        if itemSelected:
            # find the default or removed or default applications of the mimetype
            lAdded,lRemoved,lDefault = self.addMime(self.imime)
            item_desktop_file = itemSelected.text(2)
            # default application
            if itemSelected.text(0) in ["+*", "*"]:
                if item_desktop_file in lDefault:
                    lDefault.remove(item_desktop_file)
                    ret = self.update_mimeapps_list(lDefault, "D")
            # added and added orphan application
            elif itemSelected.text(0) in ["+", "+?"]:
                if item_desktop_file in lAdded:
                    lAdded.remove(item_desktop_file)
                    ret = self.update_mimeapps_list(lAdded, "A")
            # removed and removed orphan application
            elif itemSelected.text(0) in ["-", "-?"]:
                if item_desktop_file in lRemoved:
                    lRemoved.remove(item_desktop_file)
                    ret = self.update_mimeapps_list(lRemoved, "R")
        
    ###### update the mimeapps.list - self.remove_association()
    def update_mimeapps_list(self, llist, list_type):
        try:
            ### removed
            if list_type == "R":
                lRemoved = llist
                temp_lR = ["[Removed Associations]\n"]
                #
                for item in self.lR[1:]:
                    if item == "\n":
                        continue
                    # remove the old associations
                    if item[0:len(self.imime)+1] == self.imime+"=":
                        self.lR.remove(item)
                # add the new associations for the mimetype
                if lRemoved:
                    tnew = self.imime+"="
                    for titem in lRemoved:
                        tnew += titem+";"
                    tnew += "\n"
                    temp_lR.append(tnew)
                # add the other associations
                for item in self.lR[1:]:
                    if item == "\n":
                        continue
                    temp_lR.append(item)
                #
                self.lR = temp_lR
                #
            ### added
            elif list_type == "A":
                lAdded = llist
                temp_lA = ["[Added Associations]\n"]
                #
                for item in self.lA[1:]:
                    if item == "\n":
                        continue
                    if item[0:len(self.imime)+1] == self.imime+"=":
                        self.lA.remove(item)
                #
                if lAdded:
                    tnew = self.imime+"="
                    for titem in lAdded:
                        tnew += titem+";"
                    tnew += "\n"
                    temp_lA.append(tnew)
                #
                for item in self.lA[1:]:
                    if item == "\n":
                        continue
                    temp_lA.append(item)
                #
                self.lA = temp_lA
            ### default
            elif list_type == "D":
                lDefault = llist
                temp_lD = ["[Default Applications]\n"]
                for item in self.lD[1:]:
                    if item == "\n":
                        continue
                    if item[0:len(self.imime)+1] == self.imime+"=":
                        self.lD.remove(item)
                #
                for item in self.lD[1:]:
                    if item == "\n":
                        continue
                    temp_lD.append(item)
                #
                self.lD = temp_lD
            #
            f = open(MIMEAPPSLIST, 'w')
            for item in self.lD:
                f.write(item)
            for item in self.lA:
                f.write(item)
            for item in self.lR:
                f.write(item)
            f.close()
        except Exception as E:
            commDialog("Error:\n{}".format(str(E)), 5)
            ret = 0
        #
        # rebuild the lists
        self.fillLARD()
        # reload treview
        self.fitem2(self.mimetype)
        #
        self.Value = 1
        #
        ret = 1
    
    #
    def add_association(self):
        # whether a mimetype has been selected from the list
        if not self.imime:
            return
        # return [exec, desktop file] or -1
        ret = listMenu().getValue()
        if ret == -1:
            return
        desktop_file = os.path.basename(ret[1])
        # add the desktop file to the list
        lAdded,lRemoved,lDefault = self.addMime(self.imime)
        if desktop_file in lAdded:
            commDialog("Info: {} has already been added.".format(ret[0]), 4)
            return
        lAdded.append(desktop_file)
        ###### update the mimeapps.list
        try:
            temp_lA = ['[Added Associations]\n']
            for item in self.lA[1:]:
                if item == "\n":
                    continue
                if item[0:len(self.imime)+1] == self.imime+"=":
                    self.lA.remove(item)
            #
            if lAdded:
                tnew = self.imime+"="
                for titem in lAdded:
                    tnew += titem+";"
                tnew += "\n"
                temp_lA.append(tnew)
            #
            for item in self.lA[1:]:
                if item == "\n":
                    continue
                temp_lA.append(item)
            self.lA = temp_lA
            #
            f = open(MIMEAPPSLIST, 'w')
            for item in self.lD:
                f.write(item)
            for item in self.lA:
                f.write(item)
            for item in self.lR:
                f.write(item)
            f.close()
        except Exception as E:
            commDialog("Error:\n{}".format(str(E)), 5)
        #
        # rebuild the lists
        self.fillLARD()
        # reload treview
        self.fitem2(self.mimetype)
        #
        self.Value = 1
        
        
############ create a menu of installed applications
class listMenu(QDialog):
    def __init__(self, parent=None):
        super(listMenu, self).__init__(parent)
        #
        self.setWindowTitle("Menu")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon("icons/file-manager-red.svg"))
        self.resize(600, 600)
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
        # buttons
        hbox = QBoxLayout(QBoxLayout.LeftToRight)
        vbox.addLayout(hbox)
        #
        button1 = QPushButton("Ok")
        hbox.addWidget(button1)
        button1.clicked.connect(self.fexecute)
        #
        button2 = QPushButton("Cancel")
        hbox.addWidget(button2)
        button2.clicked.connect(self.fcancel)
        #### the menu
        ## populate the categories
        self.fpopMenu()
        # sort the view
        self.TWD.setSortingEnabled(True)
        self.TWD.sortByColumn(0, Qt.AscendingOrder)
        #
        self.Value = []
        self.exec_()

    # create a menu of installed applications
    def fpopMenu(self):
        # main categories
        Development = []
        Education = []
        Game = []
        Graphics = []
        Multimedia = []
        Network = []
        Office = []
        Settings = []
        System = []
        Utility = []
        Other = []
        #
        #for el in self.menu:
        for el in THE_MENU:
            cat = el[1]
            if cat == "Development":
                # name - category - exec - desktop file
                Development.append(["Development",el[0],el[2],el[3]])
            elif cat == "Education":
                Education.append(["Education",el[0],el[2],el[3]])
            elif cat == "Game":
                Game.append(["Game",el[0],el[2],el[3]])
            elif cat == "Graphics":
                Graphics.append(["Graphics",el[0],el[2],el[3]])
            elif cat == "Multimedia":
                Multimedia.append(["Multimedia",el[0],el[2],el[3]])
            elif cat == "Network":
                Network.append(["Network",el[0],el[2],el[3]])
            elif cat == "Office":
                Office.append(["Office",el[0],el[2],el[3]])
            elif cat == "Settings":
                Settings.append(["Settings",el[0],el[2],el[3]])
            elif cat == "System":
                System.append(["System",el[0],el[2],el[3]])
            elif cat == "Utility":
                Utility.append(["Utility",el[0],el[2],el[3]])
            else:
                Other.append(["Other",el[0],el[2],el[3]])
        #
        main_categories = ["Development","Education","Game",
                            "Graphics","Multimedia","Network",
                            "Office","Settings","System","Utility","Other"]
        for ccat in main_categories:
            tl = QTreeWidgetItem([ccat])
            self.TWD.addTopLevelItem(tl)
        #
        # populate the categories
        for ell in [Development,Education,Game,Graphics,Multimedia,Network,Office,Settings,System,Utility,Other]:
            if ell:
                # el: category - name - exec - desktop file
                for el in ell:
                    # find the index of the category in the treeview
                    witem = self.TWD.findItems(el[0], Qt.MatchExactly, 0)[0]
                    idx = self.TWD.indexOfTopLevelItem(witem)
                    # add the item: name - exec - desktop file
                    tw_child = QTreeWidgetItem([el[1], el[2], el[3]])
                    witem.addChild(tw_child)

    # an item in the treewidget is clicked
    def fitem(self, item, col):
        # exec - desktop file
        self.Value = [item.text(1), item.text(2)]
    
    def getValue(self):
        return self.Value
    
    def fexecute(self):
        self.close()
    
    def fcancel(self):
        self.Value = -1
        self.close()

###################
# generic dialog
class commDialog(QDialog):
    def __init__(self, text, flag, parent=None):
        super(commDialog, self).__init__(parent)
        self.text = text
        self.flag = flag
        #
        if self.text == "help":
            button3_text = "Close"
            self.text = """
The upper section.
This section lists the executables (if any) associates to the item mimetype.
If one of the executables is the default program for the 
mimetype it will be marked with (*). All the associations made in 
the mimeapps.list (the default one is placed in the HOME/.config folder
but can also be used that one in this program folder) will be shown 
as follow: those added will be marken with (+) or (+*) or (+?); those removed 
will be marked with (-) or (-?). "?" means that an application has been
registered but its desktop file cannot be found, e.g. after a 
disinstallation.

The lower section.
Three buttons: the "Make default" button will make the selected executable 
the default application for the mimetype; the "Add" button will 
show a menu that let user choose which installed application 
(through the desktop files) will be added as executable for the  
mimetype (it will be marked with (+)); the "Remove" button removes first 
the "*" if the executable is marked with (+*) and the second time the 
executable from the list, also if it is marked with (-).
The 'Help' button will show this help.
"""
        else:
            if self.flag == 4:
                button3_text = "Close"
            else:
                button3_text = "Cancel"
        #
        self.setWindowTitle("Info")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon("icons/file-manager-red.svg"))
        self.resize(600, 100)
        #
        vbox = QBoxLayout(QBoxLayout.TopToBottom)
        vbox.setContentsMargins(5,5,5,5)
        self.setLayout(vbox)
        #
        label1 = QLabel("{}".format(self.text))
        vbox.addWidget(label1)
        hbox = QBoxLayout(QBoxLayout.LeftToRight)
        vbox.addLayout(hbox)
        #
        if self.flag == 0:
            button1 = QPushButton("Open")
            hbox.addWidget(button1)
            button1.clicked.connect(self.fopen)
        elif self.flag == 1:
            button1 = QPushButton("OK")
            hbox.addWidget(button1)
            button1.clicked.connect(self.fopen)
        elif self.flag == 3:
            button2 = QPushButton("Execute")
            hbox.addWidget(button2)
            button2.clicked.connect(self.fexecute)
        #
        button3 = QPushButton(button3_text)
        hbox.addWidget(button3)
        button3.clicked.connect(self.fcancel)
        self.Value = 0
        self.exec_()

    def getValue(self):
        return self.Value

    def fopen(self):
        self.Value = 1
        self.close()
    
    def fexecute(self):
        self.Value = 2
        self.close()
    
    def fcancel(self):
        self.Value = -1
        self.close()

###################
