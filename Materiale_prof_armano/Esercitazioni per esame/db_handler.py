#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 10:38:04 2022

@author: armano
"""

# -----------------------------------------------------------------------------

from sqlalchemy            import  create_engine, MetaData

# -----------------------------------------------------------------------------

from utils                 import settings

# -----------------------------------------------------------------------------

class DBHandler(object):
  
  "Simple handler for connecting to a database"
  
  def __init__(self, database, schema):
    "Init the handler for the given schema"
    self.database, self.schema = database, schema
    self.dialect, self.driver = 'postgresql', 'psycopg2'
    self.host, self.url = None, None
    self.user, self.passwd = None, None
    self.engine, self.metadata = None, None
    self.url = None

  def as_user(self, user, passwd, host='localhost', echo=False):
    "Create the global engine and metadata"
    self.host = host
    self.user, self.passwd = user, passwd
    search_path = settings(options=f'-csearch_path={self.schema}')
    dialect, driver = self.dialect, self.driver
    host, database = self.host, self.database
    self.url = f'{dialect}+{driver}://{user}:{passwd}@{host}/{database}'
    self.engine = create_engine(self.url, connect_args=search_path, echo=echo)
    self.metadata = MetaData(bind=self.engine)
    return self
    
# -----------------------------------------------------------------------------

if __name__ == '__main__':
  
  dbase = DBHandler('didattica', 'prodotti').as_user('dida', 'didapass')
  
# -----------------------------------------------------------------------------