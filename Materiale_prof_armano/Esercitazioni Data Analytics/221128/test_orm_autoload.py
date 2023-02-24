#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 11:32:26 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy import create_engine, MetaData, Table

from sqlalchemy.orm import Session

from sqlalchemy.ext.declarative import declarative_base

# -----------------------------------------------------------------------------

def settings(**kwargs): return kwargs

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

  # create an in-memory skeleton for the database table 'studenti'
  metadata = MetaData(bind=engine, schema='segreteria')
  kwargs = settings(autoload_with=engine, autoload=True)
  skstudente = Table('studenti', metadata, **kwargs)
  
  # create table Studente (declarative style with '__table__')

  Base = declarative_base(metadata=metadata) # generate the 'Base' class

  class Studente(Base):
    
    __table__ = skstudente # better to use '__tablename__', however...
    
    def __str__(self):
      slots = ( 'matricola', 'cognome', 'nome', 'data_nascita', 'anno_corso' )
      return ", ".join([ f"{slot}: {getattr(self,slot)}" for slot in slots ])
  
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
