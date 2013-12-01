#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator

svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])

def generate_gcode():
    tree = ET.parse(sys.stdin)
    root = tree.getroot()
    print "G28\n\n G1 Z5.0\n\n"
    for elem in root.iter():
        _, tag_suffix = elem.tag.split('}')
        if tag_suffix in svg_shapes:
            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            print "G4 P200"
            p = point_generator(shape_obj.d_path())
            for x,y in p:
                print "G1 X%0.1f Y%0.1f" % (x, y) 
    print "G28"

if __name__ == "__main__":
    generate_gcode()



