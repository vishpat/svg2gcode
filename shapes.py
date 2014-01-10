#!/usr/bin/env python

import logging
import traceback
import xml.etree.ElementTree as ET
import simplepath
import simpletransform 
import cubicsuperpath
import cspsubdiv
from bezmisc import beziersplitatt


class svgshape(object):
    
    def __init__(self, xml_node):
        self.xml_node = xml_node 
 
    def d_path(self):
        raise NotImplementedError

    def transformation_matrix(self):
        t = self.xml_node.get('transform')
        return simpletransform.parseTransform(t) if t is not None else None

    def svg_path(self):
        return "<path d=\"" + self.d_path() + "\"/>"

    def __str__(self):
        return self.xml_node        

class path(svgshape):
     def __init__(self, xml_node):
        super(path, self).__init__(xml_node)

        if not self.xml_node == None:
            path_el = self.xml_node
            self.d = path_el.get('d')
        else:
            self.d = None 
            logging.error("path: Unable to get the attributes for %s", self.xml_node)

     def d_path(self):
        return self.d     

class rect(svgshape):
  
    def __init__(self, xml_node):
        super(rect, self).__init__(xml_node)

        if not self.xml_node == None:
            rect_el = self.xml_node
            self.x  = float(rect_el.get('x')) if rect_el.get('x') else 0
            self.y  = float(rect_el.get('y')) if rect_el.get('y') else 0
            self.rx = float(rect_el.get('rx')) if rect_el.get('rx') else 0
            self.ry = float(rect_el.get('ry')) if rect_el.get('ry') else 0
            self.width = float(rect_el.get('width')) if rect_el.get('width') else 0
            self.height = float(rect_el.get('height')) if rect_el.get('height') else 0
        else:
            self.x = self.y = self.rx = self.ry = self.width = self.height = 0
            logging.error("rect: Unable to get the attributes for %s", self.xml_node)

    def d_path(self):
        a = list()
        a.append( ['M ', [self.x, self.y]] )
        a.append( [' l ', [self.width, 0]] )
        a.append( [' l ', [0, self.height]] )
        a.append( [' l ', [-self.width, 0]] )
        a.append( [' Z', []] )
        return simplepath.formatPath(a)     

class ellipse(svgshape):

    def __init__(self, xml_node):
        super(ellipse, self).__init__(xml_node)

        if not self.xml_node == None:
            ellipse_el = self.xml_node
            self.cx  = float(ellipse_el.get('cx')) if ellipse_el.get('cx') else 0
            self.cy  = float(ellipse_el.get('cy')) if ellipse_el.get('cy') else 0
            self.rx = float(ellipse_el.get('rx')) if ellipse_el.get('rx') else 0
            self.ry = float(ellipse_el.get('ry')) if ellipse_el.get('ry') else 0
        else:
            self.cx = self.cy = self.rx = self.ry = 0
            logging.error("ellipse: Unable to get the attributes for %s", self.xml_node)

    def d_path(self):
        x1 = self.cx - self.rx
        x2 = self.cx + self.rx
        p = 'M %f,%f ' % ( x1, self.cy ) + \
            'A %f,%f ' % ( self.rx, self.ry ) + \
            '0 1 0 %f,%f ' % ( x2, self.cy ) + \
            'A %f,%f ' % ( self.rx, self.ry ) + \
            '0 1 0 %f,%f' % ( x1, self.cy )
        return p

class circle(ellipse):
    def __init__(self, xml_node):
        super(ellipse, self).__init__(xml_node)

        if not self.xml_node == None:
            circle_el = self.xml_node
            self.cx  = float(circle_el.get('cx')) if circle_el.get('cx') else 0
            self.cy  = float(circle_el.get('cy')) if circle_el.get('cy') else 0
            self.rx = float(circle_el.get('r')) if circle_el.get('r') else 0
            self.ry = self.rx
        else:
            self.cx = self.cy = self.r = 0
            logging.error("Circle: Unable to get the attributes for %s", self.xml_node)

class line(svgshape):

    def __init__(self, xml_node):
        super(line, self).__init__(xml_node)

        if not self.xml_node == None:
            line_el = self.xml_node
            self.x1  = float(line_el.get('x1')) if line_el.get('x1') else 0
            self.y1  = float(line_el.get('y1')) if line_el.get('y1') else 0
            self.x2 = float(line_el.get('x2')) if line_el.get('x2') else 0
            self.y2 = float(line_el.get('y2')) if line_el.get('y2') else 0
        else:
            self.x1 = self.y1 = self.x2 = self.y2 = 0
            logging.error("line: Unable to get the attributes for %s", self.xml_node)

    def d_path(self):
        a = []
        a.append( ['M ', [self.x1, self.y1]] )
        a.append( ['L ', [self.x2, self.y2]] )
        return simplepath.formatPath(a)

class polycommon(svgshape):

    def __init__(self, xml_node, polytype):
        super(polycommon, self).__init__(xml_node)
        self.points = list()

        if not self.xml_node == None:
            polycommon_el = self.xml_node
            points = polycommon_el.get('points') if polycommon_el.get('points') else list() 
            for pa in points.split():
                self.points.append(pa)
        else:
            logging.error("polycommon: Unable to get the attributes for %s", self.xml_node)


class polygon(polycommon):

    def __init__(self, xml_node):
         super(polygon, self).__init__(xml_node, 'polygon')

    def d_path(self):
        d = "M " + self.points[0]
        for i in range( 1, len(self.points) ):
            d += " L " + self.points[i]
        d += " Z"
        return d

class polyline(polycommon):

    def __init__(self, xml_node):
         super(polyline, self).__init__(xml_node, 'polyline')

    def d_path(self):
        d = "M " + self.points[0]
        for i in range( 1, len(self.points) ):
            d += " L " + self.points[i]
        return d

def point_generator(path, mat, flatness):

        if len(simplepath.parsePath(path)) == 0:
                return
       
        simple_path = simplepath.parsePath(path)
        startX,startY = float(simple_path[0][1][0]), float(simple_path[0][1][1])
        yield startX, startY

        p = cubicsuperpath.parsePath(path)
        
        if mat:
            simpletransform.applyTransformToPath(mat, p)

        for sp in p:
                cspsubdiv.subdiv( sp, flatness)
                for csp in sp:
                    ctrl_pt1 = csp[0]
                    ctrl_pt2 = csp[1]
                    end_pt = csp[2]
                    yield end_pt[0], end_pt[1],    
