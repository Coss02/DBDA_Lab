#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 11:23:34 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy import create_engine

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  # Define global vars (user, database and schema)
  user, passwd = 'dida', 'didapass'
  database, schema = 'didattica', 'segreteria'

  # Set the URL for accessing the database
  url = f'postgresql+psycopg2://{user}:{passwd}@localhost/didattica'
  
  # Create engine and metadata
  engine = create_engine(url, echo=False)
  
  # Execute a "raw" SQL query (no ORM)
  with engine.connect() as connection:
     query = "select * from segreteria.studenti"
     students = connection.execute(query)
     
  # Display studenti
  for student in students: print(student)

# -----------------------------------------------------------------------------

