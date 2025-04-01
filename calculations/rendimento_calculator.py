from datetime import datetime


class RendimentoCalculator:
    """
    Classe responsável pelo cálculo de rendimentos com base no CDI.
    
    Esta classe calcula o rendimento de um investimento considerando:
    - Um valor inicial
    - Aportes mensais
    - Taxa de CDI mensal
    - Período de tempo (data inicial até data final)
    """
    
    def __init__(self, valor_inicial, aporte_mensal, ano_final, mes_final, taxa_cdi, data_inicial=None):
        """
        Inicializa a calculadora de rendimentos.
        
        Args:
            valor_inicial (float): Valor inicial do investimento
            aporte_mensal (float): Valor a ser aportado mensalmente
            ano_final (int): Ano final para o cálculo
            mes_final (int): Mês final para o cálculo (1-12)
            taxa_cdi (float): Taxa de CDI mensal em percentual (ex: 0.5 para 0.5%)
            data_inicial (datetime, opcional): Data inicial do cálculo. Se None, usa a data atual.
        """
        self.valor_inicial = valor_inicial
        self.aporte_mensal = aporte_mensal
        self.ano_final = ano_final
        self.mes_final = mes_final
        self.taxa_cdi = taxa_cdi / 100  # Converte a taxa para decimal
        self.data_inicial = data_inicial or datetime.today()
        self.reset()
    
    def reset(self):
        """Reinicia os valores calculados para permitir recalcular se necessário."""
        self.saldo = self.valor_inicial
        self.total_rendimento = 0
        self.historico = []
    
    def calcular(self):
        """
        Calcula os rendimentos mês a mês até a data final.
        
        Returns:
            tuple: Contendo (historico_mensal, total_rendimento)
                - historico_mensal: Lista de tuplas (mes/ano, saldo, rendimento_mensal)
                - total_rendimento: Valor total de rendimentos no período
        """
        self.reset()
        data_atual = self.data_inicial
        data_final = datetime(self.ano_final, self.mes_final, 1)
        
        # Verifica se a data final é maior que a data inicial
        if data_final <= data_atual:
            raise ValueError("A data final deve ser posterior à data inicial")
        
        while data_atual <= data_final:
            # Adiciona o aporte mensal (exceto no primeiro mês se já tiver valor inicial)
            if not (data_atual.month == self.data_inicial.month and 
                   data_atual.year == self.data_inicial.year and self.valor_inicial > 0):
                self.saldo += self.aporte_mensal
            
            # Aplica o rendimento mensal baseado no CDI
            rendimento = self.saldo * self.taxa_cdi
            self.saldo += rendimento
            self.total_rendimento += rendimento
            
            # Armazena no histórico
            self.historico.append((
                data_atual.strftime('%m/%Y'),
                round(self.saldo, 2),
                round(rendimento, 2)
            ))
            
            # Avança para o próximo mês
            mes = data_atual.month + 1
            ano = data_atual.year
            if mes > 12:
                mes = 1
                ano += 1
            data_atual = datetime(ano, mes, 1)
        
        return self.historico, self.total_rendimento
    
    def obter_saldo_final(self):
        """Retorna o saldo final após o cálculo."""
        if not self.historico:
            return self.valor_inicial
        return self.historico[-1][1]