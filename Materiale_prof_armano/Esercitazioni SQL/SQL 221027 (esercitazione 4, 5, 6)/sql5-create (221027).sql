-- Crea schema 'prestiti'

create schema prestiti;

-- Crea tabella 'cliente'

create table prestiti.cliente (
  IDcliente char(3) primary key, 
  cognome varchar(20) not null, 
  nome varchar(20) not null, 
  citta_residenza varchar(20) 
) ;

-- Crea tabella 'filiale'

create table prestiti.filiale (
  IDfiliale char(3) primary key, 
  importo_max decimal(10,2) not null, 
  citta varchar(20)
) ;

-- Crea tabella 'prestito'

create table prestiti.prestito (
  IDprestito char(3) primary key,
  IDfiliale char(3) not null references prestiti.filiale on update cascade,
  importo decimal(8,2) not null, 
  data_accensione date not null, 
  data_scadenza date not null, 
  check ( data_scadenza > data_accensione )
) ;

-- Crea tabella 'accordato_a'

create table prestiti.accordato_a (
  IDprestito char(3) references prestiti.prestito on delete cascade on update cascade, 
  IDcliente char(3) references prestiti.cliente on delete cascade on update cascade, 
  primary key(IDprestito, IDcliente)
) ;
