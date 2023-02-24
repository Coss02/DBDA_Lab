-- h) Incrementare del 20% l'importo massimo (importo_max) 
--    relativo alle filiali che hanno concesso almeno due prestiti.

update prestiti.filiale 
  set importo_max = 1.2 * importo_max
    where IDfiliale in ( select IDfiliale 
                           from prestiti.prestito 
                           group by IDfiliale
                           having count(*) > 1 ) ;
             
-- i) Cancellare le filiali che non hanno concesso alcun prestito.

delete from prestiti.filiale 
  where IDfiliale not in ( select IDfiliale from prestiti.prestito ) ;
