#!/bin/bash

function check_number
{
    expr $1 + 0 > /dev/null 2>&1
    if [ $? -eq 0 ]; then
	return 1
    else
	return 0
    fi
}

DEST='/tmp/proc/'
SRC='/proc/'

if [[ ! -d $DEST ]]; then
    mkdir $DEST
else
    rm -rf $DEST'/*'
fi

cp '/proc/meminfo' $DEST
cp '/etc/os-release' $DEST

sleep 1

files=`ls /proc/`
for f in $files 
do
	check_number $f
	
	if [ $? -eq 0 ]; then
	    continue
	fi

	path='/proc/'$f
	if [ -d $path ]; then
	    DEST_PATH=$DEST$f
	    if [[ ! -d $DEST_PATH ]]; then
		mkdir -p $DEST_PATH
	    fi

	    cp $path'/cmdline' $DEST_PATH'/cmdline'
	    cp $path'/smaps' $DEST_PATH'/smaps'
	fi	    
done
