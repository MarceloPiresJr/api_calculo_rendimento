from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class ParametrosCalculoRendimento:
    """
    Modelo de domínio para os parâmetros do cálculo de rendimento.
    Contém apenas os dados necessários para o cálculo.
    """
    valor_inicial: float
    aporte_mensal: float
    ano_final: int
    mes_final: int
    taxa_cdi_anual: Optional[float] = None
    percentual_sobre_cdi: float = 100.0
    data_inicial: Optional[datetime] = None


@dataclass
class ParametrosCalculoJurosSaque(ParametrosCalculoRendimento):
    """
    Modelo de domínio para os parâmetros do cálculo de juros de saque.
    Estende o modelo de cálculo de rendimento, adicionando taxa de juros de saque.
    """
    taxa_juros_saque: float = 1.0


@dataclass
class InformeRendimentoMensal:
    """
    Modelo de domínio para um informe mensal de rendimento.
    Representa o estado do investimento em um mês específico.
    """
    data: datetime
    saldo: float
    rendimento: float
    
    @property
    def mes_ano_formatado(self) -> str:
        """Retorna mês/ano formatado"""
        return self.data.strftime("%B/%Y")


@dataclass
class InformeJurosSaqueMensal:
    """
    Modelo de domínio para um informe mensal de juros de saque.
    Representa os juros que seriam pagos para sacar o dinheiro em um mês específico.
    """
    data: datetime
    saldo: float
    juros_saque: float
    
    @property
    def mes_ano_formatado(self) -> str:
        """Retorna mês/ano formatado"""
        return self.data.strftime("%B/%Y")


@dataclass
class ResultadoCalculoRendimento:
    """
    Modelo de domínio para o resultado completo de um cálculo de rendimento.
    """
    taxa_cdi_utilizada: float
    percentual_sobre_cdi: float
    informes_mensais: List[InformeRendimentoMensal]
    total_rendimento: float
    valor_total_aplicado: float
    data_calculo: Optional[datetime] = None
    
    def __post_init__(self):
        if self.data_calculo is None:
            self.data_calculo = datetime.now()
            
    @property
    def data_calculo_formatada(self) -> str:
        """Retorna a data e hora do cálculo no formato DD/MM/AAAA HH:mm"""
        return self.data_calculo.strftime("%d/%m/%Y %H:%M")


@dataclass
class ResultadoCalculoJurosSaque:
    """
    Modelo de domínio para o resultado completo de um cálculo de juros de saque.
    """
    taxa_cdi_utilizada: float
    percentual_sobre_cdi: float
    taxa_juros_saque: float
    informes_mensais: List[InformeJurosSaqueMensal]
    total_juros_saque: float
    valor_total_aplicado: float
    data_calculo: Optional[datetime] = None
    
    def __post_init__(self):
        if self.data_calculo is None:
            self.data_calculo = datetime.now()
            
    @property
    def data_calculo_formatada(self) -> str:
        """Retorna a data e hora do cálculo no formato DD/MM/AAAA HH:mm"""
        return self.data_calculo.strftime("%d/%m/%Y %H:%M") 