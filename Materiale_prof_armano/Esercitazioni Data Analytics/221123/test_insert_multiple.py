# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -----------------------------------------------------------------------------

from os.path import join as join_path

# -----------------------------------------------------------------------------

from sqlalchemy import insert

# -----------------------------------------------------------------------------

from table_utility import TABUtility # REQUIRES TABUtility

# -----------------------------------------------------------------------------

class DataLoader(object):
  
  "Simple data loader from csv file (a header occurs at the first row)"
  
  fullname = property(lambda self: join_path(self.path,self.fname))
  
  def __init__(self, path='', sep=','):
    "Init the data loader"
    self.fname, self.path = None, path
    self.sep = sep
    self.header, self.content = list(), list()
    
  def __lshift__(self, fname):
    "Load data from text file"
    self.fname = fname
    with open(self.fullname) as infile:
      self.content = [ line.strip().split(self.sep) for line in infile ]
    self.content = [ self.strip_values(values) for values in self.content ]
    header, content = self.content[0], self.content[1:]
    return tuple(header), [ tuple(values) for values in content ]

  def strip_values(self, values):
    "Remove blanks from values"
    return [ value.strip() for value in values ]
  
# -----------------------------------------------------------------------------

class DataHandler(TABUtility):
  
  "Simple data handler (just inserts values into a database table)"
  
  fullname = property(lambda self: join_path(self.path,self.fname))
  
  def __init__(self, *args, **kwargs):
    "Init the data handler"
    super().__init__(*args, **kwargs)
    self.attributes, self.items = None, None
    self.insert_clause = None
    
  def __call__(self, attributes):
    "Set the attributes for the data handler"
    self.attributes = attributes
    return self

  def __lshift__(self, items):
    "Embed attributes and content into the data handler"
    self.items = items
    return self

  def __rshift__(self, table):
    "Store all items into the database"
    assert self.attributes and self.items
    print(table) # just for debugging
    with self.engine.connect() as connection:
      query = insert(table).values(self.items)
      connection.execute(query)
    return self

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  user, passwd = 'dida', 'didapass'
  database, schema = 'didattica', 'segreteria'
  
  # Load the items from csv file
  loader = DataLoader(sep=';') # same folder of the Python code...
  attributes, content = loader << "students.csv"
  
  # Store items into a table of the database
  handler = DataHandler(database).as_user(user,passwd).with_schema(schema)
  students = handler.table('segreteria.studenti')
  handler(attributes) << content # embed attrs and content into the handler
  handler >> students # store info to the database table 'studenti'

# -----------------------------------------------------------------------------