-- CREATE SCHEMA segreteria (if needed)

create schema if not exists segreteria;

-- CREATE TABLES studenti, docenti, corsi, esami

create table segreteria.studenti (
  matricola char(6) primary key,
  cognome varchar(20) not null, 
  nome varchar(20) not null, 
  data_nascita date, 
  anno_corso smallint,
  constraint check_anno_corso check(anno_corso >=1 and anno_corso <=3)
) ;

create table segreteria.docenti (
  cod_docente char(6) primary key, 
  cognome varchar(20) not null, 
  nome varchar(20) not null, 
  indirizzo varchar(40) 
) ;

create table segreteria.corsi (
  cod_corso char(3) primary key, 
  nome varchar(20), 
  docente char(6) references segreteria.docenti on update cascade
) ;

create table segreteria.esami (
  studente char(6) references segreteria.studenti on update cascade,
  corso char(3) references segreteria.corsi on update cascade,
  data date not null, 
  voto smallint not null, 
  primary key(studente, corso)
) ;
