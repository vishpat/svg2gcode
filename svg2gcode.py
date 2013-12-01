#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator

preamble = "G28\n\n G1 Z5.0\n\n"
postamble = "G28"
shape_preamble = "G4 P200"
shape_postamble = "G4 P200"

def generate_gcode():
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
    
    tree = ET.parse(sys.stdin)
    root = tree.getroot()
    
    print preamble 
    
    for elem in root.iter():
        _, tag_suffix = elem.tag.split('}')
        if tag_suffix in svg_shapes:
            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()
            if d:
                print shape_preamble 
                p = point_generator(d)
                for x,y in p:
                    print "G1 X%0.1f Y%0.1f" % (x, y) 
                print shape_postamble

    print postamble 

if __name__ == "__main__":
    generate_gcode()



