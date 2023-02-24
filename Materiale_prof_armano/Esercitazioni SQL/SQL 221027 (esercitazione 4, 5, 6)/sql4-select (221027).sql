-- a) Selezionare il nome del progetto col budget più elevato.

select nome
  from progetti.progetto
  where budget = ( select max(budget) from progetti.progetto ) ;
  -- impongo che il budget sia quello massimo

select nome
  from progetti.progetto
  where budget >= ALL ( select budget from progetti.progetto ) ;
  -- selezioni i budget più alti usando 'ALL'

-- b) Selezionare i dati dei progetti cui partecipano almeno un
--    dipendente di Cagliari e un dipendente di Sassari.

select *
  from progetti.progetto 
  where codP IN ( select progetto -- progetti con dip di Cagliari
                    from progetti.partecipa, progetti.dipendente
                    where dipendente = codD and citta = 'Cagliari' )
    and codP IN ( select progetto -- progetti con dip di Sassari
                    from progetti.partecipa, progetti.dipendente
                    where dipendente = codD and citta = 'Sassari' ) ;

select *
  from progetti.progetto
  where codP IN ( select progetto -- progetti con dip di Cagliari
                    from progetti.partecipa, progetti.dipendente
                    where dipendente = codD and citta = 'Cagliari'

                  intersect -- faccio l'intersezioen tra i due insiemi
                  
                  select progetto -- progetti con dip di Sassari
                    from progetti.partecipa, progetti.dipendente
                    where dipendente = codD and citta = 'Sassari');

-- c) Selezionare i dati dei progetti cui partecipano almeno due 
--    dipendenti di Cagliari.

select *
  from progetti.progetto 
  where codP IN ( select progetto
                    from progetti.partecipa, progetti.dipendente
                    where dipendente = codD and citta = 'Cagliari'
                    group by progetto having count(*) > 1 ) ;
                    -- impongo almeno due dipendenti

-- d) Selezionare il cognome e il nome dei dipendenti 
--    che non partecipano a nessun progetto iniziato prima del 2005.

select cognome, nome
  from progetti.dipendente 
  where codD NOT IN ( select dipendente -- dip in progetti prima del 2005
                        from progetti.partecipa, progetti.progetto
                        where progetto = codP and anno < 2005 ) ;

-- e) Selezionare il cognome e il nome dei dipendenti 
--    che partecipano esclusivamente a progetti del 2005.

select cognome, nome
  from progetti.dipendente 
  where codD IN ( select dipendente -- solo dip in progetti
                   from progetti.partecipa )
    and codD NOT IN ( select dipendente -- dip in progetti non del 2005
                        from progetti.partecipa, progetti.progetto
                        where progetto = codP and anno <> 2005 ) ;

-- f) Selezionare il codice dei dipendenti che partecipano ai progetti
--    con almeno tre ruoli distinti.

select dipendente
  from progetti.partecipa 
  group by dipendente 
  having count(distinct ruolo) >= 3 ; -- dip con almeno 3 ruoli distinti

-- g) Per ogni dipendente (che ha preso parte ad almeno un progetto), 
--    selezionare il codice del progetto in cui egli ha lavorato per il maggior numero di mesi.

select dipendente, progetto
  from progetti.partecipa P
  where mesi = ( select max(mesi) -- seleziono solo il max numero di mesi
                   from progetti.partecipa Q
                   where Q.dipendente = P.dipendente ) ;
