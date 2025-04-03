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
    """DTO para receber dados da requisição de cálculo de juros de saque"""
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
    taxa_juros_saque: Optional[float] = Field(1.0, 
        description="Taxa de juros mensal para saque em percentual",
        example=1.0)
    
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
    
    @validator('taxa_juros_saque')
    def validar_taxa_juros_saque(cls, v):
        if v is not None and v < 0:
            raise ValueError("A taxa de juros de saque não pode ser negativa")
        return v
    
    class Config:
        title = "Parâmetros para Cálculo de Juros de Saque"
        description = "Dados necessários para calcular os juros que seriam pagos para sacar o dinheiro"


class InformeJurosSaqueDTO(BaseModel):
    """DTO para representar um item do informe mensal de juros de saque"""
    mes_ano: str = Field(..., 
        description="Mês e ano no formato 'mês/ano'",
        example="janeiro/2024")
    valor_total: float = Field(..., 
        description="Valor total acumulado no período",
        example=11112.50)
    juros_saque_mensal: float = Field(..., 
        description="Juros que seriam pagos para saque no mês",
        example=111.13)
    
    class Config:
        title = "Informe Mensal de Juros de Saque"
        description = "Dados de juros mensais para saque do investimento"


class CalculoJurosSaqueResponseDTO(BaseModel):
    """DTO para enviar resultado do cálculo de juros de saque"""
    informe_mensal: List[InformeJurosSaqueDTO] = Field(..., 
        description="Lista de informes mensais com valores e juros de saque")
    total_juros_saque: float = Field(..., 
        description="Valor total de juros de saque no período",
        example=5250.75)
    valor_total_aplicado: float = Field(..., 
        description="Valor total investido (inicial + aportes)",
        example=82000.00)
    taxa_cdi_utilizada: float = Field(..., 
        description="Taxa de CDI anual utilizada no cálculo",
        example=13.25)
    percentual_sobre_cdi: float = Field(..., 
        description="Percentual sobre o CDI utilizado no cálculo",
        example=100.0)
    taxa_juros_saque: float = Field(..., 
        description="Taxa de juros mensal para saque utilizada no cálculo",
        example=1.0)
    data_calculo: str = Field(..., 
        description="Data e hora do cálculo no formato DD/MM/AAAA HH:MM",
        example="15/07/2024 10:30")
    
    class Config:
        title = "Resultado do Cálculo de Juros de Saque"
        description = "Resultado detalhado do cálculo de juros para saque do investimento" 