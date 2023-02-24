-- Tabella 'progetto'

insert into progetti.progetto values 
  ('P01', 'Marte', 2002, 12000),
  ('P02', 'Giove', 2004, 25000),
  ('P03', 'Terra', 2005, 100000),
  ('P04', 'Venere', 2005, 50000);

-- Tabella 'dipendente'

insert into progetti.dipendente values
  ('D01', 'Mocci', 'Efisio', 'Cagliari'),
  ('D02', 'Sanna', 'Alberto', 'Cagliari'),
  ('D03', 'Medda', 'Monica', 'Nuoro'),
  ('D04', 'Cocco', 'Angelo', 'Sassari'),
  ('D05', 'Salis', 'Antioco', 'Cagliari');

-- Tabella 'partecipa'

insert into progetti.partecipa values
  ('P01', 'D02', 3, 'consulente'),
  ('P01', 'D03', 6, 'tecnico'),
  ('P01', 'D04', 24, 'responsabile'),
  ('P02', 'D03', 12, 'responsabile'),
  ('P03', 'D04', 18, 'responsabile'),
  ('P04', 'D02', 12, 'consulente'),
  ('P04', 'D03', 3, 'consulente'),
  ('P04', 'D04', 6, 'tecnico'),
  ('P04', 'D05', 12, 'responsabile');
