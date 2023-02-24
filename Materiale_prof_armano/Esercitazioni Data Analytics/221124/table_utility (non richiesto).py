#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 11:03:02 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy import __version__ as sqlalchemy_version

from sqlalchemy import create_engine, inspect, MetaData, Table

# -----------------------------------------------------------------------------

from accessify import private

# -----------------------------------------------------------------------------

def settings(**kwargs): return kwargs

def strip_table_info(table):
  return ", ".join( [ str(x).split('.')[1] for x in table.columns ] )

# -----------------------------------------------------------------------------

class TABUtility(object):
  
  "Simple database handler based on SQLAlchemy"
  
  def __init__(self, database):
    "Init the handler"
    self.database = database
    self.user, self.password = None, None
    self.metadata, self.engine, self.inspector = None, None, None
    self.active_schema = None
    
  def as_user(self, user, password):
    "Bind the handler to a given user (and create the SQL engine)..."
    self.user, self.password = user, password
    url = f'postgresql+psycopg2://{user}:{password}@localhost/{self.database}'
    self.engine = create_engine(url, echo=False)
    self.inspector = inspect(self.engine)
    return self
  
  @property # Get the current schema
  def schema(self): return self.active_schema
  
  @schema.setter # Set the current schema
  def schema(self, schema):
    self.metadata = MetaData(schema=schema, bind=None)
    self.metadata.reflect(self.engine) # just to show a different way ...
    self.active_schema = schema
    
  def with_schema(self, schema):
    "Alternative way to set the current schema (see also @schema.setter)"
    self.schema = schema # Activates the @schema.setter
    return self

  def tables(self, *table_names):
    "Get multiple tables based on thier name"
    return tuple([ self.table(table_name) for table_name in table_names ])    
    
  def table(self, table_name):
    "Get a table given its name"
    schema = self.metadata.schema
    if '.' not in table_name and schema: table_name = f"{schema}.{table_name}"
    return self.metadata.tables[table_name]
  
  def display_table_schemas(self, comment=''):
    if comment: comment = f"({comment})"
    print(f"\n*** Schema: {self.schema} {comment} ***")
    tables = self.metadata.tables.values()
    if len(tables) == 0: print(f"\nNo tables defined for {self.schema}...")
    for table in tables:
      self.display_table_schema(table, comment=f"\nTable name: {table.name}")
    print()
        
  def display_table_schema(self, table, comment=''):
    "Display the schema of a table"
    if comment: ( print(comment), print() )
    table_columns = self.inspector.get_columns(table.name, schema=self.schema)
    for column in table_columns: print(column)
  
  def display_table_content(self, table, comment=''):
    "Display a table content (table can be of type Table or string)"
    tablename, table = self.get_table_info(table)
    comment = comment if comment else f"Tabella {tablename}"
    print(f"\n*** {comment} ***\n")
    columns = strip_table_info(table) ; print(f"Columns: {columns}\n")
    items = self.engine.execute(table.select()).fetchall()
    for item in items: print(item)

  @private
  def get_table_info(self, table):
    "Get table info (table can be of type Table or string)"
    assert type(table) in [ Table, str ]
    metadata, engine = self.metadata, self.engine
    kwargs = settings(autoload=True, autoload_with=engine)
    tablename = table.name if type(table) is Table else table
    table = table if type(table) is Table else Table(table, metadata, **kwargs)
    return tablename, table

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  # Print SQLAlchemy version
  print(f"\nUsing SQLAlchemy (version {sqlalchemy_version})\n")
  
  # Define global vars (user, password, database and schema)
  user, passwd = 'dida', 'didapass'
  database, schema = 'didattica', 'segreteria'
  
  # Create a TABUtility instance
  handler = TABUtility(database).as_user(user,password=passwd)
  
  # Set the schema to work on
  handler.with_schema(schema)
  
  # List tables defined in schema 'segreteria'
  handler.display_table_schemas()
    
  # Display the content of table 'studenti'
  handler.display_table_content('studenti')

# -----------------------------------------------------------------------------
