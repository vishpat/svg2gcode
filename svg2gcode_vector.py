#!/usr/bin/env python

import sys
import os 

import inkex
import shapes as shapes_pkg
from shapes import point_generator

class svg2gcode_vector(inkex.Effect):

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
        
        self.OptionParser.add_option('-p', '--preamble', action = 'store',
          type = 'string', dest = 'preamble', default = 'G28\nG1 Z5.0\n',
          help = 'Preamble G-code')
        self.OptionParser.add_option('-q', '--postamble', action = 'store',
          type = 'string', dest = 'postamble', default = 'G28\nG1 Z5.0\n',
          help = 'Postamble G-code')
        self.OptionParser.add_option('-s', '--shape-preamble', action = 'store',
          type = 'string', dest = 'shape_preamble', default = 'G4 P200\n',
          help = 'Shape Preamble G-code')
        self.OptionParser.add_option('-t', '--shape-postamble', action = 'store',
          type = 'string', dest = 'shape_postamble', default = 'G4 P200\n',
          help = 'Shape Postamble G-code')
        
    def generate_gcode(self, svg):
        gcode_file = os.path.join(os.path.expanduser('~'), self.options.gcode_file)
        try:
            os.remove(gcode_file)
        except OSError:
            pass

        bed_width = self.options.bed_width
        bed_height = self.options.bed_height
        
        width = svg.get('width')
        height = svg.get('height')

        width = inkex.unittouu(width)
        height = inkex.unittouu(height)

        if width > bed_width or height > bed_height:
            raise ValueError(('The document size (%d x %d) is greater than the bedsize' % 
                             (round(width, 1), round(height, 1)))) 

        with open(gcode_file, 'w') as gcode:  
            gcode.write(self.options.preamble + '\n')
     
            svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
            
            for elem in svg.iter():
                try:
                    _, tag_suffix = elem.tag.split('}')
                except ValueError:
                    continue

                if tag_suffix in svg_shapes:
                    shape_class = getattr(shapes_pkg, tag_suffix)
                    shape_obj = shape_class(elem)
                    d = shape_obj.d_path()
                    m = shape_obj.transformation_matrix()

                    if d:
                        gcode.write(self.options.shape_preamble + '\n')

                        p = point_generator(d, m, 0.05)
                        for x,y in p:
                            gcode.write("G1 X%0.1f Y%0.1f\n" % (x, y)) 

                        gcode.write(self.options.shape_postamble + '\n')

            gcode.write(self.options.postamble + '\n')

    def effect(self):
        svg = self.document.getroot()
        self.generate_gcode(svg)

effect = svg2gcode_vector();
effect.affect();


