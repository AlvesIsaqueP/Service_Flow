import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os

def conectar():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

# CLIENTES
def adicionar_cliente(nome, telefone, email, endereco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes (nome, telefone, email, endereco)
        VALUES (%s, %s, %s, %s)
    ''', (nome, telefone, email, endereco))
    conn.commit()
    cursor.close()
    conn.close()

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return clientes

def buscar_cliente_por_id(cliente_id):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (cliente_id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    return cliente

def atualizar_cliente(cliente_id, nome, telefone, email, endereco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clientes
        SET nome = %s, telefone = %s, email = %s, endereco = %s
        WHERE id = %s
    ''', (nome, telefone, email, endereco, cliente_id))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
    conn.commit()
    cursor.close()
    conn.close()

# ORDENS DE SERVIÇO
def buscar_ordens(termo):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    termo = f'%{termo}%'
    cursor.execute('''
        SELECT o.id, c.nome, o.descricao, o.status, o.data_abertura
        FROM ordens_servico o
        JOIN clientes c ON o.cliente_id = c.id
        WHERE o.descricao LIKE %s OR o.status LIKE %s OR c.nome LIKE %s
        ORDER BY o.data_abertura DESC
    ''', (termo, termo, termo))
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado

def adicionar_ordem(cliente_id, descricao, setor, status):
    conn = conectar()
    cursor = conn.cursor()
    data_abertura = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO ordens_servico (cliente_id, descricao, setor, status, data_abertura)
        VALUES (%s, %s, %s, %s, %s)
    ''', (cliente_id, descricao, setor, status, data_abertura))
    conn.commit()
    cursor.close()
    conn.close()

def listar_ordens():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('''
        SELECT o.id, c.nome, o.descricao, o.status, o.data_abertura
        FROM ordens_servico o
        JOIN clientes c ON o.cliente_id = c.id
    ''')
    ordens = cursor.fetchall()
    cursor.close()
    conn.close()
    return ordens

def buscar_ordem_por_id(ordem_id):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM ordens_servico WHERE id = %s", (ordem_id,))
    ordem = cursor.fetchone()
    cursor.close()
    conn.close()
    return ordem

def atualizar_ordem(ordem_id, descricao, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE ordens_servico
        SET descricao = %s, status = %s
        WHERE id = %s
    ''', (descricao, status, ordem_id))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_ordem(ordem_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ordens_servico WHERE id = %s", (ordem_id,))
    conn.commit()
    cursor.close()
    conn.close()
def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            telefone TEXT,
            email TEXT,
            endereco TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ordens_servico (
            id SERIAL PRIMARY KEY,
            cliente_id INTEGER REFERENCES clientes(id),
            descricao TEXT,
            setor TEXT,
            status TEXT,
            data_abertura TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# Chama a função automaticamente quando o módulo for importado
criar_tabelas()
