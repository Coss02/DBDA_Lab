insert into immobili.immobile values
  ('I13', 'Via Marte 12, Roma', 'appartamento', 'residenziale', 900000.00), 
  ('I24', 'Via Giove 5, Milano', 'appartamento', 'residenziale', 1250000.00), 
  ('I31', 'Via Saturno 20, Roma', 'villetta', 'residenziale', 1100000.00), 
  ('I42', 'Via Terra 120, Cagliari', 'magazzino', 'periferia', 120000.00), 
  ('I53', 'Via Marte 34, Milano', 'appartamento', 'centro', 850000.00), 
  ('I65', 'Via Venere 23, Cagliari', 'villetta', 'periferia', 350000.00), 
  ('I76', 'Via Giove 40, Roma', 'appartamento', 'residenziale', 980000.00), 
  ('I80', 'Via Plutone 2, Cagliari', 'villetta', 'centro', 575000.00), 
  ('I92', 'Via Venere 100, Milano', 'magazzino', 'periferia', 320000.00) ;

insert into immobili.agente values
  ('A01', 'Rossi', 'Alessandro', 'CambiaCasa'), 
  ('A02', 'Rossi', 'Carlo', 'CambiaCasa'), 
  ('A04', 'Verdi', 'Francesco', 'CasaOggi'), 
  ('A05', 'Bianchi', 'Angela', 'CambiaCasa'), 
  ('A07', 'Neri', 'Alessandra', 'CasaOggi'), 
  ('A08', 'Bruni', 'Valeria', 'CasaFacile'), 
  ('A09', 'Bruni', 'Valeria', 'CasaFacile') ;

insert into immobili.visita values
  ('I13', 'A01', '2002-06-05'),
  ('I13', 'A04', '2003-07-07'), 
  ('I24', 'A09', '2004-10-12'), 
  ('I31', 'A04', '2004-11-23'),
  ('I42', 'A04', '2005-01-13'), 
  ('I42', 'A07', '2005-02-24'),  
  ('I53', 'A09', '2005-04-05'),
  ('I65', 'A07', '2005-06-12'), 
  ('I76', 'A01', '2005-09-10'),  
  ('I76', 'A01', '2006-01-20'),
  ('I76', 'A05', '2006-01-20') ;

insert into immobili.vendita values
  ('I13', 'A04', '2003-07-24', 900000.00),
  ('I31', 'A04', '2004-12-06', 980000.00),
  ('I53', 'A09', '2005-04-27', 750000.00),
  ('I65', 'A07', '2005-07-02', 300000.00),
  ('I80', 'A07', '2006-01-27', 530000.00) ;
