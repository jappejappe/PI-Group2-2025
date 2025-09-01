CREATE TABLE compradores (
    id_comprador SERIAL NOT NULL,
    nome_cliente VARCHAR NOT NULL,
    apelido_cliente VARCHAR NOT NULL,
    email_cliente VARCHAR NOT NULL,
    data_nascimento DATE NOT NULL,
    cep_cliente CHAR(8) NULL,
    cpf_cliente CHAR(11) NULL,
    senha VARCHAR NOT NULL,
	foto TEXT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT compradores_unique UNIQUE (apelido_cliente, email_cliente, cpf_cliente),
    CONSTRAINT compradores_pk PRIMARY KEY (id_comprador)
);


CREATE TABLE vendedores (
	id_vendedor SERIAL NOT NULL,
	cep_empresa CHAR(8) NULL,
	nome_empresa VARCHAR NOT NULL,
	telefone_empresa VARCHAR NULL,
	email_empresa VARCHAR NOT NULL,
	descricao_empresa VARCHAR NULL,
    id_comprador INTEGER NOT NULL REFERENCES compradores(id_comprador),
	CONSTRAINT vendedores_unique UNIQUE (id_vendedor,email_empresa,telefone_empresa,id_comprador),
	CONSTRAINT vendedores_pk PRIMARY KEY (id_vendedor)
);


CREATE TABLE tipos_produtos (
	tipo VARCHAR NOT NULL,
	id_tipo SERIAL NOT NULL,
	CONSTRAINT tipos_produtos_unique UNIQUE (tipo,id_tipo),
	CONSTRAINT tipos_produtos_pk PRIMARY KEY (id_tipo)
);


CREATE TABLE condicoes_produtos (
	id_condicao SERIAL NOT NULL,
	condicao VARCHAR NOT NULL,
	CONSTRAINT condicoes_produtos_unique UNIQUE (id_condicao,condicao),
	CONSTRAINT condicoes_produtos_pk PRIMARY KEY (id_condicao)
);


CREATE TABLE carregamentos (
	id_carregamento SERIAL NOT NULL,
	carregamento VARCHAR NOT NULL,
	CONSTRAINT carregamentos_unique UNIQUE (id_carregamento,carregamento),
	CONSTRAINT carregamentos_pk PRIMARY KEY (id_carregamento)
);


CREATE TABLE vendedores_carregamento (
	id_vendedor INTEGER NOT NULL REFERENCES vendedores(id_vendedor),
	id_carregamento INTEGER NOT NULL REFERENCES carregamentos(id_carregamento)
);


CREATE TABLE usuarios (
	id_comprador INTEGER NOT NULL REFERENCES compradores(id_comprador),
	id_vendedor INTEGER NULL REFERENCES vendedores(id_vendedor),
	id_usuario SERIAL NOT NULL,
	CONSTRAINT usuarios_unique UNIQUE (id_usuario,id_vendedor,id_comprador),
	CONSTRAINT usuarios_pk PRIMARY KEY (id_usuario)
);


CREATE TABLE anuncios (
	id_anuncio SERIAL NOT NULL,
	titulo_anuncio VARCHAR NOT NULL,
	tipo_anuncio INTEGER NOT NULL REFERENCES tipos_produtos(id_tipo),
	descricao_anuncio VARCHAR NULL,
	condicao_anuncio INTEGER NOT NULL,
	quantidade_anuncio INTEGER DEFAULT 1 NOT NULL,
	preco_anuncio INTEGER DEFAULT 0 NOT NULL,
	data_criacao timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	id_vendedor INTEGER NOT NULL REFERENCES vendedores(id_vendedor),
	CONSTRAINT anuncios_unique UNIQUE (id_anuncio),
	CONSTRAINT anuncios_pk PRIMARY KEY (id_anuncio)
);


CREATE TABLE carrinhos (
	id_comprador INTEGER NOT NULL REFERENCES compradores(id_comprador),
	id_produto INTEGER NOT NULL REFERENCES anuncios(id_anuncio),
	quantidade INTEGER NOT NULL,
	data_adicao timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL
);


CREATE TABLE fotos_anuncios (
	id_anuncio INTEGER NOT NULL REFERENCES anuncios(id_anuncio),
	id_foto SERIAL NOT NULL,
	foto TEXT NOT NULL,
	CONSTRAINT fotos_anuncios_unique UNIQUE (id_foto),
	CONSTRAINT fotos_anuncios_pk PRIMARY KEY (id_foto)
);