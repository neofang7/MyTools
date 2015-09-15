#!/usr/bin/python

class ThreadInput:

    def __init__(self):
        self.ip = self.port = ''
        self.user = self.password = ''
        self.password = self.output = ''
        self.pocess = ''
        self.libref = False


    def _myself(self):
        return '[ip=' + self.ip + ', port=' + self.port + ', user=' + self.user + ', password=' + self.password + ']'

    def set_machine(self, ip, port, user, password, output):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.output = output
