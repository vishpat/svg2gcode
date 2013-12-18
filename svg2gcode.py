#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator

import inkex
from simplestyle import *

class svg2gcode(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('-w', '--bed-width', action = 'store',
          type = 'int', dest = 'bed_width', default = 200,
          help = 'Bed Width')
        self.OptionParser.add_option('-x', '--bed-height', action = 'store',
          type = 'int', dest = 'bed_height', default = 200,
          help = 'Bed Height')
        self.OptionParser.add_option('-o', '--gcode-file', action = 'store',
          type = 'string', dest = 'gcode_file', default = 'plastibot.gcode',
          help = 'The generated gcode file path')

    def generate_gcode():

        svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
        
        tree = ET.parse(sys.stdin)
        root = tree.getroot()
        
        width = root.get('width')
        height = root.get('height')
        if width == None or height == None:
            viewbox = root.get('viewBox')
            if viewbox:
                _, _, width, height = viewbox.split()                

        if width == None or height == None:
            print "Unable to get width and height for the svg"
            sys.exit(1)

        width = float(width)
        height = float(height)

        scale_x = bed_max_x / max(width, height)
        scale_y = bed_max_y / max(width, height)

        print preamble 
        
        for elem in root.iter():
            
            try:
                _, tag_suffix = elem.tag.split('}')
            except ValueError:
                continue

            if tag_suffix in svg_shapes:
                shape_class = getattr(shapes_pkg, tag_suffix)
                shape_obj = shape_class(elem)
                d = shape_obj.d_path()
                if d:
                    print shape_preamble 
                    p = point_generator(d, smoothness)
                    for x,y in p:
                        if x > 0 and x < bed_max_x and y > 0 and y < bed_max_y:  
                            print "G1 X%0.1f Y%0.1f" % (scale_x*x, scale_y*y) 
                    print shape_postamble

        print postamble 

    def effect(self):
        what = self.options.gcode_file

        # Get access to main SVG document element and get its dimensions.
        svg = self.document.getroot()
        # or alternatively
        # svg = self.document.xpath('//svg:svg',namespaces=inkex.NSS)[0]

        # Again, there are two ways to get the attibutes:
        width  = inkex.unittouu(svg.get('width'))
        height = inkex.unittouu(svg.attrib['height'])

        # Create a new layer.
        layer = inkex.etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), 'Hello %s Layer' % (what))
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

        # Create text element
        text = inkex.etree.Element(inkex.addNS('text','svg'))
        text.text = 'Hello %s!' % (what)

        # Set text position to center of document.
        text.set('x', str(width / 2))
        text.set('y', str(height / 2))

        # Center text horizontally with CSS style.
        style = {'text-align' : 'center', 'text-anchor': 'middle'}
        text.set('style', formatStyle(style))

        # Connect elements together.
        layer.append(text)


effect = svg2gcode();
effect.affect();


