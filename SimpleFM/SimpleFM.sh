#!/bin/bash
thisdir=$(dirname "$0")
cd $thisdir
# chromium hack
DOWNLOAD="$HOME/Scaricati/"
if [[ "$@" = "." && -d "$DOWNLOAD" ]]; then
  NEWFILE=`ls -Art $DOWNLOAD | tail -n 1`
  python3 SimpleFM.py "$DOWNLOAD/$NEWFILE" &
else
  python3 SimpleFM.py "$@" &
fi

cd $HOME
