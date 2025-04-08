/**
 * Calculadora de Rendimentos Financeiros
 * Aplicação principal que inicializa os módulos
 * @author Empresa
 * @version 1.0.0
 */
import { API } from './config/api.js';
import { UI } from './modules/ui.js';
import { Calculadora } from './modules/calculadora.js';

// Namespace principal da aplicação
const CalculadoraRendimentos = (() => {
    'use strict';

    // Função de inicialização da aplicação
    const init = () => {
        // Inicializa todos os módulos
        API.init();
        UI.init();
        UI.setupEventListeners();
        
        // Busca taxa CDI ao carregar a página
        Calculadora.buscarTaxaCDI();
    };

    // Interface pública do módulo
    return {
        init
    };
})();

// Inicializa a aplicação quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    CalculadoraRendimentos.init();
}); 