/**
 * Funções auxiliares genéricas
 */

/**
 * Função para manipular erros de forma uniforme
 * @param {Error} error - Objeto de erro
 * @param {Function} callback - Função de callback para tratamento específico
 */
export const handleError = (error, callback) => {
    console.error('Erro:', error);
    
    if (typeof callback === 'function') {
        callback(error.message || 'Ocorreu um erro inesperado.');
    }
    
    return {
        success: false,
        message: error.message || 'Ocorreu um erro inesperado.',
        error
    };
};

/**
 * Cria um debounce para evitar múltiplas chamadas de função
 * @param {Function} func - Função a ser executada
 * @param {number} wait - Tempo de espera em ms
 * @returns {Function} - Função com debounce
 */
export const debounce = (func, wait = 300) => {
    let timeout;
    
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}; 