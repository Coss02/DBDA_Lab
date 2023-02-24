from sqlalchemy import MetaData, Table, create_engine, join
from sqlalchemy import select
from sqlalchemy import desc
from sqlalchemy import func, distinct


# Define global vars (user, password, database and schema)
user, passwd = 'marcocosseddu', '1234'
database, schema = 'marcocosseddu', 'prestiti'

# Set the URL for accessing the database
url = f'postgresql+psycopg2://{user}:{passwd}@localhost:5432/{database}'

# Create engine and metadata
engine = create_engine(url, echo=False)
metadata = MetaData(schema=schema, bind=engine)

# Get info about the table 'studenti' and display it
prestito = Table("prestito", metadata, autoload=True)
cliente = Table("cliente", metadata, autoload=True)
filiale = Table("filiale", metadata, autoload = True)
accordato = Table("accordato_a", metadata, autoload = True)

print(" Info about the table 'studenti' ")
print(repr(cliente)) # see also sqlalchemy.inspect to printout a table
print()

query = []

# a) Selezionare i dati dei clienti a cui è stato accordato almeno un prestito da una filiale non situata nella città in cui risiedono, ordinati in senso crescente rispetto al cognome (prima) e al nome (poi).
C1 = cliente.alias()
A2 = accordato.alias()
P3 = prestito.alias()
F4 = filiale.alias()
query.append(select(C1.c.idcliente,C1.c.nome,C1.c.cognome,C1.c.citta_attuale)
            .select_from(C1.join(A2, C1.c.idcliente == A2.c.cliente)\
                .join(P3, A2.c.prestito == P3.c.idprestito)\
                .join(F4, P3.c.filiale == F4.c.idfiliale))\
                    .where(C1.c.citta_attuale != F4.c.citta)\
                        .order_by(C1.c.cognome, C1.c.nome)
            )

# b) Selezionare il cognome e il nome dei clienti a cui sono stati accordati almeno due prestiti.
query.append(select(C1.c.nome, C1.c.cognome)
            .where(C1.c.idcliente\
                .in_(select(A2.c.cliente)\
                    .group_by(A2.c.cliente)\
                        .having(func.count(distinct(A2.c.prestito))>1))))

# c) Selezionare i dati delle filiali che hanno concesso almeno due prestiti di importo superiore a 50000 euro.
query.append(select(F4.c.idfiliale, F4.c.importo_max, F4.c.citta)
            .where(F4.c.idfiliale\
                .in_(select(P3.c.filiale)\
                    .where(P3.c.importo>50000)\
                    .group_by(P3.c.filiale)\
                        .having(func.count(distinct(P3.c.importo))>1))))

# d) Selezionare i dati delle filiali che non hanno concesso alcun prestito tra il 01/01/2000 e il 31/12/2005.
query.append(select(F4)\
            .where(F4.c.idfiliale\
                .not_in(select(P3.c.filiale)\
                    .where(P3.c.data_accensione\
                        .between('01-01-2000', '12-31-2005')))))


# e) Selezionare i dati delle filiali che hanno concesso prestiti esclusivamente a clienti residenti nella propria città.
query.append(select (distinct(F4.c.idfiliale), F4.c.importo_max, F4.c.citta)\
    .where(F4.c.citta == C1.c.citta_attuale))

# f) Selezionare l’identificativo della filiale che complessivamente ha concesso in prestito la somma più elevata.
query.append(select(distinct(P3.c.filiale))\
    .group_by(P3.c.filiale)\
        .having(func.sum(P3.c.importo)>=\
            func.all(select(func.sum(P3.c.importo))\
                .group_by(P3.c.filiale))))

# g) Selezionare gli identificativi delle filiali per cui il totale dei prestiti accordati supera il 50% dell’importo massimo che può essere concesso in prestito dalla filiale.

subquery = select(func.sum(P3.c.importo))\
    .where(P3.c.filiale == F4.c.idfiliale)\
        .scalar_subquery()

query.append(select(F4.c.idfiliale)\
    .where((0.5*F4.c.importo_max)<\
        (subquery)))





with engine.connect() as connection:
    content = connection.execute(query.pop()) # Execute the query

 # Display the result
print(" This is the query result ")
for item in content: 
    print(item)
print()