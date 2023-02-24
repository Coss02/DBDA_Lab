-- a)  Vista 'immobile_invenduto'
--     Contiene i dati di tutti gli immobili ancora invenduti

create view immobili.immobile_invenduto as
  select *
    from immobili.immobile 
    where codI NOT IN ( select codI from immobili.vendita ) ;

-- b)  Vista 'statistiche_visite' che contiene, per ogni agente: 
--     - il codice dell'agente (attributo 'codA'), 
--     - l'agenzia presso cui l'agente lavora (attributo 'agenzia), 
--     - il numero di visite effettuate dall'agente (attributo 'num_visite') 
--     - il numero di immobili distinti visitati dall'agente (attributo 'num_immobili_visitati');

create view immobili.statistiche_visite as
  select codA,
         agenzia,
         count(codI) as num_visite, 
         count(distinct codI) as num_immobili_visitati
    from immobili.agente natural left join immobili.visita
    group by codA, agenzia ;

-- c)  Vista 'statistiche_vendite' che contiene, per ogni agente:
--     - il codice dell'agente (attributo 'codA'), 
--     - l'agenzia presso cui l'agente lavora (attributo 'agenzia'), 
--     - il numero di vendite effettuate dall'agente (attributo 'num_vendite') 
--     - la somma persa dall'agenzia per le vendite effettuate dall'agente (*) 

--     (*) Ovvero lo scarto tra i prezzi di vendita richiesti e quelli 
--         effettivamente ottenuti mediante la vendita.

create view immobili.statistiche_vendite as
  select codA,
         agenzia,
         count(codI) as num_vendite, 
         sum(prezzo_richiesto - prezzo) as somma_persa
    from immobili.agente natural left join immobili.vendita 
                         natural left join immobili.immobile
    group by codA, agenzia ;

-- d)  Vista 'statistiche' che contiene, per ogni agente: 
--     - il codice dell'agente (attributo 'codA'), 
--     - l'agenzia presso cui l'agente lavora (attributo 'agenzia'), 
--     - il numero di visite effettuate dall'agente (attributo 'num_visite'), 
--     - il numero di immobili distinti visitati dall'agente (attributo 'num_immobili_visitati'), 
--     - il numero di vendite effettuate dall'agente (attributo 'num_vendite') 
--     - la somma persa dall'agenzia per le vendite effettuate dall'agente (*)

--     (*) Ovvero lo scarto tra i prezzi di vendita richiesti e quelli 
--         effettivamente ottenuti mediante la vendita.

create view immobili.statistiche as -- usa altre viste...
  select *
    from immobili.statistiche_visite
         natural join immobili.statistiche_vendite ;

create view immobili.statistiche as
  select codA,
         agenzia, 
         ( select count(codI)
             from immobili.visita where codA = A.codA ) as num_visite, 
         ( select count(distinct codI)
             from immobili.visita where codA = A.codA ) as num_immobili_visitati,
         ( select count(codI)
             from immobili.vendita where codA = A.codA ) as num_vendite,
         ( select sum(prezzo_richiesto - prezzo)
             from immobili.vendita 
                  natural join immobili.immobile where codA = A.codA ) as somma_persa
    from immobili.agente A;
