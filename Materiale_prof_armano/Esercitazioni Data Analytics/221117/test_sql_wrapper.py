#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 10:02:59 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy import create_engine, text

# -----------------------------------------------------------------------------

def settings(**kwargs): return kwargs

# -----------------------------------------------------------------------------

class SQLWrapper(object):
  
  results = property(lambda self: self._results) # read-only virtual slot
  
  def __init__(self, schema, database, host='localhost', port=5432):
    "Init the wrapper"
    self.schema, self.database = schema, database
    self.user, self.password = 'postgres', '' # default user and password
    self.host, self.port = host, port
    self.query, self.params = '', dict()
    self.engine = None
    self._results = list()
    
  @property
  def url(self): # read-only virtual slot
    "Return the url to be used for creating the engine"
    host, port, database = self.host, self.port, self.database
    user, password = self.user, self.password
    return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

  def logon(self, user=None, password=None):
    "Create the engine (after optionally setting user and password)"
    self.user = user if user else self.user
    self.password = password if password else self.password
    search_path = settings(options=f'-csearch_path={self.schema}')
    self.engine = create_engine(self.url, connect_args=search_path)
    return self # connect_args allow to set the schema once for all...
    
  def __call__(self, **params):
    "Store binding params to be used in the next 'execute' (see __lshift__)"
    self.params = params
    return self
  
  def __lshift__(self, query):
    "Ask the wrapper to perform a query (delegates a connection)"
    self.query = text(query).bindparams(**self.params)
    with self.engine.connect() as connection:
      self._results = connection.execute(self.query)
    self.params = dict() # parameters must be reset after each execute!!!  
    return self._results # the result is also returned to the client...
  
  def execute(self, query):
    "Alternative to __lshift__"
    return self << query

  def display_results(self, comment='Display the result of the last query'):
    "Display the results of the last query"
    print(f"\n*** {comment} ***\n")
    for k, item in enumerate(self.results):
      print(f"[{k:2d}] {item}")
    print()

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  # Create the SQL wrapper
  sql = SQLWrapper(schema='segreteria', database='didattica')
  
  # Perform logon
  sql.logon(user='dida', password='didapass') # to be called only once...
  
  # Ask the wrapper to execute a query (without parameters)
  sql.execute("select * from studenti") # no binding
  sql.display_results("Simple command (no parameters)")
  
  # Ask the wrapper to execute a generic query (with parameters)
  sql(cognome='Rossi') << "select * from studenti where cognome=:cognome"
  sql.display_results("Simple command (with parameters)")
  
# -----------------------------------------------------------------------------