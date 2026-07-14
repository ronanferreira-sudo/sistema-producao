const API_URL = 'http://localhost:5000/api';

async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_URL}${endpoint}`, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.mensagem || 'Erro na requisição');
        }

        return result;
    } catch (error) {
        console.error(`Erro na requisição ${endpoint}:`, error);
        throw error;
    }
}

// ==================== AUTENTICAÇÃO ====================
async function login(matricula, senha) {
    return apiRequest('/login', 'POST', { matricula, senha });
}

// ==================== USUÁRIOS ====================
async function listarUsuarios() {
    return apiRequest('/usuarios');
}

async function criarUsuario(usuario) {
    return apiRequest('/usuarios', 'POST', usuario);
}

async function atualizarUsuario(id, usuario) {
    return apiRequest(`/usuarios/${id}`, 'PUT', usuario);
}

async function deletarUsuario(id) {
    return apiRequest(`/usuarios/${id}`, 'DELETE');
}

// ==================== PRODUTOS ====================
async function listarProdutos() {
    return apiRequest('/produtos');
}

async function criarProduto(produto) {
    return apiRequest('/produtos', 'POST', produto);
}

async function atualizarProduto(id, produto) {
    return apiRequest(`/produtos/${id}`, 'PUT', produto);
}

async function deletarProduto(id) {
    return apiRequest(`/produtos/${id}`, 'DELETE');
}

// ==================== ORDENS DE PRODUÇÃO ====================
async function listarOrdens() {
    return apiRequest('/ordens');
}

async function criarOrdem(ordem) {
    return apiRequest('/ordens', 'POST', ordem);
}

async function atualizarOrdem(id, ordem) {
    return apiRequest(`/ordens/${id}`, 'PUT', ordem);
}

async function deletarOrdem(id) {
    return apiRequest(`/ordens/${id}`, 'DELETE');
}

// ==================== TAREFAS KANBAN ====================
async function listarTarefas() {
    return apiRequest('/tarefas');
}

async function criarTarefa(tarefa) {
    return apiRequest('/tarefas', 'POST', tarefa);
}

async function atualizarTarefa(id, tarefa) {
    return apiRequest(`/tarefas/${id}`, 'PUT', tarefa);
}

async function deletarTarefa(id) {
    return apiRequest(`/tarefas/${id}`, 'DELETE');
}

// ==================== KPIs ====================
async function listarKpis() {
    return apiRequest('/kpis');
}

async function criarKpi(kpi) {
    return apiRequest('/kpis', 'POST', kpi);
}

async function atualizarKpi(id, kpi) {
    return apiRequest(`/kpis/${id}`, 'PUT', kpi);
}

// ==================== CRONOGRAMAS ====================
async function listarCronogramas() {
    return apiRequest('/cronogramas');
}

async function criarCronograma(cronograma) {
    return apiRequest('/cronogramas', 'POST', cronograma);
}

async function atualizarCronograma(id, cronograma) {
    return apiRequest(`/cronogramas/${id}`, 'PUT', cronograma);
}

async function deletarCronograma(id) {
    return apiRequest(`/cronogramas/${id}`, 'DELETE');
}

// ==================== DASHBOARD ====================
async function carregarDashboard() {
    return apiRequest('/dashboard');
}