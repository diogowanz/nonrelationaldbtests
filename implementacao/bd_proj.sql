BEGIN;

drop table if exists tb007_documento_dependente;
drop sequence if exists sq007_pk;
drop table if exists tb006_documento_empregado;
drop sequence if exists sq006_pk;
drop table if exists tb005_empregado_dependente;
drop sequence if exists sq005_pk;
drop table if exists tb004_empregado;
drop sequence if exists sq004_pk;
drop table if exists tb003_tipo_vinculo;
drop sequence if exists sq003_pk;
drop table if exists tb002_orgao;
drop sequence if exists sq002_pk;
drop table if exists tb001_tipo_documento;
drop sequence if exists sq001_pk;


CREATE SEQUENCE sq001_pk;

CREATE TABLE tb001_tipo_documento
(
  id_tipo_documento integer NOT NULL DEFAULT nextval('sq001_pk'::regclass),
  no_tipo_documento character varying(50),
  ic_ativo boolean,
  CONSTRAINT pk_tb001 PRIMARY KEY (id_tipo_documento)
);

CREATE SEQUENCE sq002_pk;

CREATE TABLE tb002_orgao
(
  id_orgao integer NOT NULL DEFAULT nextval('sq002_pk'::regclass),
  nu_cnpj numeric(14,0) NOT NULL,
  no_orgao character varying(250) NOT NULL,
  no_cidade character varying(250) NOT NULL,
  no_endereco character varying(250) NOT NULL,
  no_uf character varying(2) NOT NULL,
  CONSTRAINT pk_tb002 PRIMARY KEY (id_orgao)
);

CREATE SEQUENCE sq003_pk;

CREATE TABLE tb003_tipo_vinculo
(
  id_tipo_vinculo integer NOT NULL DEFAULT nextval('sq003_pk'::regclass),
  no_tipo_vinculo varchar(250) NOT NULL,
  CONSTRAINT pk_tb003 PRIMARY KEY (id_tipo_vinculo)
);


CREATE SEQUENCE sq004_pk;

CREATE TABLE tb004_empregado
(
  id_empregado integer NOT NULL DEFAULT nextval('sq004_pk'::regclass),
  no_empregado character varying(150),
  dt_contratacao date,
  dt_desligamento date,
  dt_nascimento date,
  nu_matricula character varying(8),
  nu_rg numeric(7,0),
  nu_cpf numeric(11,0),
  id_orgao integer NOT NULL,
  CONSTRAINT pk_cectb004 PRIMARY KEY (id_empregado),
  CONSTRAINT fk_tb004_tb002 FOREIGN KEY (id_orgao)
      REFERENCES tb002_orgao (id_orgao) 
);

CREATE SEQUENCE sq005_pk;

CREATE TABLE tb005_empregado_dependente
(
  id_empregado_dependente integer NOT NULL DEFAULT nextval('sq005_pk'::regclass),
  no_empregado_dependente character varying(150),
  nu_rg numeric(7,0),
  nu_cpf numeric(11,0),
  nu_certidao numeric(11,0),
  id_empregado integer NOT NULL,
  id_tipo_vinculo integer NOT NULL,
  dt_nascimento date,
  CONSTRAINT pk_cectb005 PRIMARY KEY (id_empregado_dependente),
  CONSTRAINT fk_tb005_tb003 FOREIGN KEY (id_tipo_vinculo)
      REFERENCES tb003_tipo_vinculo (id_tipo_vinculo),
  CONSTRAINT fk_tb005_tb004 FOREIGN KEY (id_empregado)
      REFERENCES tb004_empregado (id_empregado)
);

CREATE SEQUENCE sq006_pk;

CREATE TABLE tb006_documento_empregado
(
  id_documento integer NOT NULL DEFAULT nextval('sq006_pk'::regclass),
  id_tipo_documento integer NOT NULL,
  id_empregado integer NOT NULL,
  no_documento character varying(250) NOT NULL,
  dh_upload timestamp without time zone NOT NULL,
  CONSTRAINT pk_tb006 PRIMARY KEY (id_documento),
  CONSTRAINT fk_tb006_tb001 FOREIGN KEY (id_tipo_documento)
      REFERENCES tb001_tipo_documento (id_tipo_documento),
  CONSTRAINT fk_tb006_tb004 FOREIGN KEY (id_empregado)
      REFERENCES tb004_empregado (id_empregado)
);

CREATE SEQUENCE sq007_pk;

CREATE TABLE tb007_documento_dependente
(
  id_documento integer NOT NULL DEFAULT nextval('sq007_pk'::regclass),
  id_tipo_documento integer NOT NULL,
  id_empregado_dependente integer,
  no_documento character varying(250) NOT NULL,
  dh_upload timestamp without time zone NOT NULL,
  CONSTRAINT pk_tb007 PRIMARY KEY (id_documento),
  CONSTRAINT fk_tb007_tb001 FOREIGN KEY (id_tipo_documento)
      REFERENCES tb001_tipo_documento (id_tipo_documento),
  CONSTRAINT fk_tb007_tb005 FOREIGN KEY (id_empregado_dependente)
      REFERENCES tb005_empregado_dependente (id_empregado_dependente)
);

insert into tb001_tipo_documento (no_tipo_documento, ic_ativo) values ('RG',TRUE);
insert into tb001_tipo_documento (no_tipo_documento, ic_ativo) values ('CPF',TRUE);
insert into tb001_tipo_documento (no_tipo_documento, ic_ativo) values ('CERTIDAO DE CASAMENTO',TRUE);
insert into tb001_tipo_documento (no_tipo_documento, ic_ativo) values ('CERTIDAO DE NASCIMENTO',TRUE);
insert into tb001_tipo_documento (no_tipo_documento, ic_ativo) values ('COMPROVANTE DE RESIDENCIA',TRUE);
insert into tb001_tipo_documento (no_tipo_documento, ic_ativo) values ('DIPLOMA',TRUE);
insert into tb001_tipo_documento (no_tipo_documento, ic_ativo) values ('CERTIFICADO',TRUE);

insert into tb003_tipo_vinculo (no_tipo_vinculo) values ('CONJUGE');
insert into tb003_tipo_vinculo (no_tipo_vinculo) values ('FILHO');
insert into tb003_tipo_vinculo (no_tipo_vinculo) values ('PAI');
insert into tb003_tipo_vinculo (no_tipo_vinculo) values ('MAE');
insert into tb003_tipo_vinculo (no_tipo_vinculo) values ('SOGRO');
insert into tb003_tipo_vinculo (no_tipo_vinculo) values ('SOGRA');
insert into tb003_tipo_vinculo (no_tipo_vinculo) values ('ENTEADO');

COMMIT;
