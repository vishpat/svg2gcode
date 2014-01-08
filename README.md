An Inkscape extension to convert a SVG drawing to G-code for reprap machines.

Installation
------------
Copy the __svg2gcode.py__, __svg2gcode.inx__ and __shapes.py__ to Inkscape __extensions__ directory  

* on Windows : "C:\Program Files\Inkscape\share\extensions"
* on Linux: "/usr/share/inkscape/extensions"
* on OS X: "/Applications/Inkscape.app/Contents/Resources/extensions"

Copy the __plastibot_laser.svg__ to Inkscape __templates__ directory  
* on Windows : "C:\Program Files\Inkscape\share\template"
* on Linux: "/usr/share/inkscape/template"
* on OS X: "/Applications/Inkscape.app/Contents/Resources/template"

Parameters
----------
The size of the bed is controlled via the __bed-width__ and __bed-height__ parameters in __svg2gcode_*.inx__ file. Please note that the size of the SVG image should match with the size of the printer/plotter bed. This can be achived using the __File -> New -> plastibot_laser__ type when creating a new SVG in inkscape.

Output
------

By default the gcode is stored in a file called __vector.gcode__ (for vector laser) or __raster.gcode__ (for raster laser) in your home directory. The file name can be changed using the options provided in the extension pop-up.
