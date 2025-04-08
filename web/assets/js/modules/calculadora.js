/**
 * Módulo de cálculos e operações principais
 */
import { API } from '../config/api.js';
import { UI } from './ui.js';
import { Validador } from './validador.js';

export const Calculadora = {
    // Armazena o resultado atual para uso em exportação e outros
    resultadoAtual: null,
    
    /**
     * Calcula o rendimento usando a API
     */
    async calcularRendimento() {
        if (!Validador.validarFormulario()) return;
        
        try {
            UI.mostrarLoading(true);
            UI.prepararParaRendimento();
            
            const params = Validador.obterParametrosFormulario();
            
            const dados = await API.fetch(API.endpoints.calcularRendimento, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(params)
            });
            
            this.resultadoAtual = dados;
            
            UI.preencherTabelaResultados(dados.informe_mensal, 'rendimento_mensal');
            UI.atualizarResumo(dados, false);
            UI.elements.btnExportar.disabled = false;
            
        } catch (error) {
            UI.mostrarErro(error.message);
        } finally {
            UI.mostrarLoading(false);
        }
    },
    
    /**
     * Calcula os juros de saque usando a API
     */
    async calcularJurosSaque() {
        if (!Validador.validarFormulario()) return;
        
        try {
            UI.mostrarLoading(true);
            UI.prepararParaJurosSaque();
            
            const params = Validador.obterParametrosFormulario();
            params.taxa_juros_saque = 1.0; // Valor padrão
            
            const dados = await API.fetch(API.endpoints.calcularJurosSaque, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(params)
            });
            
            this.resultadoAtual = dados;
            
            UI.preencherTabelaResultados(dados.informe_mensal, 'juros_saque_mensal');
            UI.atualizarResumo(dados, true);
            UI.elements.btnExportar.disabled = false;
            
        } catch (error) {
            UI.mostrarErro(error.message);
        } finally {
            UI.mostrarLoading(false);
        }
    },
    
    /**
     * Busca a taxa CDI atual da API
     */
    async buscarTaxaCDI() {
        try {
            UI.atualizarBotaoCDI(true);
            
            const dados = await API.fetch(API.endpoints.cdiAtual);
            UI.elements.taxaCDI.value = dados.cdi_anual.toFixed(2);
            
        } catch (error) {
            UI.mostrarErro(error.message);
        } finally {
            UI.atualizarBotaoCDI(false);
        }
    }
}; 