
select * from users

select * from prestador


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
	[admin]			BINARY					NOT NULL
)

insert into users values ('5','bruno gay','123456978','2020','Boqueteiro','11:00','10pm','todo dia','rua do rato vei','bruno','321',0)

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


create table ponto (
	id			INT IDENTITY(1,1) PRIMARY KEY,
	id_ponto 	INTEGER	FOREIGN KEY REFERENCES users(id_ponto),
	dataHora	DATETIME
)

select * from prestador

select * from controle_acesso

insert into controle_acesso values (1,Null,DATEADD(hour,-3,getdate()),Null,1,Null)

select * from users

select DATEADD(hour,-3,getdate())


