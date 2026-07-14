# =============================================================================
# SinaPCP - Aplicação Principal (Rotas da API)
# =============================================================================

# === Dependências Externas ===
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# === Dependências Internas ===
from backend.config import Config
from backend.models import db, Usuario, Produto, OrdemProducao, TarefaKanban, Kpi, Cronograma

# === Inicialização da Aplicação ===
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# =============================================================================
# ROTAS ESTÁTICAS
# =============================================================================

@app.route('/')
def servir_index():
    """Serve o arquivo index.html na raiz."""
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/<path:filename>')
def servir_arquivos(filename):
    """Serve arquivos .html, .css e estáticos."""
    if filename.endswith('.html') or filename.endswith('.css'):
        return send_from_directory(BASE_DIR, filename)
    return send_from_directory(os.path.join(BASE_DIR, 'backend', 'static'), filename)


@app.errorhandler(404)
def not_found(e):
    """Tenta servir como HTML se a rota não for encontrada."""
    path = e.description
    if path:
        return send_from_directory(BASE_DIR, path)
    return jsonify({'error': 'Not found'}), 404


# =============================================================================
# AUTENTICAÇÃO
# =============================================================================

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    matricula = data.get('matricula')
    senha = data.get('senha')
    
    usuario = Usuario.query.filter_by(matricula=matricula).first()
    
    if usuario and check_password_hash(usuario.senha, senha):
        return jsonify({
            'success': True,
            'usuario': usuario.to_dict()
        })
    
    return jsonify({'success': False, 'mensagem': 'Credenciais inválidas'}), 401


# =============================================================================
# USUÁRIOS
# =============================================================================

@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])


@app.route('/api/usuarios', methods=['POST'])
def criar_usuario():
    data = request.json
    usuario = Usuario(
        matricula=data['matricula'],
        nome=data['nome'],
        senha=generate_password_hash(data['senha']),
        perfil=data.get('perfil', 'aluno')
    )
    db.session.add(usuario)
    db.session.commit()
    return jsonify(usuario.to_dict()), 201


