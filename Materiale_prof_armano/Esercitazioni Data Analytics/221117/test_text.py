#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 11:23:34 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy import text, create_engine


# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  # Define global vars (user, password, database and schema)
  user, passwd = 'dida', 'didapass'
  database, schema = 'didattica', 'segreteria'

  # Set the URL for accessing the database
  url = f'postgresql+psycopg2://{user}:{passwd}@localhost/didattica'
  
  # Create engine and metadata
  engine = create_engine(url, echo=False)

  # Perform the query and print results
  query = text("select * from studenti where cognome = :cognome")
  query = query.bindparams(cognome='Rossi')
  with engine.connect() as connection:
    connection.execute("set schema 'segreteria'")
    result = connection.execute(query)
  for item in result: print(item)

# -----------------------------------------------------------------------------

