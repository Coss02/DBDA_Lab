#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 11:12:33 2022

@author: armano
"""

# ---------- UTILITIES --------------------------------------------------------

# ---------- Generic utils ----------------------------------------------------

def settings(**kwargs):
  "Utility for building a dictionary using the key-value parameter passing"
  return kwargs

def flatten(L):
  "Naive implementation of list flattening..."
  outlist = list()
  for item in L:
    if type(item) in (tuple,list): item = [ item ]
    outlist += item
  return outlist

def strip_keys(keys):
  "Strip the schema name (if any) from keys"
  keys = tuple([ str(key) for key in keys ]) # ensure that keys are strings
  return tuple([ key.split('.')[1] if '.' in key else key for key in keys ])

# ---------- Print utils ------------------------------------------------------

def display_result(items, comment='Query results', end=''):
  "Display the result of a query"
  print(f"\n--- {comment} ---\n")
  no_items = True
  for item in items :
    print(item) ; no_items = False
  if no_items: print("Non ci sono elementi in questa lista...")
  if end: print(end)
  
# -----------------------------------------------------------------------------

def display_table_info(table):
  print(f"\n*** Table: '{table.description}' ***")
  for column in table.columns: print(column)
  
# ---------- Set operations on lists ------------------------------------------

def make_list_difference(L1, L2, selector=None, key=lambda x: x):
  "Eval the difference between two lists (as they were in fact two sets)"
  list_diff = sorted ( list(set(L1)-set(L2)), key=key )
  return list_diff if not selector else [selector(item) for item in list_diff]

def make_list_intersection(L1, L2, selector=None, key=lambda x: x):
  "Eval the difference between two lists (as they were in fact two sets)"
  list_inter = sorted ( list(set(L1) & set(L2)), key=key )
  return list_inter if not selector else [ selector(x) for x in list_inter ]

# -----------------------------------------------------------------------------