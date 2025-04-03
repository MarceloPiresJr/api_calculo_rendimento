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
    taxa_cdi_anual: float
    data_inicial: Optional[datetime] = None


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
class ResultadoCalculoRendimento:
    """
    Modelo de domínio para o resultado completo de um cálculo de rendimento.
    """
    taxa_cdi_utilizada: float
    informes_mensais: List[InformeRendimentoMensal]
    total_rendimento: float
    valor_total_aplicado: float
    data_calculo: datetime = None
    
    def __post_init__(self):
        if self.data_calculo is None:
            self.data_calculo = datetime.now() 