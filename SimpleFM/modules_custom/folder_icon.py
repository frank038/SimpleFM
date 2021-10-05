#!/usr/bin/env python3
"""
set/unset a folder custom icon
"""

from PyQt5.QtWidgets import QFileDialog, QMessageBox
import shutil, os

# action name: this appears in the menu
def mmodule_name():
    return "Folder icon"

# 1 : one item selected - 2 : more than one item selected - 3 : one or more items selected- 4 on background - 5 always
# action type
def mmodule_type(mainLView):
    path = mainLView.lvDir
    # home dir
    if path[0:6] == "/home/":
        return 4
    else:
        return 0


class ModuleCustom():
    
    def __init__(self, mainLView):
        try:
            path = mainLView.lvDir
            directory_file = os.path.join(path, ".directory")
            # has already an icon
            if os.path.exists(directory_file):
                msgBox = QMessageBox()
                msgBox.setText("This folder has already an icon.\nApply: change icon.\nReset: remove the icon.\nClose: close this dialog.")
                btnApply = msgBox.addButton(QMessageBox.Apply)
                btnClose = msgBox.addButton(QMessageBox.Close)
                btnReset = msgBox.addButton(QMessageBox.Reset)
                msgBox.exec_()
                #
                if msgBox.clickedButton() == btnReset:
                    try:
                        with open(directory_file,"r") as f:
                            dcontent = f.readlines()
                            for el in dcontent:
                                if "Icon=" in el:
                                    icon_name = el.split("=")[1].strip("\n")
                                    os.remove(os.path.join(path, icon_name))
                                    break
                        os.remove(directory_file)
                    except Exception as E:
                        self.errorMsg(str(E))
                elif msgBox.clickedButton() == btnApply:
                    # remove the old files
                    try:
                        with open(directory_file,"r") as f:
                            dcontent = f.readlines()
                            for el in dcontent:
                                if "Icon=" in el:
                                    icon_name = el.split("=")[1].strip("\n")
                                    os.remove(os.path.join(path, icon_name))
                                    break
                        os.remove(directory_file)
                    except Exception as E:
                        self.errorMsg(str(E))
                    filename = self.choose_folder_icon()
                    if filename:
                        self.set_folder_icon(directory_file, path, filename[0])
            # set the icon
            else:
                filename = self.choose_folder_icon()
                if filename:
                    self.set_folder_icon(directory_file, path, filename[0])
        except Exception as E:
            self.errorMsg(str(E))
    
    def errorMsg(self, error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(error)
        msg.setWindowTitle("Error")
        msg.exec_()
    
    def choose_folder_icon(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setMimeTypeFilters({"image/jpeg", "image/png", "image/svg+xml"})
        filename = []
        if file_dialog.exec_():
            filename = file_dialog.selectedFiles()
        #
        return filename
    
    def set_folder_icon(self, directory_file, path, filename):
        icon_file = os.path.basename(filename)
        if not icon_file[0] == ".":
            icon_file = "."+icon_file
        try:
            with open(directory_file, "w") as ff:
                ff.write("Icon={}".format(icon_file))
            shutil.copy(filename, os.path.join(path, icon_file))
        except Exception as E:
            self.errorMsg(str(E))
