import sqlite3
from datetime import datetime
import psycopg2
import os

DB_PATH = 'sf.db'

def conectar():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

# CLIENTES
def adicionar_cliente(nome, telefone, email, endereco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes (nome, telefone, email, endereco)
        VALUES (?, ?, ?, ?)
    ''', (nome, telefone, email, endereco))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def buscar_cliente_por_id(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente

def atualizar_cliente(cliente_id, nome, telefone, email, endereco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clientes
        SET nome = ?, telefone = ?, email = ?, endereco = ?
        WHERE id = ?
    ''', (nome, telefone, email, endereco, cliente_id))
    conn.commit()
    conn.close()

def deletar_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()

# ORDENS DE SERVIÇO
def buscar_ordens(termo):
    conn = conectar()
    cursor = conn.cursor()
    termo = f'%{termo}%'
    cursor.execute('''
        SELECT o.id, c.nome, o.descricao, o.status, o.data_abertura
        FROM ordens_servico o
        JOIN clientes c ON o.cliente_id = c.id
        WHERE o.descricao LIKE ? OR o.status LIKE ? OR c.nome LIKE ?
        ORDER BY o.data_abertura DESC
    ''', (termo, termo, termo))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def adicionar_ordem(cliente_id, descricao, setor, status):
    conn = conectar()
    cursor = conn.cursor()
    data_abertura = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO ordens_servico (cliente_id, descricao, setor, status, data_abertura)
        VALUES (?, ?, ?, ?, ?)
    ''', (cliente_id, descricao, setor, status, data_abertura))
    conn.commit()
    conn.close()

def listar_ordens():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.id, c.nome, o.descricao, o.status, o.data_abertura
        FROM ordens_servico o
        JOIN clientes c ON o.cliente_id = c.id
    ''')
    ordens = cursor.fetchall()
    conn.close()
    return ordens

def buscar_ordem_por_id(ordem_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ordens_servico WHERE id = ?", (ordem_id,))
    ordem = cursor.fetchone()
    conn.close()
    return ordem

def atualizar_ordem(ordem_id, descricao, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE ordens_servico
        SET descricao = ?, status = ?
        WHERE id = ?
    ''', (descricao, status, ordem_id))
    conn.commit()
    conn.close()

def deletar_ordem(ordem_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ordens_servico WHERE id = ?", (ordem_id,))
    conn.commit()
    conn.close()
