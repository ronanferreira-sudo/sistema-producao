# =============================================================================
# SinaPCP - Inicialização do Banco de Dados
# =============================================================================
# Script para criar as tabelas e popular com dados de exemplo.
# Uso: python backend/init_db.py
# =============================================================================

# === Dependências Externas ===
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# === Dependências Internas ===
from app import app, db
from models import Usuario, Produto, OrdemProducao, TarefaKanban, Kpi, Cronograma

def init_database():
    with app.app_context():
        # Cria todas as tabelas
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")

        # Verifica se já existem dados
        if Usuario.query.first():
            print("⚠️  Banco já possui dados. Pulando inserção de exemplo.")
            return

        # ==================== USUÁRIOS ====================
        usuarios = [
            Usuario(matricula='admin', nome='Administrador', senha=generate_password_hash('123'), perfil='instrutor'),
            Usuario(matricula='aluno1', nome='João Silva', senha=generate_password_hash('123'), perfil='aluno'),
            Usuario(matricula='aluno2', nome='Maria Santos', senha=generate_password_hash('123'), perfil='aluno'),
            Usuario(matricula='aluno3', nome='Pedro Oliveira', senha=generate_password_hash('123'), perfil='aluno'),
        ]
        db.session.add_all(usuarios)
        db.session.flush()
        print("✅ Usuários criados!")

        # ==================== PRODUTOS ====================
        produtos = [
            Produto(codigo='P001', nome='Parafuso M8x30', descricao='Parafuso de aço inox M8 com 30mm de comprimento', quantidade=5000, preco=0.50),
            Produto(codigo='P002', nome='Porca M8', descricao='Porca sextavada M8 em aço carbono', quantidade=8000, preco=0.30),
            Produto(codigo='P003', nome='Arruela M8', descricao='Arruela lisa M8 em aço zincado', quantidade=10000, preco=0.15),
            Produto(codigo='P004', nome='Eixo Motor 20mm', descricao='Eixo de motor elétrico 20mm x 500mm', quantidade=200, preco=45.00),
            Produto(codigo='P005', nome='Mola Compressão 50mm', descricao='Mola helicoidal de compressão 50mm', quantidade=1000, preco=2.50),
        ]
        db.session.add_all(produtos)
        db.session.flush()
        print("✅ Produtos criados!")

        # ==================== ORDENS DE PRODUÇÃO ====================
        ordens = [
            OrdemProducao(numero='OP-2024-001', produto_id=1, quantidade=1000, status='finalizada', prioridade='alta', 
                         data_entrega=datetime.now() - timedelta(days=5)),
            OrdemProducao(numero='OP-2024-002', produto_id=2, quantidade=2000, status='produzindo', prioridade='normal',
                         data_entrega=datetime.now() + timedelta(days=3)),
            OrdemProducao(numero='OP-2024-003', produto_id=3, quantidade=5000, status='aberta', prioridade='baixa',
                         data_entrega=datetime.now() + timedelta(days=15)),
            OrdemProducao(numero='OP-2024-004', produto_id=4, quantidade=100, status='aberta', prioridade='urgente',
                         data_entrega=datetime.now() + timedelta(days=1)),
            OrdemProducao(numero='OP-2024-005', produto_id=5, quantidade=500, status='produzindo', prioridade='alta',
                         data_entrega=datetime.now() + timedelta(days=7)),
        ]
        db.session.add_all(ordens)
        db.session.flush()
        print("✅ Ordens de produção criadas!")

        # ==================== TAREFAS KANBAN ====================
        tarefas = [
            TarefaKanban(titulo='Separar matéria-prima OP-002', descricao='Separar aço carbono para produção de porcas', 
                        status='a_fazer', ordem_id=2, responsavel='João Silva', prioridade='normal'),
            TarefaKanban(titulo='Configurar máquina CNC', descricao='Ajustar parâmetros da CNC para eixos 20mm', 
                        status='fazendo', ordem_id=4, responsavel='Maria Santos', prioridade='urgente'),
            TarefaKanban(titulo='Inspecionar lotes OP-001', descricao='Verificar qualidade dos parafusos produzidos', 
                        status='concluido', ordem_id=1, responsavel='Pedro Oliveira', prioridade='alta'),
            TarefaKanban(titulo='Embalar molas OP-005', descricao='Embalar molas em lotes de 100 unidades', 
                        status='a_fazer', ordem_id=5, responsavel='João Silva', prioridade='normal'),
        ]
        db.session.add_all(tarefas)
        print("✅ Tarefas Kanban criadas!")

        # ==================== KPIs ====================
        kpis = [
            Kpi(nome='Produtividade', valor=78.5, meta=85.0, unidade='%', periodo='mensal'),
            Kpi(nome='Qualidade', valor=92.3, meta=95.0, unidade='%', periodo='mensal'),
            Kpi(nome='Entregas no Prazo', valor=65.0, meta=80.0, unidade='%', periodo='mensal'),
            Kpi(nome='Eficiência OEE', valor=72.1, meta=80.0, unidade='%', periodo='mensal'),
            Kpi(nome='Lead Time Médio', valor=4.5, meta=3.0, unidade='dias', periodo='mensal'),
        ]
        db.session.add_all(kpis)
        print("✅ KPIs criados!")

        # ==================== CRONOGRAMAS ====================
        cronogramas = [
            Cronograma(titulo='Produção de Porcas M8', 
                      data_inicio=datetime.now() - timedelta(days=2),
                      data_fim=datetime.now() + timedelta(days=3),
                      ordem_id=2, progresso=40, cor='#28a745'),
            Cronograma(titulo='Produção de Eixos Motor', 
                      data_inicio=datetime.now(),
                      data_fim=datetime.now() + timedelta(days=1),
                      ordem_id=4, progresso=10, cor='#dc3545'),
            Cronograma(titulo='Produção de Molas', 
                      data_inicio=datetime.now() + timedelta(days=1),
                      data_fim=datetime.now() + timedelta(days=7),
                      ordem_id=5, progresso=0, cor='#007bff'),
        ]
        db.session.add_all(cronogramas)
        print("✅ Cronogramas criados!")

        # Commit final
        db.session.commit()
        print("\n🎉 Banco de dados inicializado com sucesso!")
        print("\n📋 Credenciais de acesso:")
        print("   Admin: matrícula='admin', senha='123'")
        print("   Alunos: matrícula='aluno1'..'aluno3', senha='123'")

if __name__ == '__main__':
    init_database()