-- Gerado por Oracle SQL Developer Data Modeler 24.3.1.351.0831
--   em:        2025-08-24 22:11:16 BRT
--   site:      Oracle Database 11g
--   tipo:      Oracle Database 11g



DROP TABLE leituras_sensores CASCADE CONSTRAINTS 
;

DROP TABLE maquinas CASCADE CONSTRAINTS 
;

DROP TABLE ocorrencias CASCADE CONSTRAINTS 
;

DROP TABLE parametros CASCADE CONSTRAINTS 
;

DROP TABLE parametros_maquinas_sensores CASCADE CONSTRAINTS 
;

-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE leituras_sensores 
    ( 
     id_leitura_sensor INTEGER  NOT NULL , 
     data_hora         TIMESTAMP WITH LOCAL TIME ZONE  NOT NULL , 
     temperatura       NUMBER (4,2)  NOT NULL , 
     vibracao          NUMBER (4,2)  NOT NULL , 
     corrente          NUMBER (4,2)  NOT NULL , 
     pressao           NUMBER (5,2)  NOT NULL , 
     umidade           NUMBER (4,2)  NOT NULL , 
     tensao            NUMBER (5,2)  NOT NULL , 
     nivel             INTEGER  NOT NULL , 
     velocidade        INTEGER  NOT NULL , 
     posicao           INTEGER  NOT NULL , 
     qualidade_ar      INTEGER  NOT NULL , 
     fumaca            CHAR (1)  NOT NULL 
    ) 
;

ALTER TABLE leituras_sensores 
    ADD CONSTRAINT PK_leituras_sensores PRIMARY KEY ( id_leitura_sensor ) ;

CREATE TABLE maquinas 
    ( 
     id_maquina         INTEGER  NOT NULL , 
     nome               VARCHAR2 (255)  NOT NULL , 
     numero_serie       VARCHAR2 (100)  NOT NULL , 
     modelo             VARCHAR2 (100)  NOT NULL , 
     fabricante         VARCHAR2 (100)  NOT NULL , 
     localizacao        VARCHAR2 (100)  NOT NULL , 
     data_instalacao    DATE  NOT NULL , 
     status             VARCHAR2 (50)  NOT NULL , 
     ultima_manutencao  DATE , 
     proxima_manutencao DATE 
    ) 
;
CREATE INDEX UN_maquinas_numero_serie ON maquinas 
    ( 
     numero_serie ASC 
    ) 
;

ALTER TABLE maquinas 
    ADD CONSTRAINT CK_maquinas_proxima_manutencao 
    CHECK (proxima_manutencao > ultima_manutencao)
;


ALTER TABLE maquinas 
    ADD CONSTRAINT CK_maquinas_ultima_manutencao 
    CHECK (ultima_manutencao < proxima_manutencao)
;
ALTER TABLE maquinas 
    ADD CONSTRAINT PK_maquinas PRIMARY KEY ( id_maquina ) ;

CREATE TABLE ocorrencias 
    ( 
     id_ocorrencia          INTEGER  NOT NULL , 
     id_leitura_sensor      INTEGER  NOT NULL , 
     id_parametros          INTEGER  NOT NULL , 
     id_maquina             INTEGER  NOT NULL , 
     nmr_ocorrencia         INTEGER  NOT NULL , 
     tipo_anomalia          VARCHAR2 (100)  NOT NULL , 
     severidade             VARCHAR2 (20)  NOT NULL , 
     descricao              VARCHAR2 (500) , 
     status_ocorrencia      VARCHAR2 (50)  NOT NULL , 
     data_hora_abertura     DATE  NOT NULL , 
     data_hora_encerramento DATE 
    ) 
;
CREATE UNIQUE INDEX IDX_ocorrencias_ ON ocorrencias 
    ( 
     id_leitura_sensor ASC 
    ) 
;

ALTER TABLE ocorrencias 
    ADD CONSTRAINT CK_ocorrencias_dt_hr_encerrar 
    CHECK (data_hora_encerramento > data_hora_abertura)
;
ALTER TABLE ocorrencias 
    ADD CONSTRAINT PK_ocorrencias PRIMARY KEY ( id_ocorrencia, id_leitura_sensor, id_parametros, id_maquina ) ;

ALTER TABLE ocorrencias 
    ADD CONSTRAINT UN_ocorrencias_nmr_ocorrencia UNIQUE ( nmr_ocorrencia ) ;

CREATE TABLE parametros 
    ( 
     id_parametros  INTEGER  NOT NULL , 
     descricao_tipo VARCHAR2 (100)  NOT NULL 
    ) 
;

ALTER TABLE parametros 
    ADD CONSTRAINT PK_parametros PRIMARY KEY ( id_parametros ) ;

ALTER TABLE parametros 
    ADD CONSTRAINT UN_parametros_descricao_tipo UNIQUE ( descricao_tipo ) ;

CREATE TABLE parametros_maquinas_sensores 
    ( 
     id_maquina    INTEGER  NOT NULL , 
     id_parametros INTEGER  NOT NULL , 
     valor_maximo  NUMBER  NOT NULL , 
     valor_minimo  NUMBER  NOT NULL 
    ) 
;

ALTER TABLE parametros_maquinas_sensores 
    ADD CONSTRAINT PK_parametros_maquinas_sens PRIMARY KEY ( id_maquina, id_parametros ) ;

ALTER TABLE ocorrencias 
    ADD CONSTRAINT FK_ocorrencias_leit_sens FOREIGN KEY 
    ( 
     id_leitura_sensor
    ) 
    REFERENCES leituras_sensores 
    ( 
     id_leitura_sensor
    ) 
;

ALTER TABLE ocorrencias 
    ADD CONSTRAINT FK_ocorrencias_param_maq_sens FOREIGN KEY 
    ( 
     id_maquina,
     id_parametros
    ) 
    REFERENCES parametros_maquinas_sensores 
    ( 
     id_maquina,
     id_parametros
    ) 
;

ALTER TABLE parametros_maquinas_sensores 
    ADD CONSTRAINT FK_parametros_maq_sens_m FOREIGN KEY 
    ( 
     id_maquina
    ) 
    REFERENCES maquinas 
    ( 
     id_maquina
    ) 
;

ALTER TABLE parametros_maquinas_sensores 
    ADD CONSTRAINT FK_parametros_maq_sens_p FOREIGN KEY 
    ( 
     id_parametros
    ) 
    REFERENCES parametros 
    ( 
     id_parametros
    ) 
;



-- Relatório do Resumo do Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                             5
-- CREATE INDEX                             2
-- ALTER TABLE                             14
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
