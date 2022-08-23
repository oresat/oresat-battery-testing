#!/bin/sh
dir1=.
while inotifywait -qqre modify "$dir1"; do
    rsync * /run/user/1000/gvfs/sftp:host=192.168.1.113/home/batteries/Documents/oresat-battery-testing/test-software/cpp --out-format="%n"
    echo Copied at $( date '+%F %H:%M:%S' )
done
