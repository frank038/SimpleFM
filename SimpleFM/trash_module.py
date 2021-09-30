#!/usr/bin/env python3

import os
import sys
import stat
from urllib.parse import unquote
import shutil
import datetime

class TrashItems():
    def __init__(self):
        self.fakename = ""
        self.realname = ""
        self.deletiondate = ""

# only HOME
class mountPoint():
    def __init__(self, mpath):
        self.path = mpath
        
    def find_trash_path(self):
        trash_path = ""
        if self.path == "HOME":
            trash_path = os.path.join(os.path.expanduser("~"), ".local/share/Trash")
        else:
            user_id = os.getuid()
            trash_path = os.path.join(self.path, ".Trash-"+str(user_id))
        return trash_path

class ReadTrash():
    def __init__(self, tpath):
        self.tpath = tpath
        # HOME trash path
        self.Ttrash = mountPoint(self.tpath).find_trash_path()
        self.Tfiles = os.path.join(self.Ttrash, "files")
        self.Tinfo = os.path.join(self.Ttrash, "info")
        self.can_read_trash = 0
        self.Ttrash_can_read_trash()
        
    def Ttrash_can_read_trash(self):
        if not os.path.exists(self.Ttrash) or not os.path.exists(self.Tfiles) or not os.path.exists(self.Tinfo):
            return
        if not os.access(self.Tfiles, os.R_OK) or not os.access(self.Tinfo, os.R_OK):
            return
        #
        self.can_read_trash = 1
        return
    
    def trashed_items(self):
        list_trasheditems = []
        info_items = os.listdir(self.Tinfo)
        for iitem in info_items:
            try:
                with open(os.path.join(self.Tinfo, iitem), 'r') as read_data:
                    read_data.readline()
                    fake_name = os.path.splitext(os.path.basename(iitem))[0]
                    spath = unquote(read_data.readline())[5:].rstrip()
                    deletion_date = read_data.readline()[13:].rstrip()
                    diskpart = TrashItems()
                    diskpart.fakename = fake_name
                    if self.tpath == "HOME":
                        diskpart.realname = spath[len(os.path.expanduser('~'))+1:]
                    else:
                        diskpart.realname = spath
                    diskpart.deletiondate = deletion_date
                    list_trasheditems.append(diskpart)
            except:
                return -1
        #
        return list_trasheditems
    
    #
    def return_the_list(self):
        if self.can_read_trash:
            self.items_in_trash = self.trashed_items()
        else:
            return -2
        if self.items_in_trash != -1:
            return self.items_in_trash
        else:
            return -1

class RestoreTrash():
    def __init__(self, tpath, items_in_trash):
        self.items_in_trash = items_in_trash
        self.Ttrash = mountPoint(tpath).find_trash_path()
        self.Tfiles = os.path.join(self.Ttrash, "files")
        self.Tinfo = os.path.join(self.Ttrash, "info")
        self.can_restore = 0
        self.Ttrash_can_restore()

    def Ttrash_can_restore(self):
        if not os.access(self.Tfiles, os.W_OK) or not os.access(self.Tinfo, os.W_OK):
            return
        else:
            self.can_restore = 1

    def itemsRestore(self):
        if self.can_restore:
            iitem = self.items_in_trash[0]
            fake_name = iitem.fakename
            real_name = iitem.realname
            ret = os.path.exists(real_name)

            if ret:
                new_path = self.setNewname(real_name)
                try:
                    shutil.move(os.path.join(self.Tfiles, fake_name), new_path)
                    fake_path = os.path.join(self.Tinfo, fake_name+".trashinfo")
                    os.unlink(fake_path)
                except Exception as E:
                    return str(E)
            
            elif not ret:
                try:
                    shutil.move(os.path.join(self.Tfiles, fake_name), real_name)
                    fake_path = os.path.join(self.Tinfo, fake_name+".trashinfo")
                    os.unlink(fake_path)
                except Exception as E:
                    return str(E)
            return [1,-1]
        else:
            return -2

    def setNewname(self, oldName):
        oName = os.path.basename(oldName)
        oDir = os.path.dirname(oldName)
        z = datetime.datetime.now()
        dts = "_{}.{}.{}_{}.{}.{}".format(z.year, z.month, z.day, z.hour, z.minute, z.second)
        nroot, suffix = os.path.splitext(oName)
        newName = nroot+dts+suffix
        newPath = os.path.join(oDir, newName)
        if os.path.exists(newPath):
            self.setNewname(oldName)
        else:
            return newPath


class deleteTrash():
    
    def __init__(self, tpath, items_in_trash):
        self.items_in_trash = items_in_trash
        self.Ttrash = mountPoint(tpath).find_trash_path()
        self.Tfiles = os.path.join(self.Ttrash, "files")
        self.Tinfo = os.path.join(self.Ttrash, "info")
        self.can_delete = 0
        self.Ttrash_can_delete()

    def Ttrash_can_delete(self):
        if not os.access(self.Tfiles, os.W_OK) or not os.access(self.Tinfo, os.W_OK):
            return
        else:
            self.can_delete = 1
    
    def itemsDelete(self):
        if self.can_delete:
            iitem = self.items_in_trash[0]
            fake_name = iitem.fakename
            real_name = iitem.realname
            full_fake_name = os.path.join(self.Tfiles, fake_name)
            item_trashinfo = os.path.join(self.Tinfo, fake_name+".trashinfo")
            if os.path.isdir(full_fake_name):
                try:
                    shutil.rmtree(full_fake_name)
                    os.unlink(item_trashinfo)
                except Exception as E:
                    return str(E)
            else:
                try:
                    os.unlink(full_fake_name)
                    os.unlink(item_trashinfo)
                except Exception as E:
                    return str(E)
            
            return [1,-1]
        else:
            return -2


class emptyTrash():
    def __init__(self, tpath):
        self.tpath = tpath
        self.Ttrash = mountPoint(tpath).find_trash_path()
        self.Tfiles = os.path.join(self.Ttrash, "files")
        self.Tinfo = os.path.join(self.Ttrash, "info")
        self.can_delete = 0
        self.Ttrash_can_delete()
    
    def Ttrash_can_delete(self):
        if not os.access(self.Tfiles, os.W_OK) or not os.access(self.Tinfo, os.W_OK):
            return
        else:
            self.can_delete = 1
        
    def tempty(self):
        if self.can_delete:
            ret = 0
            for ffile in os.listdir(self.Tfiles):
                ffile_path = os.path.join(self.Tfiles, ffile)
                if os.path.isfile(ffile_path) or os.path.islink(ffile_path):
                    try:
                        os.unlink(ffile_path)
                    except:
                        ret = -1
                elif os.path.isdir(ffile_path):
                    try:
                        shutil.rmtree(ffile_path)
                    except:
                        ret = -1
                else:
                    try:
                        os.unlink(ffile_path)
                    except:
                        ret = -1
                    
            for ffile in os.listdir(self.Tinfo):
                ffile_path = os.path.join(self.Tinfo, ffile)
                try:
                    os.unlink(ffile_path)
                except:
                    ret = -1
            
            return ret
        else:
            return -2


class TrashIsEmpty():
    def __init__(self, path):
        self.path = path
        self.trash_path = mountPoint(self.path).find_trash_path()
        self.Tfiles = os.path.join(self.trash_path, "files")
        
    def isEmpty(self):
        if os.path.exists(self.Tfiles):
            iitems = os.listdir(self.Tfiles)
            if len(iitems) > 0:
                return 1
            else:
                return 0
        else:
            return 0
