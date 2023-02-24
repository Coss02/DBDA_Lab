-- Crea schema 'progetti'

create schema progetti;

-- Crea tabella 'progetto'

create table progetti.progetto (
  codP char(3) primary key, 
  nome varchar(20), 
  anno smallint, 
  budget int not null check ( budget > 10000 )
) ;

-- Crea tabella 'dipendente'

create table progetti.dipendente (
  codD char(3) primary key, 
  cognome varchar(20) not null, 
  nome varchar(20) not null, 
  citta varchar(20)
) ;

-- Crea tabella 'partecipa' (a progetto)

create table progetti.partecipa (
  progetto char(3) references progetti.progetto on delete cascade,
  dipendente char(3) references progetti.dipendente on delete cascade,
  mesi smallint check(mesi between 3 and 24), 
  ruolo varchar(20), 
  primary key(progetto, dipendente) -- chiave su due attributi
) ;
