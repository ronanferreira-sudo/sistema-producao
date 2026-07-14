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
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:123@localhost:5432/grandprix'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # === Segurança ===
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sua-chave-secreta-aqui')
