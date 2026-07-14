from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    perfil = db.Column(db.String(20), nullable=False)  # aluno, instrutor
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'matricula': self.matricula,
            'nome': self.nome,
            'perfil': self.perfil
        }

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    quantidade = db.Column(db.Integer, default=0)
    preco = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'descricao': self.descricao,
            'quantidade': self.quantidade,
            'preco': self.preco
        }

class OrdemProducao(db.Model):
    __tablename__ = 'ordens_producao'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_emissao = db.Column(db.DateTime, default=datetime.utcnow)
    data_entrega = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='aberta')  # aberta, produzindo, finalizada, cancelada
    prioridade = db.Column(db.String(20), default='normal')  # baixa, normal, alta, urgente
    observacoes = db.Column(db.Text)
    
    produto = db.relationship('Produto', backref='ordens')

    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'produto_id': self.produto_id,
            'produto_nome': self.produto.nome if self.produto else None,
            'quantidade': self.quantidade,
            'data_emissao': self.data_emissao.isoformat() if self.data_emissao else None,
            'data_entrega': self.data_entrega.isoformat() if self.data_entrega else None,
            'status': self.status,
            'prioridade': self.prioridade,
            'observacoes': self.observacoes
        }

class TarefaKanban(db.Model):
    __tablename__ = 'tarefas_kanban'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    status = db.Column(db.String(20), default='a_fazer')  # a_fazer, fazendo, concluido
    ordem_id = db.Column(db.Integer, db.ForeignKey('ordens_producao.id'))
    responsavel = db.Column(db.String(100))
    prioridade = db.Column(db.String(20), default='normal')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    ordem = db.relationship('OrdemProducao', backref='tarefas')

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'status': self.status,
            'ordem_id': self.ordem_id,
            'responsavel': self.responsavel,
            'prioridade': self.prioridade
        }

class Kpi(db.Model):
    __tablename__ = 'kpis'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, default=0.0)
    meta = db.Column(db.Float, default=0.0)
    unidade = db.Column(db.String(20), default='%')
    periodo = db.Column(db.String(20), default='mensal')
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'valor': self.valor,
            'meta': self.meta,
            'unidade': self.unidade,
            'periodo': self.periodo
        }

class Cronograma(db.Model):
    __tablename__ = 'cronogramas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    ordem_id = db.Column(db.Integer, db.ForeignKey('ordens_producao.id'))
    progresso = db.Column(db.Integer, default=0)
    cor = db.Column(db.String(20), default='#007bff')
    
    ordem = db.relationship('OrdemProducao', backref='cronogramas')

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'ordem_id': self.ordem_id,
            'progresso': self.progresso,
            'cor': self.cor
        }