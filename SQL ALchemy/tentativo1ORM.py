from sqlalchemy import create_engine,MetaData,Column,String,Date,ForeignKey,SmallInteger,CheckConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DIRECT MAPPING | stile dichiarativo -> __tablename__
Base=declarative_base(metadata=MetaData(schema="segreteria"))
class Studente(Base):
    __tablename__="studenti"
    matricola=Column(String,primary_key=True)
    cognome=Column(String,nullable=False)
    nome=Column(String,nullable=False)
    data_nascita=Column(Date,nullable=False)
    anno_corso=Column(SmallInteger,CheckConstraint('anno_corso>=1','anno_corso<=3'), nullable=False)
class Corso(Base):
    __tablename__="corsi"
    cod_corso=Column(String,primary_key=True)
    nome=Column(String,nullable=False)
    docente=Column(String,ForeignKey("docenti.cod_docente"))
class Docente(Base):
    __tablename__="docenti"
    cod_docente=Column(String,primary_key=True)
    cognome=Column(String,nullable=False)
    nome=Column(String,nullable=False)
    indirizzo=Column(String)
class Esame(Base):
    __tablename__="esami"
    studente=Column(String,ForeignKey("segreteria.studenti"),primary_key=True)
    corso=Column(String,ForeignKey("segreteria.corsi"),primary_key=True)
    data=Column(Date,nullable=False)
    voto=Column(SmallInteger)

# MEDIATED MAPPING
# ...

if __name__=="__main__":
    url="postgresql+psycopg2://marcocosseddu@localhost:5432/marcocosseddu"
    engine=create_engine(url=url,echo=False)
    Session=sessionmaker(bind=engine)
    # QUERY 
    # [+] prova ad importare Session() e ad usarlo anzichÃ¨ sessionmaker
    with Session() as session:
        # Stampa tutti gli Studenti
        results=session.query(Studente)
        for s in results:
            print(s.matricola,s.cognome,s.nome,s.data_nascita,s.anno_corso)
    print()
    with Session() as session:
        # Lista studenti iscritti al terzo anno
        results=session.query(Studente).filter(Studente.anno_corso==3)
        for s in results:
            print(s.matricola,s.cognome,s.nome,s.data_nascita,s.anno_corso)
    print()
    with Session() as session:
        pass
        # Aggiungiamo esami
        #session.add(Esame(studente="451100",corso="C04",data="2022-04-21",voto=27))
        #session.add(Esame(studente="438984",corso="C06",data="2022-06-11",voto=28))
        #session.add(Esame(studente="424200",corso="C02",data="2022-10-13",voto=30))
    print()
    with Session() as session:
        # Lista degli esami sostenuti dallo studente 424200
        esamiStudente=session.query(Esame,Studente).filter(Studente.matricola==Esame.studente).filter(Studente.matricola=='424200')
        for esame,studente in esamiStudente:
            print(esame.studente,esame.voto,esame.corso)
    print()
    with Session() as session:
        # Lista studenti che hanno dato almeno un esame
        S,E=Studente,Esame
        from sqlalchemy import func
        results=session.query(S,func.count(E.corso).label("numero_esami")).join(E,S.matricola==E.studente).group_by(S)
        for studente,numero_esami in results:
            print(studente.matricola,numero_esami)
    print()
    with Session() as session:
        #Lista studenti che hanno dato uno specifico esame
        S,E,C=Studente,Esame,Corso
        from sqlalchemy import and_
        esami=session.query(S,E).join(E,E.studente==S.matricola).where(E.corso==C.cod_corso).where(C.cod_corso=='C06')
        for studente,esame in esami:
            print(studente.matricola,esame.corso,esame.data,esame.voto)
    print()
    with Session() as session:
        # Lista degli esami per ogni studente
        S,E=Studente,Esame
        result=session.query(S,func.count(E.corso).label("numero_esami")).join(E,E.studente==S.matricola).where(E.corso==C.cod_corso).group_by(S.matricola).order_by(S.cognome,S.nome)
        for studente,numero_esami in result:
            print(studente.matricola,studente.nome,studente.cognome,numero_esami)
    print()
    with Session() as session:
        # Numero esami dati per ogni corso
        E,C=Esame,Corso
        result=session.query(C,func.count(E.corso).label("numero_esami")).join(E,E.corso==C.cod_corso).group_by(C.cod_corso).order_by(C.nome)
        for corso,numero_esami in result:
            print(corso.cod_corso,corso.nome,numero_esami)