@app.route('/api/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    data = request.json
    usuario.nome = data.get('nome', usuario.nome)
    usuario.matricula = data.get('matricula', usuario.matricula)
    usuario.perfil = data.get('perfil', usuario.perfil)
    if data.get('senha'):
        usuario.senha = generate_password_hash(data['senha'])
    db.session.commit()
    return jsonify(usuario.to_dict())


@app.route('/api/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'success': True})


# =============================================================================
# PRODUTOS
# =============================================================================

@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([p.to_dict() for p in produtos])


@app.route('/api/produtos', methods=['POST'])
def criar_produto():
    data = request.json
    produto = Produto(
        codigo=data['codigo'],
        nome=data['nome'],
        descricao=data.get('descricao', ''),
        quantidade=data.get('quantidade', 0),
        preco=data.get('preco', 0.0)
    )
    db.session.add(produto)
    db.session.commit()
    return jsonify(produto.to_dict()), 201


@app.route('/api/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)
    data = request.json
    produto.nome = data.get('nome', produto.nome)
    produto.descricao = data.get('descricao', produto.descricao)
    produto.quantidade = data.get('quantidade', produto.quantidade)
    produto.preco = data.get('preco', produto.preco)
    db.session.commit()
    return jsonify(produto.to_dict())


@app.route('/api/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'success': True})


# =============================================================================
# ORDENS DE PRODUÇÃO
# =============================================================================

@app.route('/api/ordens', methods=['GET'])
def listar_ordens():
    ordens = OrdemProducao.query.order_by(OrdemProducao.data_emissao.desc()).all()
    return jsonify([o.to_dict() for o in ordens])


@app.route('/api/ordens', methods=['POST'])
def criar_ordem():
    data = request.json
    ordem = OrdemProducao(
        numero=data['numero'],
        produto_id=data['produto_id'],
        quantidade=data['quantidade'],
        status=data.get('status', 'aberta'),
        prioridade=data.get('prioridade', 'normal'),
        observacoes=data.get('observacoes', ''),
        data_entrega=datetime.fromisoformat(data['data_entrega']) if data.get('data_entrega') else None
    )
    db.session.add(ordem)
    db.session.commit()
    return jsonify(ordem.to_dict()), 201


@app.route('/api/ordens/<int:id>', methods=['PUT'])
def atualizar_ordem(id):
    ordem = OrdemProducao.query.get_or_404(id)
    data = request.json
    ordem.status = data.get('status', ordem.status)
    ordem.prioridade = data.get('prioridade', ordem.prioridade)
    ordem.quantidade = data.get('quantidade', ordem.quantidade)
    ordem.observacoes = data.get('observacoes', ordem.observacoes)
    if data.get('data_entrega'):
        ordem.data_entrega = datetime.fromisoformat(data['data_entrega'])
    db.session.commit()
    return jsonify(ordem.to_dict())


@app.route('/api/ordens/<int:id>', methods=['DELETE'])
def deletar_ordem(id):
    ordem = OrdemProducao.query.get_or_404(id)
    db.session.delete(ordem)
    db.session.commit()
    return jsonify({'success': True})


# =============================================================================
# TAREFAS KANBAN
# =============================================================================

@app.route('/api/tarefas', methods=['GET'])
def listar_tarefas():
    tarefas = TarefaKanban.query.all()
    return jsonify([t.to_dict() for t in tarefas])


@app.route('/api/tarefas', methods=['POST'])
def criar_tarefa():
    data = request.json
    tarefa = TarefaKanban(
        titulo=data['titulo'],
        descricao=data.get('descricao', ''),
        status=data.get('status', 'a_fazer'),
        ordem_id=data.get('ordem_id'),
        responsavel=data.get('responsavel', ''),
        prioridade=data.get('prioridade', 'normal')
    )
    db.session.add(tarefa)
    db.session.commit()
    return jsonify(tarefa.to_dict()), 201


@app.route('/api/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    tarefa = TarefaKanban.query.get_or_404(id)
    data = request.json
    tarefa.status = data.get('status', tarefa.status)
    tarefa.titulo = data.get('titulo', tarefa.titulo)
    tarefa.descricao = data.get('descricao', tarefa.descricao)
    tarefa.responsavel = data.get('responsavel', tarefa.responsavel)
    tarefa.prioridade = data.get('prioridade', tarefa.prioridade)
    db.session.commit()
    return jsonify(tarefa.to_dict())


@app.route('/api/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    tarefa = TarefaKanban.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({'success': True})


# =============================================================================
# KPIs (INDICADORES)
# =============================================================================

@app.route('/api/kpis', methods=['GET'])
def listar_kpis():
    kpis = Kpi.query.all()
    return jsonify([k.to_dict() for k in kpis])


@app.route('/api/kpis', methods=['POST'])
def criar_kpi():
    data = request.json
    kpi = Kpi(
        nome=data['nome'],
        valor=data.get('valor', 0.0),
        meta=data.get('meta', 0.0),
        unidade=data.get('unidade', '%'),
        periodo=data.get('periodo', 'mensal')
    )
    db.session.add(kpi)
    db.session.commit()
    return jsonify(kpi.to_dict()), 201


@app.route('/api/kpis/<int:id>', methods=['PUT'])
def atualizar_kpi(id):
    kpi = Kpi.query.get_or_404(id)
    data = request.json
    kpi.valor = data.get('valor', kpi.valor)
    kpi.meta = data.get('meta', kpi.meta)
    db.session.commit()
    return jsonify(kpi.to_dict())


# =============================================================================
# CRONOGRAMAS
# =============================================================================

@app.route('/api/cronogramas', methods=['GET'])
def listar_cronogramas():
    cronogramas = Cronograma.query.all()
    return jsonify([c.to_dict() for c in cronogramas])


@app.route('/api/cronogramas', methods=['POST'])
def criar_cronograma():
    data = request.json
    cronograma = Cronograma(
        titulo=data['titulo'],
        data_inicio=datetime.fromisoformat(data['data_inicio']),
        data_fim=datetime.fromisoformat(data['data_fim']),
        ordem_id=data.get('ordem_id'),
        progresso=data.get('progresso', 0),
        cor=data.get('cor', '#007bff')
    )
    db.session.add(cronograma)
    db.session.commit()
    return jsonify(cronograma.to_dict()), 201


@app.route('/api/cronogramas/<int:id>', methods=['PUT'])
def atualizar_cronograma(id):
    cronograma = Cronograma.query.get_or_404(id)
    data = request.json
    cronograma.progresso = data.get('progresso', cronograma.progresso)
    cronograma.data_inicio = datetime.fromisoformat(data['data_inicio']) if data.get('data_inicio') else cronograma.data_inicio
    cronograma.data_fim = datetime.fromisoformat(data['data_fim']) if data.get('data_fim') else cronograma.data_fim
    db.session.commit()
    return jsonify(cronograma.to_dict())


@app.route('/api/cronogramas/<int:id>', methods=['DELETE'])
def deletar_cronograma(id):
    cronograma = Cronograma.query.get_or_404(id)
    db.session.delete(cronograma)
    db.session.commit()
    return jsonify({'success': True})


# =============================================================================
# DASHBOARD
# =============================================================================

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    total_produtos = Produto.query.count()
    total_ordens = OrdemProducao.query.count()
    ordens_abertas = OrdemProducao.query.filter_by(status='aberta').count()
    ordens_finalizadas = OrdemProducao.query.filter_by(status='finalizada').count()
    ordens_produzindo = OrdemProducao.query.filter_by(status='produzindo').count()
    
    return jsonify({
        'total_produtos': total_produtos,
        'total_ordens': total_ordens,
        'ordens_abertas': ordens_abertas,
        'ordens_finalizadas': ordens_finalizadas,
        'ordens_produzindo': ordens_produzindo
    })


# =============================================================================
# EXECUÇÃO
# =============================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)