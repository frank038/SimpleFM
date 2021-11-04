#!/usr/bin/env python3
"""
send to desktop a folder by using a desktop file
"""

from PyQt5.QtWidgets import QMessageBox
import os, stat

# action name: this appears in the menu
def mmodule_name():
    return "Send to desktop"

# 1 : one item selected - 2 : more than one item selected - 3 : one or more items selected- 4 on background - 5 always
# action type
def mmodule_type(mainLView):
    if mainLView.selection:
        if len(mainLView.selection) == 1:
            index = mainLView.selection[0]
            path = mainLView.fileModel.fileInfo(index).absoluteFilePath()
            if os.path.isdir(path) or stat.S_ISREG(os.stat(path).st_mode) and os.path.exists(path) and not os.path.islink(path):
                desktop_home = os.path.join(os.path.expanduser("~"), "Desktop")
                if os.path.exists(desktop_home):
                    return 1


class ModuleCustom():
    
    def __init__(self, mainLView):
        try:
            index = mainLView.selection[0]
            dpath = mainLView.fileModel.fileInfo(index).absoluteFilePath()
            directory_name = os.path.basename(dpath)
            directory_name_fixed = directory_name
            directory_file = directory_name+".directory"
            #
            desktop_home = os.path.join(os.path.expanduser("~"), "Desktop")
            i = 1
            while os.path.exists(os.path.join(desktop_home, directory_file)):
                directory_name_temp = directory_name_fixed+"_{}".format(i)
                directory_file = directory_name_temp+".directory"
                i += 1
            #
            dest_path = os.path.join(desktop_home, directory_file)
            # the custom icon
            iicon = "folder"
            if os.path.exists(os.path.join(dpath, ".directory")):
                tmp = None
                with open(os.path.join(dpath, ".directory"), "r") as ff:
                    tmp = ff.readlines()
                iicon = os.path.join(dpath, tmp[0][5:])
            # type: Directory - Link
            if os.path.isdir(dpath):
                ttype = "Directory"
            elif stat.S_ISREG(os.stat(dpath).st_mode):
                ttype = "Link"
                iicon = None
            # write the desktop file
            with open(dest_path, "w") as ff:
                ff.write("[Desktop Entry]\n")
                ff.write("Name={}\n".format(directory_name))
                if iicon == None:
                    ff.write("Icon=\n")
                else:
                    ff.write("Icon={}\n".format(iicon))
                ff.write("Type={}\n".format(ttype))
                ff.write("URL=file://{}\n".format(dpath))
        except Exception as E:
            self.errorMsg(str(E))
                
    def errorMsg(self, error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(error)
        msg.setWindowTitle("Error")
        msg.exec_()
