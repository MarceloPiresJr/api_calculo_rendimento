// Configuração da API
const API_URL = {
    // Determina a URL da API com base no ambiente
    getBaseUrl: function() {
        // No ambiente de produção (Render), a API terá um domínio diferente
        // Para desenvolvimento local, mantém localhost:8000
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:8000/api/v1';
        } else {
            // Em produção, usa o domínio do Render para a API
            // Nota: Substitua este URL pelo URL real da sua API no Render quando estiver disponível
            return 'https://api-calculo-rendimento.onrender.com/api/v1';
        }
    }
};

const API_BASE_URL = API_URL.getBaseUrl();
const API_ENDPOINTS = {
    calcularRendimento: `${API_BASE_URL}/calcular_rendimento`,
    calcularJurosSaque: `${API_BASE_URL}/calcular_juros_saque`,
    cdiAtual: `${API_BASE_URL}/cdi_atual`
};

// Elementos DOM
const elementos = {
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
    btnCalcularJuros: document.getElementById('btnCalcularJuros'),
    btnBuscarCDI: document.getElementById('btnBuscarCDI'),
    btnExportar: document.getElementById('btnExportar'),
    
    // Containers e elementos de UI
    loadingIndicator: document.getElementById('loadingIndicator'),
    resultadoContainer: document.getElementById('resultadoContainer'),
    resultadoTabela: document.getElementById('resultadoTabela'),
    resumoContainer: document.getElementById('resumoContainer'),
    totalInvestido: document.getElementById('totalInvestido'),
    totalRendimentos: document.getElementById('totalRendimentos'),
    taxaCdiUtilizada: document.getElementById('taxaCdiUtilizada'),
    percentualCdiUtilizado: document.getElementById('percentualCdiUtilizado'),
    taxaJurosSaque: document.getElementById('taxaJurosSaque'),
    taxaJurosRow: document.getElementById('taxaJurosRow'),
    colunaDinamica: document.getElementById('colunaDinamica'),
    resultadoTitulo: document.getElementById('resultadoTitulo')
};

// Variável global para armazenar os resultados atuais
let dadosResultadoAtual = null;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    // Definir ano atual como valor mínimo
    const anoAtual = new Date().getFullYear();
    elementos.anoFinal.min = anoAtual;
    elementos.anoFinal.value = anoAtual + 1;

    // Event listeners
    elementos.btnCalcular.addEventListener('click', calcularRendimento);
    elementos.btnCalcularJuros.addEventListener('click', calcularJurosSaque);
    elementos.btnBuscarCDI.addEventListener('click', buscarTaxaCDI);
    elementos.btnExportar.addEventListener('click', exportarCSV);
    
    // Buscar taxa CDI ao carregar a página
    buscarTaxaCDI();
});

// Funções de cálculo

/**
 * Calcula o rendimento usando a API
 */
async function calcularRendimento() {
    if (!validarFormulario()) return;
    
    try {
        mostrarLoading(true);
        elementos.colunaDinamica.textContent = 'Rendimento';
        elementos.resultadoTitulo.textContent = 'Resultados de Rendimentos';
        elementos.taxaJurosRow.classList.add('d-none');
        
        const params = obterParametrosFormulario();
        
        const response = await fetch(API_ENDPOINTS.calcularRendimento, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });
        
        if (!response.ok) {
            const erro = await response.json();
            throw new Error(erro.detail || 'Erro ao calcular rendimento');
        }
        
        const dados = await response.json();
        dadosResultadoAtual = dados;
        
        preencherTabelaResultados(dados.informe_mensal, 'rendimento_mensal');
        atualizarResumo(dados, false);
        elementos.btnExportar.disabled = false;
        
    } catch (error) {
        mostrarErro(error.message);
    } finally {
        mostrarLoading(false);
    }
}

/**
 * Calcula os juros de saque usando a API
 */
async function calcularJurosSaque() {
    if (!validarFormulario()) return;
    
    try {
        mostrarLoading(true);
        elementos.colunaDinamica.textContent = 'Juros de Saque';
        elementos.resultadoTitulo.textContent = 'Resultados de Juros de Saque';
        elementos.taxaJurosRow.classList.remove('d-none');
        
        const params = obterParametrosFormulario();
        params.taxa_juros_saque = 1.0; // Valor padrão
        
        const response = await fetch(API_ENDPOINTS.calcularJurosSaque, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });
        
        if (!response.ok) {
            const erro = await response.json();
            throw new Error(erro.detail || 'Erro ao calcular juros de saque');
        }
        
        const dados = await response.json();
        dadosResultadoAtual = dados;
        
        preencherTabelaResultados(dados.informe_mensal, 'juros_saque_mensal');
        atualizarResumo(dados, true);
        elementos.btnExportar.disabled = false;
        
    } catch (error) {
        mostrarErro(error.message);
    } finally {
        mostrarLoading(false);
    }
}

