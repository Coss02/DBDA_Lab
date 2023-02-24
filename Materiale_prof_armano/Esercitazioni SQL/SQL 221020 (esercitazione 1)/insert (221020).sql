-- INSERT SOME DATA INTO TABLES studenti, corsi, esami

insert into segreteria.studenti values
	('424200', 'Rossi', 'Mario', '1984-01-07', 3),
	('451100', 'Verdi', 'Carlo', '1986-10-10', 1),
	('395500', 'Rossi', 'Lucia', '1982-05-06', 3),
	('438984', 'Bianchi', 'Rosa', '1985-04-01', 2);

insert into segreteria.docenti values 
	('100100', 'Neri', 'Paolo', 'Via Roma 240, Cagliari'),
	('100245', 'Bruni', 'Valeria', 'Via Mazzini 10, Roma'),
	('100476', 'Rossi', 'Francesco', 'Via Garibaldi 5, Roma');

insert into segreteria.corsi values
	('C02', 'Algebra', '100100'),
	('C04', 'Geometria', '100100'),
	('C06', 'Programmazione', '100245');

insert into segreteria.esami values
	('424200', 'C02', '2003-06-06', 24),
	('424200', 'C04', '2003-09-12', 27),
	('395500', 'C06', '2004-01-20', 21),
	('438984', 'C06', '2005-09-15', 30);
