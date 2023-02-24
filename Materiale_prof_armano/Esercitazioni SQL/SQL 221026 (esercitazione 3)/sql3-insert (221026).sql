-- Inserimento dati magazzino

insert into prodotti.magazzino values
  ('M01', 'Via Giove 14', 'Roma'),
  ('M04', 'Via Venere 5', 'Cagliari'),
  ('M05', 'Via Marte 27', 'Milano'),
  ('M11', 'Via Saturno 67', 'Milano'),
  ('M17', 'Via Plutone 34', 'Roma'),
  ('M18', 'Via Marte 76', 'Cagliari') ;

-- Inserimento prodotti

insert into prodotti.prodotto values
  ('P01', 'spaghetti', 'alimentari'),
  ('P06', 'biscotti', 'alimentari'),
  ('P07', 'latte', 'alimentari'),
  ('P11', 'camicia uomo', 'abbigliamento'),
  ('P13', 'gonna', 'abbigliamento'),
  ('P20', 'forno', 'elettrodomestici'),
  ('P22', 'frigo', 'elettrodomestici') ;

-- Inserimento inventario

insert into prodotti.inventario values
  ('M01', 'P06', 50, 2.00),
  ('M01', 'P07', 400, 1.20),
  ('M01', 'P20', 10, 450.00),
  ('M04', 'P22', 20, 780.00),
  ('M05', 'P22', 45, 700.00),
  ('M11', 'P11', 80, 65.00),
  ('M11', 'P13', 60, 85.00),
  ('M11', 'P20', 15, 430.00),
  ('M17', 'P01', 550, 0.75) ;
