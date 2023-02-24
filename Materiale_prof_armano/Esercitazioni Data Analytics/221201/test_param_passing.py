#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 10:06:48 2022

@author: armano
"""

# -----------------------------------------------------------------------------

def foo(*args, **kwargs):
  print("args:", args)
  print("kwargs:", kwargs)
  print()
  
# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  foo()
  
  foo(10, 20, 30)
  
  foo(a=22, pinco='oops', ahah=33)
  
  foo(10, 20, 30, a=22, pinco='oops', ahah=33)

# -----------------------------------------------------------------------------
