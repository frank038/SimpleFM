#!/bin/bash
thisdir=$(dirname "$0")
cd $thisdir
./SimpleFM.py "$@" &
cd $HOME
