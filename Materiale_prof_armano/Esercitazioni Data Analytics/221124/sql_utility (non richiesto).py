#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 15:16:22 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy import __version__ as sqlalchemy_version

from sqlalchemy import select

# -----------------------------------------------------------------------------

from table_utility import TABUtility # see file table_utility.py

# -----------------------------------------------------------------------------

class SQLUtility(TABUtility):
  
  "Handler for multiple SQL raw / Expr. Language queries"
  
  # After execute queries and answers are saved to saved_queries and saved_answers
  # __call__ = operator() can be used to retrieve queries and answers

  def __init__(self, database):
    "Init the handler" 
    super().__init__(database)
    self.queries, self.answers = list(), list()
    self.saved_queries, self.saved_answers = list(), list()

  def __lshift__(self, query):
    "Embed a query (either raw or in Core format)"
    self.queries += [ query ]
    return self

  def __call__(self):
    "Returns the last queries and answers (check on the length of queries)"
    queries, answers = self.queries, self.answers
    if len(queries) == 0: return None, None # no queries and answers
    elif len(self.queries) == 1: return queries[0], answers[0] # one query and answer
    else: return queries, answers # multiple queries and answers

  def execute(self):
    "Execute all queries and return all the answers"
    assert len(self.queries) > 0
    self.answers = list()
    with self.engine.connect() as connection:
      self.answers += [ connection.execute(query) for query in self.queries ]
    # Now method the current queries and answers must be saved and then reset
    self.saved_queries, self.saved_answers = self.queries, self.answers
    self.queries, self.answers = list(), list() # RESET queries and answers
    return self() # delegation to __call__
 
  def display_queries(self, comment='display queries'):
    "Display multiple queries"
    print(f"\n*** {comment} ***\n")
    for k, query in enumerate(self.saved_queries): self.display_query(at=k)

  def display_answers(self, comment='display answers'): 
    "Display multiple answers (from multiple queries)"
    print(f"\n*** {comment} ***\n")
    for k, answer in enumerate(self.saved_answers): self.display_answer(at=k)
    print()

  def display_query(self, comment='', at=-1):
    "Display the k-th query"
    if comment: print(f"\n*** {comment} ***\n")
    print(self.saved_queries[at]) ; print()
  
  def display_answer(self, comment='', at=-1):
    "Display the k-th answer"
    if comment: print(f"\n*** {comment} ***\n")
    for item in self.saved_answers[at]: print(item)
    print()

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  # ---------------------------------------------------------------------------

  # Print SQLAlchemy version
  print(f"\n*** Using SQLAlchemy (version {sqlalchemy_version}) ***\n")
  
  # Define global vars (user, database and schema)
  user, password = 'dida', 'didapass'
  database, schema = 'didattica', 'segreteria'
  
  # Create an SQLUtility instance
  dbms = SQLUtility(database).as_user(user,password).with_schema(schema)
  
  # Display table schemas
  dbms.display_table_schemas("all table schemas follow")
  
  # --------- DEALING WITH SINGLE QUERIES -------------------------------------

  # Run a query in SQL mode (select-from-where) and display it
  dbms << "select * from segreteria.corsi where nome='Algebra'"
  query1, answer1 = dbms.execute()
  dbms.display_query("Just selected 'Algebra' (using raw SQL)...")
  dbms.display_answer("Result (from raw SQL)")
  
  # Run the same query using SQL Expr. Language and display it
  corsi = dbms.table('segreteria.corsi')
  dbms << select(corsi).where(corsi.columns.nome=='Algebra')
  query2, answer2 = dbms.execute()
  dbms.display_query("Just selected 'Algebra' (using the SQL Core)...")
  dbms.display_answer("Result (from SQL Expr. Language)")
  
  # --------- DEALING WITH MULTIPLE QUERIES -----------------------------------

  # Create a query in RAW mode (select-from-where in SQL)
  query3 = "select C.cod_corso, C.nome, E.studente, E.data, E.voto \
              from segreteria.esami as E, segreteria.corsi as C, segreteria.studenti as S \
              where E.studente=S.matricola and E.corso = C.cod_corso and C.nome='Programmazione'"
  # With schema set to 'segreteria' the query would be:
  # select C.cod_corso, C.nome, E.studente, E.data, E.voto
  #   from esami as E, corsi as C, studenti as S 
  #   where E.studente=S.matricola and E.corso = C.cod_corso and C.nome='Algebra'
  
  # Create the same query using the SQL Expression Language
  corsi, esami, studenti = dbms.tables('corsi', 'esami', 'studenti')
  
  attributes = [ corsi.c.cod_corso, corsi.c.nome, 
                 esami.c.studente, esami.c.data, esami.c.voto ]
  
  view = studenti.join(esami, studenti.c.matricola == esami.c.studente) \
                 .join(corsi, esami.c.corso==corsi.c.cod_corso)
  
  query4 = select(attributes) \
             .select_from(view) \
             .where(corsi.c.nome=='Programmazione')

  # Store the queries into the handler
  dbms << query3 << query4

  # Display the last queries and run them
  queries34, answers34 = dbms.execute()
  dbms.display_queries("Queries 3 and 4")
  dbms.display_answers("The corresponding answers follow")
  
  # ---------------------------------------------------------------------------

# -----------------------------------------------------------------------------
