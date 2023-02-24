#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 11:11:27 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy.inspection       import inspect

# -----------------------------------------------------------------------------

from utils                    import strip_keys

# -----------------------------------------------------------------------------

class BaseModel(object):
  
  "Simple base model for the SQLAlchemy ORM class Base"
  
  __abstract__ = True
  
  def __init__(self):
    "Init an instance of the base model"
    self.__mapper__ = None

  def __call__(self, *keys, dtype=tuple): # no keys --> ALL keys...
    "Get the values corresponding to the given keys (as tuple or dict)"
    assert dtype in (tuple, dict)
    keys = keys if keys else strip_keys(self.__mapper__.columns)
    values = tuple([ getattr(self, key, None) for key in keys])
    return values if dtype == tuple else dict(zip(keys,values))

  @classmethod
  def describe(cls): #using 'inspect' (with relationships)
    "Describe the current ORM table"
    icls = inspect(cls) # icls = handle for the inspector of class 'cls'
    clsname = str(icls.class_) ; tabname = icls.tables[0].name
    print(f"\n--- ORM class {clsname} (tablename: {tabname})")
    columns, relationships = icls.columns.items(), icls.relationships.items()
    print()
    for key, column in columns: print(key, "-->", column)
    if not relationships: return
    print("\nRelations:")
    for key, column in relationships: print(key, "-->", column)
  
  @classmethod
  def describe2(cls): # using the mapper (w/out relationships)
    "Describe the current ORM table"
    __, clsname = str(cls.__mapper__._sort_key).split('.')
    tablename = str(cls.__mapper__.local_table)
    print(f"\n--- ORM class {clsname} (tablename: {tablename})")
    for column in cls.__mapper__.columns: print(column)
  
  def __str__(self):
    "Convert the object into a string"
    return str(self()) # delegation to __call__
  
# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  pass

# -----------------------------------------------------------------------------