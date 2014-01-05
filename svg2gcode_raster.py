#!/usr/bin/env python

import sys
import os 
import bisect

import inkex
import shapes as shapes_pkg
from shapes import point_generator

class svg2gcode_raster(inkex.Effect):

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

        scale_x = bed_width / max(width, height)
        scale_y = bed_height / max(width, height)
        
        points = []

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
                    if d:
                        p = point_generator(d, 0.1)
                        bisect.insort(points, p)
                        
            cur_x = 0.0
            cur_y = 0.0
            for x, y in points:
                   pass 

            gcode.write(self.options.postamble + '\n')

    def effect(self):
        svg = self.document.getroot()
        self.generate_gcode(svg)

effect = svg2gcode_raster();
effect.affect();


