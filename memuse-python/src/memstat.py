#!/usr/bin/python

import os
import os.path
import string

from proc import *
from target_machine import *

class MemStat:
    def __init__(self, path):
        self.procs = []
        #self.libs = []
        self._analyze_all_processes(path)


    def _list_pids(self, path):
        pids = []
        for i in os.listdir(path):
            f = ""
            name = os.path.split(i)
            if os.path.isdir(path + '/' + name[1]):
                if name[1].isdigit():
                    pids.append(name[1])
        return pids

    def _analyze_all_processes(self, path):
        parser = Parser(path)
        pids = self._list_pids(path)
        for p in pids:
            #print p
            proc = parser.parse_smaps(p)
            self.procs.append(proc)
        self.procs.sort(lambda a,b:b.prop.size - a.prop.size)

    def _search_lib(self, lib_name, libs):
        index = -1
        found = 0
        for l in libs:
            index = index + 1
            if cmp(lib_name, l.cmd) == 0:
                found = 1
                break
        if found == 1:
            return index
        else:
            return -1

    
    def _fetch_lib_list(self):
        libs = []
        for p in self.procs:
            #check the libs in Process
            for l in p.libs:
                index = self._search_lib(l.cmd, libs)
                if index == -1:
                    libs.append(l)
                else:
                    libs[index].procs.append(p.cmd)
        return libs

    def fetch_lib_with_size(self):
        libs = self._fetch_lib_list()
        libs.sort(lambda a,b:b.prop.size - a.prop.size)
        return libs

    def fetch_lib_with_references(self):
        libs = self._fetch_lib_list()
        libs.sort(lambda a,b:len(a.procs) - len(b.procs))
        return libs


if __name__ == '__main__':
    memstat = MemStat('/proc')
    #libs = memstat.fetch_lib_with_size()
    libs = memstat.fetch_lib_with_references()
    
    for l in libs:
        print l._myself() + '\tReferences: ' + str(len(l.procs)) + '\t' + l.cmd
                    
                
