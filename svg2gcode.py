#!/usr/bin/env python

from xml.dom import minidom
import sys

import shapes as shapes_pkg
from shapes import point_generator

svg_shapes = ['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path']

def generate_gcode():
    dom = minidom.parse(sys.stdin)
    print "G28\n\n G1 Z5.0\n\n" 
    for svg_shape in svg_shapes:
        shapes = dom.getElementsByTagName(svg_shape)
        for shape in shapes:
            shape_class = getattr(shapes_pkg, shape.nodeName)
            shape_obj = shape_class(shape.toxml())
            print "G4 P200"
            p = point_generator(shape_obj.d_path())
            for x,y in p:
                print "G1 X%0.1f Y%0.1f" % (x, y) 
    print "G28"
    dom.unlink()

if __name__ == "__main__":
    generate_gcode()



