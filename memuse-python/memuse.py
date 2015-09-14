#!/usr/bin/python

import sys
sys.path.insert(0, './src')

import argparse
import threading, time

from target_machine import *
from target_xml import *

thread_args = []

def menu():
    parser = argparse.ArgumentParser(description='memuse for Ostro')
    parser.add_argument('--ip', '-i', nargs=1)
    parser.add_argument('--port', '-p', nargs=1, type=int)
    parser.add_argument('--user', '-u', nargs=1, default='root')
    parser.add_argument('--password', '-w', nargs=1, default='iotos')
    parser.add_argument('--load', '-l', nargs=1)
    parser.add_argument('--output', '-o', nargs=1, default='./outputs')
    
    args = parser.parse_args()

    return args


def test_target(ti):
    tm = TargetMachine(ti.ip, ti.port, ti.user, ti.password)
    print ti.ip
    dst = '/tmp/' + ti.ip
    src = '/tmp/proc/'
    tm.analyze_memstat(src, dst, ti.output)
    

if __name__ == '__main__':
    #err = 0
    args = menu()
    #print args.ip[0], args.port[0], args.user, args.password, args.load, args.output

    threads = []
    
    if args.load == None:
        ti = ThreadInput(args.ip[0], args.port[0], args.user, args.password, args.output)
        #thread_args.append(ti)
        #index = thread_args.
        arglist = []
        arglist.append(ti)
        thread = threading.Thread(target=test_target, args=arglist)
        threads.append(thread)
    else:
        config = args.load[0]
        print config
        if os.path.exists(config) == False:
            print 'Invalid target config file.'
            #err = -1
        else:
            inputs = parse_target_xml(config)
            for i in inputs:
                i.outputs = args.output
                print i._myself()
                arglist = []
                arglist.append(i)
                thread = threading.Thread(target=test_target, args=arglist)
                threads.append(thread)
            

    for t in threads:
        t.start()

    for t in threads:
        threading.Thread.join(t)

    print 'All of the jobs have completed.'
