import constants

import xml.etree.ElementTree as ET


def writeXML(individual, filename):
    f = open(filename, "w")
    root = ET.Element("Level")
    tree = ET.ElementTree(root)
    root.set('width', '2')

    camera = ET.SubElement(root, 'Camera')
    camera.set('x', '0')
    camera.set('y', '0')
    camera.set('minWidth', '20')
    camera.set('maxWidth', '25')

    birds = ET.SubElement(root, 'Birds')
    ET.SubElement(birds, 'Bird').set('type', 'BirdRed')
    ET.SubElement(birds, 'Bird').set('type', 'BirdBlack')
    ET.SubElement(birds, 'Bird').set('type', 'BirdWhite')

    slingshot = ET.SubElement(root, 'Slingshot')
    slingshot.set('x', '-5')
    slingshot.set('y', '-2.5')

    gameObject = ET.SubElement(root, 'GameObjects')
    for b in individual.blocks:
        e = ET.SubElement(gameObject, constants.getTag(b.type))
        e.set('type', constants.block_names[str(b.type)])
        e.set('material', constants.materials[b.mat])
        e.set('x', str(b.x))
        e.set('y', str(b.y))
        e.set('rotation', str(b.rot))

    tree.write(f, xml_declaration=True, encoding='unicode', method="xml")
    f.close()


def readXML(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    game_objects = root.find('GameObject')
    velocity = []
    for element in game_objects:
        # extract elements to calculate fitness
        velocity.append(element.attrib['averageVelocity'])

    return velocity
