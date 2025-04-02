from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class StatusEnum(str, Enum):
    """Enumeração para status de operações na API"""
    SUCESSO = "sucesso"
    ERRO = "erro"
    ALERTA = "alerta"
    PROCESSANDO = "processando"


class MensagemResponseDTO(BaseModel):
    """DTO para resposta com mensagem simples"""
    mensagem: str = Field(..., 
        description="Mensagem informativa",
        example="Operação realizada com sucesso")
    status: StatusEnum = Field(default=StatusEnum.SUCESSO,
        description="Status da operação")
    codigo: Optional[str] = Field(None,
        description="Código de referência (opcional)",
        example="SUCCESS_001")
    timestamp: datetime = Field(default_factory=datetime.now,
        description="Data e hora da mensagem")
    
    class Config:
        title = "Mensagem de Resposta"
        description = "Resposta simples com mensagem informativa"


class ErroResponseDTO(BaseModel):
    """DTO para resposta de erro"""
    erro: str = Field(...,
        description="Descrição do erro ocorrido",
        example="Parâmetro inválido")
    detalhe: Optional[str] = Field(None,
        description="Detalhes adicionais sobre o erro",
        example="O valor inicial não pode ser negativo")
    codigo_erro: Optional[str] = Field(None,
        description="Código de identificação do erro",
        example="ERR_001")
    timestamp: datetime = Field(default_factory=datetime.now,
        description="Data e hora do erro")
    
    class Config:
        title = "Erro"
        description = "Informações sobre um erro ocorrido"


class PaginacaoDTO(BaseModel):
    """DTO para informações de paginação"""
    pagina_atual: int = Field(..., 
        description="Número da página atual", 
        ge=1,
        example=1)
    total_paginas: int = Field(..., 
        description="Total de páginas disponíveis",
        ge=1,
        example=10)
    itens_por_pagina: int = Field(..., 
        description="Quantidade de itens por página",
        ge=1,
        example=20)
    total_itens: int = Field(..., 
        description="Quantidade total de itens",
        ge=0,
        example=195)
    
    class Config:
        title = "Informações de Paginação"
        description = "Metadados sobre paginação de resultados" 