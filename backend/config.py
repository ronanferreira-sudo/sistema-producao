# =============================================================================
# SinaPCP - Configuração do Sistema
# =============================================================================

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (se existir)
load_dotenv()


class Config:
    """Configurações principais da aplicação."""
    
    # === Banco de Dados ===
    # Por padrão usa SQLite (para facilitar desenvolvimento local)
    # Para usar PostgreSQL, defina a variável de ambiente DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///grandprix.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # === Segurança ===
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sua-chave-secreta-aqui')