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
       
        if width > bed_width or height > bed_height:
            raise ValueError(('The document size (%d x %d) is greater than the bedsize' % 
                             (round(width, 1), round(height, 1)))) 

        points = []
        threshold = 0.1
        intermediate_points = 5
        svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
       
        min_x = min_y = sys.maxint
        max_x = max_y = 0

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
                    prev_x = prev_y = None
                    p = point_generator(d, threshold)
                    for x, y in p:
                        
                        if prev_x is not None and prev_y is not None:
                            x_incr = (x - prev_x)/intermediate_points 
                            y_incr = (y - prev_y)/intermediate_points 
                            for i in range(1, intermediate_points):
                                bisect.insort(points, (round(prev_x + i*x_incr, 1) , 
                                                       round(prev_y + i*y_incr,  1)))
       
                        min_x = x if x < min_x else min_x
                        min_y = y if y < min_y else min_y
                        max_x = x if x > max_x else max_x
                        max_y = y if y > max_y else max_y
                        bisect.insort(points, (round(x, 1) , round(y, 1)))

        with open(gcode_file, 'w') as gcode:  
            gcode.write(self.options.preamble + '\n')
            
            laser_high = False
            y = min_y
            while y <= max_y:
                x = min_x
                while x <= max_x:
                    i = bisect.bisect_left(points, (round(x, 1), round(y, 1)))
                    if i != len(points) and cmp(points[i], (round(x, 1), round(y, 1))) == 0:
                        
                        if not laser_high:
                            gcode.write("M104 S255\n")
                            laser_high = True

                        gcode.write("G1 X%0.1f Y%0.1f\n" % (x, y))
                    else:
                        
                        if laser_high:
                            gcode.write("M104 S0\n")
                            laser_high = False

                        gcode.write("G1 X%0.1f Y%0.1f\n" % (x, y))
                    x += threshold
                y += threshold                    

            gcode.write(self.options.postamble + '\n')

    def effect(self):
        svg = self.document.getroot()
        self.generate_gcode(svg)

effect = svg2gcode_raster();
effect.affect();


