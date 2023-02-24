-- Modify the column anno_corso in table studenti

alter table segreteria.studenti
  alter anno_corso set default 1 ;

-- Remove indirizzo from table docenti

alter table segreteria.docenti
  drop indirizzo;

-- Add num_telefono to table docenti

alter table segreteria.docenti
  add num_telefono varchar(15) default null ;

-- Add a constraint to column voto in table esami

alter table segreteria.esami
  add constraint check_voto check ( (voto >= 18 and voto <= 30) or voto = 33 ) ;
