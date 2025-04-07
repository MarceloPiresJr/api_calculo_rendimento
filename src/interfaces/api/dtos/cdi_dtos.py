from pydantic import BaseModel, Field
from datetime import datetime


class TaxaCDIResponseDTO(BaseModel):
    """DTO para enviar resposta com informações da taxa CDI atual"""
    cdi_anual: float = Field(..., 
        description="Valor anual da taxa CDI em percentual",
        example=13.25)
    data_atualizacao: datetime = Field(..., 
        description="Data e hora da última atualização dessa taxa")
    fonte: str = Field(..., 
        description="Fonte da informação",
        example="Banco Central do Brasil")
    
    class Config:
        title = "Taxa CDI Atual"
        description = "Informações sobre a taxa CDI atual e sua fonte" 