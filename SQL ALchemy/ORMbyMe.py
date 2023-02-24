from sqlalchemy import create_engine,MetaData,Column,String,Date,ForeignKey,SmallInteger,CheckConstraint, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select
from sqlalchemy import or_, and_

Base = declarative_base(metadata=MetaData(schema="segreteria"))
class Studente(Base):
    __tablename__="studenti"
    matricola=Column(String,primary_key = True)
    cognome=Column(String,nullable=False)
    nome=Column(String,nullable=False)
    data_nascita=Column(Date,nullable=False);
    anno_corso = Column(SmallInteger, CheckConstraint('anno_corso>=1', 'anno_corso<=3'),nullable=False)
class Corso(Base):
    __tablename__="corso"
    cod_corso=Column(String,primary_key=True)
    nome=Column(String,nullable=False)
    docente=Column(String,ForeignKey("docenti.cod_docente"))
class Docente(Base):
    __tablename__="docenti"
    coddocente=Column(String,primary_key=True)
    cognome=Column(String,nullable=False)
    nome=Column(String,nullable=False)
    num_telefono=Column(String)
    
class Esame(Base):
    __tablename__="esami"
    studente=Column(String,ForeignKey("segreteria.studenti"),primary_key=True)
    corso=Column(String,ForeignKey("segreteria.corsi"),primary_key=True)
    data_=Column(Date,nullable=False)
    voto=Column(SmallInteger)
    
if __name__=="__main__":
    user, passwd = 'marcocosseddu', '1234'
    database, schema = 'marcocosseddu', 'segreteria'
# Set the URL for accessing the database
    url = f'postgresql+psycopg2://{user}:{passwd}@localhost:5432/{database}'
    engine = create_engine(url = url, echo= False)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        results = session.query(Studente)
        for s in results:
            print(s.matricola, s.cognome,s.nome,s.data_nascita, s.anno_corso)
        print()
        
    with Session() as session:
        esamiStudente = session.query(Esame,Studente).filter(Studente.matricola==Esame.studente).filter(Studente.matricola == '424200')
        for esame,studente in esamiStudente:
            print(esame.studente, esame.corso, esame.voto)
        print()
    
    with Session() as session:
        query1 = session.query(Esame).where(or_(Esame.voto < 21,Esame.voto >27))
        for esame in query1:
            print(esame.studente, esame.corso, esame.data_, esame.voto)
        print()
        
    with Session() as session:
        query2 = session.query(Docente).where(Docente.num_telefono == None)
        for docente in query2:
            print(docente.nome, docente.cognome)
        print()
        
#-- c) Matricola degli studenti il cui cognome inizia con 'M' o 'N' e termina con 'i'
    with Session() as session:
        query3 = session.query(Studente).where(or_(Studente.cognome.like("M%i"), Studente.cognome.like("N%i")))
        for studente in query3:
            print(studente.matricola)
        print()

# Matricola degli studenti che hanno sostenuto nel 2006 o nel 2007 un esame con voto pari a 30 o 33 (lode)
    with Session() as session:
        query4 = session.query(Studente,Esame).where(Studente.matricola == Esame.studente).where(and_(Esame.data_.between('01-01-2006','12-31-2007')),(or_(Esame.voto == 30, Esame.voto == 33)))
        for studente,esame in query4:
            print(studente.matricola)
        print()
    
        