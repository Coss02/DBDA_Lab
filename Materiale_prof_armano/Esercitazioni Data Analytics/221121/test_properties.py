#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 14:30:55 2022

@author: armano
"""

# -----------------------------------------------------------------------------

# How to define and use properties

# -----------------------------------------------------------------------------

from math import sqrt

#------------------------------------------------------------------------------

def distance_from_origin(point2D):
  "Distance from origin (for 2D points)"
  return point2D.distance(Point2D(0,0))

# -----------------------------------------------------------------------------

class Point(object):
  
  "Testing properties (old style)"
  
  color = property(lambda s: s.get_color(), lambda s, v: s.set_color(v))
  
  from_origin = property(distance_from_origin) # using an external function
  from_origin2 = property(lambda self: self.distance(Point())) # using a method

  def __init__(self, x=0, y=0):
    "Init the 2D point"
    self.x, self.y = x, y
    self._color = 'black'

  def get_color(self):
    "Get the current color"
    return self._color
  
  def set_color(self, color):
    "Set the current color"
    self._color = color
    
  def distance(self, point):
    "Distance between self and another point"
    dx, dy = (self.x - point.x), (self.y - point.y)
    return sqrt(dx**2+dy**2)

  def __str__(self):
    "Convert a 2D point to string (typically for printing)"
    return f"<x={self.x}, y={self.y}, color={self._color}>"

# -----------------------------------------------------------------------------

class Point2D(object):
  
  "Testing properties (old style)"
  
  def __init__(self, x=0, y=0):
    "Init the 2D point"
    self.x, self.y = x, y
    self._color = 'black'

  @property
  def color(self):
    "Get the current color"
    return self._color
  
  @color.setter
  def color(self, color):
    "Set the current color"
    self._color = color
  
  @property
  def from_origin(self):
    "Get the distance from origin of the current point (self)"
    return self.distance(Point2D())

  def distance(self, point):
    "Distance between self and another point"
    dx, dy = (self.x - point.x), (self.y - point.y)
    return sqrt(dx**2+dy**2)

  def __str__(self):
    "Convert a 2D point to string (typically for printing)"
    return f"<x={self.x}, y={self.y}, color={self._color}>"

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  print("\n*** Using OLD style ***\n")
  p = Point()
  print(p) ; p.color = 'red' ; print(p)
  print("Distance from origin (method call):", p.distance(Point()))
  print("Distance from origin (as property):", p.from_origin)
  print("Distance from origin (as property):", p.from_origin2)

  print("\n*** Using NEW style ***\n")
  q = Point2D()
  print(q) ; q.color = 'red' ; print(q)
  print("Distance from origin (method call):", q.distance(Point2D()))
  print("Distance from origin (as property):", q.from_origin)

# -----------------------------------------------------------------------------
