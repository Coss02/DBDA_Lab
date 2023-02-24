-- a) Selezionare i dati dei clienti a cui è stato accordato almeno un  
--    prestito da una filiale non situata nella città in cui risiedono, 
--    ordinati in senso crescente rispetto al cognome (prima) e al nome (poi).

select IDcliente, cognome, nome, citta_residenza
  from prestiti.cliente natural join prestiti.accordato_a 
                        natural join prestiti.prestito 
                        natural join prestiti.filiale 
  where citta_residenza <> citta -- impongo che le città siano diverse
  order by cognome, nome ;

-- b) Selezionare il cognome e il nome dei clienti a cui sono stati 
--    accordati almeno due prestiti.

select cognome, nome
  from prestiti.cliente
  where IDcliente IN ( select A1.IDcliente -- impongo almeno due prestiti
                         from prestiti.accordato_a A1, prestiti.accordato_a A2
                         where A1.IDcliente = A2.IDcliente
                           and A1.IDprestito <> A2.IDprestito ) ; 

select cognome, nome 
  from prestiti.cliente 
  where IDcliente IN ( select IDcliente
                         from prestiti.accordato_a
                         group by IDcliente
                         having count(*) > 1 ) ;
                         -- impongo almeno due prestiti usando 'count'

-- c) Selezionare i dati delle filiali che hanno concesso almeno due  
--    prestiti di importo superiore a 50000 euro.

select * from prestiti.filiale 
  where IDfiliale IN ( select P1.IDfiliale 
                         from prestiti.prestito P1, prestiti.prestito P2
                         where P1.importo > 50000
                           and P2.importo > 50000
                           and P1.IDfiliale = P2.IDfiliale 
                           and P1.IDprestito <> P2.IDprestito);

select * from prestiti.filiale 
  where IDfiliale IN ( select IDfiliale from prestiti.prestito 
                         where importo > 50000
                         group by IDfiliale
                         having count(*) > 1 ) ;
                         -- impongo almeno due prestiti > 50K usando 'count'

-- d) Selezionare i dati delle filiali che non hanno concesso alcun prestito
--    tra il 01/01/2000 e il 31/12/2005. 

select * from prestiti.filiale
  where IDfiliale NOT IN ( select IDfiliale -- filiali con prestiti nel range di date
                             from prestiti.prestito 
                             where data_accensione between '2000-01-01' and '2005-12-31');

-- e) Selezionare i dati delle filiali che hanno concesso prestiti 
--    esclusivamente a clienti residenti nella propria città.

select * from prestiti.filiale 
  where IDfiliale IN ( select IDfiliale from prestiti.prestito )
    and IDfiliale NOT IN ( select IDfiliale 
                             from prestiti.filiale
                                  natural join prestiti.prestito 
                                  natural join prestiti.accordato_a 
                                  natural join prestiti.cliente
                                  -- join su colonne condivise (natural join)
                             where citta <> citta_residenza ) ;
                             -- impongo vincolo sulle città

-- f) Selezionare l'identificativo della filiale che complessivamente 
--    ha concesso in prestito la somma più elevata.

select IDfiliale
  from prestiti.prestito 
  group by IDfiliale
  having SUM(importo) >= ALL ( select SUM(importo) 
                                 from prestiti.prestito
                                 group by IDfiliale ) ; 

-- g) Selezionare gli identificativi delle filiali per cui il totale dei
--    prestiti accordati supera il 50% dell'importo massimo che può essere
--    concesso in prestito dalla filiale.

select IDfiliale
  from prestiti.filiale F
  where 0.5 * importo_max < ( select SUM(importo) 
                                from prestiti.prestito P
                                where P.IDfiliale = F.IDfiliale ) ;