/**
 * Busca a taxa CDI atual da API
 */
async function buscarTaxaCDI() {
    try {
        elementos.btnBuscarCDI.disabled = true;
        elementos.btnBuscarCDI.innerHTML = '<i class="bi bi-arrow-repeat"></i> Buscando...';
        
        const response = await fetch(API_ENDPOINTS.cdiAtual);
        
        if (!response.ok) {
            throw new Error('Não foi possível obter a taxa CDI atual');
        }
        
        const dados = await response.json();
        elementos.taxaCDI.value = dados.cdi_anual.toFixed(2);
        
    } catch (error) {
        mostrarErro(error.message);
    } finally {
        elementos.btnBuscarCDI.disabled = false;
        elementos.btnBuscarCDI.innerHTML = '<i class="bi bi-arrow-repeat"></i> Atualizar';
    }
}

// Funções auxiliares

/**
 * Valida o formulário antes do envio
 * @returns {boolean} - Verdadeiro se o formulário for válido
 */
function validarFormulario() {
    if (!elementos.form.checkValidity()) {
        // Destacar campos inválidos
        Array.from(elementos.form.elements).forEach(campo => {
            if (!campo.checkValidity()) {
                campo.classList.add('is-invalid');
            } else {
                campo.classList.remove('is-invalid');
            }
        });
        
        mostrarErro('Preencha todos os campos corretamente');
        return false;
    }
    
    return true;
}

/**
 * Obtém os parâmetros do formulário para envio à API
 * @returns {Object} - Objeto com os parâmetros da requisição
 */
function obterParametrosFormulario() {
    return {
        valor_inicial: parseFloat(elementos.valorInicial.value),
        aporte_mensal: parseFloat(elementos.aporteMensal.value),
        ano_final: parseInt(elementos.anoFinal.value),
        mes_final: parseInt(elementos.mesFinal.value),
        taxa_cdi_anual: parseFloat(elementos.taxaCDI.value),
        percentual_sobre_cdi: parseFloat(elementos.percentualCDI.value)
    };
}

/**
 * Preenche a tabela com os resultados da API
 * @param {Array} dados - Lista de informes mensais
 * @param {string} campoValor - Nome do campo com o valor a exibir na coluna dinâmica
 */
function preencherTabelaResultados(dados, campoValor) {
    elementos.resultadoTabela.innerHTML = '';
    
    if (!dados || dados.length === 0) {
        elementos.resultadoTabela.innerHTML = `
            <tr>
                <td colspan="3" class="text-center">Nenhum resultado encontrado</td>
            </tr>
        `;
        return;
    }
    
    dados.forEach(item => {
        const tr = document.createElement('tr');
        
        // Formatação dos valores em reais
        const valorTotal = formatarMoeda(item.valor_total);
        const valorDinamico = formatarMoeda(item[campoValor]);
        
        tr.innerHTML = `
            <td>${item.mes_ano}</td>
            <td class="valor-monetario">${valorTotal}</td>
            <td class="valor-monetario ${campoValor === 'rendimento_mensal' ? 'text-success' : 'text-danger'}">${valorDinamico}</td>
        `;
        
        elementos.resultadoTabela.appendChild(tr);
    });
}

/**
 * Atualiza o resumo dos resultados
 * @param {Object} dados - Dados completos retornados pela API
 * @param {boolean} isJurosSaque - Indica se o cálculo é de juros de saque
 */
function atualizarResumo(dados, isJurosSaque) {
    elementos.resumoContainer.classList.remove('d-none');
    
    elementos.totalInvestido.textContent = formatarMoeda(dados.valor_total_aplicado);
    
    if (isJurosSaque) {
        elementos.totalRendimentos.textContent = formatarMoeda(dados.total_juros_saque);
        elementos.totalRendimentos.classList.remove('text-success');
        elementos.totalRendimentos.classList.add('text-danger');
        elementos.taxaJurosSaque.textContent = `${dados.taxa_juros_saque.toFixed(2)}% ao mês`;
    } else {
        elementos.totalRendimentos.textContent = formatarMoeda(dados.total_rendimento);
        elementos.totalRendimentos.classList.add('text-success');
        elementos.totalRendimentos.classList.remove('text-danger');
    }
    
    elementos.taxaCdiUtilizada.textContent = `${dados.taxa_cdi_utilizada.toFixed(2)}% ao ano`;
    elementos.percentualCdiUtilizado.textContent = `${dados.percentual_sobre_cdi.toFixed(2)}%`;
}

