-- Crea schema 'immobili'

create schema immobili;

-- Crea tabella 'immobile'

create table immobili.immobile (
  codI char(3) primary key, 
  indirizzo varchar(30) not null, 
  tipo varchar(15) not null,
  zona varchar(15) not null,
  prezzo_richiesto decimal(10,2) not null,
  -- constraints
  constraint check_tipo_immobile
    check ( tipo in ('appartamento', 'villetta', 'magazzino') ),
  constraint check_ubicazione
    check ( zona in ('residenziale', 'centro', 'periferia') )
) ;  

-- Crea tabella 'agente'

create table immobili.agente (
  codA char(3) primary key, 
  cognome varchar(20), 
  nome varchar(20), 
  agenzia varchar(20) not null
) ;

-- Crea tabella 'visita'

create table immobili.visita (
  codI char(3) references immobili.immobile 
               on update cascade on delete cascade, 
  codA char(3) references immobili.agente
               on update cascade on delete no action, 
  data date, 
  primary key(codI, codA, data)
) ;

-- Crea tabella 'vendita'

create table immobili.vendita (
  codI char(3) primary key references immobili.immobile 
               on update cascade on delete no action,
  codA char(3) not null references immobili.agente 
                        on update cascade on delete no action,
  data date, 
  prezzo decimal(10,2) not null
) ;
