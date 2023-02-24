-- a) Dati relativi agli esami il cui voto è minore di 21 o maggiore di 27

select *
  from segreteria.esami 
  where voto < 21 or voto > 27 ;

select *
  from segreteria.esami 
  where voto not between 21 and 27 ;

-- b) Codice e cognome dei docenti di cui non è noto il numero di telefono

select cod_docente, cognome
  from segreteria.docenti
  where num_telefono is null;

-- c) Matricola degli studenti il cui cognome inizia con 'M' o 'N' e termina con 'i'

select matricola from segreteria.studenti 
       where cognome like 'M%i' or cognome like 'N%i';
       
-- d) Matricola degli studenti che hanno sostenuto nel 2006 o nel 2007 un esame con voto pari a 30 o 33 (lode)

select studente
  from segreteria.esami 
  where data between '2006-01-01' and '2007-12-31' and voto in (30, 33) ;

select studente
  from segreteria.esami 
  where data between '2006-01-01' and '2007-12-31' and (voto = 30 or voto = 33) ;
                                                                                             
-- e) Cognome e nome degli studenti nati prima del 1984, con l'eliminazione di eventuali duplicati

select distinct cognome, nome
  from segreteria.studenti 
  where data_nascita < '1984-01-01';

-- f) Dati di tutti gli studenti del biennio, ordinati in modo decrescente rispetto all'età e, a parità di età,  
-- ordinati in modo crescente rispetto al cognome (prima) e al nome (poi)

select *
  from segreteria.studenti 
  where anno_corso = 1 or anno_corso = 2
  order by data_nascita, cognome, nome ;
