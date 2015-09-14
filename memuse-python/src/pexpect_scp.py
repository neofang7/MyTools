#!/usr/bin/python

import os
import pexpect

class SCPExpect:
    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password

    def fetch_file(self, dest, src):
        if os.path.isdir(dest) == False:
            return False
        command = 'scp ' + self.user + '@' + self.ip + ':' + src + ' ' + dest
        child = pexpect.spawn(command)
        child.expect('password:')
        child.sendline(self.password)
        child.expect('$')
        child.interact()

    def fetch_dir(self, dest, src):
        if os.path.isdir(dest) == False:
            return False
        command = 'scp -r ' + self.user + '@' + self.ip + ':' + src + ' ' + dest
        #f = open('/tmp/expect_log.txt')
        child = pexpect.spawn(command)
        #child.logfile_send = f
        #child.logfile_send = '/dev/null'
        child.expect('password:')
        child.sendline(self.password)
        child.expect('$')
        child.interact()
        
if __name__ == '__main__':
    scp_client = SCPExpect('10.239.13.111', 'root', 'iotos')
    scp_client.fetch_file('/tmp/', '/proc/1/smaps')
    print 'done'
