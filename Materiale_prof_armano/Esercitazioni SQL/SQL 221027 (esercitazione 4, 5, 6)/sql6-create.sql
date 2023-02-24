create schema immobili;

create table immobili.immobile
( codI char(3) primary key, 
  indirizzo varchar(30) not null, 
  tipo varchar(15) not null check(tipo in('appartamento', 'villetta', 'magazzino')),
  zona varchar(15) not null check(zona in('residenziale', 'centro', 'periferia')),
  prezzo_richiesto decimal(10,2) not null
);  

create table immobili.agente
( codA char(3) primary key, 
  cognome varchar(20), 
  nome varchar(20), 
  agenzia varchar(20) not null
);

create table immobili.visita
( codI char(3) references immobili.immobile 
               on update cascade on delete cascade, 
  codA char(3) references immobili.agente
               on update cascade on delete no action, 
  data date, 
  primary key(codI, codA, data)
);

create table immobili.vendita
( codI char(3) primary key references immobili.immobile 
                           on update cascade on delete no action,
  codA char(3) not null references immobili.agente 
                        on update cascade on delete no action,
  data date, 
  prezzo decimal(10,2) not null
);


