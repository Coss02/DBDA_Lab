#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 13:46:42 2022

@author: armano
"""
# -----------------------------------------------------------------------------
# ---------- REF. TO ESERCITAZIONE ORM 1 (ORM no-relationships) ---------------
# -----------------------------------------------------------------------------

from sqlalchemy import MetaData

from sqlalchemy import ForeignKey

from sqlalchemy import Column, String, Integer, DateTime

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

# -----------------------------------------------------------------------------

Base = declarative_base(metadata=MetaData(schema="segreteria"))

# -----------------------------------------------------------------------------

class Esame(Base):

    __tablename__ = "esami"

    studente = Column(String, ForeignKey("studenti.matricola"), primary_key=True)
    corso = Column(String, ForeignKey("corsi.cod_corso"), primary_key=True)
    data = Column(String, nullable=False)
    voto = Column(Integer, nullable=False)
    
# -----------------------------------------------------------------------------

class Studente(Base):

    __tablename__ = "studenti"
    
    matricola = Column(String, primary_key=True)
    cognome = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    data_nascita = Column(DateTime, nullable=False)
    anno_corso = Column(Integer, nullable=False)
    
# -----------------------------------------------------------------------------

class Corso(Base):

    __tablename__ = "corsi"

    cod_corso = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    docente = Column(String, ForeignKey("docenti.cod_docente"))

# -----------------------------------------------------------------------------

class Docente(Base):

    __tablename__ = "docenti"

    cod_docente = Column(String, primary_key=True)
    cognome = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    indirizzo = Column(String, default="")
    
# -----------------------------------------------------------------------------

if __name__ == '__main__': 
  
  # ---------------------------------------------------------------------------

  from sqlalchemy import create_engine, func

  # ---------------------------------------------------------------------------
  
  # Utility for printing ORM rows (optional)

  def display_item(row, astype='dict', end='\n'):
    "Display an ORM row (typically resulting from a session.query)"
    assert astype in ('dict', 'values', 'string')
    keys = tuple([ k.name for k in row.__mapper__.columns])
    values = tuple([ getattr(row,k) for k in keys ])
    items = list(zip(keys,values))
    if astype == 'dict': to_print = dict(items)
    elif astype == 'values': to_print = values
    elif astype == 'string': to_print = ", ".join([f"{k}: {v}" for k,v in items])
    print(to_print, end=end)

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
  
  # ---------- QUESTION 1 -----------------------------------------------------
  
  # Print out all students
  print("\n^^^ Domanda 1 ^^^")
  with Session() as session:
    print("Elenco di tutti gli studenti")
    for s in session.query(Studente):
      print(s.matricola, s.cognome, s.nome, s.data_nascita, s.anno_corso)
  
  # ---------- QUESTION 2 -----------------------------------------------------
  
  # Print out all students, provided that their 'anno_corso' is 3"
  print("\n^^^ Domanda 2 ^^^")
  with Session() as session:
    S = Studente # defining a shortcut...
    print("Elenco studenti iscritti al terzo anno di corso") 
    for s in session.query(S).filter(S.anno_corso==3):
      print(s.matricola, s.cognome, s.nome, s.data_nascita, s.anno_corso)

  # ---------- QUESTION 3 -----------------------------------------------------

  # Add some exams
  print("\n^^^ Domanda 3 ^^^")
  with Session() as session:
    if False: # set to True or False -- just make it once (then set to False)
      print("Aggiungiamo qualche esame al database")
      session.add(Esame(studente='451100',corso='C04',data="2022-04-21",voto=27))
      session.add(Esame(studente='438984',corso='C06',data="2022-06-11",voto=28))
      session.add(Esame(studente='424200',corso='C02',data="2022-10-13",voto=30))
      session.commit()
    print("Elenco esami (complessivo)")
    for esame in session.query(Esame): display_item(esame, astype='string')

  # ---------- QUESTION 4 -----------------------------------------------------
  
  # Get the list of 'esami' for student '424200'
  print("\n^^^ Domanda 4 ^^^")
  with Session() as session: 
    esami_studente = session.query(Esame, Studente) \
                       .filter(Studente.matricola == Esame.studente) \
                       .filter(Studente.matricola=='424200')
    print("Esami dello studente con matricola = '424200'")
    for esame, studente in esami_studente:
      corso = session.query(Corso).filter(Corso.cod_corso == esame.corso).one()
      display_item(esame, end='') ; print(corso.nome)

  # ---------- QUESTION 5 -----------------------------------------------------
  
  # Get the list of students that gave at least an exam
  print("\n^^^ Domanda 5 ^^^")
  with Session() as session:
    S, E = Studente, Esame
    print("Lista di studenti con almeno un esame")
    result = session.query(S, func.count(E.corso).label('numero_esami')) \
                .join(E).group_by(S)
    for studente, numero_esami in result:
      display_item(studente, astype='string', end=', ')
      print("numero_esami:", numero_esami)
      
  # ---------- QUESTION 6 -----------------------------------------------------
  
  # Get the list of students that gave a specific exam
  print("\n^^^ Domanda 6 ^^^")
  with Session() as session:
    S, E, C = Studente, Esame, Corso # defining shortcuts...
    esami = session.query(S, E) \
              .where((E.studente==S.matricola) & (E.corso==C.cod_corso)) \
              .where(C.cod_corso=='C06')
    C06 = session.query(Corso).filter(Corso.cod_corso == 'C06').one()
    print(f"Esami dati del corso 'C06' ({C06.nome})")
    for studente, esame in esami:
      print(studente.matricola, esame.corso, esame.data, esame.voto)

  # ---------- QUESTION 7 -----------------------------------------------------
  
  # Get the number of exams for each student
  print("\n^^^ Domanda 7 ^^^")
  with Session() as session:
    S, E = Studente, Esame # defining shortcuts...
    result = session.query(S, func.count(E.corso)) \
              .where((E.studente==S.matricola) & (E.corso==C.cod_corso)) \
              .group_by(S.matricola).order_by(S.cognome, S.nome)
    print("Numero esami dati da ogni studente")
    for studente, numero_esami in result:
      matr, cognome, nome = studente.matricola, studente.cognome, studente.nome
      print(matr, cognome, nome, numero_esami)

  # ---------- QUESTION 8 -----------------------------------------------------
  
  # Get the number of exams given for each course
  print("\n^^^ Domanda 8 ^^^")
  with Session() as session:
    E, C = Esame, Corso # defining shortcuts...
    result = session.query(C, func.count(E.corso)) \
              .where(E.corso==C.cod_corso) \
              .group_by(C.cod_corso).order_by(C.nome)
    print("Numero esami dati per ogni corso")
    for corso, numero_esami in result:
      print(corso.nome, corso.cod_corso, numero_esami)
      
# -----------------------------------------------------------------------------
