A fast svg to gcode compiler.

cat svgfile | python svg2gcode.py

The compiler is based on the eggbot project and it basically converts all of the SVG shapes into bezier curves. The bezier curves are then recursively sub divided until desired smoothness is achieved. The sub curves are then approximated as lines which are then converted into g-code. 

Some of the characteristics of the compiler can be changed by editing the config.py

Inkscape Plugin
---------------

To get the Inkscape plugin please checkout the __plasibot_laser__ branch.
