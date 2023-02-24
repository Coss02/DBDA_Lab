#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 19:01:53 2022

@author: armano
"""
# -----------------------------------------------------------------------------

from sqlalchemy      import Table, select, except_
from sqlalchemy      import func
from sqlalchemy      import text

# -----------------------------------------------------------------------------

from db_handler      import DBHandler

from utils           import display_table_info, display_result

# -----------------------------------------------------------------------------

from operator        import itemgetter

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  # Create engine and metadata

  dbase = DBHandler('didattica', 'prodotti').as_user('dida', 'didapass')
  
  engine, metadata = dbase.engine, dbase.metadata

  # --- Domanda n. 1 ----------------------------------------------------------
  # --- Sottoporre alla DBAPI delle query SQL in formato testuale (stringa) ---
  
  # Eseguo una query SQL in formato stringa
  
  print("\n*** Domanda n. 1 ***")
  
  with engine.connect() as connection:
     query = "select * from magazzino" # vedi 'connect_args' di 'create_engine'
     magazzini = connection.execute(query)

  print("\nSQL query con stringa...")
  for magazzino in magazzini: print(magazzino)
  
  # Eseguo una query SQL con istanze della classe 'sqlalchemy.text'

  with engine.connect() as connection:
     query = text("select * from magazzino") # text è utile quando ci sono params
     magazzini = connection.execute(query)

  print("\nSQL query con istanze della classe 'text'...")
  for magazzino in magazzini: print(magazzino)
  
  # --- Domanda n. 2 ----------------------------------------------------------
  # --- Definire 'magazzino', 'prodotto' e 'inventario' -----------------------
  
  print("\n*** Domanda n. 2 ***")
  
  magazzino = Table('magazzino', metadata, autoload_with=engine)
  prodotto = Table('prodotto', metadata, autoload_with=engine)
  inventario = Table('inventario', metadata, autoload_with=engine)
  
  P, I, M = prodotto, inventario, magazzino # set alias (vedi sotto)...
  
  # Stampo le info sulle varie tabelle
  for table in (magazzino, prodotto, inventario): display_table_info(table)

  # --- Domanda n. 3 ----------------------------------------------------------
  # --- Prodotti presenti nel magazzino 'M05' in quantità maggiore di 30 ------
  
  print("\n*** Domanda n. 3 ***")
  
  with engine.connect() as connection:
     query = select(P,I.c.quantita) \
               .where(P.c.codp == I.c.prodotto) \
               .where((I.c.magazzino == 'M05') & (I.c.quantita > 30))
     risultato = connection.execute(query)

  commento = "Prodotti nel magazzino 'M05' in quantità superiore alle 30 unità"
  display_result(risultato, comment=commento)
  
  
  # --- Domanda n. 4 ----------------------------------------------------------
  # --- Prodotti disponibili al magazzino 'M01', raggruppati per categoria ----
  
  print("\n*** Domanda n. 4 ***")
  
  with engine.connect() as connection:
     query = select(P.c.categoria,P.c.codp, I.c.quantita) \
               .where((P.c.codp == I.c.prodotto) & (I.c.magazzino == 'M01')) \
               .order_by(P.c.categoria, P.c.codp)
     risultato = connection.execute(query)

  commento = "Prodotti disponibili al magazzino 'M01'"
  display_result(risultato, comment=commento)
  
  # --- Domanda n. 5 ----------------------------------------------------------
  # --- Prodotti assenti dai magazzini ----------------------------------------
  
  print("\n*** Domanda n. 5 ***")
  
  # Soluzione (a) con 'inner' select
  
  with engine.connect() as connection:
     query = select(P).where(~P.c.codp.in_(select(I.c.prodotto)))  
     risultato = connection.execute(query)

  commento = "Prodotti assenti dai magazzini (sol. a)"
  display_result(risultato, comment=commento)
  
  # Soluzione (b) con operazioni insiemistiche (except)
  
  with engine.connect() as connection:
     query = except_(select(P), select(P).where(I.c.prodotto==P.c.codp))
     risultato = connection.execute(query)

  commento = "Prodotti assenti dai magazzini (sol. b)"
  display_result(risultato, comment=commento)
  
  # --- Domanda n. 6 ----------------------------------------------------------
  # --- Elettrodomestici assenti in qualche magazzino -----------
  # --- (per ognuno di tali prodotti indicare i magazzini che ne sono sprovvisti)
  
  print("\n*** Domanda n. 6 ***")

  with engine.connect() as connection:
    
     elettrodomestici = select(P.c.codp.label('prodotto'), M.c.codm.label('magazzino')) \
                         .select_from(P.join(M, True)) \
                         .where(P.c.categoria=='elettrodomestici')
     query = except_(elettrodomestici, select(I.c.prodotto, I.c.magazzino)) \
               .order_by(I.c.prodotto, I.c.magazzino)
     risultato = connection.execute(query)

  commento = "Elettrodomestici assenti in qualche magazzino"
  display_result(risultato, comment=commento)

  # --- Domanda n. 7 ----------------------------------------------------------
  # --- Prodotti non disponibili in almeno 60 unità complessive ---------------

  print("\n*** Domanda n. 7 ***")
  
  with engine.connect() as connection:
    
    # Recupera l'insieme dei prodotti assenti da qualunque magazzino
    assenti = select(P.c.codp.label('prodotto')) \
                .select_from(P.join(I, P.c.codp == I.c.prodotto, isouter=True)) \
                .where(I.c.magazzino == None)
    assenti = [ (x[0],0) for x in connection.execute(assenti).all() ]
    
    # Recupera i totali dei prodotti presenti in magazzino (in quantita < 60)
    disponibilita = select(I.c.prodotto, func.sum(I.c.quantita).label('totale')) \
                      .group_by(I.c.prodotto).subquery()
    query = select(disponibilita).where(disponibilita.c.totale < 60)
    disponibilita = connection.execute(query).all()
    
    # Unisco le due liste
    risultato = sorted(assenti + disponibilita, key=itemgetter(0))

  commento = "Prodotti non disponibili in almeno 60 unità complessive"
  display_result(risultato, comment=commento)

# -----------------------------------------------------------------------------
 