/**
 * Formata um valor numérico como moeda brasileira
 * @param {number} valor - Valor a ser formatado
 * @returns {string} - Valor formatado como R$ X.XXX,XX
 */
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', { 
        style: 'currency', 
        currency: 'BRL'
    }).format(valor);
}

/**
 * Mostra ou esconde o indicador de carregamento
 * @param {boolean} mostrar - Indica se deve mostrar o loading
 */
function mostrarLoading(mostrar) {
    elementos.loadingIndicator.classList.toggle('d-none', !mostrar);
    elementos.resultadoContainer.classList.toggle('d-none', mostrar);
    elementos.btnCalcular.disabled = mostrar;
    elementos.btnCalcularJuros.disabled = mostrar;
}

/**
 * Exibe uma mensagem de erro na tabela de resultados
 * @param {string} mensagem - Mensagem de erro
 */
function mostrarErro(mensagem) {
    elementos.resultadoTabela.innerHTML = `
        <tr>
            <td colspan="3" class="text-danger text-center">
                <i class="bi bi-exclamation-triangle"></i> ${mensagem}
            </td>
        </tr>
    `;
    elementos.resultadoContainer.classList.remove('d-none');
    elementos.btnExportar.disabled = true;
}

/**
 * Exporta os dados da tabela para um arquivo CSV
 */
function exportarCSV() {
    if (!dadosResultadoAtual) return;
    
    try {
        // Determina se é um resultado de rendimento ou juros de saque
        const isJurosSaque = 'total_juros_saque' in dadosResultadoAtual;
        const tipoCalculo = isJurosSaque ? 'juros_saque' : 'rendimento';
        const campoValor = isJurosSaque ? 'juros_saque_mensal' : 'rendimento_mensal';
        
        // Extrai dados do resultado
        const dados = dadosResultadoAtual.informe_mensal;
        
        // Cria as linhas do CSV - usar BOM para garantir que o Excel reconheça o UTF-8
        let csvContent = 'data:text/csv;charset=utf-8,\uFEFF';
        
        // Cabeçalho
        const colunaDinamica = isJurosSaque ? 'Juros de Saque' : 'Rendimento';
        csvContent += `"Mês/Ano";"Valor Total";"${colunaDinamica}"\r\n`;
        
        // Dados
        dados.forEach(item => {
            // Usar ponto e vírgula como separador e garantir que valores decimais usem vírgula
            const valorTotal = item.valor_total.toFixed(2).replace('.', ',');
            const valorDinamico = item[campoValor].toFixed(2).replace('.', ',');
            csvContent += `"${item.mes_ano}";"${valorTotal}";"${valorDinamico}"\r\n`;
        });
        
        // Linha em branco antes do resumo
        csvContent += '\r\n';
        
        // Resumo
        csvContent += `"Resumo";"";""\r\n`;
        csvContent += `"Valor Total Aplicado";"${dadosResultadoAtual.valor_total_aplicado.toFixed(2).replace('.', ',')}";"";\r\n`;
        
        if (isJurosSaque) {
            csvContent += `"Total de Juros de Saque";"${dadosResultadoAtual.total_juros_saque.toFixed(2).replace('.', ',')}";"";\r\n`;
            csvContent += `"Taxa de Juros de Saque";"${dadosResultadoAtual.taxa_juros_saque.toFixed(2).replace('.', ',')}% ao mês";"";\r\n`;
        } else {
            csvContent += `"Total de Rendimentos";"${dadosResultadoAtual.total_rendimento.toFixed(2).replace('.', ',')}";"";\r\n`;
        }
        
        csvContent += `"Taxa CDI Utilizada";"${dadosResultadoAtual.taxa_cdi_utilizada.toFixed(2).replace('.', ',')}% ao ano";"";\r\n`;
        csvContent += `"Percentual sobre CDI";"${dadosResultadoAtual.percentual_sobre_cdi.toFixed(2).replace('.', ',')}%";"";\r\n`;
        csvContent += `"Data do Cálculo";"${dadosResultadoAtual.data_calculo}";"";\r\n`;
        
        // Cria o link para download
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement('a');
        link.setAttribute('href', encodedUri);
        
        const dataAtual = new Date().toISOString().slice(0, 10);
        link.setAttribute('download', `resultado_${tipoCalculo}_${dataAtual}.csv`);
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
    } catch (error) {
        console.error('Erro ao exportar CSV:', error);
        alert('Não foi possível exportar os dados.');
    }
} 