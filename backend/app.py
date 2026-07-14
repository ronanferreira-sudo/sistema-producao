# =============================================================================
# SinaPCP - Aplicação Principal (Server-Side Rendering)
# =============================================================================
# Sistema 100% Python, sem JavaScript
# =============================================================================

# === Dependências Externas ===
import os
from datetime import datetime, timedelta
from flask import Flask, request, redirect, url_for, render_template_string, session, flash, send_from_directory, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# === Dependências Internas ===
from .config import Config
from .models import db, Usuario, Produto, OrdemProducao, TarefaKanban, Kpi, Cronograma

# === Inicialização da Aplicação ===
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
db.init_app(app)
CORS(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


# =============================================================================
# HELPER - CARREGAR TEMPLATES
# =============================================================================

def carregar_template(nome):
    """Carrega um template HTML da pasta templates e retorna como string."""
    caminho = os.path.join(TEMPLATE_DIR, nome)
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()


def renderizar(nome_template, **kwargs):
    """Renderiza um template com dados."""
    template_str = carregar_template(nome_template)
    # Injeta variáveis padrão
    kwargs.setdefault('perfil', session.get('perfil', ''))
    kwargs.setdefault('usuario_nome', session.get('usuario_nome', ''))
    kwargs.setdefault('menu_crono', session.get('perfil') != 'aluno')
    kwargs.setdefault('menu_relatorios', session.get('perfil') != 'aluno')
    kwargs.setdefault('menu_kpis', session.get('perfil') != 'aluno')
    return render_template_string(template_str, **kwargs)


def login_required(rota):
    """Decorator para verificar se o usuário está logado."""
    from functools import wraps
    @wraps(rota)
    def rota_protegida(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login_page'))
        return rota(*args, **kwargs)
    return rota_protegida


# =============================================================================
# ROTAS PÚBLICAS (SSR - Server-Side Rendering)
# =============================================================================

@app.route('/')
def login_page():
    return renderizar('login.html')


@app.route('/login', methods=['POST'])
def login():
    matricula = request.form.get('matricula', '')
    senha = request.form.get('senha', '')
    perfil_form = request.form.get('perfil', '')

    usuario = Usuario.query.filter_by(matricula=matricula).first()
    if usuario and check_password_hash(usuario.senha, senha):
        if usuario.perfil != perfil_form:
            return renderizar('login.html', erro='Perfil selecionado não corresponde ao perfil do usuário.')
        
        session['usuario_id'] = usuario.id
        session['usuario_nome'] = usuario.nome
        session['perfil'] = usuario.perfil
        return redirect(url_for('dashboard'))
    
    return renderizar('login.html', erro='Credenciais inválidas.')


@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form.get('nome', '').strip()
    matricula = request.form.get('matricula', '').strip()
    senha = request.form.get('senha', '')
    confirma_senha = request.form.get('confirma_senha', '')
    perfil = request.form.get('perfil', 'aluno')

    if not nome or not matricula or not senha or not confirma_senha:
        return renderizar('login.html', erro_cadastro='Preencha todos os campos.')
    if senha != confirma_senha:
        return renderizar('login.html', erro_cadastro='As senhas não conferem.')
    if len(senha) < 4:
        return renderizar('login.html', erro_cadastro='A senha deve ter pelo menos 4 caracteres.')

    if Usuario.query.filter_by(matricula=matricula).first():
        return renderizar('login.html', erro_cadastro='Matrícula já cadastrada.')

    usuario = Usuario(matricula=matricula, nome=nome, senha=generate_password_hash(senha), perfil=perfil)
    db.session.add(usuario)
    db.session.commit()
    return renderizar('login.html', sucesso='Conta criada com sucesso! Faça o login.')


# =============================================================================
# ROTAS DE API (JSON - para frontend estático)
# =============================================================================

@app.route('/api/login', methods=['POST'])
def api_login():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados inválidos.'}), 400
    
    matricula = dados.get('matricula', '')
    senha = dados.get('senha', '')

    usuario = Usuario.query.filter_by(matricula=matricula).first()
    if usuario and check_password_hash(usuario.senha, senha):
        return jsonify({
            'usuario': {
                'id': usuario.id,
                'nome': usuario.nome,
                'matricula': usuario.matricula,
                'perfil': usuario.perfil
            }
        })
    
    return jsonify({'erro': 'Credenciais inválidas.'}), 401


@app.route('/api/cadastro', methods=['POST'])
def api_cadastro():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados inválidos.'}), 400

    nome = dados.get('nome', '').strip()
    matricula = dados.get('matricula', '').strip()
    senha = dados.get('senha', '')
    perfil = dados.get('perfil', 'aluno')

    if not nome or not matricula or not senha:
        return jsonify({'erro': 'Preencha todos os campos.'}), 400
    if len(senha) < 4:
        return jsonify({'erro': 'A senha deve ter pelo menos 4 caracteres.'}), 400

    if Usuario.query.filter_by(matricula=matricula).first():
        return jsonify({'erro': 'Matrícula já cadastrada.'}), 400

    usuario = Usuario(matricula=matricula, nome=nome, senha=generate_password_hash(senha), perfil=perfil)
    db.session.add(usuario)
    db.session.commit()
    return jsonify({
        'mensagem': 'Conta criada com sucesso!',
        'usuario': {
            'id': usuario.id,
            'nome': usuario.nome,
            'matricula': usuario.matricula,
            'perfil': usuario.perfil
        }
    }), 201


@app.route('/api/dashboard')
def api_dashboard():
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
# API - PRODUTOS
# =============================================================================

@app.route('/api/produtos', methods=['GET'])
def api_listar_produtos():
    produtos = Produto.query.all()
    return jsonify([p.to_dict() for p in produtos])


@app.route('/api/produtos', methods=['POST'])
def api_criar_produto():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados inválidos.'}), 400
    codigo = dados.get('codigo', '').strip()
    nome = dados.get('nome', '').strip()
    if not codigo or not nome:
        return jsonify({'erro': 'Código e nome são obrigatórios.'}), 400
    if Produto.query.filter_by(codigo=codigo).first():
        return jsonify({'erro': 'Código já cadastrado.'}), 400
    produto = Produto(
        codigo=codigo,
        nome=nome,
        descricao=dados.get('descricao', ''),
        quantidade=int(dados.get('quantidade', 0)),
        preco=float(dados.get('preco', 0))
    )
    db.session.add(produto)
    db.session.commit()
    return jsonify(produto.to_dict()), 201


@app.route('/api/produtos/<int:id>', methods=['PUT'])
def api_atualizar_produto(id):
    produto = Produto.query.get_or_404(id)
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados inválidos.'}), 400
    produto.nome = dados.get('nome', produto.nome)
    produto.descricao = dados.get('descricao', produto.descricao)
    produto.quantidade = int(dados.get('quantidade', produto.quantidade))
    produto.preco = float(dados.get('preco', produto.preco))
    db.session.commit()
    return jsonify(produto.to_dict())


@app.route('/api/produtos/<int:id>', methods=['DELETE'])
def api_deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'mensagem': 'Produto excluído com sucesso.'})


