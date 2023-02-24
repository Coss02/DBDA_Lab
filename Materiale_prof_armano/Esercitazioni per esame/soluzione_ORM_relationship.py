#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 19:01:53 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy                  import Column, String, Integer, Float
from sqlalchemy                  import ForeignKey, CheckConstraint

from sqlalchemy.orm              import sessionmaker, relationship

# -----------------------------------------------------------------------------

from sqlalchemy.ext.declarative  import declarative_base

# -----------------------------------------------------------------------------

from db_handler                  import DBHandler

from base_model                  import BaseModel

from utils                       import settings, flatten, display_result
from utils                       import make_list_difference

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  # Create engine and metadata

  dbase = DBHandler('didattica', 'prodotti').as_user('dida', 'didapass')
  
  engine, metadata = dbase.engine, dbase.metadata

  # Create the classes Base and Session
  Base = declarative_base(cls=BaseModel, metadata=metadata)
  Session = sessionmaker(bind=engine)
  
  # --- Domanda n. 2R ---------------------------------------------------------
  # --- Definire 'Magazzino', 'Prodotto' e 'Inventario' -----------------------
  
  print("\n*** Domanda n. 2R (classi con relazioni) ***")

  # Definisco prima 'Inventario' perché mi serve per le relazioni successive
  
  class Inventario(Base):
    
    __tablename__ = 'inventario'
  
    prodotto  = Column(String, ForeignKey('prodotto.codp'), primary_key=True)
    magazzino = Column(String, ForeignKey('magazzino.codm'), primary_key=True)
    quantita  = Column(Integer, CheckConstraint('quantita > 0'))
    prezzo    = Column(Float, CheckConstraint('prezzo > 0'))
  
  class Magazzino(Base):
    
    __tablename__ = 'magazzino'
    
    codm = Column(String, primary_key=True)
    indirizzo = Column(String, nullable=False)
    citta = Column(String, nullable=False)
    lista_prodotti = relationship("Prodotto", secondary=Inventario.__table__,
                                  back_populates='lista_magazzini')
    
  class Prodotto(Base):
    
    __tablename__ = 'prodotto'
    
    codp = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    lista_magazzini = relationship("Magazzino", secondary=Inventario.__table__,
                                  back_populates='lista_prodotti')

  # Stampo info sulle classi ORM appena create
  for cls in (Magazzino, Prodotto, Inventario): cls.describe()

  # Definisco degli alias per le classi appena definite
  M, P, I = Magazzino, Prodotto, Inventario
  
  # Si possono definire anche veri e propri alias:
  # from sqlalchemy.orm              import aliased
  # M, P, I = aliased(Magazzino), aliased(Prodotto), aliased(Inventario)  

  # --- Domanda n. 5R ---------------------------------------------------------
  # --- Prodotti assenti dai magazzini ----------------------------------------

  print("\n*** Domanda n. 5R ***")
  
  with Session() as session:
    assenti = [ p for p in session.query(P) if not p.lista_magazzini ]

  commento = "Prodotti assenti dai magazzini"
  display_result(assenti, comment=commento)

  # --- Domanda n. 6R ---------------------------------------------------------
  # --- Elettrodomestici assenti in qualche magazzino -----------
  # --- (per ognuno di tali prodotti indicare i magazzini che ne sono sprovvisti)

  print("\n*** Domanda n. 6R ***")

  kwargs = settings(selector=lambda x: x.codm, key=lambda x: x.codm)

  with Session() as session:
    magazzini = session.query(M).all()
    elettrodomestici = session.query(P).where(P.categoria=='elettrodomestici')
    magazzini_no_em = list()
    for e in elettrodomestici:
      em_assenti = make_list_difference(magazzini, e.lista_magazzini, **kwargs)
      magazzini_no_em += [ (e.codp, em_assenti) ]

  commento = "Elettrodomestici assenti in qualche magazzino"
  display_result(magazzini_no_em, comment=commento)

  # --- Domanda n. 7R ---------------------------------------------------------
  # --- Prodotti non disponibili in almeno 60 unità complessive ---------------

  print("\n*** Domanda n. 7R ***")

  kwargs = settings(selector=lambda x: x.codm, key=lambda x: x.codm)
  
  def conta_prodotto(prodotto, magazzini, inventario):
    "Conta quante unità di un prodotto esistono nei magazzini indicati"
    with Session() as session:
      parziali = session.query(inventario.quantita) \
                   .where(inventario.prodotto==prodotto) \
                   .where(inventario.magazzino.in_(magazzini)).all()
      totale = sum(flatten(parziali))
    return totale

  with Session() as session:
    prodotti60 = list()
    for prodotto in session.query(P):
      magazzini = [ m.codm for m in prodotto.lista_magazzini ]
      unita = conta_prodotto(prodotto.codp, magazzini, Inventario)
      if unita >= 60: continue
      prodotti60 += [ (prodotto.codp, unita) ]

  commento = "Prodotti con disponibilità inferiore alle 60 unità"
  display_result(prodotti60, comment=commento)

# -----------------------------------------------------------------------------
