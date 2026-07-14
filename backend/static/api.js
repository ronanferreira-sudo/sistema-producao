// =============================================================================
// SinaPCP - API Client (Funções para comunicação com o backend Flask)
// =============================================================================

const API_BASE = 'http://localhost:5000';

// =============================================================================
// AUTENTICAÇÃO
// =============================================================================

async function login(matricula, senha) {
    const response = await fetch(`${API_BASE}/api/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ matricula, senha })
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.erro || 'Credenciais inválidas.');
    }
    return await response.json();
}

async function criarUsuario(dados) {
    const response = await fetch(`${API_BASE}/api/cadastro`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.erro || 'Erro ao criar conta.');
    }
    return await response.json();
}

// =============================================================================
// DASHBOARD
// =============================================================================

async function carregarDashboard() {
    const response = await fetch(`${API_BASE}/api/dashboard`);
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.erro || 'Erro ao carregar dashboard.');
    }
    return await response.json();
}

// =============================================================================
// PRODUTOS
// =============================================================================

async function listarProdutos() {
    const response = await fetch(`${API_BASE}/api/produtos`);
    if (!response.ok) throw new Error('Erro ao listar produtos.');
    return await response.json();
}

async function criarProduto(dados) {
    const response = await fetch(`${API_BASE}/api/produtos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.erro || 'Erro ao criar produto.');
    }
    return await response.json();
}

async function atualizarProduto(id, dados) {
    const response = await fetch(`${API_BASE}/api/produtos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.erro || 'Erro ao atualizar produto.');
    }
    return await response.json();
}

async function deletarProduto(id) {
    const response = await fetch(`${API_BASE}/api/produtos/${id}`, {
        method: 'DELETE'
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.erro || 'Erro ao excluir produto.');
    }
    return await response.json();
}

// =============================================================================
// ORDENS DE PRODUÇÃO
// =============================================================================

async function listarOrdens() {
    const response = await fetch(`${API_BASE}/api/ordens`);
    if (!response.ok) throw new Error('Erro ao listar ordens.');
    return await response.json();
}

async function criarOrdem(dados) {
    const response = await fetch(`${API_BASE}/api/ordens`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.erro || 'Erro ao criar ordem.');
    }
    return await response.json();
}

async function atualizarOrdem(id, dados) {
    const response = await fetch(`${API_BASE}/api/ordens/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.erro || 'Erro ao atualizar ordem.');
    }
    return await response.json();
}

async function deletarOrdem(id) {
    const response = await fetch(`${API_BASE}/api/ordens/${id}`, {
        method: 'DELETE'
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.erro || 'Erro ao excluir ordem.');
    }
    return await response.json();
}

// =============================================================================
// TAREFAS KANBAN
// =============================================================================

async function listarTarefas() {
    const response = await fetch(`${API_BASE}/api/tarefas`);
    if (!response.ok) throw new Error('Erro ao listar tarefas.');
    return await response.json();
}

async function criarTarefa(dados) {
    const response = await fetch(`${API_BASE}/api/tarefas`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.erro || 'Erro ao criar tarefa.');
    }
    return await response.json();
}

async function atualizarTarefa(id, dados) {
    const response = await fetch(`${API_BASE}/api/tarefas/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.erro || 'Erro ao atualizar tarefa.');
    }
    return await response.json();
}

async function deletarTarefa(id) {
    const response = await fetch(`${API_BASE}/api/tarefas/${id}`, {
        method: 'DELETE'
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.erro || 'Erro ao excluir tarefa.');
    }
    return await response.json();
}

// =============================================================================
// KPIs
// =============================================================================

async function listarKpis() {
    const response = await fetch(`${API_BASE}/api/kpis`);
    if (!response.ok) throw new Error('Erro ao listar KPIs.');
    return await response.json();
}

// =============================================================================
// CRONOGRAMAS
// =============================================================================

async function listarCronogramas() {
    const response = await fetch(`${API_BASE}/api/cronogramas`);
    if (!response.ok) throw new Error('Erro ao listar cronogramas.');
    return await response.json();
}