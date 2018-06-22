CREATE TABLE tb_leito(
    id_leito     SERIAL,
    id_leito_unidade    INTEGER NOT NULL,
    id_estado_leito  INTEGER NOT NULL,
    id_estabelecimento_saude INTEGER NOT NULL,
    area                VARCHAR(100) NOT NULL,
    PRIMARY KEY(id_leito),
    UNIQUE(id_leito_unidade, id_estabelecimento_saude)
)

CREATE TABLE tb_estabelecimento_saude(
    id_estabelecimento_saude    SERIAL,
    id_municipio                   INTEGER NOT NULL,
    cod_cnes                    INTEGER NOT NULL,
    PRIMARY KEY(id_estabelecimento_saude),
    FOREIGN KEY(id_municipio) REFERENCES tb_municipio(id_municipio)
)

CREATE TABLE tb_estado(
    id_estado   SERIAL,
    cod_uf      INTEGER,
    sigla       VARCHAR(2) NOT NULL,
    descricao   VARCHAR(100) NOT NULL,
    PRIMARY KEY(id_estado),
    UNIQUE(cod_uf)
)

CREATE TABLE tb_municipio(
    id_municipio    SERIAL,
    id_estado       INTEGER NOT NULL,
    nome            VARCHAR(100) NOT NULL,
    cod_ibge        INTEGER NOT NULL,
    PRIMARY KEY(id_municipio),
    FOREIGN KEY(id_estado) REFERENCES tb_estado(cod_uf)
)

CREATE TABLE tb_referencia(
    id_referencia   SERIAL,
    descricao       TEXT,
    PRIMARY KEY(id_referencia)
)

CREATE TABLE tb_classificacao(
    id_classificacao    SERIAL,
    id_referencia       INTEGER,
    id_leito            INTEGER,
    id_tipo_ref         INTEGER,
    PRIMARY KEY(id_classificacao),
    UNIQUE(id_referencia, id_leito),
    FOREIGN KEY(id_leito) REFERENCES tb_leito(id_leito),
    FOREIGN KEY(id_referencia) REFERENCES tb_referencia(id_referencia)
)