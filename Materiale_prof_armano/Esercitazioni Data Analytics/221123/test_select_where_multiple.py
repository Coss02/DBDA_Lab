#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 11:23:34 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy import select, asc

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
  exams = Table("esami", metadata, autoload=True)
  students = Table("studenti", metadata, autoload=True)
  print("*** Info about the tables 'studenti' and 'esami' ***")
  print(repr(students)) # see also sqlalchemy.inspect to printout a table
  print()
  
  # Select students from the table 'studenti'
  es_view = students.join(exams, students.c.matricola == exams.c.studente)
  query = select(students).select_from(es_view) \
            .where(exams.c.corso == 'C06') \
            .order_by(asc(students.c.cognome)) # however, 'asc' is the default

  print("*** This is the query ***", query, "\n") 

  # Get the content of the table 'studenti' (needs a connection)
  with engine.connect() as connection:
    content = connection.execute(query)
  
  # Display the result of query...
  print("*** This is the query result ***")
  for item in content: print(item)
  print()

# -----------------------------------------------------------------------------

