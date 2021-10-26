# SimpleFM
V. 0.7.2 (testing - no more features will be added in the main program)

A file manager written in PyQt5.

Requirements:
- python3 at least 3.3
- pyqt5
- python3-xdg
- pkexec
- python3-psutil

Optionals:
- python3-dbus.mainloop.pyqt5 (for mass storage devices)
- pdftocairo - ffmpegthumbnailer (for thumbnailers)
- 7z (for custom actions - raccomended)
- md5sum - sha256sum - sha1sum - tar - xterm (for custom actions)
- archivemount (for mounting archive files - custom action)
- coreurils at least 8.31 to get the right creation date and time of items.

Features:
- thumbnailers
- trashcan
- media
- bookmarks
- mount some archive files through archivemount (more types can be added if supported by archivemount) 
- custom actions
- custom thumbnailers
- custom folder icon
- sticky selection by pressing in the circle
- and more...

Tested a bit also under wayland.

Customizations throu the cfg.py file.


![My image](https://github.com/frank038/SimpleFM/blob/main/screenshot1.png)
