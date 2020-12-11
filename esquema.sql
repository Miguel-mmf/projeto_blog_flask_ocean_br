DROP TABLE IF EXISTS entradas;
-- cria tabela para guardar os posts do blog
CREATE TABLE entradas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title STRING NOT NULL,
    texto STRING NOT NULL
);

-- criação de um esquema para armazenar o conteúdo enviado pelos usuários do blog