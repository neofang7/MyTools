#!/usr/bin/python

import os

class SysMem:
    def __init__(self, path):
        self.MemTotal = ''
        self.MemFree = ''
        self.MemUsed = ''
        self.MemSlab = ''
        self.MemAvailable = ''
        self.ReleaseInfo = []
        
        os_release = path + '/os-release'
        meminfo = path + '/meminfo'
        
        if self.analyze_sysmem(meminfo, os_release) == False:
            print 'Error in analyze system memory'
        

    def analyze_sysmem(self, meminfo, osrelease):
        result = self._analyze_meminfo(meminfo)
        if result == False:
            return False
        
        result = self._fetch_releaseinfo(osrelease)
        print self.ReleaseInfo

        return result

    def _myself(self):
        strs = []
        #line = ''
        strs.append('\n' + 45 * '-' + 'Release Info' + 40 * '-' + '\n')
        #while line in self.ReleaseInfo:
        #    print line
        #    strs.append(line)
        strs.extend(self.ReleaseInfo)
        strs.append('\n')
        strs.append('\n' + 45 * '-' + 'System  Info' + 40 * '-' + '\n')
        strs.append('MemTotal     :\t' + self.MemTotal + '\tMB\n')
        strs.append('MemUsed      :\t' + self.MemUsed + '\tMB\n')
        strs.append('MemAvailable :\t' + self.MemAvailable + '\tMB\n')
        strs.append('MemFree      :\t' + self.MemFree + '\tMB\n')
        strs.append('MemSlab      :\t' + self.MemSlab + '\tMB\n')
        return strs
        
        
    def _analyze_meminfo(self, fname):
        #print fname
        if os.path.exists(fname) == False:
            return False

        f = open(fname, 'r')
        line = f.readline()
        while line:
            l = line.split()
            if cmp(l[0], 'MemTotal:') == 0:
                self.MemTotal = str(int(l[1]) >> 10)
            elif cmp(l[0], 'MemFree:') == 0:
                self.MemFree = str(int(l[1]) >> 10)
            elif cmp(l[0], 'Slab:') == 0:
                self.MemSlab = str(int(l[1]) >> 10)
            elif cmp(l[0], 'MemAvailable:') == 0:
                self.MemAvailable = str(int(l[1]) >> 10)
            line = f.readline()
        f.close()
        if self.MemTotal != '' and self.MemFree != '':
            self.MemUsed = str(int(self.MemTotal) - int(self.MemAvailable))
            print self.MemUsed
        return True

    #Read os-release file
    def _fetch_releaseinfo(self, fname):
        print fname
        if os.path.exists(fname) == False:
            return False
        f = open(fname, 'r')
        line = f.readline()
        while line:
            self.ReleaseInfo.append(line)
            line = f.readline()
        f.close()
        return True
