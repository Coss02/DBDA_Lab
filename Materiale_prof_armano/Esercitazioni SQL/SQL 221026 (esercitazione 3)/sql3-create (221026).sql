create schema prodotti ;

create table prodotti.magazzino (
  codM char(3) primary key, 
  indirizzo varchar(40) not null, 
  citta varchar(20) not null
) ;

create table prodotti.prodotto (
  codP char(3) primary key, 
  nome varchar(20) not null, 
  categoria varchar(20) not null
) ;

create table prodotti.inventario (
  magazzino char(3) references prodotti.magazzino on delete cascade on update cascade, 
  prodotto char(3) references prodotti.prodotto on delete cascade on update cascade, 
  quantita int not null check ( quantita > 0 ), 
  prezzo decimal(8,2) not null check ( prezzo > 0.00 ),
  primary key(magazzino,prodotto) -- la PK non è su singolo attributo...
) ;
