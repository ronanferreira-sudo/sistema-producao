# =============================================================================
# SinaPCP - Ponto de Entrada do Sistema
# =============================================================================
# Para iniciar o servidor: python app.py
# =============================================================================

# === Importa a aplicação Flask configurada ===
from backend.app import app

# === Executa o servidor ===
if __name__ == '__main__':
    # Para acessar de outras máquinas na rede, use host='0.0.0.0'
    # Altere debug=False em produção
    app.run(debug=True, host='0.0.0.0', port=5000)
