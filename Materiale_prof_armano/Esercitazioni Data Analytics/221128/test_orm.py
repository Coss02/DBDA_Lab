#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 11:32:26 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy import create_engine, MetaData

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
  dialect, driver= "postgresql", "psycopg2"
  user, passwd = "dida", "didapass"
  host, port = "localhost", 5432
  database = "didattica"
  
  # create an engine
  url = f"{dialect}+{driver}://{user}:{passwd}@{host}:{port}/{database}"
  engine = create_engine(url, echo=False)

  # create a configured "Session" class (bound to the engine)
  Session = sessionmaker(bind=engine) # ... or import Session

  # print all students' info
  with Session() as session:
    students = session.query(Studente).all()
    # print students (all attributes)
    print("\n*** Printing students (all attributes) ***\n")
    for k, s in enumerate(students): print(f"[{k:2d}] {s}")

  # print some students' info
  with Session() as session:
    # print students (some attributes)
    print("\n*** Printing students (some attributes) ***\n")
    args = (Studente.matricola, Studente.cognome, Studente.nome)
    for student in session.query(*args): print(student)

# -----------------------------------------------------------------------------
