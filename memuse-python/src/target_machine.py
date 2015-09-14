#!/usr/bin/python

import os, shutil, time
from ssh_exec import *
from scp_fetch import *
from pexpect_scp import *
from memstat import *
from sysmem import *

class TargetMachine:
    def __init__(self, ip, port, user, password):
        self.ip = ip
        self.user = user
        self.password = password
        self.port = port
        self.ssh_client = None
        #self.dest = dest
        

    def connect(self):
        try:
            self.ssh_client = SSHRemoteClient(self.ip, self.user, self.password, self.port)
            #self.scp_client = SCPClient(ip, user, password, 22)
        except Exception, e:
            print str(e)
        

    def exec_cmd(self, command):
        list = None
        try:
            self.connect()
            list = self.ssh_client.execute(command)
        except Exception, e:
            print str(e)
        return list
    
    
    def _map_smaps(self):
        scp_client = SCPClient(self.ip, self.user, self.password, 22)
        scp_client.send('./local_copy.sh')
        self.exec_cmd('sh ./local_copy.sh')
        scp_client.send('./local_copy.py')
        self.exec_cmd('python ./local_copy.py')

    def fetch_smaps(self, dest, src):
        self. _map_smaps()
        scp_client = SCPExpect(self.ip, self.user, self.password)
        scp_client.fetch_dir(dest, src)

    #write the string list into fname
    def write_to_file(self, fname, strs):
        f = open(fname, 'a')
        for s in strs:
            f.write(s)
        f.close()

    def write_sysmem(self, sysmem, output_file):
        self.write_to_file(output_file, sysmem)

    def write_proc_prop(self, procs, output_file):
        sp = '\n' + 45 * '-' + 'Processes' + 45*'-' + '\n'
        self.write_to_file(output_file, sp)
        for p in procs:
            if p.prop.size == 0 and p.prop.rss == 0 and p.prop.pss == 0:
                continue
            self.write_to_file(output_file, p._myself())
            
    def write_libs(self, libs, output_file):
        strs = []
        sp = '\n' + 45 * '-' + 'Libraries' + 45*'-' + '\n'
        strs.append(sp)
        for l in libs:
            strs.append(l._myself())
        self.write_to_file(output_file, strs)
        

    def analyze_memstat(self, src, dest, root_output_dir):
        #create output dir and file.
        if os.path.exists(root_output_dir) == False:
            os.mkdir(root_output_dir, 0755)
        #create the output sub dir under output_dir
        output_dir = root_output_dir + '/' + self.ip
        if os.path.exists(output_dir) == True:
            shutil.move(output_dir, output_dir+'.bak-'+str(time.time()))
        #print output_dir
        #print root_output_dir
        
        os.mkdir(output_dir, 0755)
        output_file = output_dir + '/memstat'

        if os.path.exists(dest):
            shutil.rmtree(dest)
        os.mkdir(dest, 0755)
        self.fetch_smaps(dest, src)

        sysmem = SysMem(dest + '/proc')
        self.write_sysmem(sysmem._myself(), output_file)

        memstat = MemStat(dest + '/proc')
        self.write_proc_prop(memstat.procs, output_file)

        libs = memstat.fetch_lib_with_size()
        self.write_libs(libs, output_file)

        if os.path.exists(dest):
            print 'remove target machine folder ' + dest
            shutil.rmtree(dest)
        #DBG
        #print len(libs)
        #for l in libs:
        #    print l._myself() + '\tReferences: ' + str(len(l.procs)) + '\t' + l.cmd
        #return libs

if __name__ == '__main__':
    ip = '10.239.13.111'
    dest = '/tmp/' + ip
    src = '/tmp/proc/'
    target = TargetMachine(ip, 'root', 'iotos', 22)
    target.analyze_memstat(src, dest, './output')
