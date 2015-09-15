#!/bin/sh

DEST=/tmp/proc/

if [ -x $DEST ]; then
    rm -rf $DEST
fi

mkdir $DEST
echo 3 > /proc/sys/vm/drop_caches
cp /proc/meminfo $DEST
cp /etc/os-release $DEST

LINES=`dmesg | grep 'Memory:'` 
echo $LINES > /tmp/proc/kernel-memory
