
CREATE TABLE marcas (
  id serial PRIMARY KEY NOT NULL,
  marca varchar(100) NOT NULL
);

CREATE TABLE productos (
  id serial PRIMARY KEY NOT NULL,
  nom_pro varchar(100) NOT NULL,
  marca_id int NOT NULL,
  talla_id int NOT NULL,
  cantidad int NOT NULL,
  fecha date NOT NULL,
  observaciones varchar(300) NOT NULL
);

CREATE TABLE talla (
  id serial PRIMARY KEY NOT NULL,
  talla varchar(4) NOT NULL
);


alter table productos 
add constraint FKmarcas 
FOREIGN key (marca_id) 
REFERENCES marcas(id)
ON DELETE CASCADE 
ON UPDATE CASCADE;

alter table productos 
add constraint FKtalla 
FOREIGN key (talla_id) 
REFERENCES talla(id)
ON DELETE CASCADE 
ON UPDATE CASCADE;

INSERT INTO talla (talla) VALUES
( 'S'),
( 'M'),
( 'L'),
( 'X'),
( 'XL'),
('XXL');

INSERT INTO marcas ( marca) VALUES
( 'koaj'),
( 'kenzo jeans'),
( 'Studio F'),
( 'Totto'),
( 'arturo calle'),
( 'Adidas'),
( 'Nike')

select * from talla;

INSERT INTO productos ( nom_pro, marca_id, talla_id, cantidad, fecha, observaciones) VALUES
( 'pantalon vaqueros', 2, 2, 6, '2020-12-08', 'son para dama');

SELECT  productos.id ,nom_pro, marcas.marca, talla.talla , cantidad, fecha, observaciones 
	FROM productos, marcas, talla 
	WHERE marcas.id = marca_id AND talla.id = talla_id;