# =============================================================================
# API - ORDENS DE PRODUÇÃO
# =============================================================================

@app.route('/api/ordens', methods=['GET'])
def api_listar_ordens():
    ordens = OrdemProducao.query.order_by(OrdemProducao.data_emissao.desc()).all()
    return jsonify([o.to_dict() for o in ordens])


@app.route('/api/ordens', methods=['POST'])
def api_criar_ordem():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados inválidos.'}), 400
    numero = dados.get('numero', '').strip()
    produto_id = int(dados.get('produto_id', 0))
    quantidade = int(dados.get('quantidade', 0))
    if not numero or not produto_id:
        return jsonify({'erro': 'Número da OP e produto são obrigatórios.'}), 400
    data_entrega = None
    if dados.get('data_entrega'):
        from datetime import datetime
        data_entrega = datetime.fromisoformat(dados['data_entrega'].replace('Z', '+00:00'))
    ordem = OrdemProducao(
        numero=numero,
        produto_id=produto_id,
        quantidade=quantidade,
        prioridade=dados.get('prioridade', 'normal'),
        data_entrega=data_entrega,
        observacoes=dados.get('observacoes', '')
    )
    db.session.add(ordem)
    db.session.commit()
    return jsonify(ordem.to_dict()), 201


@app.route('/api/ordens/<int:id>', methods=['PUT'])
def api_atualizar_ordem(id):
    ordem = OrdemProducao.query.get_or_404(id)
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados inválidos.'}), 400
    ordem.quantidade = int(dados.get('quantidade', ordem.quantidade))
    ordem.prioridade = dados.get('prioridade', ordem.prioridade)
    ordem.observacoes = dados.get('observacoes', ordem.observacoes)
    db.session.commit()
    return jsonify(ordem.to_dict())


