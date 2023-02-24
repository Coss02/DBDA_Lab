#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 11:23:34 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy import update, select

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
  
  # Get info about the table 'studenti' and display it
  students = Table("studenti", metadata, autoload=True)
  print("*** Info about the table 'studenti' ***")
  print(repr(students)) # see also sqlalchemy.inspect to printout a table
  print()
  
  # Insert a tuple into the table 'studenti'
  query = update(students). \
            where(students.c.matricola == '45825'). \
            values(matricola='458350')

  print("*** This is the query ***") 
  print(query)
  print()

  # Get the content of the table 'studenti' (needs a connection)
  with engine.connect() as connection:
    # Execute the update
    connection.execute(query)
    # Check whether the 'update' has been performed...
    print("*** This is the query result ***")
    for item in connection.execute(select(students)): print(item)
    print()

# -----------------------------------------------------------------------------

