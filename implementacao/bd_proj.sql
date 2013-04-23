BEGIN;

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
  no_orgao varchar(250) NOT NULL,
  CONSTRAINT pk_tb002 PRIMARY KEY (id_orgao)
);

CREATE SEQUENCE sq003_pk;

CREATE TABLE tb003_tipo_vinculo
(
  id_tipo_vinculo integer NOT NULL DEFAULT nextval('sq003_pk'::regclass),
  no_tipo_vinculo varchar(250) NOT NULL,
  CONSTRAINT pk_tb003 PRIMARY KEY (id_vinculo)
);


CREATE SEQUENCE sq004_pk;

CREATE TABLE tb004_empregado
(
  id_empregado integer NOT NULL DEFAULT nextval('sq004_pk'::regclass),
  no_empregado character varying(50),
  dt_contratacao date,
  dt_desligamento date,
  dt_nascimento date,
  nu_matricula character varying(8),
  id_orgao integer NOT NULL,
  CONSTRAINT pk_cectb004 PRIMARY KEY (id_empregado),
  CONSTRAINT fk_tb004_tb002 FOREIGN KEY (id_orgao)
      REFERENCES tb002_orgao (id_orgao)
);

CREATE SEQUENCE sq005_pk;

CREATE TABLE tb005_empregado_dependente
(
  id_empregado_dependente integer NOT NULL DEFAULT nextval('sq005_pk'::regclass),
  id_empregado integer NOT NULL,
  id_tipo_vinculo NOT NULL,
  no_empregado_dependente character varying(50),
  dt_nascimento date,
  CONSTRAINT pk_cectb005 PRIMARY KEY (id_empregado_dependente),
  CONSTRAINT fk_tb005_tb004 FOREIGN KEY (id_empregado)
      REFERENCES tb004_empregado (id_empregado),
  CONSTRAINT fk_tb005_tb003 FOREIGN KEY (id_tipo_vinculo)
      REFERENCES tb003_tipo_vinculo (id_tipo_vinculo)
);

CREATE SEQUENCE sq006_pk;

CREATE TABLE tb006_documento
(
  id_documento integer NOT NULL DEFAULT nextval('sq006_pk'::regclass),
  id_tipo_documento integer NOT NULL,
  id_empregado integer NOT NULL,
  id_empregado_dependente integer,
  no_documento varchar(250) NOT NULL,
  dh_upload timestamp NOT NULL,
  CONSTRAINT pk_tb006 PRIMARY KEY (id_documento),
  CONSTRAINT fk_tb006_tb001 FOREIGN KEY (id_tipo_documento)
      REFERENCES tb001_tipo_documento (id_tipo_documento),
  CONSTRAINT fk_tb006_tb004 FOREIGN KEY (id_empregado)
      REFERENCES tb004_empregado (id_empregado),
  CONSTRAINT fk_tb006_tb005 FOREIGN KEY (id_empregado_dependente)
      REFERENCES tb005_empregado_dependente (id_empregado_dependente)
);

COMMIT;