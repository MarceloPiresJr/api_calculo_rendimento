from pydantic import BaseModel, Field
from datetime import datetime


class TaxaCDIResponseDTO(BaseModel):
    """DTO para enviar informações sobre a taxa CDI atual"""
    cdi_anual: float = Field(..., 
        description="Taxa CDI anual atual em percentual",
        example=13.25)
    data_atualizacao: datetime = Field(default_factory=datetime.now, 
        description="Data e hora da consulta",
        example="2024-07-15T10:30:00")
    fonte: str = Field("Banco Central do Brasil", 
        description="Fonte dos dados da taxa CDI",
        example="Banco Central do Brasil")
    
    class Config:
        title = "Informações da Taxa CDI"
        description = "Dados atualizados da taxa CDI anual"


class HistoricoCDIItemDTO(BaseModel):
    """DTO para representar um item do histórico de taxas CDI"""
    data: datetime = Field(...,
        description="Data de referência da taxa",
        example="2024-01-15")
    valor: float = Field(...,
        description="Valor percentual da taxa CDI",
        example=13.15)
    
    class Config:
        title = "Item do Histórico de CDI"
        description = "Valor histórico da taxa CDI em uma data específica"


class HistoricoCDIResponseDTO(BaseModel):
    """DTO para enviar histórico de taxas CDI"""
    taxas: list[HistoricoCDIItemDTO] = Field(...,
        description="Lista de taxas CDI históricas",
        min_items=1)
    periodo_inicio: datetime = Field(...,
        description="Data de início do período consultado",
        example="2023-01-01")
    periodo_fim: datetime = Field(...,
        description="Data de fim do período consultado",
        example="2023-12-31")
    
    class Config:
        title = "Histórico de Taxas CDI"
        description = "Dados históricos das taxas CDI em um período específico" 