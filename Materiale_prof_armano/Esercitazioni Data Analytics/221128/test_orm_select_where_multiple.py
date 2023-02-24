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

# create table Esame (declarative style with '__tablename__')

class Esame(Base):
  
  __tablename__ = "esami"
  
  studente = Column(String, primary_key=True)
  corso = Column(String, primary_key=True)
  data = Column(Date)
  voto = Column(Integer)
  
  def __str__(self):
    slots = ( 'studente', 'corso', 'data', 'voto' )
    return ", ".join([ f"{slot}: {getattr(self,slot)}" for slot in slots ])

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  # Global info
  dialect, driver = "postgresql", "psycopg2"
  user, passwd = "dida", "didapass"
  host, port = "localhost", 5432
  database = "didattica"
  
  # create an engine
  url = f"{dialect}+{driver}://{user}:{passwd}@{host}:{port}/{database}"
  engine = create_engine(url,echo=False)

  # create a configured "Session" class (bound to the engine)
  Session = sessionmaker(bind=engine)

  # get students that passed the exam 'C06' (using 'where')
  with Session() as session:
    print("\n^^^ Trial 1 ^^^")
    constraints = (Studente.matricola==Esame.studente) & (Esame.corso == 'C06')
    results = session.query(Studente, Esame.voto).where(constraints)
    print("\n*** Printing results (old style query) ***\n")
    for k, (studente,voto) in enumerate(results):
      print(f"[{k:2d}] {studente}, voto = {voto}")

  # get students that passed the exam 'C06' (using 'filter')
  with Session() as session:
    print("\n^^^ Trial 2 ^^^")
    S, E = Studente, Esame # defining shorcuts...
    query = select(S.matricola, S.cognome, S.nome, E.voto) \
              .filter(S.matricola==E.studente & E.corso=='C06')      
    print("\n*** Printing results (new style query) ***\n")
    for k, (studente,voto) in enumerate(results):
      print(f"[{k:2d}] {studente}, voto = {voto}")

# -----------------------------------------------------------------------------
