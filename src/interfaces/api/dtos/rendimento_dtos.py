from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class CalculoRendimentoRequestDTO(BaseModel):
    """DTO para receber dados da requisição de cálculo de rendimento"""
    valor_inicial: float = Field(..., 
        description="Valor inicial do investimento", 
        gt=0,
        example=10000.0)
    aporte_mensal: float = Field(..., 
        description="Valor a ser aportado mensalmente", 
        ge=0,
        example=1000.0)
    ano_final: int = Field(..., 
        description="Ano final para o cálculo", 
        gt=2000,
        example=2030)
    mes_final: int = Field(..., 
        description="Mês final para o cálculo", 
        ge=1, 
        le=12,
        example=12)
    taxa_cdi_anual: Optional[float] = Field(None, 
        description="Taxa de CDI anual em percentual",
        example=13.25)
    percentual_sobre_cdi: Optional[float] = Field(100.0, 
        description="Percentual sobre o CDI (ex: 100% = CDI puro, 120% = CDI + 20%)",
        ge=0,
        example=100.0)
    
    @validator('valor_inicial')
    def validar_valor_inicial(cls, v):
        if v < 0:
            raise ValueError("O valor inicial não pode ser negativo")
        return v
    
    @validator('ano_final')
    def validar_ano_final(cls, v):
        ano_atual = datetime.now().year
        if v < ano_atual:
            raise ValueError(f"O ano final deve ser igual ou posterior a {ano_atual}")
        return v
    
    class Config:
        title = "Parâmetros para Cálculo de Rendimento"
        description = "Dados necessários para calcular rendimento financeiro"


class InformeRendimentoDTO(BaseModel):
    """DTO para representar um item do informe mensal de rendimentos"""
    mes_ano: str = Field(..., 
        description="Mês e ano no formato 'mês/ano'",
        example="janeiro/2024")
    valor_total: float = Field(..., 
        description="Valor total acumulado no período",
        example=11112.50)
    rendimento_mensal: float = Field(..., 
        description="Rendimento obtido no mês",
        example=112.50)
    
    class Config:
        title = "Informe Mensal de Rendimento"
        description = "Dados de um mês específico do cálculo de rendimento"


class CalculoRendimentoResponseDTO(BaseModel):
    """DTO para enviar resultado do cálculo de rendimentos"""
    informe_mensal: List[InformeRendimentoDTO] = Field(..., 
        description="Lista de informes mensais com valores e rendimentos")
    total_rendimento: float = Field(..., 
        description="Valor total de rendimentos no período",
        example=12500.75)
    valor_total_aplicado: float = Field(..., 
        description="Valor total investido (inicial + aportes)",
        example=82000.00)
    taxa_cdi_utilizada: float = Field(..., 
        description="Taxa de CDI anual utilizada no cálculo",
        example=13.25)
    percentual_sobre_cdi: float = Field(..., 
        description="Percentual sobre o CDI utilizado no cálculo",
        example=100.0)
    data_calculo: str = Field(..., 
        description="Data e hora do cálculo no formato DD/MM/AAAA HH:MM",
        example="15/07/2024 10:30")
    
    class Config:
        title = "Resultado do Cálculo de Rendimento"
        description = "Resultado detalhado do cálculo de rendimento financeiro"


class CalculoJurosSaqueRequestDTO(BaseModel):
    """DTO para receber dados da requisição de cálculo de resgate"""
    valor_inicial: float = Field(..., 
        description="Valor inicial do investimento", 
        gt=0,
        example=10000.0)
    aporte_mensal: float = Field(..., 
        description="Valor a ser aportado mensalmente (incluindo o primeiro mês)", 
        ge=0,
        example=1000.0)
    ano_final: int = Field(..., 
        description="Ano final para o cálculo", 
        gt=2000,
        example=2030)
    mes_final: int = Field(..., 
        description="Mês final para o cálculo", 
        ge=1, 
        le=12,
        example=12)
    taxa_cdi_anual: Optional[float] = Field(None, 
        description="Taxa de CDI anual em percentual",
        example=13.25)
    percentual_sobre_cdi: Optional[float] = Field(100.0, 
        description="Percentual sobre o CDI (ex: 100% = CDI puro, 120% = CDI + 20%)",
        ge=0,
        example=100.0)
    considerar_ir: Optional[bool] = Field(True,
        description="Se deve considerar o Imposto de Renda no cálculo",
        example=True)
    considerar_iof: Optional[bool] = Field(True,
        description="Se deve considerar o IOF para resgates em menos de 30 dias",
        example=True)
    
    @validator('valor_inicial')
    def validar_valor_inicial(cls, v):
        if v < 0:
            raise ValueError("O valor inicial não pode ser negativo")
        return v
    
    @validator('ano_final')
    def validar_ano_final(cls, v):
        ano_atual = datetime.now().year
        if v < ano_atual:
            raise ValueError(f"O ano final deve ser igual ou posterior a {ano_atual}")
        return v
    
    class Config:
        title = "Parâmetros para Cálculo de Resgate"
        description = "Dados necessários para calcular os impostos e valores líquidos de resgate"


class InformeResgateDTO(BaseModel):
    """DTO para representar um item do informe mensal de resgate"""
    mes_ano: str = Field(..., 
        description="Mês e ano no formato 'mês/ano'",
        example="janeiro/2024")
    valor_total: float = Field(..., 
        description="Valor total acumulado no período",
        example=11112.50)
    imposto_resgate: float = Field(..., 
        description="Impostos que seriam pagos no resgate (IR + IOF)",
        example=111.13)
    aliquota_ir: float = Field(...,
        description="Alíquota de IR aplicada no período (%)",
        example=22.5)
    
    class Config:
        title = "Informe Mensal de Resgate"
        description = "Dados de impostos mensais para resgate do investimento"


class CalculoResgateResponseDTO(BaseModel):
    """DTO para enviar resultado do cálculo de resgate"""
    informe_mensal: List[InformeResgateDTO] = Field(..., 
        description="Lista de informes mensais com valores e impostos de resgate")
    total_impostos: float = Field(..., 
        description="Valor total de impostos no período",
        example=5250.75)
    rendimento_liquido: float = Field(...,
        description="Valor total dos rendimentos menos os impostos",
        example=7250.25)
    rendimento_bruto: float = Field(...,
        description="Valor total dos rendimentos antes do desconto dos impostos",
        example=12501.00)
    valor_total_aplicado: float = Field(..., 
        description="Valor total investido (inicial + aportes)",
        example=82000.00)
    taxa_cdi_utilizada: float = Field(..., 
        description="Taxa de CDI anual utilizada no cálculo",
        example=13.25)
    percentual_sobre_cdi: float = Field(..., 
        description="Percentual sobre o CDI utilizado no cálculo",
        example=100.0)
    considera_ir: bool = Field(...,
        description="Se o cálculo considerou o Imposto de Renda",
        example=True)
    considera_iof: bool = Field(...,
        description="Se o cálculo considerou o IOF",
        example=True)
    data_calculo: str = Field(..., 
        description="Data e hora do cálculo no formato DD/MM/AAAA HH:MM",
        example="15/07/2024 10:30")
    
    class Config:
        title = "Resultado do Cálculo de Resgate"
        description = "Resultado detalhado do cálculo de impostos e valores líquidos para resgate do investimento" 