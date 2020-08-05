
select * from users

select * from prestador


select *  from ponto

truncate table p
truncate table ponto
truncate table ponto

CREATE TABLE users (
	--id				INT IDENTITY(1,1),
	id_ponto		INTEGER	PRIMARY KEY		NOT NULL,
	nome			VARCHAR(255)			NOT NULL,
	documento		VARCHAR(255)			NOT NULL,
	data_admissao	DATE					NOT NULL,
	func			VARCHAR(255)			NOT NULL,
	entrada			TIME					NOT NULL,
	saida			TIME					NOT NULL,
	dia_folga		VARCHAR(255)			NOT NULL,
	endereco		VARCHAR(255)			NOT NULL,
	username		VARCHAR(255) UNIQUE		NOT NULL,
	senha			VARCHAR(255)			NOT NULL,
	[admin]			BIT   					NOT NULL,
	[status]        BIT  					NOT NULL
)

alter table users alter column [status] BIT NOT NULL

select * from users

update users set [status] = 0 where id_ponto = 1

insert into users values (1,'Gabriel Collares','123456789','2020','ADM','00:00','00:00','Sab/Dom','Rua Hilário de Gouveia 120','gabriel','902',1,1)

CREATE TABLE prestador (
	id				INT IDENTITY(1,1) PRIMARY KEY,
	nome			VARCHAR(255)		NOT NULL,
	doc				VARCHAR(255)		NOT NULL,
	empresa			VARCHAR(255)		NOT NULL,
	tipo_servico	VARCHAR(255)		NOT NULL,
	id_ponto 		INTEGER				FOREIGN KEY REFERENCES users(id_ponto) --quem fez o cadastro
)

insert into prestador values ('joao','456','sprite','sprite',1)

CREATE TABLE controle_acesso(
	id				INT IDENTITY(1,1) PRIMARY KEY,
	id_prestador	INTEGER				FOREIGN KEY REFERENCES prestador(id), --quem esta entrando 
	apt				INTEGER NOT NULL,
	h_entrada		DATETIME NOT NULL,
	h_saida 		DATETIME,
	id_ponto_e 		INTEGER				FOREIGN KEY REFERENCES users(id_ponto), --quem deu entrada
	id_ponto_s 		INTEGER				FOREIGN KEY REFERENCES users(id_ponto) --quem deu saida
)

select * from ponto

drop table ponto

create table ponto (
	id			INT IDENTITY(1,1) PRIMARY KEY,
	id_ponto 	INTEGER	FOREIGN KEY REFERENCES users(id_ponto) NOT NULL,
	entrada		DATETIME NOT NULL,
	saida_a		DATETIME,
	volta_a		DATETIME,
	saida       DATETIME
)

truncate table ponto   ok
select * from ponto   ok

delete from prestador
delete from users
delete from  controle_acesso

truncate table prestador
drop table prestador
select * from prestador

truncate table users
drop table  users
select * from users

truncate table controle_acesso
select * from controle_acesso

insert into ponto values
(1, GETDATE(), NULL,NULL,NULL)

select * from prestador

select * from controle_acesso

insert into controle_acesso values (1,Null,DATEADD(hour,-3,getdate()),Null,1,Null)

select * from users

select DATEADD(hour,-3,getdate())

Select *, CAST(validade as DATE) nova_data from mural

select * from mural

create table mural(
	id INT IDENTITY (1,1) PRIMARY KEY,
	titulo VARCHAR(200),
	mensagem VARCHAR(MAX),
	validade DATETIME
)




