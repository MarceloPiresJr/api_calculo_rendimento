# Pacote de DTOs (Data Transfer Objects)
# Contém os modelos de transferência de dados da API

# DTOs de Rendimento
from app.dtos.rendimento_dtos import (
    CalculoRendimentoRequestDTO,
    InformeRendimentoDTO,
    CalculoRendimentoResponseDTO
)

# DTOs de CDI
from app.dtos.cdi_dtos import (
    TaxaCDIResponseDTO,
    HistoricoCDIItemDTO,
    HistoricoCDIResponseDTO
)

# DTOs comuns/utilitários
from app.dtos.common_dtos import (
    StatusEnum,
    MensagemResponseDTO,
    ErroResponseDTO,
    PaginacaoDTO
)

# Exporta todos os DTOs para facilitar a importação
__all__ = [
    # Rendimento
    'CalculoRendimentoRequestDTO',
    'InformeRendimentoDTO',
    'CalculoRendimentoResponseDTO',
    
    # CDI
    'TaxaCDIResponseDTO',
    'HistoricoCDIItemDTO',
    'HistoricoCDIResponseDTO',
    
    # Comuns
    'StatusEnum',
    'MensagemResponseDTO',
    'ErroResponseDTO',
    'PaginacaoDTO'
] 