@app.route('/api/ordens/<int:id>', methods=['DELETE'])
def api_deletar_ordem(id):
    ordem = OrdemProducao.query.get_or_404(id)
    db.session.delete(ordem)
    db.session.commit()
    return jsonify({'mensagem': 'Ordem excluída com sucesso.'})


# =============================================================================
# API - TAREFAS KANBAN
# =============================================================================

@app.route('/api/tarefas', methods=['GET'])
def api_listar_tarefas():
    tarefas = TarefaKanban.query.all()
    return jsonify([t.to_dict() for t in tarefas])


@app.route('/api/tarefas', methods=['POST'])
def api_criar_tarefa():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados inválidos.'}), 400
    titulo = dados.get('titulo', '').strip()
    if not titulo:
        return jsonify({'erro': 'Título é obrigatório.'}), 400
    ordem_id = dados.get('ordem_id')
    if ordem_id:
        ordem_id = int(ordem_id) if ordem_id else None
    tarefa = TarefaKanban(
        titulo=titulo,
        descricao=dados.get('descricao', ''),
        status=dados.get('status', 'a_fazer'),
        responsavel=dados.get('responsavel', ''),
        prioridade=dados.get('prioridade', 'normal'),
        ordem_id=ordem_id
    )
    db.session.add(tarefa)
    db.session.commit()
    return jsonify(tarefa.to_dict()), 201


@app.route('/api/tarefas/<int:id>', methods=['PUT'])
def api_atualizar_tarefa(id):
    tarefa = TarefaKanban.query.get_or_404(id)
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados inválidos.'}), 400
    if 'status' in dados and dados['status'] in ('a_fazer', 'fazendo', 'concluido'):
        tarefa.status = dados['status']
    db.session.commit()
    return jsonify(tarefa.to_dict())


@app.route('/api/tarefas/<int:id>', methods=['DELETE'])
def api_deletar_tarefa(id):
    tarefa = TarefaKanban.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({'mensagem': 'Tarefa excluída com sucesso.'})


# =============================================================================
# API - KPIs
# =============================================================================

@app.route('/api/kpis')
def api_listar_kpis():
    kpis = Kpi.query.all()
    return jsonify([k.to_dict() for k in kpis])


# =============================================================================
# API - CRONOGRAMAS
# =============================================================================

@app.route('/api/cronogramas')
def api_listar_cronogramas():
    cronogramas = Cronograma.query.all()
    return jsonify([c.to_dict() for c in cronogramas])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


# =============================================================================
# ROTAS ESTÁTICAS (CSS)
# =============================================================================

@app.route('/style.css')
def servir_css():
    return send_from_directory(BASE_DIR, 'style.css')


# =============================================================================
# DASHBOARD
# =============================================================================

# =============================================================================
# PMP (PLANO MESTRE DE PRODUÇÃO)
# =============================================================================

@app.route('/pmp', methods=['GET', 'POST'])
@login_required
def pmp():
    dados = {}
    if request.method == 'POST':
        demanda = float(request.form.get('demanda', 0))
        dias = float(request.form.get('dias', 0))
        horas = float(request.form.get('horas', 0))
        tempo_total = int(dias * horas)
        takt_time = round((tempo_total * 60) / demanda, 2) if demanda > 0 else 0
        meta_diaria = int(demanda / dias) if dias > 0 else 0
        dados = {'tempo_total': tempo_total, 'takt_time': takt_time, 'meta_diaria': meta_diaria, 'demanda': demanda, 'dias': dias, 'horas': horas}
    return renderizar('pmp.html', active='pmp', **dados)


