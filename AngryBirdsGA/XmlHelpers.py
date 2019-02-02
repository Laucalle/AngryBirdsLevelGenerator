import xml.etree.ElementTree as ET
from AngryBirdsGA import *

def initXMLLevel():
    """ Returns a list of strings containing the structure of the XML Level definition """
    root = ET.Element("Level")
    tree = ET.ElementTree(root)
    root.set('width', '2')

    camera = ET.SubElement(root, 'Camera')


    birds = ET.SubElement(root, 'Birds')
    ET.SubElement(birds, 'Bird').set('type', 'BirdRed')
    ET.SubElement(birds, 'Bird').set('type', 'BirdBlack')
    ET.SubElement(birds, 'Bird').set('type', 'BirdWhite')

    slingshot = ET.SubElement(root, 'Slingshot')
    slingshot.set('x', '-5')
    slingshot.set('y', '-2.5')

    gameObject = ET.SubElement(root, 'GameObjects')

    s_xml = ET.tostring(root, encoding='unicode', method='xml')
    return s_xml.replace('>', '>\n')


def writeXML(individual, filename):
    """ Writes the XML Level representation of individual to the file filename """
    global STRING_XML
    if STRING_XML == "":
        STRING_XML = initXMLLevel()

    f = open(filename, "w")
    index = STRING_XML.find('Camera')
    final_xml = []
    final_xml.append('<?xml version="1.0" encoding="utf-8"?>')
    final_xml.append(STRING_XML[:index + len('Camera')])
    final_xml.append(' x="0" y="0" minWidth="20" maxWidth="25" ')
    prev_index = index+len('Camera')
    index = STRING_XML.find('GameObjects')
    final_xml.append(STRING_XML[prev_index:index + len('GameObjects')])
    final_xml.append('>\n')
    i = 0
    for b in individual.blocks():
        final_xml.append('<' + getTag(b.type) +
                         ' type="' + BLOCK_NAMES[str(b.type)] + '"' +
                         ' material="' + MATERIALS[b.mat] + '"' +
                         ' x="' + str(b.x) + '"' +
                         ' y="' + str(b.y) + '"' +
                         ' rotation="' + ROTATION[b.rot] + '"' +
                         ' id="' + str(i) + '"/>\n')
        i+=1

    final_xml.append('</GameObjects>\n')
    final_xml.append(STRING_XML[index + len('<GameObjects\>'):])

    f.write(''.join(final_xml))

    f.close()


def readXML(filename):
    """ Reads the filename containing the XML output of the simulation and returns the list of velocities"""
    tree = ET.parse(filename)
    root = tree.getroot()
    game_objects = root.find('GameObjects')
    velocity = []
    for element in game_objects:
        # extract elements to calculate fitness
        velocity.append(float(element.attrib['aVelocity']))

    return velocity

def writePlain(individual, filename):
    f = open(filename, "w")
    text = []
    for b in individual.blocks():
        text.append(' '.join([str(b.x),str(b.y), str(BLOCKS[str(b.type)][0]/2), 
            str(BLOCKS[str(b.type)][1]/2), ROTATION[b.rot], str(FRICTION[MATERIALS[b.mat]])]))

    f.write("\n".join(text))

    f.close()

