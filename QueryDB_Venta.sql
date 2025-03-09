create database venta
use venta
drop database venta

create table cliente(
id_cliente int primary key,
nombre varchar(30) not null,
telefono varchar(10),
direccion varchar(50)
)

create table categoria(
id_categoria int primary key,
nombre varchar(30)
)

create table producto(
id_producto int primary key,
descripcion varchar(50) not null,
precio float not null,
stock int not null,
id_categoria int not null,
foreign key(id_categoria)references categoria(id_categoria)
)

create table notaventa(
id_venta int primary key,
fecha date not null,
monto float not null,
id_cliente int not null,
foreign key(id_cliente)references cliente(id_cliente)
)


create table detalleventa(
id_venta int not null,
id_producto int not null,
cantidad int not null,
preciov float not null,
primary key(id_venta,id_producto),
foreign key(id_venta)references notaventa(id_venta),
foreign key(id_producto)references producto(id_producto),
)

create table historial_ven(
 id int identity(1,1) primary key,
 fecha date,
 transaccion varchar(20),
 cod_tabla int,
 usuario varchar(20)
)

insert into cliente values(1,'Carlos Perez',73145789,'Bolivar 560')
insert into cliente values(2,'Maria Suarez',70078456,'Sucre 354')
insert into cliente values(3,'Elvis Quinteros',67553789,'Warnes 920')

insert into notaventa values(1,'2023-01-05',700,1)
insert into notaventa values(2,'2023-01-05',240,2)
insert into notaventa values(3,'2023-01-06',240,1)
insert into notaventa values(4,'2023-01-07',450,1)
insert into notaventa values(5,'2023-01-07',500,2)
insert into notaventa values(6,'2023-02-01',500,2)
insert into notaventa values(7,'2023-02-01',120,3)


insert into categoria values(1,'MEMORIA')
insert into categoria values(2,'DISCO DURO')
insert into categoria values(3,'TARJETA MADRE')
SELECT*FROM categoria

insert into producto values(1,'RAM 2Gb marvision',200,1000,1)
insert into producto values(2,'RAM 1Gb marvision',120,500,1)
insert into producto values(3,'HDD Samsung 1Tb',450,500,2)
insert into producto values(4,'HDD Toshiba 1Tb',500,500,2)
insert into producto values(5,'MB Intel s.v',900,300,3)
SELECT*FROM producto

insert into detalleventa values(1,1,1,200)
insert into detalleventa values(1,4,1,500)
insert into detalleventa values(2,2,2,120)
insert into detalleventa values(3,2,2,120)
insert into detalleventa values(4,3,1,450)
insert into detalleventa values(5,4,1,500)
insert into detalleventa values(6,4,1,500)
insert into detalleventa values(7,2,1,120)

select *from cliente
select *from categoria
select *from detalleventa
select *from notaventa
select *from producto


