/**
 * Módulo de interface do usuário
 */
import { Calculadora } from './calculadora.js';
import { Exportador } from './exportador.js';
import { Formatador } from './formatador.js';

export const UI = {
    // Elementos do DOM
    elements: {},
    
    /**
     * Inicializa os elementos do DOM
     */
    init() {
        this.elements = {
            // Formulário e campos
            form: document.getElementById('calculoForm'),
            valorInicial: document.getElementById('valorInicial'),
            aporteMensal: document.getElementById('aporteMensal'),
            anoFinal: document.getElementById('anoFinal'),
            mesFinal: document.getElementById('mesFinal'),
            taxaCDI: document.getElementById('taxaCDI'),
            percentualCDI: document.getElementById('percentualCDI'),
            
            // Botões
            btnCalcular: document.getElementById('btnCalcular'),
            btnCalcularResgate: document.getElementById('btnCalcularResgate'),
            btnBuscarCDI: document.getElementById('btnBuscarCDI'),
            btnExportar: document.getElementById('btnExportar'),
            
            // Containers e elementos de UI
            loadingIndicator: document.getElementById('loadingIndicator'),
            resultadoContainer: document.getElementById('resultadoContainer'),
            resultadoTabela: document.getElementById('resultadoTabela'),
            resumoContainer: document.getElementById('resumoContainer'),
            totalInvestido: document.getElementById('totalInvestido'),
            totalRendimentos: document.getElementById('totalRendimentos'),
            rendimentoBruto: document.getElementById('rendimentoBruto'),
            rendimentoBrutoRow: document.getElementById('rendimentoBrutoRow'),
            rendimentoLiquido: document.getElementById('rendimentoLiquido'),
            rendimentoLiquidoRow: document.getElementById('rendimentoLiquidoRow'),
            taxaCdiUtilizada: document.getElementById('taxaCdiUtilizada'),
            percentualCdiUtilizado: document.getElementById('percentualCdiUtilizado'),
            taxaJurosSaque: document.getElementById('taxaJurosSaque'),
            taxaJurosRow: document.getElementById('taxaJurosRow'),
            colunaDinamica: document.getElementById('colunaDinamica'),
            resultadoTitulo: document.getElementById('resultadoTitulo')
        };
        
        // Configurações iniciais de UI
        const anoAtual = new Date().getFullYear();
        this.elements.anoFinal.min = anoAtual;
        this.elements.anoFinal.value = anoAtual + 1;
    },
    
    /**
     * Configura event listeners
     */
    setupEventListeners() {
        this.elements.btnCalcular.addEventListener('click', () => Calculadora.calcularRendimento());
        this.elements.btnCalcularResgate.addEventListener('click', () => Calculadora.calcularResgate());
        this.elements.btnBuscarCDI.addEventListener('click', () => Calculadora.buscarTaxaCDI());
        this.elements.btnExportar.addEventListener('click', () => Exportador.exportarCSV());
        
        // Adicionar validação em tempo real nos campos
        Array.from(this.elements.form.elements).forEach(campo => {
            if (campo.tagName === 'INPUT' || campo.tagName === 'SELECT') {
                campo.addEventListener('change', () => {
                    if (!campo.checkValidity()) {
                        campo.classList.add('is-invalid');
                    } else {
                        campo.classList.remove('is-invalid');
                    }
                });
            }
        });
    },
    
    /**
     * Mostra ou esconde o indicador de carregamento
     * @param {boolean} mostrar - Indica se deve mostrar o loading
     */
    mostrarLoading(mostrar) {
        this.elements.loadingIndicator.classList.toggle('d-none', !mostrar);
        this.elements.resultadoContainer.classList.toggle('d-none', mostrar);
        this.elements.btnCalcular.disabled = mostrar;
        this.elements.btnCalcularResgate.disabled = mostrar;
    },
    
    /**
     * Exibe uma mensagem de erro na tabela de resultados
     * @param {string} mensagem - Mensagem de erro
     */
    mostrarErro(mensagem) {
        this.elements.resultadoTabela.innerHTML = `
            <tr>
                <td colspan="4" class="text-danger text-center">
                    <i class="bi bi-exclamation-triangle"></i> ${mensagem}
                </td>
            </tr>
        `;
        this.elements.resultadoContainer.classList.remove('d-none');
        this.elements.btnExportar.disabled = true;
    },
    
    /**
     * Prepara a UI para exibir resultados de rendimento
     */
    prepararParaRendimento() {
        this.elements.colunaDinamica.textContent = 'Rendimento';
        this.elements.resultadoTitulo.textContent = 'Resultados de Rendimentos';
        this.elements.taxaJurosRow.classList.add('d-none');
        this.elements.rendimentoLiquidoRow.classList.add('d-none');
        this.elements.rendimentoBrutoRow.classList.add('d-none');
        
        // Esconde a coluna de alíquota
        document.getElementById('colunaTaxa').classList.add('d-none');
    },
    
    /**
     * Prepara a UI para exibir resultados de resgate
     */
    prepararParaResgate() {
        this.elements.colunaDinamica.textContent = 'Impostos de Resgate';
        this.elements.resultadoTitulo.textContent = 'Resultados de Resgate com Impostos';
        this.elements.taxaJurosRow.classList.remove('d-none');
        this.elements.rendimentoLiquidoRow.classList.remove('d-none');
        this.elements.rendimentoBrutoRow.classList.remove('d-none');
        
        // Mostra a coluna de alíquota
        document.getElementById('colunaTaxa').classList.remove('d-none');
        document.getElementById('colunaTaxa').textContent = 'Alíquota IR';
    },
    
    /**
     * Preenche a tabela com os resultados
     * @param {Array} dados - Lista de informes mensais
     * @param {string} campoValor - Nome do campo com o valor a exibir
     */
    preencherTabelaResultados(dados, campoValor) {
        this.elements.resultadoTabela.innerHTML = '';
        
        if (!dados || dados.length === 0) {
            this.elements.resultadoTabela.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center">Nenhum resultado encontrado</td>
                </tr>
            `;
            return;
        }
        
        const isResgate = campoValor === 'imposto_resgate';
        
        dados.forEach(item => {
            const tr = document.createElement('tr');
            
            // Formatação dos valores em reais
            const valorTotal = Formatador.formatarMoeda(item.valor_total);
            const valorDinamico = Formatador.formatarMoeda(item[campoValor]);
            
            // HTML base para linha
            let html = `
                <td>${item.mes_ano}</td>
                <td class="valor-monetario">${valorTotal}</td>
                <td class="valor-monetario ${campoValor === 'rendimento_mensal' ? 'text-success' : 'text-danger'}">${valorDinamico}</td>
            `;
            
            // Adiciona coluna de alíquota se for resgate
            if (isResgate) {
                html += `<td>${item.aliquota_ir}%</td>`;
            } else {
                html += `<td class="d-none">-</td>`;
            }
            
            tr.innerHTML = html;
            this.elements.resultadoTabela.appendChild(tr);
        });
    },
    
    /**
     * Atualiza o resumo dos resultados
     * @param {Object} dados - Dados completos retornados pela API
     * @param {boolean} isResgate - Indica se o cálculo é de resgate
     */
    atualizarResumo(dados, isResgate) {
        this.elements.resumoContainer.classList.remove('d-none');
        
        this.elements.totalInvestido.textContent = Formatador.formatarMoeda(dados.valor_total_aplicado);
        
        if (isResgate) {
            this.elements.totalRendimentos.textContent = Formatador.formatarMoeda(dados.total_impostos);
            this.elements.totalRendimentos.classList.remove('text-success');
            this.elements.totalRendimentos.classList.add('text-danger');
            this.elements.taxaJurosSaque.textContent = dados.considera_ir ? 'IR e IOF aplicados' : 'Sem impostos';
            this.elements.rendimentoBruto.textContent = Formatador.formatarMoeda(dados.rendimento_bruto);
            this.elements.rendimentoLiquido.textContent = Formatador.formatarMoeda(dados.rendimento_liquido);
            this.elements.rendimentoLiquido.classList.add('text-success');
        } else {
            this.elements.totalRendimentos.textContent = Formatador.formatarMoeda(dados.total_rendimento);
            this.elements.totalRendimentos.classList.add('text-success');
            this.elements.totalRendimentos.classList.remove('text-danger');
        }
        
        this.elements.taxaCdiUtilizada.textContent = `${dados.taxa_cdi_utilizada.toFixed(2)}% ao ano`;
        this.elements.percentualCdiUtilizado.textContent = `${dados.percentual_sobre_cdi.toFixed(2)}%`;
    },
    
    /**
     * Atualiza a UI do botão Buscar CDI
     * @param {boolean} buscando - Indica se está buscando ou não
     */
    atualizarBotaoCDI(buscando) {
        this.elements.btnBuscarCDI.disabled = buscando;
        this.elements.btnBuscarCDI.innerHTML = buscando
            ? '<i class="bi bi-arrow-repeat"></i> Buscando...'
            : '<i class="bi bi-arrow-repeat"></i> Atualizar';
    }
}; 