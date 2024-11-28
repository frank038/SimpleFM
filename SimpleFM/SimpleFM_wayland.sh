#!/bin/bash
thisdir=$(dirname "$0")
cd $thisdir
# chromium hack
DOWNLOAD="$HOME/Downloads/"
if [[ "$@" = "." && -d "$DOWNLOAD" ]]; then
  NEWFILE=`ls -Art $DOWNLOAD | tail -n 1`
  QT_SCALE_FACTOR=1 python3 SimpleFM.py "$DOWNLOAD/$NEWFILE" &
else
  QT_SCALE_FACTOR=1 python3 SimpleFM.py "$@" &
fi

cd $HOME
