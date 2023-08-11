# SimpleFM
V. 0.9.117

A file manager written with PyQt5.

Requirements:
- python3 at least 3.3
- pyqt5
- python3-xdg
- python3-psutil

Optionals:
- pkexec (alternatively a su/sudo method can be used)
- udisk2 and python3-dbus.mainloop.pyqt5 (for mass storage devices)
- pdftocairo - ffmpegthumbnailer (for thumbnailers)
- 7z (for custom actions - recommended)
- md5sum - sha256sum - sha1sum - tar - xterm (for custom actions)
- archivemount (and 7z for mounting archive files - custom action)
- coreurils at least 8.31 to get the right creation date and time of items.

Features:
- thumbnailers
- trashcan
- media
- bookmarks
- mounts some archive files through archivemount (more types can be added if supported by archivemount) 
- custom actions
- custom thumbnailers
- custom folder icon
- sticky selection by pressing in the circle
- sends items to the desktop as special desktop files (feature of my SimpleDesktop program)
- and more...

Support for drag and drop from my archive manager. For this operation it is used a custom solution, so no need of changing any window property.

The 'Shift key' behaviour: to select a certain amount of contiguous items, select the first, press the shift key and select the last; to move the selected items by using the shift key, press the shift key and start dragging the last selected item.

Pkexec: a different solution has been implemented to avoid it: if chosed in the config file, sudo - with user password - will be used; alternatively, also the su command - with the root password - can be used, just comment out the sudo section and uncomment the su section in the file pkexec.sh. A dialog for asking the password will appear.

Customizations throu the cfg.py file.

Some custom modules are disabled: just remove "-t" from its file name to be enabled.

![My image](https://github.com/frank038/SimpleFM/blob/main/screenshot1.png)
