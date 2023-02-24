#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 08:49:55 2022

@author: armano
"""

# -----------------------------------------------------------------------------

class Point(object):
  
  def __init__(self, x=0, y=0):
    self.x, self.y = x, y
    
  def __str__(self):
    return f"<x={self.x},y={self.y}>"
  
  def __repr__(self):
    return str(self) # equivalent to: self.__str__()
    
# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  p = Point(y=22)
  
  print(p) # equivalent to: print(p.__str__()) || also: print(str(p))
  
  p # equivalent to: p.__repr__() || also: repr(p)
    # it is shown only when executing this statement under jupyter lab/notebook
  
# -----------------------------------------------------------------------------