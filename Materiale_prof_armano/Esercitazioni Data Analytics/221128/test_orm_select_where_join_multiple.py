#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 11:32:26 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy import create_engine, MetaData, ForeignKey

from sqlalchemy import Column, String, Integer, Date

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

# -----------------------------------------------------------------------------

class Formatter(object): 
  
  "Simple utility to produce printable output from a list of attributes"

  def __init__(self, *attributes):
    "Init the formatter"
    self.attributes = attributes
    self.values = None

  def __lshift__(self, values):
    "Generate a printable output from values"
    self.values = values # just for debugging...
    items = zip(self.attributes, self.values)    
    return ", ".join([ f"{attr}: {value}" for attr, value in items ])

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

class Corso(Base):
  
  __tablename__ = "corsi"
  
  cod_corso = Column(String, primary_key=True)
  nome = Column(String, nullable=False)
  docente = Column(Date, nullable=False)
  
  def __str__(self):
    slots = ( 'cod_corso', 'nome', 'docente' )
    return ", ".join([ f"{slot}: {getattr(self,slot)}" for slot in slots ])

# -----------------------------------------------------------------------------

# create table Esame (declarative style with '__tablename__')

class Esame(Base):
  
  __tablename__ = "esami"
  
  studente = Column(String, ForeignKey("studenti.matricola"), primary_key=True)
  corso = Column(String, ForeignKey("corsi.cod_corso"), primary_key=True)
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
  engine = create_engine(url, echo=False)

  # create a configured "Session" class (bound to the engine)
  Session = sessionmaker(bind=engine) # ... or import Session

  # get students that passed the exam 'C06' (with school mark)
  with Session() as session:
    print("\n^^^ Trial 1.1 ^^^")
    result = session.query(Studente, Esame.voto) \
               .join(Studente).filter(Esame.corso=='C06')
    print("\n*** Printing results (select: corso == 'C06') ***\n")
    for k, (studente,voto) in enumerate(result):
      print(f"[{k:2d}] {studente}, voto: {voto}")

  # get students that passed the exam 'C06' (with school mark)
  with Session() as session:
    print("\n^^^ Trial 1.2 ^^^")
    result = session.query(Studente, Esame.voto) \
               .join(Studente).filter(Esame.corso=='C06')
    print("\n*** Printing results (select: corso == 'C06') ***\n")
    for k, (studente,voto) in enumerate(result):
      print(f"[{k:2d}] {studente}, voto: {voto}")

  # get students that passed the exam 'C06' (some attributes)
  with Session() as session:
    print("\n^^^ Trial 2.1 ^^^")
    S, E, C = Studente, Esame, Corso # defining shortcuts...
    attributes = (S.matricola, S.cognome, S.nome, C.nome, E.voto)
    result = session.query(*attributes) \
               .join(Studente).join(Corso).filter(Esame.corso == 'C06')
    print("\n*** Printing results (select: corso == 'C06') ***\n")
    for (cognome, nome, matricola, corso, voto) in result:
      formatter = Formatter('matricola','cognome', 'nome', 'corso', 'voto')
      print(formatter << (matricola, cognome, nome, corso, voto))

  with Session() as session:
    print("\n^^^ Trial 2.2 ^^^")
    S, C, E = Studente, Corso, Esame # defining shortcuts for convenience...
    attributes = (S.matricola, S.cognome, S.nome, C.nome, E.voto)
    result = session.query(*attributes).join(S,C).filter(E.corso == 'C06')
    print("\n*** Printing results (select: corso == 'C06') ***\n")
    for matricola, cognome, nome, corso, voto in result:
      formatter = Formatter('matricola','cognome', 'nome', 'corso', 'voto')
      print(formatter << (matricola, cognome, nome, corso, voto))

# -----------------------------------------------------------------------------
