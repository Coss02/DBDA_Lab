#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 11:32:26 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy import create_engine, MetaData, select

from sqlalchemy import Column, String, Integer, Date

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

# -----------------------------------------------------------------------------

def settings(**kwargs): return kwargs

# -----------------------------------------------------------------------------

Base = declarative_base(metadata=MetaData(schema="segreteria"))

# -----------------------------------------------------------------------------

# create table Studente (declarative style with '__tablename__')

class Studente(Base):
  
  __tablename__ = "studenti"
  
  matricola = Column(String, primary_key=True)
  cognome = Column(String)
  nome = Column(String)
  data_nascita = Column(Date)
  anno_corso = Column(Integer)
  
  def __str__(self):
    slots = ( 'matricola', 'cognome', 'nome', 'data_nascita', 'anno_corso' )
    return ", ".join([ f"{slot}: {getattr(self,slot)}" for slot in slots ])

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  # Global info
  dialect, driver = "postgresql", "psycopg2"
  user, passwd = "dida", "didapass"
  host, port = 'localhost', 5432 
  database = 'didattica'
  
  # Create an engine
  url = f"{dialect}+{driver}://{user}:{passwd}@{host}:{port}/{database}"
  engine = create_engine(url,echo=False)

  # create a configured "Session" class (bound to the engine)
  Session = sessionmaker(bind=engine)

  # Get students with cognome=='Rossi' using 'execute'
  with Session() as session:
    query = select(Studente).where(Studente.cognome=='Rossi')
    print("\n*** Printing results (using 'execute') ***\n")
    for k, s in enumerate(session.execute(query)): print(f"[{k:2d}] {s[0]}")

  # Get students with cognome =='Rossi' using 'query' (BETTER)
  with Session() as session:
    students = session.query(Studente).filter(Studente.cognome == 'Rossi')
    print("\n*** Printing results (using 'query') ***\n")
    for k, student in enumerate(students): print(f"[{k:2d}] {student}")

  # Get students with cognome=='Rossi' (only some attrs) using 'execute'
  with Session() as session:
    attributes = (Studente.nome, Studente.cognome, Studente.matricola)
    query = select(*attributes).where(Studente.cognome == 'Rossi')
    print("\n*** Printing results (using 'execute') ***\n")
    for student in session.execute(query): print(student)
    
  # Get students with cognome=='Rossi' (only some attrs) using 'query' (BETTER)
  with Session() as session:
    attributes = (Studente.nome, Studente.cognome, Studente.matricola)
    students = session.query(*attributes).filter(Studente.cognome == 'Rossi')
    print("\n*** Printing results (using 'query') ***\n")
    for student in students: print(student)

# -----------------------------------------------------------------------------
