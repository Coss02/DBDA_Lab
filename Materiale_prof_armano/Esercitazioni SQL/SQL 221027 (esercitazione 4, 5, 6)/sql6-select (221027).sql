-- e) Per ciascun immobile ancora invenduto, 
--    determinare il numero di volte in cui è stato visitato.

select codI, count(codA) 
  from immobili.immobile_invenduto natural left join immobili.visita
  group by codI ;

-- senza la vista 'immobile_invenduto'

select codI, count(codA)
  from immobili.immobile natural left join immobili.visita 
  where codI NOT IN (select codI from immobili.vendita)
  group by codI;

-- f) Selezionare i dati degli agenti che hanno effettuato almeno due
--    visite ma nessuna vendita.

select immobili.agente.*
  from immobili.agente natural join immobili.statistiche
  where num_visite >= 2 and num_vendite = 0;

-- senza la vista 'statistiche'

select * from immobili.agente
  where codA in ( select codA
                    from immobili.visita
                    group by codA having count(*) >= 2 )
    and codA not in ( select codA from immobili.vendita ) ;

-- g)  Per ciascun agente che ha effettuato almeno due visite e almeno due vendite, 
--     determinare la data dell'ultima visita effettuata e la data dell'ultima vendita effettuata.

select codA, VI.data, VE.data
  from immobili.statistiche S join immobili.visita VI using(codA)
                              join immobili.vendita VE using(codA)
    where num_visite >=2 and num_vendite >=2
      and VI.data >= ALL ( select data from immobili.visita where codA = S.codA )
      and VE.data >= ALL ( select data from immobili.vendita where codA = S.codA ) ;

-- senza la vista 'statistiche'

select codA, VI.data, VE.data
       from immobili.agente A join immobili.visita VI using(codA)
                              join immobili.vendita VE using(codA)
            where codA in (select codA from immobili.visita
                                  group by codA having count(*) >= 2)
              and codA in (select codA from immobili.vendita
                                  group by codA having count(*) >= 2)
              and VI.data >= ALL (select data from immobili.visita where codA = A.codA)
              and VE.data >= ALL (select data from immobili.vendita where codA = A.codA);

-- h)  Determinare, fra tutti gli immobili invenduti, quali sono quelli più cari 
--     per la zona e il tipo a cui si riferiscono (ovvero il più caro degli appartamenti 
--     invenduti in zona residenziale, il più caro degli appartamenti invenduti in centro, etc...).

select *
  from immobili.immobile_invenduto I
  where prezzo_richiesto >= ALL ( select prezzo_richiesto
                                    from immobili.immobile_invenduto 
                                    where tipo = I.tipo and zona = I.zona ) ;

-- senza la vista 'immobile_invenduto'

select *
  from immobili.immobile I
  where codI NOT IN (select codI from immobili.vendita)
    and prezzo_richiesto >= ALL ( select prezzo_richiesto
                                    from immobili.immobile 
                                    where codI NOT IN ( select codI from immobili.vendita ) 
                                      and tipo = I.tipo and zona = I.zona ) ;
