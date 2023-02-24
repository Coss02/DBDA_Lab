insert into prestiti.cliente values
  ('C01', 'Rossi', 'Andrea', 'Cagliari'),
  ('C02', 'Bianchi', 'Maria', 'Cagliari'),
  ('C03', 'Verdi', 'Anna', 'Roma'),
  ('C04', 'Neri', 'Marco', 'Milano'),
  ('C05', 'Rossi', 'Marta', 'Milano'),
  ('C06', 'Bruni', 'Valerio', 'Firenze'),
  ('C07', 'Bruni', 'Paolo', 'Roma') ;

insert into prestiti.filiale values
  ('F01', 2000000.00, 'Milano'),
  ('F02', 600000.00, 'Roma'),
  ('F03', 1500000.00, 'Roma'),
  ('F04', 500000.00, 'Napoli'),
  ('F05', 500000.00, 'Cagliari') ;

insert into prestiti.prestito values
  ('P45', 'F03', 80000.00, '1992-02-01', '2012-01-31'),
  ('P56', 'F01', 60000.00, '1995-06-01', '2015-05-31'),
  ('P63', 'F05', 75000.00, '1999-10-10', '2014-09-30'),
  ('P70', 'F02', 200000.00, '2000-01-08', '2019-12-31'),
  ('P81', 'F02', 130000.00, '2002-04-04', '2012-03-31'),
  ('P89', 'F05', 25000.00, '2003-05-02', '2013-04-30'),
  ('P98', 'F01', 110000.00, '2005-06-10', '2025-05-31') ;

insert into prestiti.accordato_a values
  ('P45', 'C03'),
  ('P56', 'C04'),
  ('P63', 'C01'),
  ('P63', 'C02'),
  ('P70', 'C07'),
  ('P81', 'C04'),
  ('P81', 'C05'),
  ('P89', 'C01'),
  ('P98', 'C06') ;
