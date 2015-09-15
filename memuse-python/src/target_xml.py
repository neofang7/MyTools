import xml.etree.ElementTree as ET
from target_machine import *
from thread_input import *

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
        m = ThreadInput  ()
        m.set_machine(child.find('ip').text, 
                          child.find('port').text,
                          child.find('user').text,
                          child.find('password').text, './outputs')
        tis.append(m)

    return tis


if __name__ == '__main__':
    targets = parse_target_xml('config/targets.xml')
    for m in targets:
        print '[ip=' + m.ip + ', port=' + m.port + ', user=' + m.user + ', password=' + m.password + ']'
