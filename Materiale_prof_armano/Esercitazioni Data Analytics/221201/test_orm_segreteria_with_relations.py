#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 13:46:42 2022

@author: armano
"""

# -----------------------------------------------------------------------------
# ---------- REF. TO ESERCITAZIONE ORM 2 (ORM with relationships) -------------
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------

from sqlalchemy import MetaData

from sqlalchemy import ForeignKey

from sqlalchemy import Column, String, Integer, DateTime

from sqlalchemy.orm import sessionmaker, relationship

from sqlalchemy.ext.declarative import declarative_base

# ---------- QUESTION 1 (BaseModel as superclass of Base ----------------------

class BaseModel(object):
  
  __abstract__ = True
  
  def __init__(self):
    "Init the base model for ORM objects"
    self.__mapper__ = None
    
  def __call__(self, *keys, dtype=None):
    "Get specific slot values, depending on the given parameters"
    values = [ getattr(self,key) for key in keys ]
    if not dtype: return values
    return ", ".join([ str(val) for val in values ])
      
  def keys(self): # dtype not required as keys are always strings...
    "Get the keys of the ORM object"
    return self.__mapper__.columns.keys()
    
  def values(self, dtype=None):
    "Get the values of the ORM object (as string if dtype==str)"
    assert dtype in (None, str)
    keys = self.__mapper__.columns.keys()
    return self(*keys, dtype=dtype) # delegation to __call__

  def items(self, dtype=None):
    "Get keys and values of the ORM object (as string if dtype==str)"
    assert dtype in (None, str)
    keys = self.__mapper__.columns.keys()
    values = [ getattr(self,key) for key in keys ]
    if not dtype: return zip(keys,values)
    return ", ".join([ f"{key}: str(val)" for key, val in zip(keys,values) ])

  def __str__(self):
    keys = self.__mapper__.columns.keys()
    values = [ getattr(self,key) for key in keys ]
    return ", ".join([ f"{k}: {str(val)}" for (k,val) in zip(keys,values) ])
  
# -----------------------------------------------------------------------------

Base = declarative_base(cls=BaseModel, metadata=MetaData(schema="segreteria"))

# ---------- QUESTION 2 (see relationships) -----------------------------------

class Esame(Base):

    __tablename__ = "esami"

    studente = Column(String, ForeignKey("studenti.matricola"), primary_key=True)
    corso = Column(String, ForeignKey("corsi.cod_corso"), primary_key=True)
    data = Column(String, nullable=False)
    voto = Column(Integer, nullable=False)
    
    # many-to-many relationships (Esame <--> Corso, Esame <--> Studente)
    lista_studenti = relationship('Studente', back_populates='lista_esami')
    lista_corsi = relationship("Corso", back_populates="lista_esami")

# -----------------------------------------------------------------------------

class Studente(Base):

    __tablename__ = "studenti"
    
    matricola = Column(String, primary_key=True)
    cognome = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    data_nascita = Column(DateTime, nullable=False)
    anno_corso = Column(Integer, nullable=False)
    
    # many-to-many relationship (Studente <--> Esame)
    lista_esami = relationship('Esame', back_populates="lista_studenti")

# -----------------------------------------------------------------------------

class Corso(Base):

    __tablename__ = "corsi"

    cod_corso = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    docente = Column(String, ForeignKey("docenti.cod_docente"))

    # many-to-many relationship (Corso <--> Esame)
    lista_esami = relationship("Esame", back_populates="lista_corsi")

# -----------------------------------------------------------------------------

class Docente(Base):

    __tablename__ = "docenti"

    cod_docente = Column(String, primary_key=True)
    cognome = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    indirizzo = Column(String, default="")
    
    # one-to-many relationship (Docente --> Corso)
    lista_corsi = relationship('Corso') 
    
# -----------------------------------------------------------------------------

if __name__ == '__main__': 
  
  # ---------------------------------------------------------------------------

  from sqlalchemy import create_engine
  
  # ---------- SET GLOBAL VARS ------------------------------------------------
  
  # Global info
  user, passwd = "dida", "didapass"
  dialect, driver = "postgresql", "psycopg2"
  host, port = 'localhost', 5432
  database = "didattica"

  # Create an engine
  url = f"{dialect}+{driver}://{user}:{passwd}@{host}:{port}/{database}"
  engine = create_engine(url,echo=False)

  # Create the Session class (with bound engine)
  Session = sessionmaker(bind=engine)
  
  # ---------- QUESTION 3/4 ---------------------------------------------------
  
  # Get the list of 'esami' for student '424200' (from 'Studente.lista_esami')
  print("\n^^^ Domanda 4 ^^^")
  with Session() as session: 
    mat424200 = session.query(Studente).filter(Studente.matricola=='424200').one()
    print("Esami dello studente con matricola = '424200'")
    for esame in mat424200.lista_esami:
      corso = session.query(Corso).filter(Corso.cod_corso == esame.corso).one()
      print(esame.values(dtype=str), corso.nome)

  # ---------- QUESTION 3/5 ---------------------------------------------------
  
  # Get the list of students that gave at least an exam (from 'Studente.lista_esami')
  print("\n^^^ Domanda 5 ^^^")
  with Session() as session:
    print("Lista di studenti con almeno un esame")
    studenti_con_esami = list()
    for studente in session.query(Studente):
      if studente.lista_esami:
        studenti_con_esami += [ (studente, len(studente.lista_esami)) ]
    for studente, numero_esami in studenti_con_esami:
      print(studente, ", numero esami:", numero_esami)
      
  # ---------- QUESTION 3/6 ---------------------------------------------------
  
  # Get the list of students that gave a specific exam (from 'Esame.lista_studenti')
  print("\n^^^ Domanda 6 ^^^")
  with Session() as session:
    C06 = session.query(Corso).filter(Corso.cod_corso=='C06').one()
    print(f"Esami dati del corso 'C06' ({C06.nome})")
    for studente in session.query(Studente):
      for esame in studente.lista_esami: # select 'C06' from 'lista_esami'
        if esame.corso == 'C06': print(esame.values(dtype=str))

  # ---------- QUESTION 3/7 ---------------------------------------------------
  
  # Get the number of exams for each student (from 'Studente.lista_esami')
  print("\n^^^ Domanda 7 ^^^")
  S = Studente # defining shorcuts
  with Session() as session:
    print("Numero esami dati da ogni studente")
    for studente in session.query(S).order_by(S.cognome, S.nome):
      matricola, cognome, nome = studente('matricola', 'cognome', 'nome')
      print(matricola, cognome, nome, len(studente.lista_esami))

  # ---------- QUESTION 3/8 ---------------------------------------------------
  
  # Get the number of exams given for each course (from 'Corso.lista_esami')
  print("\n^^^ Domanda 8 ^^^")
  C = Corso # defining shorcuts
  with Session() as session:
    print("Numero esami dati per ogni corso")
    for corso in session.query(C).order_by(C.nome):
      print(corso.nome, corso.cod_corso, len(corso.lista_esami))
      
# -----------------------------------------------------------------------------


