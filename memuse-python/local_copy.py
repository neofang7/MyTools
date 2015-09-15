#!/usr/bin/python

import sys, shutil, os, string

def copy_smaps(pid):
    dest = '/tmp/proc/'
    #if os.path.exists(dest):
    #    shutil.rmtree(dest)
    #os.mkdir(dest)

    #shutil.copy('/proc/meminfo', dest)
    #shutil.copy('/etc/os-release', dest)
    #print 'start to map smaps'

    if pid != '':
        src = '/proc/'+pid+'/smaps'
        cmdline = '/proc/'+pid+'cmdline'
        if os.path.exists(src):
            os.mkdir (dest + pid + '/')
            shutil.copy(src, dest + pid + '/')
            shutil.copy(cmdline, dest + pid + '/')

    for i in os.listdir('/proc/'):
        
        if i.isdigit() == True:
            name = os.path.split(i)
            if os.path.isdir('/proc/' + name[1]):
                if name[1].isdigit():
                    #pids.append(name[1])
                    src = '/proc/' + name[1] + '/smaps'
                    cmdline = '/proc/' + name[1] + '/cmdline'
                    #print src
                    if os.path.exists(src):
                        os.mkdir(dest + name[1] + '/')
                        shutil.copy(src, dest+name[1]+'/')
                        shutil.copy(cmdline, dest+name[1]+'/')
                        

if __name__ == '__main__':
    args = str(sys.argv)
    if len(args) != 1:
        copy_smaps(args[1])
    else:
        copy_smaps('')
