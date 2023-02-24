#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 11:23:34 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy import MetaData, create_engine
from sqlalchemy import Table, Column, String, Integer, DateTime
from sqlalchemy import select

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  # Define global vars (user, password, database and schema)
  user, passwd = 'dida', 'didapass'
  database, schema = 'didattica', 'segreteria'

  # Set the URL for accessing the database
  url = f'postgresql+psycopg2://{user}:{passwd}@localhost/{database}'
  
  # Create engine and metadata
  engine = create_engine(url, echo=False)
  metadata = MetaData(schema=schema, bind=engine)
  
  # Create columns for table 'studenti'
  columns = ( Column('matricola', String(6)),
              Column('cognome', String(20)),
              Column('nome', String(20)),
              Column('data_nascita', DateTime),
              Column('anno_corso', Integer) )

  # Create table 'studenti'
  students = Table("studenti", metadata, *columns)
  
  # Print info about the table 'studenti'
  print("*** Info about the table 'studenti' ***", repr(students), "\n")
  
  # Set the query using the SQLAlchemy Core
  query = select(students)
  print("*** This is the query ***", query, "\n") 

  # Get the content of the table 'studenti' (needs a connection)
  with engine.connect() as connection:
    content = connection.execute(query)
  
  # Print the result returned by the DBAPI
  print("*** This is the query result ***")
  for item in content: print(item)
  print()

# -----------------------------------------------------------------------------

