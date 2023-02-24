#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 13:46:42 2022

@author: armano
"""

# -----------------------------------------------------------------------------
# ---------- REF. TO ESERCITAZIONE ORM 1 (SQL Alchemy CORE) -------------------
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------

def settings(**kwargs): return kwargs

# -----------------------------------------------------------------------------

if __name__ == '__main__':   
  
  # ---------------------------------------------------------------------------

  from sqlalchemy import MetaData, Table
  
  from sqlalchemy import func

  from sqlalchemy import create_engine, select, insert
  
  # ---------- SET GLOBAL VARS -------------------------------------------------
  
  # Global info
  user, passwd = "dida", "didapass"
  dialect, driver = "postgresql", "psycopg2"
  host, port = 'localhost', 5432
  database = "didattica"

  # ---------- CREATE ENGINE, METADATA AND SET SCHEMA -------------------------

  # Create an engine
  url = f"{dialect}+{driver}://{user}:{passwd}@{host}:{port}/{database}"
  engine = create_engine(url,echo=False)

  # Create a MetaData object
  
  metadata = MetaData(schema='segreteria', bind=engine)

  # ---------- DEFINE TABLES (CORE LEVEL) -------------------------------------

  studenti = Table('studenti', metadata, autoload=True)
  esami = Table('esami', metadata, autoload=True)
  corsi = Table('corsi', metadata, autoload=True)
  docenti = Table('docenti', metadata, autoload=True)
  
  # ---------- QUESTION 1 -----------------------------------------------------
  
  # Print out all students
  print("\n^^^ Domanda 1 ^^^")
  with engine.connect() as connection:
    print("Elenco di tutti gli studenti")
    for s in connection.execute(select(studenti)):
      print(s.matricola, s.cognome, s.nome, s.data_nascita, s.anno_corso)
  
  # ---------- QUESTION 2 -----------------------------------------------------
  
  # Print out all students, provided that their 'anno_corso' is 3"
  print("\n^^^ Domanda 2  ^^^")
  with engine.connect() as connection:
    print("Elenco studenti iscritti al terzo anno di corso")
    query = select(studenti).where(studenti.c.anno_corso == 3)
    for s in connection.execute(query):
      print(s.matricola, s.cognome, s.nome, s.data_nascita, s.anno_corso)

  # ---------- QUESTION 3 -----------------------------------------------------

  # Add some exams and see what happens with the relationships
  print("\n^^^ Domanda 3 ^^^")
  with engine.connect() as connection:
    if False: # set to True or False, just make it once...
      values = settings(studente='451100',corso='C04',data="2022-04-21",voto=27)
      connection.execute(insert(esami).values(values))
      values = settings(studente='438984',corso='C06',data="2022-06-11",voto=28)
      connection.execute(insert(esami).values(values))
      values = settings(studente='424200',corso='C02',data="2022-10-13",voto=30)
      connection.execute(insert(esami).values(values))
      # now printing the content of table esami
    print("Elenco esami (complessivo)")
    for esame in connection.execute(select(esami)): print(esame)

  # ---------- QUESTION 4 -----------------------------------------------------
  
  # Get the list of 'esami' for student '424200'
  print("\n^^^ Domanda 4 ^^^")
  with engine.connect() as connection: 
    query = select(esami).join(studenti) \
                 .where((esami.c.studente == studenti.c.matricola) & \
                        (studenti.c.matricola=='424200'))
    print("Esami dello studente con matricola = '424200'")
    for esame in connection.execute(query): print(esame)

  # ---------- QUESTION 5 -----------------------------------------------------
  
  # Get the list of students that gave at least an exam
  print("\n^^^ Domanda 5 ^^^")
  with engine.connect() as connection:
    print("Lista di studenti con almeno un esame")
    query = select(studenti, func.count(studenti.c.matricola).label('numero_esami')) \
              .join(esami, esami.c.studente == studenti.c.matricola) \
              .group_by(studenti.c.matricola)
    for row in connection.execute(query):
      item = dict(row)
      numero_esami = item['numero_esami'] ; del item['numero_esami']
      print(tuple(item.values()), ", numero esami:", numero_esami)

  # ---------- QUESTION 6 -----------------------------------------------------
  
  # Get the list of students that gave a specific exam
  print("\n^^^ Domanda 6 ^^^")
  with engine.connect() as connection:
    E, C = esami, corsi # defining shortcuts...
    corso = connection.execute(select(corsi).where(corsi.c.cod_corso=='C06'))
    corso = corso.fetchone() ; nome_corso = dict(corso)['nome']
    query = select(E).where(E.c.corso == C.c.cod_corso) \
                     .where(C.c.cod_corso == 'C06')
    print(f"Esami dati del corso 'C06' ({nome_corso})")
    for item in connection.execute(query): print(item)

  # ---------- QUESTION 7 -----------------------------------------------------
  
  # Get the number of exams for each student (from the database)
  print("\n^^^ Domanda 7 ^^^")
  with engine.connect() as connection:
    S, E = studenti, esami # defining shortcuts...
    query = select(S, func.count(E.c.corso).label('numero_esami')) \
              .where((E.c.studente==S.c.matricola) & (E.c.corso==C.c.cod_corso)) \
              .group_by(S.c.matricola).order_by(S.c.cognome, S.c.nome)
    print("Numero esami dati da ogni studente")
    for row in connection.execute(query):
      item = dict(row)
      matricola, cognome, nome = item['matricola'], item['cognome'], item['nome']
      numero_esami = item['numero_esami']
      print(matricola, cognome, nome, "numero esami:", numero_esami)

  # ---------- QUESTION 8 -----------------------------------------------------
  
  # Get the number of exams given for each course (from the database)
  print("\n^^^ Domanda 8 ^^^")
  with engine.connect() as connection:
    E, C = esami, corsi # defining shortcuts...
    query = select(C, func.count(E.c.corso).label('numero_esami')) \
              .where(E.c.corso==C.c.cod_corso) \
              .group_by(C.c.cod_corso).order_by(C.c.nome)
    print("Numero esami dati per ogni corso")
    for row in connection.execute(query):
      item = dict(row)
      nome_corso, cod_corso = item['nome'], item['cod_corso']
      numero_esami = item['numero_esami']
      print(f"{nome_corso} ({cod_corso}) = {numero_esami}")
      
# -----------------------------------------------------------------------------

