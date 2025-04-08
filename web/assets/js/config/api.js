/**
 * Módulo de configuração e comunicação com a API
 */
export const API = {
    /**
     * Determina a URL base da API com base no ambiente
     * @returns {string} URL base da API
     */
    getBaseUrl() {
        return (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
            ? 'http://localhost:8000/api/v1'
            : 'https://api-calculo-rendimento.onrender.com/api/v1';
    },
    
    /**
     * Endpoints da API
     */
    endpoints: {},
    
    /**
     * Inicializa os endpoints da API
     */
    init() {
        const baseUrl = this.getBaseUrl();
        this.endpoints = {
            calcularRendimento: `${baseUrl}/calcular_rendimento`,
            calcularResgate: `${baseUrl}/calcular_resgate`,
            cdiAtual: `${baseUrl}/cdi_atual`
        };
    },
    
    /**
     * Realiza chamada à API
     * @param {string} endpoint - Endpoint da API a ser chamado
     * @param {Object} options - Opções da requisição fetch
     * @returns {Promise<Object>} - Resposta da API em JSON
     * @throws {Error} - Erro da requisição
     */
    async fetch(endpoint, options = {}) {
        try {
            const response = await fetch(endpoint, options);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `Erro ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error(`Erro na chamada à API (${endpoint}):`, error);
            throw error;
        }
    }
}; 