/**
 * Módulo de validação de dados
 */
import { UI } from './ui.js';

export const Validador = {
    /**
     * Valida o formulário antes do envio
     * @returns {boolean} - Verdadeiro se o formulário for válido
     */
    validarFormulario() {
        if (!UI.elements.form.checkValidity()) {
            // Destacar campos inválidos
            Array.from(UI.elements.form.elements).forEach(campo => {
                if (!campo.checkValidity()) {
                    campo.classList.add('is-invalid');
                } else {
                    campo.classList.remove('is-invalid');
                }
            });
            
            UI.mostrarErro('Preencha todos os campos corretamente');
            return false;
        }
        return true;
    },
    
    /**
     * Obtém os parâmetros do formulário para envio à API
     * @returns {Object} - Objeto com os parâmetros da requisição
     */
    obterParametrosFormulario() {
        return {
            valor_inicial: parseFloat(UI.elements.valorInicial.value),
            aporte_mensal: parseFloat(UI.elements.aporteMensal.value),
            ano_final: parseInt(UI.elements.anoFinal.value),
            mes_final: parseInt(UI.elements.mesFinal.value),
            taxa_cdi_anual: parseFloat(UI.elements.taxaCDI.value),
            percentual_sobre_cdi: parseFloat(UI.elements.percentualCDI.value)
        };
    }
}; 