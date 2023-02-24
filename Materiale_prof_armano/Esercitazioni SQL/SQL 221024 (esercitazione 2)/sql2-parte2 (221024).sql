-- a) Matricola degli studenti che hanno superato l'esame di Basi di Dati
-- con un voto superiore a 27 

select studente
  from segreteria.esami, segreteria.corsi 
  where corso = cod_corso and voto > 27 and nome = 'Basi di Dati' ;

select studente 
  from segreteria.esami join segreteria.corsi on corso = cod_corso
  where voto > 27 and nome = 'Basi di Dati';

-- b) Cognome e nome degli studenti che hanno superato almeno un esame nel 2007, 
-- con l'eliminazione di eventuali duplicati

select distinct cognome, nome
  from segreteria.studenti, segreteria.esami 
  where matricola = studente and data between '2007-01-01' and '2007-12-31' ;

select distinct cognome, nome
  from segreteria.studenti join segreteria.esami on matricola = studente
  where data between '2007-01-01' and '2007-12-31' ;

-- c) Dati relativi agli esami sostenuti dallo studente Mario Rossi, 
-- ordinati in senso decrescente rispetto al voto e, a parità di voto, 
-- in senso crescente rispetto alla data 

select segreteria.esami.*
  from segreteria.esami, segreteria.studenti 
  where studente = matricola and cognome = 'Rossi' and nome = 'Mario'
  order by voto desc, data ;

select segreteria.esami.*
  from segreteria.esami join segreteria.studenti on studente = matricola 
  where cognome = 'Rossi' and nome = 'Mario'
  order by voto desc, data ;

-- d) Coppie (matricola1, matricola2) di studenti omonimi (stesso cognome e stesso nome)
-- NB In mancanza di omonimie inserirne alcune oppure fare la verifica solo sul cognome

select S1.matricola, S2.matricola
  from segreteria.studenti S1, segreteria.studenti S2
  where S1.cognome = S2.cognome and S1.nome = S2.nome and S1.matricola <> S2.matricola ; 

select S1.matricola, S2.matricola
  from segreteria.studenti S1 join segreteria.studenti S2
       on (S1.cognome = S2.cognome and S1.nome = S2.nome and S1.matricola <> S2.matricola) ; 

-- e) Dati degli studenti del primo anno con il codice e il voto dei relativi esami sostenuti, 
-- inclusi gli studenti che non hanno sostenuto alcun esame

select segreteria.studenti.*, corso, voto 
  from segreteria.studenti left join segreteria.esami on matricola = studente
  where anno_corso = 1 ;
       
-- f) Dati di tutti i docenti con i relativi insegnamenti, 
-- inclusi i docenti che non tengono alcun corso (da qui il "left join")

select D.*, C.cod_corso, C.nome
  from segreteria.docenti D left join segreteria.corsi C
       on D.cod_docente = C.docente ;
