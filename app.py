# =============================================================================
# SinaPCP - Ponto de Entrada do Sistema
# =============================================================================
# Para iniciar o servidor: python app.py
# =============================================================================

# === Importa a aplicação Flask configurada ===
from backend.app import app

# === Executa o servidor ===
if __name__ == '__main__':
    app.run(debug=True, port=5000)