# =============================================================================
# DASHBOARD
# =============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    total_produtos = Produto.query.count()
    total_ordens = OrdemProducao.query.count()
    ordens_abertas = OrdemProducao.query.filter_by(status='aberta').count()
    ordens_finalizadas = OrdemProducao.query.filter_by(status='finalizada').count()
    ordens_produzindo = OrdemProducao.query.filter_by(status='produzindo').count()

    return renderizar('dashboard.html', active='dashboard',
        total_produtos=total_produtos,
        total_ordens=total_ordens,
        ordens_abertas=ordens_abertas,
        ordens_finalizadas=ordens_finalizadas,
        ordens_produzindo=ordens_produzindo)


# =============================================================================
# PRODUTOS
# =============================================================================

@app.route('/produtos')
@login_required
def produtos():
    produtos_lista = Produto.query.all()
    return renderizar('produtos.html', active='produtos', produtos=produtos_lista)


@app.route('/produtos/<int:id>/editar')
@login_required
def produto_editar(id):
    produto_edit = Produto.query.get_or_404(id)
    produtos_lista = Produto.query.all()
    return renderizar('produtos.html', active='produtos', produtos=produtos_lista, produto_edit=produto_edit)


@app.route('/produtos/salvar', methods=['POST'])
@login_required
def produto_salvar():
    produto_id = request.form.get('produto_id', '')
    codigo = request.form.get('codigo', '')
    nome = request.form.get('nome', '')
    descricao = request.form.get('descricao', '')
    quantidade = int(request.form.get('quantidade', 0))
    preco = float(request.form.get('preco', 0.0))

    if produto_id:  # Atualizar
        produto = Produto.query.get_or_404(int(produto_id))
        produto.nome = nome
        produto.descricao = descricao
        produto.quantidade = quantidade
        produto.preco = preco
    else:  # Criar
        produto = Produto(codigo=codigo, nome=nome, descricao=descricao, quantidade=quantidade, preco=preco)
        db.session.add(produto)
    
    db.session.commit()
    return redirect(url_for('produtos'))


@app.route('/produtos/<int:id>/excluir')
@login_required
def produto_excluir(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('produtos'))


# =============================================================================
# ORDENS DE PRODUÇÃO
# =============================================================================

@app.route('/ordens')
@login_required
def ordens():
    ordens_lista = OrdemProducao.query.order_by(OrdemProducao.data_emissao.desc()).all()
    produtos_lista = Produto.query.all()
    return renderizar('ordens.html', active='ordens', ordens=ordens_lista, produtos=produtos_lista)


@app.route('/ordens/<int:id>/editar')
@login_required
def ordem_editar(id):
    ordem_edit = OrdemProducao.query.get_or_404(id)
    ordens_lista = OrdemProducao.query.order_by(OrdemProducao.data_emissao.desc()).all()
    produtos_lista = Produto.query.all()
    return renderizar('ordens.html', active='ordens', ordens=ordens_lista, produtos=produtos_lista, ordem_edit=ordem_edit)


@app.route('/ordens/salvar', methods=['POST'])
@login_required
def ordem_salvar():
    ordem_id = request.form.get('ordem_id', '')
    numero = request.form.get('numero', '')
    produto_id = int(request.form.get('produto_id', 0))
    quantidade = int(request.form.get('quantidade', 0))
    prioridade = request.form.get('prioridade', 'normal')
    data_entrega_str = request.form.get('data_entrega', '')
    observacoes = request.form.get('observacoes', '')

    data_entrega = None
    if data_entrega_str:
        data_entrega = datetime.strptime(data_entrega_str, '%Y-%m-%d')

    if ordem_id:  # Atualizar
        ordem = OrdemProducao.query.get_or_404(int(ordem_id))
        ordem.quantidade = quantidade
        ordem.prioridade = prioridade
        ordem.data_entrega = data_entrega
        ordem.observacoes = observacoes
    else:  # Criar
        ordem = OrdemProducao(
            numero=numero, produto_id=produto_id, quantidade=quantidade,
            prioridade=prioridade, data_entrega=data_entrega, observacoes=observacoes)
        db.session.add(ordem)
    
    db.session.commit()
    return redirect(url_for('ordens'))


