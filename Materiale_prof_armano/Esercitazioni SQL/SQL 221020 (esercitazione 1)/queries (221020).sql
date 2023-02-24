-- *** MODIFY THE SEARCH PATH TO AVOID REPEATING "segreteria"...

SET search_path TO segreteria, "$user", public ;

-- *** QUERY SAMPLES

-- Get exams of students whose surname is 'Rossi'

select matricola, nome, cognome, corso, data, voto
  from studenti as S, esami as E
  where S.cognome = 'Rossi' and E.studente = S.matricola ;

-- Get exams rated > 25 

select matricola, nome, cognome, corso, data, voto
  from studenti as S, esami as E
  where E.voto > 25 and E.studente = S.matricola ;

-- Same as before (using join)...

select matricola, nome, cognome, corso, data, voto
  from studenti JOIN esami ON studente = matricola
  where voto > 25 ;
