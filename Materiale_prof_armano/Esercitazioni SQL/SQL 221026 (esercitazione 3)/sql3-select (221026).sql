-- *** % ***

-- Selezionare i dati dei prodotti disponibili nel magazzino 'M11', con 
-- il relativo prezzo, ordinati in senso crescente rispetto alla categoria 
-- e, a parità di categoria, ordinati in senso decrescente rispetto al prezzo.

select codP, nome, categoria, prezzo 
  from prodotti.prodotto, prodotti.inventario 
  where codP = prodotto and magazzino = 'M11'
  order by categoria, prezzo desc ;

-- *** % ***

-- Selezionare il codice e l'indirizzo dei magazzini di Milano in cui è
-- presente almeno un prodotto della categoria 'elettrodomestici' in 
-- quantità superiore a 20.

select codM, indirizzo
  from prodotti.magazzino, prodotti.inventario, prodotti.prodotto 
  where codM = magazzino and 
        prodotto = codP  and
        citta = 'Milano' and
        quantita > 20    and
        categoria = 'elettrodomestici' ;

-- *** % ***

-- Selezionare il codice e la città dei magazzini in cui sono presenti 
-- gli spaghetti.

select codM, citta
  from prodotti.magazzino, prodotti.inventario, prodotti.prodotto 
  where codM = magazzino and prodotto = codP and nome = 'spaghetti' ;

-- *** % ***

-- Selezionare il codice dei magazzini attualmente vuoti (che non contengono
-- cioè nessun prodotto).

select codM
  from prodotti.magazzino 
  where codM NOT IN ( select magazzino from prodotti.inventario ) ;

-- Usando una view...

create view mag_inventario as ( select magazzino from prodotti.inventario ) ;

select codM
  from prodotti.magazzino 
  where codM NOT IN (select * from mag_inventario ) ;

-- *** % ***

-- Selezionare il codice dei magazzini che non contengono nessun prodotto 
-- della categoria 'alimentari', magazzini vuoti compresi.

select codM from prodotti.magazzino
  where codM NOT IN (
    select magazzino
      from prodotti.inventario, prodotti.prodotto 
      where prodotto = codP and categoria = 'alimentari'
) ;
      
-- Usando una view...

create view mag_alimentari as (
  select magazzino
     from prodotti.inventario, prodotti.prodotto 
     where prodotto = codP and categoria = 'alimentari'
) ;

select codM as magazzino
  from prodotti.magazzino 
  where codM NOT IN ( select * from mag_alimentari ) ;

-- *** % ***

-- Selezionare il codice dei magazzini che non contengono nessun prodotto
-- della categoria 'alimentari', magazzini vuoti esclusi.

select distinct magazzino from prodotti.inventario
  where magazzino NOT IN (
    select magazzino from prodotti.inventario, prodotti.prodotto 
      where prodotto = codP and categoria = 'alimentari' ) ;
    
-- NB Anche qui si può creare la view...

-- *** % ***

-- Selezionare il codice dei magazzini che contengono solo prodotti della
-- categoria 'alimentari'.

select distinct magazzino from prodotti.inventario 
  where magazzino NOT IN ( 
    select magazzino from prodotti.inventario, prodotti.prodotto 
      where prodotto = codP and categoria <> 'alimentari' ) ;

-- NB Anche qui si può creare la view...

-- *** % ***

-- Selezionare il codice dei prodotti che sono presenti in almeno due magazzini.

select distinct I1.prodotto
  from prodotti.inventario I1, prodotti.inventario I2
  where I1.prodotto = I2.prodotto and I1.magazzino <> I2.magazzino ;
