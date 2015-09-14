#!/usr/bin/python

import re

class Entry:
    def __init__(self):
        self.size = 0
        self.rss = 0
        self.pss = 0

    def _myself(self):
        #print '[size = %dkB; rss = %dkB; pss = %dkB]' %(self.size, self.rss, self.pss)
        return '[Size=' + str(self.size) + 'kB;\tRss=' + str(self.rss) + 'kB;\tPss=' + str(self.pss) + 'kB]' 

class Process:
    def __init__(self):
        self.cmd = ""
        self.pid = -1
        self.prop = Entry()
        self.heap = Entry()
        self.stack = Entry()
        self.vdso = Entry()
        self.libs = []

    def _myself(self):
        lines = []
        s = 'PID:' + str(self.pid) + '\t' + str(self.cmd) + '\n'
        s2 = ""
        for c in s:
            #print ord(c)
            if ord(c) == 0:
                #print 'null'
                c = ' '
            s2 = s2 + c
       # s.replace(chr(0), ' ')
        lines.append(s2)
        s = '\tProp:\t' + self.prop._myself() + '\n'
        lines.append(s)
        s = '\tHeap:\t' + self.heap._myself() + '\n'
        lines.append(s)
        s = '\tStack:\t' + self.stack._myself() + '\n'
        lines.append(s)
        s = '\tvdso:\t' + self.vdso._myself() + '\n'
        lines.append(s)

        return lines

    def print_myself(self):
        print '\t-----------'
        print '\t' + self.cmd + '\tpid:' + str(self.pid)
        print '\tProp:\t' + self.prop._myself()
        print '\tHeap:\t' + self.heap._myself()
        print '\tStack:\t' + self.stack._myself()
        print '\tvdso:\t' + self.vdso._myself()
        print '\t==========='
        for l in self.libs:
            l.print_myself()
    
class Library:
    def __init__(self):
        self.cmd = ""
        self.prop = Entry()
        self.procs = []
    

    def _myself(self):
        s = '\t Prop:' + self.prop._myself() + '\tReferenced:' + str(len(self.procs)) + '\t' + self.cmd + '\n' 
        return s

    def print_myself(self):
        print '\t' + self.prop._myself() + '\t' + self.cmd

class Parser:
    def __init__(self, path):
        self.path = path
        
 
    def search_in_libs(self, lib_name, libs):
        index = -1
        found = 0
        for lib in libs:
            index = index + 1
            if cmp(lib_name, lib.cmd) == 0:
                found = 1
                break;
        if found == 1:
            return index
        return -1
    
    def ignore_a_block(self, line, f):
        while line:
            if re.findall('VmFlags', line):
                line = f.readline()
                l = line.split()
                if len(l) == 5:
                    continue
                else: 
                    break
            line = f.readline()
        return line


    def ignore_until(self, line, f):
        while line:
            
            if re.findall('.so', line):
                break
            line = f.readline()

        return line
            
    
    def read_a_block(self, f, current_entry):
        #line = f.readline()
        #l = line.split()
        #Size:
        line = f.readline()
        l = line.split()
        if cmp(l[0], 'Size:') == 0:
            current_entry.size = current_entry.size + int(l[1])
        else:
            print "Error format, it should be size:. " + line
        #Rss:
        line = f.readline()
        l = line.split()
        if cmp(l[0], 'Rss:') == 0:
            current_entry.rss = current_entry.rss + int(l[1])
        else:
            print "Error format, it should be rss:. " + line
        #Pss:
        line = f.readline()
        l = line.split()
        if cmp(l[0], 'Pss:') == 0:
            current_entry.pss = current_entry.pss + int(l[1])
        else:
            print "Error format, it should be pss:. " + line
        #--Ignore the following lines
            #Shared_Clean          #Shared_Dirty
            #Private_Clean         #Private_Dirty
            #Referenced            #Anonymous
            #AnonHugePages         #Swap
            #KernelPageSize        #MMUPageSize
            #Locked                #VmFlags
        #lines = f.readlines(12)
        #print "End of line: " + lines[-1]
        while cmp(l[0], 'VmFlags:') != 0:
            line = f.readline()
            l = line.split()
        

    def parse_smaps(self, pid):
        #fetch the smaps from pid
        f = open(self.path + '/' + str(pid) + '/cmdline')
        #self.cmd = f.readline()
        cmd = f.readline()
        f.close()

        f = open(self.path + '/' + str(pid) + '/smaps')
        line = f.readline()
        current_proc = Process()
        current_proc.pid = pid
        current_proc.cmd = cmd

        current_entry = None
        pattern = '[0-9a-f]*\-[0-9a-f]*'
        #Handle the contents of processes
        while line:
            #print line
            l = line.split()
            if re.findall(pattern, line):
                #current_entry = current_proc.prop
                if len(l) == 5:
                    #follow the last entry as current entry
                    if current_entry == None:
                        current_entry = current_proc.prop
                    else:
                        current_entry = current_entry
                elif re.findall('heap', line):
                    current_entry = current_proc.heap
                elif re.findall('stack', line):
                    current_entry = current_proc.stack
                elif re.findall('vdso', line):
                    current_entry = current_proc.vdso
                elif re.findall('.so', line):
                    #go to the next loop to handle libs information
                    break;
                elif re.findall('.cache', line):
                    #ignore.
                    line = self.ignore_a_block(line, f)
                    
                    continue
                else:
                    #print line
                    current_entry = current_proc.prop
            
            self.read_a_block(f, current_entry)
            #Read the next 1st line of block
            line = f.readline()

        #Handle libs info
        current_lib = None
        while line:
            #self.ignore_a_block(line, f)
            l = line.split()
            if re.findall(pattern, line):
                if len(l) == 5 or cmp(l[5], '[vdso]') == 0 or cmp(l[5], '[vsyscall]') == 0:
                    current_lib = current_lib
                    self.read_a_block(f, current_lib.prop)
                    line = f.readline()
                elif re.findall('.so', line):
                    lib_name = l[5]
                    #check the lib in global libs.
                    gindex = -1
                    if len(current_proc.libs) > 0:
                        gindex = self.search_in_libs(lib_name, current_proc.libs)
                    if gindex == -1:
                        lib = Library()
                        lib.cmd = lib_name
                        lib.procs.append(pid)
                        #read libs size
                        current_proc.libs.append(lib)
                        current_lib = lib
                    else:
                        current_lib = current_proc.libs[gindex]
                    
                    self.read_a_block(f, current_lib.prop)
                    line = f.readline()
                else:
                    line = self.ignore_until(line, f)
            else:
                print "Error format: ", line
                break;
            
        return current_proc

if __name__ == '__main__':
    parser = Parser('/proc/')
    current_proc = parser.parse_smaps(1185)
    current_proc.print_myself()
                
            
    
        
                
