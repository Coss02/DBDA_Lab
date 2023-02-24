#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 19:01:53 2022

@author: armano
"""
# -----------------------------------------------------------------------------

from sqlalchemy                  import Column, String, Integer, Float
from sqlalchemy                  import ForeignKey, CheckConstraint
from sqlalchemy                  import select
from sqlalchemy                  import func

from sqlalchemy.sql.expression   import literal

from sqlalchemy.orm              import sessionmaker

from sqlalchemy.ext.declarative  import declarative_base

# -----------------------------------------------------------------------------

from db_handler                  import DBHandler

from base_model                  import BaseModel

from utils                       import display_result, flatten

# -----------------------------------------------------------------------------

from operator                    import itemgetter

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  # Create engine and metadata

  dbase = DBHandler('didattica', 'prodotti').as_user('dida', 'didapass')
  
  engine, metadata = dbase.engine, dbase.metadata

  # --- Domanda n. 1 ----------------------------------------------------------
  # --- Definire la classe BaseModel (da cui sarà derivata la classe Base) ----

  print("\n*** Domanda n. 1 ***")
  
  # Vedere definizione di BaseModel sopra...
  
  Base = declarative_base(cls=BaseModel, metadata=metadata)
  
  Session = sessionmaker(bind=engine)
  
  print(f"\nLa classe {BaseModel} è stata definita")
  
  # --- Domanda n. 2 ----------------------------------------------------------
  # --- Definire 'Magazzino', 'Prodotto' e 'Inventario' -----------------------
  
  print("\n*** Domanda n. 2 ***")
  
  class Magazzino(Base):
    
    __tablename__ = 'magazzino'
    
    codm = Column(String, primary_key=True)
    indirizzo = Column(String, nullable=False)
    citta = Column(String, nullable=False)
    
  class Prodotto(Base):
    
    __tablename__ = 'prodotto'
    
    codp = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    
  class Inventario(Base):
    
    __tablename__ = 'inventario'
  
    prodotto  = Column(String, ForeignKey('prodotto.codp'), primary_key=True)
    magazzino = Column(String, ForeignKey('magazzino.codm'), primary_key=True)
    quantita  = Column(Integer, CheckConstraint('quantita > 0'))
    prezzo    = Column(Float, CheckConstraint('prezzo > 0'))
  
  # Stampo info sulle classi ORM appena create
  for cls in (Magazzino, Prodotto, Inventario): cls.describe()

  # Definisco degli alias per le classi appena definite
  M, P, I = Magazzino, Prodotto, Inventario
  
  # Si possono definire anche verui e propri alias:
  # from sqlalchemy.orm              import aliased
  # M, P, I = aliased(Magazzino), aliased(Prodotto), aliased(Inventario)  

  # Verifico che __call__ e __str__ funzionino
  with Session() as session:
    M01 = session.query(M).where(M.codm=='M01').one()

  print("\nDati M01 (uso __call__):", M01('codm','indirizzo',dtype=dict))
  print("\nDati M01 (uso __str__):", M01) # argomento di print: M01 --> str(M01)

  # --- Domanda n. 3 ----------------------------------------------------------
  # --- Prodotti presenti nel magazzino 'M05' in quantità maggiore di 30 ------
  
  print("\n*** Domanda n. 3 ***")
  
  with Session() as session:
    risultato = session.query(P.codp, P.nome, P.categoria, I.quantita) \
                  .where(P.codp == I.prodotto) \
                  .where((I.magazzino == 'M05') & (I.quantita > 30))

  commento = "Prodotti nel magazzino 'M05' in quantità superiore alle 30 unità"
  display_result(risultato, comment=commento)
  
  
  # --- Domanda n. 4 ----------------------------------------------------------
  # --- Prodotti disponibili al magazzino 'M01', ordinati per categoria ----
  
  print("\n*** Domanda n. 4 ***")
  
  with Session() as session:
      risultato = session.query(P.categoria, P.codp, I.quantita) \
                .where((P.codp == I.prodotto) & (I.magazzino == 'M01')) \
                .order_by(P.categoria, P.codp)

  commento = "Prodotti disponibili al magazzino 'M01'"
  display_result(risultato, comment=commento)
  
  # --- Domanda n. 5 ----------------------------------------------------------
  # --- Prodotti assenti dai magazzini ----------------------------------------

  print("\n*** Domanda n. 5 ***")
  
  # Soluzione (a) con 'inner' select
  
  with Session() as session:
    risultato = session.query(P).where(~P.codp.in_(select(I.prodotto)))
    
  commento = "Prodotti assenti dai magazzini (sol. a)"
  display_result(risultato, commento)
    
  # Soluzione (b) con differenza di insiemi
  
  with Session() as session:
    prodotti = flatten(session.query(P.codp).all())
    presenti = flatten(session.query(I.prodotto).all())
    assenti = list( set(prodotti) - set(presenti) )
    risultato = session.query(P).where(P.codp.in_(assenti))
    risultato = sorted ( risultato, key = lambda x: x.codp )
    
  commento = "Prodotti assenti dai magazzini (sol. b)"
  display_result(risultato, comment=commento)

  # --- Domanda n. 6 ----------------------------------------------------------
  # --- Elettrodomestici assenti in qualche magazzino -----------
  # --- (per ognuno di tali prodotti indicare i magazzini che ne sono sprovvisti)
  
  print("\n*** Domanda n. 6 ***")

  with Session() as session:
    tutti = session.query(P.codp.label('prodotto'), M.codm.label('magazzino')) \
              .join(M, literal(True)).where(P.categoria == 'elettrodomestici')
    elettrodomestici  = session.query(I.prodotto, I.magazzino) \
                          .where(P.codp == I.prodotto) \
                          .where(P.categoria=='elettrodomestici')
  tutti, elettrodomestici = set(tutti), set(elettrodomestici)
  risultato = [ pair for pair in tutti if pair not in elettrodomestici ]
  
  risultato = sorted(risultato, key=itemgetter(0,1))

  commento = "Elettrodomestici assenti in qualche magazzino"
  display_result(risultato, comment=commento)

  # --- Domanda n. 7 ----------------------------------------------------------
  # --- Prodotti non disponibili in almeno 60 unità complessive ---------------

  print("\n*** Domanda n. 7 ***")
  
  with Session() as session:
      presenti = flatten(session.query(I.prodotto))
      assenti = flatten(session.query(P.codp).where(~P.codp.in_(presenti)))
      assenti = [ (x,0) for x in assenti ] # totale zero per i prodotti assenti
      disponibilita = session.query(P.codp, func.sum(I.quantita)) \
                        .join(I, P.codp == I.prodotto) \
                        .group_by(I.prodotto, P.codp).all()
      disponibilita = [ (prod,tot) for prod, tot in disponibilita if tot < 60 ]
      risultato = sorted(assenti+disponibilita, key=itemgetter(0))

  commento = "Prodotti non disponibili in almeno 60 unità complessive"
  display_result(risultato, comment=commento)

# -----------------------------------------------------------------------------
 