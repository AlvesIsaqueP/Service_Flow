import sqlite3

con = sqlite3.connect("sf.db")
cursor = con.cursor()

# Criar tabela de clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    email TEXT,
    endereco TEXT
)
""")

# Criar tabela de ordens de serviço
cursor.execute("""
CREATE TABLE IF NOT EXISTS ordens_servico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    descricao TEXT NOT NULL,
    data_abertura TEXT,
    setor TEXT,
    status TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
)
""")

con.commit()
con.close()

print("Tabelas criadas com sucesso.")
