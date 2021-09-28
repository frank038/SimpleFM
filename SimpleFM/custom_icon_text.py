#!/usr/bin/env python3
"""
Custom text of each icon - time
"""
import os, datetime

def fcit(fpath):
    try:
        tm = os.stat(fpath).st_mtime
        CT = str(datetime.datetime.fromtimestamp(tm))
        return CT
    except:
        return ""
