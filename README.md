# SimpleFM

A file manager written with PyQt5. There is alse the qt6 version: SimpleFM6.

Requirements:
- python3 at least 3.3
- pyqt5
- python3-xdg
- python3-psutil

Recommended:
- xterm, or any other terminal that can execute commands in the same way (xterm -e COMMAND). To be setted in the config file.

Optionals:
- pkexec (alternatively a su/sudo method can be used)
- udisk2 and python3-dbus.mainloop.pyqt5 (for mass storage devices)
- pdftocairo - ffmpegthumbnailer (for thumbnailers)
- 7z (for custom actions)
- md5sum - sha256sum - sha1sum - tar - xterm (for custom actions)
- archivemount (and 7z for mounting archive files - custom action)
- coreurils at least 8.31.

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
- manages the permissions of multiple files at once (without checking the previous state of each of them, obviously)
- and more...

The file simplefmdaemon.py is a dbus implementation of the freedesktop.org's file manager interface (let user launch SimpleFM from a browser after a file has been downloaded). The full path of the file SimpleFM.sh has to be setted in the file simplefmdaemon.py at line 23.

Support for drag and drop from my archive manager. For this operation it is used a custom solution, so no need of changing any window property.

The 'Shift key' behaviour: to select a certain amount of contiguous items, select the first, press the shift key and select the last; to move the selected items by using the shift key, press the shift key and start dragging the last selected item.

Mouse middle click to open the pointed folder. Middle click on the button in the bar to open that folder in a new tab.

Pkexec: a different solution has been implemented to avoid it: if chosed in the config file, sudo - with user password - will be used; alternatively, also the su command - with the root password - can be used, just comment out the sudo section and uncomment the su section in the file pkexec.sh. A dialog for asking the password will appear.

Customizations throu the cfg.py file.

Some custom modules are disabled: just remove "-t" from its file name to be enabled.

---------------

Wayland support is under testing.

Because the iconview font size is smaller under wayland, there are two more options in the config file:
- is_wayland: needed to apply the attribute AA_EnableHighDpiScaling, and for copying/moving operations while dragging;
- use_font_size: for setting the whole program font size.

Under wayland, launch SimpleFM.py through the script SimpleFM_wayland.sh, because it contains the environment variable QT_SCALE_FACTOR=1. For a screen scaling higher than 1, play with those settings.

The default operation while dragging one or more items is copy; press shift for the move action.


![My image](https://github.com/frank038/SimpleFM/blob/main/screenshot1.png)

![My image](https://github.com/frank038/SimpleFM/blob/main/screenshot2.png)
