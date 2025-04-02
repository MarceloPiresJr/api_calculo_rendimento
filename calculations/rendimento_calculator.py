from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class ResultadoMensal:
    data: str
    saldo: float
    rendimento: float


class RendimentoCalculator:
    """
    Classe responsável pelo cálculo de rendimentos com base no CDI.
    
    Esta classe calcula o rendimento de um investimento considerando:
    - Um valor inicial
    - Aportes mensais
    - Taxa de CDI mensal
    - Período de tempo (data inicial até data final)
    """
    
    def __init__(self, valor_inicial: float, aporte_mensal: float, 
                 ano_final: int, mes_final: int, taxa_cdi_anual: float, 
                 data_inicial: datetime = None):
        """
        Inicializa a calculadora de rendimentos.
        
        Args:
            valor_inicial: Valor inicial do investimento
            aporte_mensal: Valor a ser aportado mensalmente
            ano_final: Ano final para o cálculo
            mes_final: Mês final para o cálculo (1-12)
            taxa_cdi_anual: Taxa de CDI anual em percentual
            data_inicial: Data inicial do cálculo. Se None, usa a data atual.
        """
        self.valor_inicial = valor_inicial
        self.aporte_mensal = aporte_mensal
        self.data_final = datetime(ano_final, mes_final, 1)
        self.taxa_cdi_mensal = taxa_cdi_anual / 100 / 12  # Converte a taxa anual para mensal
        self.data_inicial = data_inicial or datetime.today()
        
        self.saldo = 0.0
        self.total_rendimento = 0.0
        self.historico = []
    
    def calcular(self) -> Tuple[List[Tuple[str, float, float]], float]:
        """
        Calcula os rendimentos mês a mês até a data final.
        
        Returns:
            Tupla contendo:
                - Lista de tuplas (mês/ano, saldo, rendimento mensal)
                - Valor total de rendimentos no período
        """
        self._inicializar_calculo()
        self._validar_datas()
        
        data_atual = self.data_inicial
        
        while data_atual <= self.data_final:
            self._processar_mes(data_atual)
            data_atual = self._avancar_para_proximo_mes(data_atual)
        
        return self.historico, self.total_rendimento
    
    def _inicializar_calculo(self) -> None:
        """Reinicia os valores para um novo cálculo"""
        self.saldo = self.valor_inicial
        self.total_rendimento = 0.0
        self.historico = []
    
    def _validar_datas(self) -> None:
        """Valida se as datas de início e fim são coerentes"""
        if self.data_final <= self.data_inicial:
            raise ValueError("A data final deve ser posterior à data inicial")
    
    def _processar_mes(self, data_atual: datetime) -> None:
        """Processa o cálculo de rendimento para um mês específico"""
        self._aplicar_aporte_mensal(data_atual)
        self._aplicar_rendimento_mensal()
        self._registrar_no_historico(data_atual)
    
    def _aplicar_aporte_mensal(self, data_atual: datetime) -> None:
        """Aplica o aporte mensal ao saldo, exceto no primeiro mês com valor inicial"""
        eh_primeiro_mes = (data_atual.month == self.data_inicial.month and 
                           data_atual.year == self.data_inicial.year)
        
        if not (eh_primeiro_mes and self.valor_inicial > 0):
            self.saldo += self.aporte_mensal
    
    def _aplicar_rendimento_mensal(self) -> None:
        """Calcula e aplica o rendimento mensal ao saldo"""
        rendimento = self.saldo * self.taxa_cdi_mensal
        self.saldo += rendimento
        self.total_rendimento += rendimento
    
    def _registrar_no_historico(self, data_atual: datetime) -> None:
        """Registra o saldo e rendimento do mês atual no histórico"""
        self.historico.append((
            data_atual.strftime('%m/%Y'),
            round(self.saldo, 2),
            round(self.saldo * self.taxa_cdi_mensal, 2)
        ))
    
    def _avancar_para_proximo_mes(self, data_atual: datetime) -> datetime:
        """Retorna a data do próximo mês"""
        mes = data_atual.month + 1
        ano = data_atual.year
        
        if mes > 12:
            mes = 1
            ano += 1
            
        return datetime(ano, mes, 1)
    
    def obter_saldo_final(self) -> float:
        """Retorna o saldo final após o cálculo."""
        if not self.historico:
            return self.valor_inicial
        return self.historico[-1][1]