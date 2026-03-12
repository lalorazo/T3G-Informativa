const API_URL = 'http://localhost:5000/api';

async function apiRequest(endpoint, method = 'GET', data = null, token = null) {
    const headers = {
        'Content-Type': 'application/json',
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const config = {
        method,
        headers,
    };
    
    if (data) {
        config.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_URL}${endpoint}`, config);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Error en la petición');
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Autenticación
async function login(codigo, email, password) {
    return apiRequest('/auth/login', 'POST', { codigo, email, password });
}

async function verifyToken(token) {
    return apiRequest('/auth/verify', 'GET', null, token);
}

// Kits
async function getKits() {
    return apiRequest('/kits/');
}

async function getKitDestacado() {
    return apiRequest('/kits/destacado');
}

// Demo
async function solicitarDemo(data) {
    return apiRequest('/demo/solicitar', 'POST', data);
}