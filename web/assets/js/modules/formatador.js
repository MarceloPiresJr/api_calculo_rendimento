/**
 * Módulo de formatação de dados
 */
export const Formatador = {
    /**
     * Formata um valor numérico como moeda brasileira
     * @param {number} valor - Valor a ser formatado
     * @returns {string} - Valor formatado como R$ X.XXX,XX
     */
    formatarMoeda(valor) {
        return new Intl.NumberFormat('pt-BR', { 
            style: 'currency', 
            currency: 'BRL'
        }).format(valor);
    },
    
    /**
     * Formata um valor decimal para exibição em CSV no padrão brasileiro
     * @param {number} valor - Valor decimal
     * @returns {string} - Valor formatado com vírgula como separador decimal
     */
    formatarDecimalCSV(valor) {
        return valor.toFixed(2).replace('.', ',');
    }
}; 