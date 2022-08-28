#!/bin/bash
thisdir=$(dirname "$0")
cd $thisdir
# # needed to display right icons in some circumstances - "gtk2" is an example
# QT_QPA_PLATFORMTHEME="gtk2" python3 SimpleFM.py "$@" &
python3 SimpleFM.py "$@" &
cd $HOME
