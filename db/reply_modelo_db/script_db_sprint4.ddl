-- Gerado por Oracle SQL Developer Data Modeler 24.3.1.351.0831
--   em:        2025-09-29 21:35:25 BRT
--   site:      Oracle Database 11g
--   tipo:      Oracle Database 11g



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE configuracao_parametros 
    ( 
     id_maquina          INTEGER  NOT NULL , 
     id_tipos_parametros INTEGER  NOT NULL , 
     valor_maximo        NUMBER  NOT NULL , 
     valor_minimo        NUMBER  NOT NULL 
    ) 
;

COMMENT ON TABLE configuracao_parametros IS 'Armazena os limites de valor para um tipo de parâmetro em uma máquina específica'
;

ALTER TABLE configuracao_parametros 
    ADD CONSTRAINT PK_config_parametros PRIMARY KEY ( id_maquina, id_tipos_parametros ) ;

CREATE TABLE leituras_sensores 
    ( 
     id_leitura_sensor   INTEGER  NOT NULL , 
     id_sensor           INTEGER  NOT NULL , 
     id_tipos_parametros INTEGER  NOT NULL , 
     valor               NUMBER (10,4)  NOT NULL , 
     unidade             VARCHAR2 (10)  NOT NULL , 
     data_hora           TIMESTAMP WITH LOCAL TIME ZONE  NOT NULL 
    ) 
;

COMMENT ON COLUMN leituras_sensores.valor IS 'valor medido pelo sensor' 
;

COMMENT ON COLUMN leituras_sensores.unidade IS 'Ex: ''°C'', ''bar'', ''A'' etc
' 
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

ALTER TABLE maquinas 
    ADD CONSTRAINT CK_maquinas_status 
    CHECK (status IN ('Em operacao', 'Em manutencao', 'Fora de operacao'))
;


ALTER TABLE maquinas 
    ADD CONSTRAINT CK_maquinas_manutencao 
    CHECK (ultima_manutencao < proxima_manutencao OR (ultima_manutencao IS NULL AND proxima_manutencao IS NOT NULL) OR (ultima_manutencao IS NULL AND proxima_manutencao IS NULL))
;
ALTER TABLE maquinas 
    ADD CONSTRAINT PK_maquinas PRIMARY KEY ( id_maquina ) ;

ALTER TABLE maquinas 
    ADD CONSTRAINT UN_maquinas_nmr_serie UNIQUE ( numero_serie ) ;

CREATE TABLE ocorrencias 
    ( 
     id_ocorrencia         INTEGER  NOT NULL , 
     id_leitura_sensor     INTEGER  NOT NULL , 
     nmr_ocorrencia        INTEGER  NOT NULL , 
     tipo_anomalia         VARCHAR2 (100)  NOT NULL , 
     severidade            VARCHAR2 (20)  NOT NULL , 
     descricao             VARCHAR2 (500) , 
     status_ocorrencia     VARCHAR2 (50)  NOT NULL , 
     data_hora             TIMESTAMP WITH LOCAL TIME ZONE  NOT NULL , 
     limite_maximo_violado NUMBER (10,4) , 
     limite_minimo_violado NUMBER (10,4) 
    ) 
;

COMMENT ON COLUMN ocorrencias.nmr_ocorrencia IS 'número exclusivo (como um número de protocolo)' 
;

COMMENT ON COLUMN ocorrencias.descricao IS 'descrição da ocorrencia que foi registrada' 
;

COMMENT ON COLUMN ocorrencias.data_hora IS 'Registra a data e hora que a ocorrência foi registrada
' 
;
CREATE UNIQUE INDEX IDX_ocorrencias_leitua ON ocorrencias 
    ( 
     id_leitura_sensor ASC 
    ) 
;

ALTER TABLE ocorrencias 
    ADD CONSTRAINT CK_ocorrencias_limite_violado 
    CHECK (limite_maximo_violado IS NOT NULL OR limite_minimo_violado IS NOT NULL)
;


ALTER TABLE ocorrencias 
    ADD CONSTRAINT CK_ocorrencias_status 
    CHECK (status_ocorrencia IN ('Aberta', 'Em Analise', 'Resolvida', 'Cancelada'))
;


ALTER TABLE ocorrencias 
    ADD CONSTRAINT CK_ocorrencias_severidade 
    CHECK (severidade IN ('Baixa', 'Media', 'Alta'))
;
ALTER TABLE ocorrencias 
    ADD CONSTRAINT PK_ocorrencias PRIMARY KEY ( id_ocorrencia ) ;

ALTER TABLE ocorrencias 
    ADD CONSTRAINT UN_ocorrencias_nmr_ocorr UNIQUE ( nmr_ocorrencia ) ;

CREATE TABLE sensores 
    ( 
     id_sensor   INTEGER  NOT NULL , 
     id_maquina  INTEGER  NOT NULL , 
     nome_sensor VARCHAR2 (50) , 
     ativo       CHAR (1) 
    ) 
;

ALTER TABLE sensores 
    ADD CONSTRAINT PK_sensores PRIMARY KEY ( id_sensor ) ;

CREATE TABLE tipos_parametros 
    ( 
     id_tipos_parametros INTEGER  NOT NULL , 
     descricao_tipo      VARCHAR2 (100)  NOT NULL 
    ) 
;

COMMENT ON COLUMN tipos_parametros.descricao_tipo IS '"temperatura", "vibracao"," corrente", "velocidade", "posicao", "pressao", "nivel", "qualidade_ar", "umidade", "tensao", "fumaca"
' 
;
CREATE UNIQUE INDEX UN_tipos_param_descricao ON tipos_parametros 
    ( 
     descricao_tipo ASC 
    ) 
;

ALTER TABLE tipos_parametros 
    ADD CONSTRAINT PK_parametros PRIMARY KEY ( id_tipos_parametros ) ;

ALTER TABLE configuracao_parametros 
    ADD CONSTRAINT FK_config_param_tipos FOREIGN KEY 
    ( 
     id_tipos_parametros
    ) 
    REFERENCES tipos_parametros 
    ( 
     id_tipos_parametros
    ) 
;

ALTER TABLE configuracao_parametros 
    ADD CONSTRAINT FK_config_parametros FOREIGN KEY 
    ( 
     id_maquina
    ) 
    REFERENCES maquinas 
    ( 
     id_maquina
    ) 
;

ALTER TABLE leituras_sensores 
    ADD CONSTRAINT FK_leituras_sensores FOREIGN KEY 
    ( 
     id_sensor
    ) 
    REFERENCES sensores 
    ( 
     id_sensor
    ) 
;

ALTER TABLE leituras_sensores 
    ADD CONSTRAINT FK_leituras_tipos_param FOREIGN KEY 
    ( 
     id_tipos_parametros
    ) 
    REFERENCES tipos_parametros 
    ( 
     id_tipos_parametros
    ) 
;

ALTER TABLE ocorrencias 
    ADD CONSTRAINT FK_ocorrencias_leituras FOREIGN KEY 
    ( 
     id_leitura_sensor
    ) 
    REFERENCES leituras_sensores 
    ( 
     id_leitura_sensor
    ) 
;

ALTER TABLE sensores 
    ADD CONSTRAINT FK_sensores_maquinas FOREIGN KEY 
    ( 
     id_maquina
    ) 
    REFERENCES maquinas 
    ( 
     id_maquina
    ) 
;



-- Relatório do Resumo do Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                             6
-- CREATE INDEX                             2
-- ALTER TABLE                             19
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
