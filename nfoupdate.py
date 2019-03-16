#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import re
import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom

reload(sys)
sys.setdefaultencoding('UTF-8')
logging.getLogger().setLevel(logging.INFO)

#target_file = str(sys.argv[1])
#targetactor = str(sys.argv[2])

target_file = str(sys.argv[1])
targetactor = str(sys.argv[2])

def removeAnnoyingLines(elem):
    hasWords = re.compile("\\w")
    for element in elem.iter():
        if not re.search(hasWords,str(element.tail)):
            element.tail=""
        if not re.search(hasWords,str(element.text)):
            pass

tree = ET.parse(target_file)  
root = tree.getroot()

actors = root.findall('actor')
for actor in actors:
    actorname = actor.find('name')

attrib = {}  
new_actor = root.makeelement('actor', attrib)  
root.append(new_actor)

ET.SubElement(new_actor, 'name', attrib={})
ET.SubElement(new_actor, 'role', attrib={})
ET.SubElement(new_actor, 'thumb', attrib={})
new_actor[0].text = targetactor
#tree.write(target_file,encoding="UTF-8",xml_declaration=True)

removeAnnoyingLines(root)
xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent='  ', newl='\n', encoding="utf-8")
with open(target_file, "w") as f:
    f.write(xmlstr)

print "Done."