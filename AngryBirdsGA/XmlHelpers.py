import xml.etree.ElementTree as ET
from AngryBirdsGA import *

def initXMLLevel():
    root = ET.Element("Level")
    tree = ET.ElementTree(root)
    root.set('width', '2')

    camera = ET.SubElement(root, 'Camera')
    # camera.set('x', '0')
    # camera.set('y', '0')
    # camera.set('minWidth', '20')
    # camera.set('maxWidth', '25')

    birds = ET.SubElement(root, 'Birds')
    ET.SubElement(birds, 'Bird').set('type', 'BirdRed')
    ET.SubElement(birds, 'Bird').set('type', 'BirdBlack')
    ET.SubElement(birds, 'Bird').set('type', 'BirdWhite')

    slingshot = ET.SubElement(root, 'Slingshot')
    slingshot.set('x', '-5')
    slingshot.set('y', '-2.5')

    gameObject = ET.SubElement(root, 'GameObjects')
    # for b in individual.blocks:
    #    e = ET.SubElement(gameObject, constants.getTag(b.type))
    #    e.set('type', constants.block_names[str(b.type)])
    #    e.set('material', constants.materials[b.mat])
    #    e.set('x', str(b.x))
    #    e.set('y', str(b.y))
    #    e.set('rotation', str(b.rot))

    s_xml = ET.tostring(root, encoding='unicode', method='xml')
    return s_xml.replace('>', '>\n')


def writeXML(individual, filename):
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
    for b in individual.blocks:
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

    #tree.write(f, xml_declaration=True, encoding='unicode', method="xml")
    f.close()


def readXML(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    game_objects = root.find('GameObjects')
    velocity = []
    for element in game_objects:
        # extract elements to calculate fitness
        velocity.append(float(element.attrib['aVelocity']))

    return velocity
