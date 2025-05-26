from flask import Flask, render_template, request, redirect, url_for
from funcoes import criar_tabelas
criar_tabelas()
from funcoes import (
    adicionar_cliente,
    buscar_ordens,
    listar_clientes,
    buscar_cliente_por_id,
    atualizar_cliente,
    deletar_cliente,
    adicionar_ordem,
    listar_ordens,
    buscar_ordem_por_id,
    atualizar_ordem,
    deletar_ordem
)

app = Flask(__name__)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Listar clientes
@app.route('/clientes')
def clientes():
    clientes = listar_clientes()
    return render_template('clientes.html', clientes=clientes)

# Adicionar cliente (GET exibe formulário, POST salva)
@app.route('/clientes/novo', methods=['GET', 'POST'])
def novo_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        adicionar_cliente(nome, email, telefone, endereco)
        return redirect(url_for('clientes'))
    return render_template('novo_cliente.html')

# Editar cliente
@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = buscar_cliente_por_id(id)
    if not cliente:
        return "Cliente não encontrado", 404
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        atualizar_cliente(id, nome, email, telefone)
        return redirect(url_for('clientes'))
    return render_template('editar_cliente.html', cliente=cliente)

# Deletar cliente
@app.route('/clientes/deletar/<int:id>', methods=['POST'])
def deletar_cliente_route(id):
    deletar_cliente(id)
    return redirect(url_for('clientes'))

# Listar ordens de serviço
@app.route('/ordens')
def ordens():
    query = request.args.get('q', '').strip()
    if query:
        ordens = buscar_ordens(query)  # função que busca as ordens filtrando pelo termo
    else:
        ordens = listar_ordens()
    return render_template('ordens.html', ordens=ordens)

# Adicionar ordem
@app.route('/ordens/novo', methods=['GET', 'POST'])
def nova_ordem():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        descricao = request.form['descricao']
        status = request.form['status']
        setor = request.form['setor']
        adicionar_ordem(cliente_id, descricao, setor, status)
        return redirect(url_for('ordens'))
    return render_template('nova_ordem.html')

# Editar ordem
@app.route('/ordens/editar/<int:id>', methods=['GET', 'POST'])
def editar_ordem(id):
    ordem = buscar_ordem_por_id(id)
    if not ordem:
        return "Ordem não encontrada", 404
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        descricao = request.form['descricao']
        setor = request.form['setor']
        status = request.form['status']
        atualizar_ordem(id, cliente_id, descricao, status)
        return redirect(url_for('ordens'))
    return render_template('editar_ordem.html', ordem=ordem)

# Deletar ordem
@app.route('/ordens/deletar/<int:id>', methods=['POST'])
def deletar_ordem_route(id):
    deletar_ordem(id)
    return redirect(url_for('ordens'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

