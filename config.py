"""G-code emitted at the start of processing the SVG file"""
preamble = "G28\nG1 Z5.0"

"""G-code emitted at the end of processing the SVG file"""
postamble = "G28"

"""G-code emitted before processing a SVG shape"""
shape_preamble = "G4 P200"

"""G-code emitted after processing a SVG shape"""
shape_postamble = "G4 P200"

"""Print bed width in mm"""
bed_max_x = 200

"""Print bed height in mm"""
bed_max_y = 200

""" 
Used to control the smoothness/sharpness of the curves.
Smaller the value greater the sharpness. Make sure the
value is greater than 0.1
"""
smoothness = 0.2


