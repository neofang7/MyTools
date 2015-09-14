import xml.etree.ElementTree as ET
from target_machine import *

class ThreadInput:
    def __init__(self, ip, port, user, password, output):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.output = output

    def _myself(self):
        return '[ip=' + self.ip + ', port=' + self.port + ', user=' + self.user + ', password=' + self.password + ']'

def parse_target_xml(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    #root = ET.fromstring('Targets')
    
    print root.tag
    if cmp(root.tag, 'Targets') != 0:
        print 'Error contents in ' + xml
        return None

    tis = []

    for child in root:
        m = ThreadInput  (child.find('ip').text, 
                          child.find('port').text,
                          child.find('user').text,
                          child.find('password').text, './outputs')
        tis.append(m)

    return tis


if __name__ == '__main__':
    targets = parse_target_xml('config/targets.xml')
    for m in targets:
        print '[ip=' + m.ip + ', port=' + m.port + ', user=' + m.user + ', password=' + m.password + ']'
