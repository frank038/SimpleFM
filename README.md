# SimpleFM
V. 0.9.3

A file manager written with PyQt5.

Requirements:
- python3 at least 3.3
- pyqt5
- python3-xdg
- pkexec
- python3-psutil

Optionals:
- python3-dbus.mainloop.pyqt5 (for mass storage devices)
- pdftocairo - ffmpegthumbnailer (for thumbnailers)
- 7z (for custom actions - recommended)
- md5sum - sha256sum - sha1sum - tar - xterm (for custom actions)
- archivemount (for mounting archive files - custom action)
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

Tested a bit also under wayland. Pkexec (for higher privileges) could not work. A different solution has to be implemented.

Customizations throu the cfg.py file.

Some custom modules are disabled: just remove "-t" from its file name to be enabled.

![My image](https://github.com/frank038/SimpleFM/blob/main/screenshot1.png)
