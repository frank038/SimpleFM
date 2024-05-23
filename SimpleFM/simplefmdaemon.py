#!/usr/bin/env python3

"""
This is a simple daemon implementing freedesktop.org's file manager interface
Useful for starting SimpleFM, and selecting the file, from a browser (after that file has been downloaded)
Set the path at line 23
"""

import gi
from gi.repository import GObject, GLib

import dbus
import dbus.service
import dbus.mainloop.glib

import os
from subprocess import Popen
from urllib.parse import unquote, quote

def open_file_manager(uri, select=False):
    
    uri =  unquote(uri).replace('file://', '')
    args = ['/FULL/PATH/TO/SimpleFM/SimpleFM.sh']

    path = str(uri)
    args.append(path)

    if os.fork() == 0:
        Popen(args)
        os._exit(0)
    else:
        os.wait()

class FmObject(dbus.service.Object):

    @dbus.service.method("org.freedesktop.FileManager1",
                         in_signature='ass', out_signature='')
    def ShowFolders(self, uris, startupId):
        open_file_manager(uris[0])

    @dbus.service.method("org.freedesktop.FileManager1",
                         in_signature='ass', out_signature='')
    def ShowItems(self, uris, startupId):
        open_file_manager(uris[0], select=True)

    @dbus.service.method("org.freedesktop.FileManager1",
                         in_signature='ass', out_signature='')
    def ShowItemProperties(self, uris, startupId):
        open_file_manager(uris[0], select=True)

    @dbus.service.method("org.freedesktop.FileManager1",
                         in_signature='', out_signature='')
    def Exit(self):
        mainloop.quit()

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("org.freedesktop.FileManager1", session_bus)
    object = FmObject(session_bus, '/org/freedesktop/FileManager1')
    mainloop = GLib.MainLoop()
    mainloop.run()
