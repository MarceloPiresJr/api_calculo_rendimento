/**
 * Módulo de exportação de dados
 */
import { Calculadora } from './calculadora.js';
import { Formatador } from './formatador.js';

export const Exportador = {
    /**
     * Exporta os dados da tabela para um arquivo CSV
     */
    exportarCSV() {
        if (!Calculadora.resultadoAtual) return;
        
        try {
            // Determina se é um resultado de rendimento ou juros de saque
            const isJurosSaque = 'total_juros_saque' in Calculadora.resultadoAtual;
            const tipoCalculo = isJurosSaque ? 'juros_saque' : 'rendimento';
            const campoValor = isJurosSaque ? 'juros_saque_mensal' : 'rendimento_mensal';
            
            // Extrai dados do resultado
            const dados = Calculadora.resultadoAtual.informe_mensal;
            
            // Cria as linhas do CSV - usar BOM para garantir que o Excel reconheça o UTF-8
            let csvContent = 'data:text/csv;charset=utf-8,\uFEFF';
            
            // Cabeçalho
            const colunaDinamica = isJurosSaque ? 'Juros de Saque' : 'Rendimento';
            csvContent += `"Mês/Ano";"Valor Total";"${colunaDinamica}"\r\n`;
            
            // Dados
            dados.forEach(item => {
                // Usar ponto e vírgula como separador e garantir valores decimais com vírgula
                const valorTotal = Formatador.formatarDecimalCSV(item.valor_total);
                const valorDinamico = Formatador.formatarDecimalCSV(item[campoValor]);
                csvContent += `"${item.mes_ano}";"${valorTotal}";"${valorDinamico}"\r\n`;
            });
            
            // Linha em branco antes do resumo
            csvContent += '\r\n';
            
            // Resumo
            csvContent += `"Resumo";"";""\r\n`;
            csvContent += `"Valor Total Aplicado";"${Formatador.formatarDecimalCSV(Calculadora.resultadoAtual.valor_total_aplicado)}";"";\r\n`;
            
            if (isJurosSaque) {
                csvContent += `"Total de Juros de Saque";"${Formatador.formatarDecimalCSV(Calculadora.resultadoAtual.total_juros_saque)}";"";\r\n`;
                csvContent += `"Taxa de Juros de Saque";"${Formatador.formatarDecimalCSV(Calculadora.resultadoAtual.taxa_juros_saque)}% ao mês";"";\r\n`;
            } else {
                csvContent += `"Total de Rendimentos";"${Formatador.formatarDecimalCSV(Calculadora.resultadoAtual.total_rendimento)}";"";\r\n`;
            }
            
            csvContent += `"Taxa CDI Utilizada";"${Formatador.formatarDecimalCSV(Calculadora.resultadoAtual.taxa_cdi_utilizada)}% ao ano";"";\r\n`;
            csvContent += `"Percentual sobre CDI";"${Formatador.formatarDecimalCSV(Calculadora.resultadoAtual.percentual_sobre_cdi)}%";"";\r\n`;
            csvContent += `"Data do Cálculo";"${Calculadora.resultadoAtual.data_calculo}";"";\r\n`;
            
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
            alert('Não foi possível exportar os dados. Erro: ' + error.message);
        }
    }
}; 