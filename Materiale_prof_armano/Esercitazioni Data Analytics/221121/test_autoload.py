#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 11:23:34 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy import select

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  # Define global vars (user, password, database, schema, etc.)
  user, passwd = 'dida', 'didapass'
  database, schema = 'didattica', 'segreteria'
  
  dialect, driver = 'postgresql', 'psycopg2'
  host, port = 'localhost', 5432 # 5432 is the default port...

  # Set the URL for accessing the database
  url = f'{dialect}+{driver}://{user}:{passwd}@{host}:{port}/{database}'
  
  # Create engine and metadata
  engine = create_engine(url, echo=False)
  metadata = MetaData(schema=schema, bind=engine)
  
  # Get info about the table 'studenti' and display it
  students = Table("studenti", metadata, autoload=True)
  # See also sqlalchemy.inspect to printout a table
  print("*** Info about the table 'studenti' ***", repr(students), "\n")
  
  # Set the query using the SQLAlchemy Core
  query = select(students) ; print("*** This is the query ***", query, "\n") 

  # Get the content of the table 'studenti' (needs a connection)
  with engine.connect() as connection:
    items = connection.execute(query)
  
  # Print the result returned by the DBAPI
  print("*** This is the query result ***")
  for item in items: print(item)
  print()

# -----------------------------------------------------------------------------