@app.route('/ordens/<int:id>/excluir')
@login_required
def ordem_excluir(id):
    ordem = OrdemProducao.query.get_or_404(id)
    db.session.delete(ordem)
    db.session.commit()
    return redirect(url_for('ordens'))


# =============================================================================
# KANBAN
# =============================================================================

@app.route('/kanban')
@login_required
def kanban():
    tarefas = TarefaKanban.query.all()
    ordens_lista = OrdemProducao.query.all()
    return renderizar('kanban.html', active='kanban', tarefas=tarefas, ordens=ordens_lista, mostrar_form=False)


@app.route('/kanban/novo')
@login_required
def kanban_novo():
    tarefas = TarefaKanban.query.all()
    ordens_lista = OrdemProducao.query.all()
    return renderizar('kanban.html', active='kanban', tarefas=tarefas, ordens=ordens_lista, mostrar_form=True)


@app.route('/kanban/salvar', methods=['POST'])
@login_required
def kanban_salvar():
    titulo = request.form.get('titulo', '')
    descricao = request.form.get('descricao', '')
    status = request.form.get('status', 'a_fazer')
    responsavel = request.form.get('responsavel', '')
    prioridade = request.form.get('prioridade', 'normal')
    ordem_id_str = request.form.get('ordem_id', '')
    ordem_id = int(ordem_id_str) if ordem_id_str else None

    tarefa = TarefaKanban(titulo=titulo, descricao=descricao, status=status,
                          responsavel=responsavel, prioridade=prioridade, ordem_id=ordem_id)
    db.session.add(tarefa)
    db.session.commit()
    return redirect(url_for('kanban'))


@app.route('/kanban/<int:id>/mover/<status>')
@login_required
def kanban_mover(id, status):
    tarefa = TarefaKanban.query.get_or_404(id)
    if status in ('a_fazer', 'fazendo', 'concluido'):
        tarefa.status = status
        db.session.commit()
    return redirect(url_for('kanban'))


@app.route('/kanban/<int:id>/excluir')
@login_required
def kanban_excluir(id):
    tarefa = TarefaKanban.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for('kanban'))


# =============================================================================
# ESTOQUE
# =============================================================================

@app.route('/estoque', methods=['GET', 'POST'])
@login_required
def estoque():
    produtos_lista = Produto.query.all()
    previsao_resultado = None
    m1 = m2 = m3 = None
    if request.method == 'POST':
        m1 = float(request.form.get('m1', 0))
        m2 = float(request.form.get('m2', 0))
        m3 = float(request.form.get('m3', 0))
        previsao_resultado = round((m1 + m2 + m3) / 3)
    return renderizar('estoque.html', active='estoque', produtos=produtos_lista,
                      previsao_resultado=previsao_resultado, m1=m1, m2=m2, m3=m3)


# =============================================================================
# KPIs
# =============================================================================

@app.route('/kpis')
@login_required
def kpis():
    kpis_lista = Kpi.query.all()
    return renderizar('kpis.html', active='kpis', kpis_lista=kpis_lista)


# =============================================================================
# CRONOANÁLISE
# =============================================================================

@app.route('/cronoanalise')
@login_required
def cronoanalise():
    cronogramas_lista = Cronograma.query.all()
    return renderizar('cronoanalise.html', active='cronoanalise', cronogramas=cronogramas_lista)


# =============================================================================
# RELATÓRIOS
# =============================================================================

@app.route('/relatorios')
@login_required
def relatorios():
    ordens_lista = OrdemProducao.query.order_by(OrdemProducao.data_emissao.desc()).all()
    return renderizar('relatorios.html', active='relatorios', ordens=ordens_lista)


# =============================================================================
# ERRO 404
# =============================================================================

@app.errorhandler(404)
def not_found(e):
    return redirect(url_for('login_page'))


# =============================================================================
# EXECUÇÃO
# =============================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Para acessar de outras máquinas na rede, use host='0.0.0.0'
    # Altere debug=False em produção
    app.run(debug=True, host='0.0.0.0', port=5000)
